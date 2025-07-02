import os
import re
import ast
import math
import pandas as pd # Using pandas for robust NaN handling

# --- Configuration ---
log_file_path = './output/regfile_dictionary.log'
template_file_path = './input/andla_regfile_cov.tmp.sv'
output_file_path = './output/andla_regfile_cov.sv'
# Be precise with the marker, including leading spaces
marker = "        // auto_gen_fme0"
# Indentation for the generated lines (relative to the marker)
indentation = " " * 8

# --- NEW --- Flag to enable special handling for *_ADDR_INIT registers
addr_init_enable = True
# --- NEW --- Default Usecase for *_ADDR_INIT registers when enabled
addr_init_default_usecase = 'range(0, 2**22)' # Covers 0 to 2^22-1 for [21:0]
# --- NEW --- Fixed Bit Locate for *_ADDR_INIT registers when enabled
addr_init_fixed_bit_locate = '[21:0]'


# --- Helper Functions ---

def safe_eval_num(num_str):
    """
    Safely evaluates a string expected to be a number or a simple
    power-of-2 expression like '2**14'. Adds support for hex '0x...'.
    """
    num_str = str(num_str).strip()
    if re.fullmatch(r'\d+', num_str):
        return int(num_str)
    # Allow simple power expressions like '2**14' or '2*14-1' or '2**22'
    power_match = re.fullmatch(r'(\d+)\s*\*\*\s*(\d+)\s*(-?\s*\d+)?', num_str)
    if power_match:
        base = int(power_match.group(1))
        exp = int(power_match.group(2))
        offset = int(power_match.group(3).replace(" ","")) if power_match.group(3) else 0
        # Add safety limit if desired (e.g., limit exponent)
        if exp < 64:
            return (base ** exp) + offset
        else:
            raise ValueError(f"Exponent too large in safe_eval_num: {num_str}")

    hex_match = re.fullmatch(r'0x[0-9a-fA-F]+', num_str, re.IGNORECASE)
    if hex_match:
        return int(num_str, 16)

    # Try simple integer conversion as a fallback for plain numbers
    try:
        return int(num_str)
    except ValueError:
        pass # Continue checking other formats

    raise ValueError(f"Unsupported number format for safe_eval_num: '{num_str}'")


def parse_usecase(usecase_str):
    """
    Parses the Usecase string into a list of values or a range tuple.
    Handles formats: range(), range[], start~end, [v1,v2,...], v1,v2,..., single_value
    Returns:
        - list of ints: If less than 32 values.
        - tuple ('range', start, end): If 32 or more values, for [start:end] format.
        - None: If parsing fails or format is unrecognized.
    """
    usecase_str = str(usecase_str).strip()
    values = None
    start_val = None
    end_val = None

    # --- Order of checks is important ---

    # 1. range(start, end) -> Python style, exclusive end
    match = re.fullmatch(r'range\s*\(\s*([^,]+)\s*,\s*([^)]+)\s*\)', usecase_str, re.IGNORECASE)
    if match:
        try:
            start = safe_eval_num(match.group(1))
            end = safe_eval_num(match.group(2)) # Exclusive end
            if start < end : # Ensure valid range
                 values = list(range(start, end))
                 start_val = start
                 end_val = end - 1 # Inclusive end for bin range
            else: # Invalid range like range(5, 2)
                 values = []
                 start_val = start # Still record attempted bounds
                 end_val = end - 1
        except ValueError as e:
            print(f"Warning: Error parsing numbers in range(): {e} for '{usecase_str}'")
            return None

    # 2. range[start, end] -> Inclusive end
    if values is None:
        match = re.fullmatch(r'range\s*\[\s*([^,]+)\s*,\s*([^\]]+)\s*\]', usecase_str, re.IGNORECASE)
        if match:
            try:
                start = safe_eval_num(match.group(1))
                end = safe_eval_num(match.group(2)) # Inclusive end
                if start <= end: # Ensure valid range
                    values = list(range(start, end + 1))
                    start_val = start
                    end_val = end
                else: # Invalid range like range[5, 2]
                    values = []
                    start_val = start
                    end_val = end
            except ValueError as e:
                print(f"Warning: Error parsing numbers in range[]: {e} for '{usecase_str}'")
                return None

    # 3. start~end -> Inclusive end
    if values is None:
        match = re.fullmatch(r'([^~]+)\s*~\s*(.+)', usecase_str)
        if match:
             try:
                start = safe_eval_num(match.group(1))
                end = safe_eval_num(match.group(2))
                if start <= end: # Ensure valid range
                    values = list(range(start, end + 1))
                    start_val = start
                    end_val = end
                else: # Invalid range like 5~2
                    values = []
                    start_val = start
                    end_val = end
             except ValueError as e:
                 print(f"Warning: Error parsing numbers in start~end: {e} for '{usecase_str}'")
                 return None

    # 4. Bracketed list: [v1, v2, v3]
    if values is None:
        if usecase_str.startswith('[') and usecase_str.endswith(']'):
             content = usecase_str[1:-1].strip() # Get content inside brackets
             if content: # Avoid processing empty "[]" here
                 try:
                     potential_values = [item.strip() for item in content.split(',')]
                     evaluated_values = [safe_eval_num(v) for v in potential_values]
                     values = evaluated_values
                     if len(values) >= 32:
                        start_val = min(values)
                        end_val = max(values)
                 except ValueError as e:
                     print(f"Warning: Error parsing numbers in bracketed list: {e} for '{usecase_str}'")
                     return None
             else: # Handle empty list "[]"
                 values = []
                 start_val = None # No range for empty list
                 end_val = None

    # 5. Comma-separated values (WITHOUT brackets)
    if values is None:
        if ',' in usecase_str and \
           not (usecase_str.startswith('[') and usecase_str.endswith(']')) and \
           not usecase_str.lower().startswith('range'):
             try:
                 potential_values = [item.strip() for item in usecase_str.split(',')]
                 evaluated_values = [safe_eval_num(v) for v in potential_values]
                 values = evaluated_values
                 if len(values) >= 32:
                    start_val = min(values)
                    end_val = max(values)
             except ValueError as e:
                 print(f"Warning: Error parsing comma-separated values: {e} for '{usecase_str}'")
                 return None # Exit if parsing fails here

    # 6. Single value (if none of the above matched)
    if values is None:
        try:
            val = safe_eval_num(usecase_str)
            values = [val]
            start_val = val
            end_val = val
        except ValueError:
             # If it's not any recognized format at this point, fail
             print(f"Warning: Could not parse Usecase string: '{usecase_str}' into any known format.")
             return None

    # --- Decide on output format based on count ---
    if values is not None:
        if len(values) >= 32:
             if start_val is not None and end_val is not None and start_val <= end_val:
                  is_contiguous = (len(values) == (end_val - start_val + 1) and \
                                   set(values) == set(range(start_val, end_val + 1)))

                  if is_contiguous:
                     return ('range', start_val, end_val)
                  else:
                     print(f"Info: Usecase '{usecase_str}' resulted in >= 32 non-contiguous values. Listing explicitly.")
                     return values
             else:
                 print(f"Warning: Usecase '{usecase_str}' has >= 32 values but range boundaries unclear or invalid. Listing explicitly.")
                 return values

        else: # < 32 values
             return values
    else:
         return None # Parsing failed earlier

def format_bit_locate(bit_locate_str):
    """Formats the bit locate string to '[ H : L ]' format."""
    bit_locate_str = str(bit_locate_str).strip()
    # Match [ H : L ]
    match = re.search(r'\[\s*(\d+)\s*:\s*(\d+)\s*\]', bit_locate_str)
    if match:
        # Ensure high bit is first
        b1 = int(match.group(1))
        b2 = int(match.group(2))
        return f"[ {max(b1, b2)} : {min(b1, b2)} ]"
    # Match [ B ] (single bit)
    match = re.search(r'\[\s*(\d+)\s*\]', bit_locate_str)
    if match:
        bit = match.group(1)
        return f"[ {bit} : {bit} ]" # Represent as range
    raise ValueError(f"Could not parse Bit Locate: '{bit_locate_str}'")

# --- Main Processing Logic ---
generated_sv_lines = []
processed_lines = 0
skipped_lines = 0

try:
    # Read the log file line by line
    with open(log_file_path, 'r', encoding='utf-8') as f_log:
        log_content = f_log.readlines()

    # Process each line from the log file
    for line_num, line in enumerate(log_content):
        line = line.strip()
        if not line:
            continue

        # Replace 'nan' with 'None' BEFORE parsing
        safe_line = re.sub(r':\s*nan\b(\s*[,}])', r': None\1', line)
        safe_line = re.sub(r':\s*nan\s*$', ': None', safe_line)

        try:
            data = ast.literal_eval(safe_line)
            if not isinstance(data, dict):
                print(f"Warning: Skipping line {line_num + 1}: Parsed data is not a dictionary.")
                skipped_lines += 1
                continue
        except Exception as e:
            print(f"Warning: Skipping line {line_num + 1} due to parsing error: {e}")
            skipped_lines += 1
            continue

        # Extract fields
        item = data.get('Item')
        register = data.get('Register')
        sub_register = data.get('SubRegister') # May be None
        bit_locate_orig = data.get('Bit Locate')
        usecase_orig = data.get('Usecase') # May be None

        # --- Check for special *_ADDR_INIT handling FIRST ---
        is_addr_init_case = False
        if addr_init_enable and register and isinstance(register, str) and register.endswith('_ADDR_INIT'):
            print(f"Info: Applying special handling for ADDR_INIT register: {register} on line {line_num + 1}")
            is_addr_init_case = True
            # Override values for this case
            bit_locate = addr_init_fixed_bit_locate
            usecase = addr_init_default_usecase
            # We won't use sub_register for naming in this case
        else:
            # --- Standard Filtering ---
            # Skip if SubRegister is missing, None, NaN or empty string
            if pd.isna(sub_register) or sub_register == "":
                 skipped_lines += 1
                 continue
            # Skip if Usecase is missing, None, NaN or empty string
            if pd.isna(usecase_orig) or usecase_orig == "":
                 skipped_lines += 1
                 continue
            # Use original values if not the special ADDR_INIT case
            bit_locate = bit_locate_orig
            usecase = usecase_orig


        # Ensure necessary base fields are present
        if not all([item, register, bit_locate, usecase]):
             print(f"Warning: Skipping line {line_num + 1} due to missing Item, Register, Bit Locate or Usecase after initial checks.")
             skipped_lines += 1
             continue

        # --- Process Valid Entries (either standard or ADDR_INIT) ---
        try:
            # Process Usecase string (either original or default)
            parsed_bins = parse_usecase(usecase)
            if parsed_bins is None:
                # Warning/Info is printed inside parse_usecase
                skipped_lines += 1
                continue

            # Format the bins part of the coverpoint
            if isinstance(parsed_bins, tuple) and parsed_bins[0] == 'range':
                bins_sv_str = f"bins b[] = [ {parsed_bins[1]} : {parsed_bins[2]} ]"
            elif isinstance(parsed_bins, list):
                 if not parsed_bins:
                     bins_sv_str = "bins b[] = { }"
                 else:
                     bins_sv_str = f"bins b[] = {{ {', '.join(map(str, parsed_bins))} }}"
            else:
                 print(f"Internal Error: Skipping line {line_num + 1}. Unexpected parse result for Usecase: {parsed_bins}")
                 skipped_lines += 1
                 continue

            # Format Bit Locate (either original or fixed)
            formatted_bit_locate = format_bit_locate(bit_locate)

            # --- Coverpoint Naming ---
            if is_addr_init_case:
                # For ADDR_INIT case, use <Item>_<Register>_CP
                cp_name_raw = f"{item}_{register}_CP"
            else:
                # For standard case, use <Item>_<Register>_<SubRegister>_CP
                cp_name_raw = f"{item}_{register}_{sub_register}_CP"
            # Sanitize name
            cp_name = re.sub(r'\W|^(?=\d)', '_', cp_name_raw)


            # Construct the signal name (lowercase item_register)
            signal_item = str(item).lower()
            signal_register = str(register).lower()
            signal_name = f"andla_regfile.{signal_item}_{signal_register}"

            # Append generated lines
            generated_sv_lines.append(f"{indentation}{cp_name}")
            generated_sv_lines.append(f"{indentation}: coverpoint {signal_name} {formatted_bit_locate} {{ {bins_sv_str}; }}")
            generated_sv_lines.append("") # Add a blank line between coverpoints
            processed_lines += 1

        except ValueError as e: # Catch errors from format_bit_locate or safe_eval_num inside processing
             print(f"Warning: Skipping line {line_num + 1} due to data processing error: {e}")
             skipped_lines += 1
             continue
        except Exception as e: # Catch unexpected errors during processing
            print(f"Error: Unexpected error processing line {line_num + 1}: {e}")
            skipped_lines += 1
            continue

    print(f"Log file processing complete. Processed entries: {processed_lines}, Skipped/Error lines: {skipped_lines}")

except FileNotFoundError:
    print(f"Error: Log file not found at {log_file_path}")
    exit(1)
except Exception as e:
    print(f"Error reading or processing log file: {e}")
    exit(1)


# --- File Writing ---
# (File writing logic remains the same as the previous version)
try:
    # Ensure output directory exists
    output_dir = os.path.dirname(output_file_path)
    if output_dir and not os.path.exists(output_dir):
        print(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir)

    # Read template and write to output, inserting generated lines
    with open(template_file_path, 'r', encoding='utf-8') as f_template, \
         open(output_file_path, 'w', encoding='utf-8') as f_output:

        found_marker = False
        for t_line in f_template:
            # Write the line from the template first
            f_output.write(t_line)
            # Check if this line contains the marker (strip whitespace for robust comparison)
            if t_line.strip() == marker.strip():
                 found_marker = True
                 print(f"Marker found. Inserting {processed_lines} coverpoints.")
                 # Write the generated content *after* the marker line
                 for gen_line in generated_sv_lines:
                     f_output.write(gen_line + '\n') # Ensure newline

    if not found_marker:
        print(f"Warning: Marker '{marker}' not found in template file {template_file_path}.")
        print("Generated content was not inserted.")
    elif processed_lines > 0:
         print(f"Successfully generated SystemVerilog file: {output_file_path}")
    else:
         print(f"Generated SystemVerilog file (no coverpoints added): {output_file_path}")


except FileNotFoundError:
    print(f"Error: Template file not found at {template_file_path}")
    exit(1)
except Exception as e:
    print(f"Error writing output file '{output_file_path}': {e}")
    exit(1)
