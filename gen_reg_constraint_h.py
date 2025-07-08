import ast
import re
import math
# import numpy as np # Used for handling nan, but this version uses string replacement

def parse_value_expression(expr_str):
    """
    Safely evaluates simple numeric expressions, including pow/** and numbers.
    Returns the calculated integer value.
    """
    expr_str = str(expr_str).strip()
    # Handle simple numbers

    if expr_str.isdigit() or (expr_str.startswith('-') and expr_str[1:].isdigit()):
            return int(expr_str)


    # Handle pow(a, b) or a**b
    pow_match_alt = re.match(r'(\d+)\s*\*\*\s*(\d+)\s*(-?\s*\d+)?', expr_str)
    if pow_match_alt:
        base = int(pow_match_alt.group(1))
        exp = int(pow_match_alt.group(2))
        offset = 0
        if pow_match_alt.group(3):
             offset = int(pow_match_alt.group(3).replace(" ", ""))
        return (base ** exp) + offset

    pow_match = re.match(r'pow\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*(-?\s*\d+)?', expr_str, re.IGNORECASE)
    if pow_match:
        base = int(pow_match.group(1))
        exp = int(pow_match.group(2))
        offset = 0
        if pow_match.group(3):
             offset = int(pow_match.group(3).replace(" ", ""))
        return (base ** exp) + offset

    # Finally, try direct conversion
    return int(expr_str)



def format_c_value_expression(expr_str):
    """
    Formats the expression string for C output, converting ** to pow()
    and adding (uint32_t) cast before pow().
    Returns the C-formatted string.
    """
    expr_str = str(expr_str).strip()
    # Convert Python's ** to C's pow() and add cast
    pow_match_alt = re.match(r'(\d+)\s*\*\*\s*(\d+)\s*(-?\s*\d+)?', expr_str)
    if pow_match_alt:
        base = pow_match_alt.group(1)
        exp = pow_match_alt.group(2)
        if pow_match_alt.group(3):
             offset_val = int(pow_match_alt.group(3).replace(" ", ""))
             final_val = (int(base) ** int(exp)) + offset_val
             return str(final_val)
        else:
            if base != '2':
                result = pow(int(base), int(exp))
                return result
            else:
                return f"1 << {exp}" # Add (uint32_t) cast

    # Check if it's already in pow() format and add cast
    pow_match = re.match(r'pow\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*(-?\s*\d+)?', expr_str, re.IGNORECASE)
    if pow_match:
        base = pow_match.group(1)
        exp = pow_match.group(2)
        if pow_match.group(3):
             offset_val = int(pow_match.group(3).replace(" ", ""))
             final_val = (int(base) ** int(exp)) + offset_val
             return str(final_val)
        else:
            if base != '2':
                result = pow(int(base), int(exp))
                return result
            else:
                return f"1 << {exp}" # Add (uint32_t) cast

    # Otherwise, assume it's a simple number
    int(expr_str)
    return expr_str


# --- Main Program ---
input_filename = 'output/regfile_dictionary.log' # Input filename
output_filename = 'output/reg_constraint.h'     # Output filename

# Store generated definition lines separately for alignment calculation
definition_lines = []
include_lines = [
    "#ifndef _REG_CONSTRAINT_H"
    "\n"
    "#define _REG_CONSTRAINT_H"
    "\n"
    "\n"
    "#include <stdint.h> // For uint32_t",
    "\n"
    "\n"
]

with open(input_filename, 'r', encoding='utf-8') as infile:
    for line_num, line in enumerate(infile):
        line = line.strip()
        if not line:
            continue

        processed_line = line.replace(': nan', ': None').replace(', nan', ', None')


        data = ast.literal_eval(processed_line)
        if not isinstance(data, dict):
            continue


        item = data.get('Item')
        register = data.get('Register')
        sub_register = data.get('SubRegister')
        usecase = data.get('Usecase')

        if not item or not register or usecase is None:
            continue
        usecase_str = str(usecase).strip()
        if not usecase_str:
            continue

        # --- Build C variable name ---
        var_name_parts = [str(item), str(register)]
        if sub_register is not None and str(sub_register).strip():
                var_name_parts.append(str(sub_register))
        var_name = "_".join(var_name_parts) + "_CONSTRAINT"
        var_name = re.sub(r'\s+', '_', var_name)
        var_name = re.sub(r'[^a-zA-Z0-9_]', '', var_name)

        # --- Parse Usecase and generate values ---
        values = []
        size = 0
        is_large = False
        c_values_str = "{}"

        range_match = re.match(r'range\s*\(\s*(.*?)\s*,\s*(.*?)\s*\)', usecase_str, re.IGNORECASE)
        list_match = re.match(r'\[(.*)\]', usecase_str)

        if range_match:
            min_expr = range_match.group(1)
            max_expr = range_match.group(2)
            min_val_num = parse_value_expression(min_expr)
            max_val_num_limit = parse_value_expression(max_expr)
            count = max_val_num_limit - min_val_num

            if count < 0: continue # Skip invalid range

            if count >= 32:
                size = 3
                c_min_val = format_c_value_expression(min_expr)
                c_max_val = format_c_value_expression(max_expr)
                c_values_str = f"{{0xffffffff, {c_min_val}, {c_max_val}}}"
            elif count > 0:
                values = list(range(min_val_num, max_val_num_limit))
                size = len(values)
                c_values_str = f"{{{','.join(map(str, values))}}}"
            else: size = 0; c_values_str = "{}"

        elif list_match:
            list_content = list_match.group(1).strip()
            if list_content:
                raw_values = ast.literal_eval(f"[{list_content}]")
                values = [int(v) for v in raw_values]
            else: values = []

            size = len(values)
            if size >= 32:
                    size = 3
                    if values:
                        min_val_num = min(values); max_val_num = max(values)
                        c_values_str = f"{{0xffffffff, {min_val_num}, {max_val_num}}}"
                    else: c_values_str = "{0xffffffff, 0, 0}"
            elif size > 0 : c_values_str = f"{{{','.join(map(str, values))}}}"
            else: size = 0; c_values_str = "{}"

        else: continue # Skip unrecognized format

        # --- Store the generated C line (unformatted for now) ---
        definition_lines.append(f"uint32_t {var_name}[{size}] = {c_values_str};")

# --- Calculate alignment ---
max_left_len = 0
for line in definition_lines:
    if '=' in line:
        left_part_len = line.find('=') # Find index of first '='
        max_left_len = max(max_left_len, left_part_len)

# --- Format lines for alignment ---
formatted_lines = []
for line in definition_lines:
        if '=' in line:
            parts = line.split('=', 1)
            left_part = parts[0].rstrip() # Remove trailing space before '='
            right_part = parts[1].lstrip() # Remove leading space after '='
            # Calculate needed padding
            padding_len = max_left_len - len(left_part)
            # Construct the aligned line, ensuring at least one space before and after '='
            formatted_lines.append(f"{left_part}{' ' * padding_len} = {right_part}")
        else:
            # Should not happen based on current logic, but handle just in case
            formatted_lines.append(line)

# --- Write the final aligned file ---
with open(output_filename, 'w', encoding='utf-8') as outfile:
    # Write includes first
    for include_line in include_lines:
        outfile.write(include_line + '\n')
    outfile.write('\n') # Add a blank line after includes

    # Write aligned definition lines
    for formatted_line in formatted_lines:
        outfile.write(formatted_line + '\n')

    outfile.write('\n' +  "#endif /* _REG_CONSTRAINT_H  */" + '\n')
