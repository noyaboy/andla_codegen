#!/usr/bin/env python3
"""Generate ``andla_regfile_cov.sv`` from template.

This rewrite mirrors the old standalone script but now leverages
:class:`utils.BaseWriter` for parsing and rendering logic.  The
implementation closely follows ``gen_reg_constraint_h.py`` which
also defines a single writer class and inserts its output at a marker
inside a template file.
"""

from pathlib import Path
import re

from utils import BaseWriter, load_dictionary_lines, register_writer

# File path configuration
log_file_path = "output/regfile_dictionary.log"
template_file_path = "input/andla_regfile_cov.tmp.sv"
output_file_path = "output/andla_regfile_cov.sv"

# Marker in the template at which the generated coverpoints are inserted
marker = "// auto_gen_fme0"
# Indentation for generated lines (eight spaces matches template style)

# Special handling for *_ADDR_INIT registers
addr_init_default_usecase = "range(0, 2**22)"
addr_init_fixed_bit_locate = "[21:0]"


def safe_eval_num(num_str: str) -> int:
    """Evaluate ``num_str`` which may contain simple ``**`` expressions."""

    num_str = str(num_str).strip()
    if re.fullmatch(r"\d+", num_str):
        return int(num_str)

    power_match = re.fullmatch(r"(\d+)\s*\*\*\s*(\d+)\s*(-?\s*\d+)?", num_str)
    if power_match:
        base = int(power_match.group(1))
        exp = int(power_match.group(2))
        offset = int(power_match.group(3).replace(" ", "")) if power_match.group(3) else 0
        if exp >= 64:
            raise ValueError(f"Exponent too large in safe_eval_num: {num_str}")
        return base ** exp + offset

    if re.fullmatch(r"0x[0-9a-fA-F]+", num_str):
        return int(num_str, 16)

    return int(num_str)


def parse_usecase(usecase_str):
    """Parse ``Usecase`` field and return a list or a ("range", start, end) tuple."""

    usecase_str = str(usecase_str).strip()
    values = None
    start_val = None
    end_val = None

    match = re.fullmatch(r"range\s*\(\s*([^,]+)\s*,\s*([^)]+)\s*\)", usecase_str, re.IGNORECASE)
    if match:
        start = safe_eval_num(match.group(1))
        end = safe_eval_num(match.group(2))
        if start < end:
            values = list(range(start, end))
            start_val, end_val = start, end - 1
        else:
            values = []
            start_val, end_val = start, end - 1

    if values is None:
        match = re.fullmatch(r"range\s*\[\s*([^,]+)\s*,\s*([^\]]+)\s*\]", usecase_str, re.IGNORECASE)
        if match:
            start = safe_eval_num(match.group(1))
            end = safe_eval_num(match.group(2))
            if start <= end:
                values = list(range(start, end + 1))
                start_val, end_val = start, end
            else:
                values = []
                start_val, end_val = start, end

    if values is None:
        match = re.fullmatch(r"([^~]+)\s*~\s*(.+)", usecase_str)
        if match:
            start = safe_eval_num(match.group(1))
            end = safe_eval_num(match.group(2))
            if start <= end:
                values = list(range(start, end + 1))
                start_val, end_val = start, end
            else:
                values = []
                start_val, end_val = start, end

    if values is None and usecase_str.startswith("[") and usecase_str.endswith("]"):
        content = usecase_str[1:-1].strip()
        if content:
            vals = [safe_eval_num(v.strip()) for v in content.split(",")]
            values = vals
            if len(values) >= 32:
                start_val, end_val = min(values), max(values)
        else:
            values = []
            start_val = end_val = None

    if values is None and "," in usecase_str and not usecase_str.lower().startswith("range"):
        vals = [safe_eval_num(v.strip()) for v in usecase_str.split(",")]
        values = vals
        if len(values) >= 32:
            start_val, end_val = min(values), max(values)

    if values is None:
        val = safe_eval_num(usecase_str)
        values = [val]
        start_val = end_val = val

    if len(values) >= 32 and start_val is not None and end_val is not None:
        is_contig = len(values) == end_val - start_val + 1 and set(values) == set(range(start_val, end_val + 1))
        if is_contig:
            return ("range", start_val, end_val)

    return values


def format_bit_locate(bit_locate_str: str) -> str:
    """Normalize bit locate string to ``[ H : L ]`` form."""

    bit_locate_str = str(bit_locate_str).strip()
    m = re.search(r"\[\s*(\d+)\s*:\s*(\d+)\s*\]", bit_locate_str)
    if m:
        b1, b2 = int(m.group(1)), int(m.group(2))
        return f"[ {max(b1, b2)} : {min(b1, b2)} ]"
    m = re.search(r"\[\s*(\d+)\s*\]", bit_locate_str)
    if m:
        bit = m.group(1)
        return f"[ {bit} : {bit} ]"
    raise ValueError(f"Could not parse Bit Locate: '{bit_locate_str}'")


@register_writer("cov")
class CovWriter(BaseWriter):
    """Writer generating coverpoints for FME0 registers."""

    def skip_rule(self) -> bool:
        if self.item_upper != "FME0":
            return True
        if self.register_upper.endswith("_ADDR_INIT"):
            return False
        return not self.subregister_lower or not self.usecase

    def render(self):  # noqa: D401 - short description from BaseWriter
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip():
                continue

            if 'ADDR_INIT' in self.register_upper:
                self.usecase = addr_init_default_usecase

            parsed = parse_usecase(self.usecase)
            if isinstance(parsed, tuple) and parsed[0] == "range":
                bins_str = f"bins b[] = [ {parsed[1]} : {parsed[2]} ]"
            elif isinstance(parsed, list):
                bins_str = "bins b[] = { }" if not parsed else f"bins b[] = {{ {', '.join(map(str, parsed))} }}"
            else:
                continue

            bit_loc = addr_init_fixed_bit_locate if 'ADDR_INIT' in self.register_upper else self.bit_locate
            bit_loc = format_bit_locate(bit_loc)

            if 'ADDR_INIT' in self.register_upper:
                cp_name_raw = f"{self.item_upper}_{self.register_upper}_CP"
            else:
                cp_name_raw = f"{self.item_upper}_{self.register_upper}_{self.subregister_upper}_CP"
            cp_name = re.sub(r"\W|^(?=\d)", "_", cp_name_raw)

            signal_name = f"andla_regfile.{self.item_lower}_{self.register_lower}"

            self.render_buffer.append(f"        {cp_name}\n")
            self.render_buffer.append(f"        : coverpoint andla_regfile.{self.doublet_lower} {bit_loc} {{ {bins_str}; }}\n")
            self.render_buffer.append("\n")


        return self.render_buffer


def gen_regfile_cov_sv():
    template_lines = Path(template_file_path).read_text().splitlines(True)
    dict_lines = load_dictionary_lines(log_file_path)
    writer = CovWriter(None, dict_lines)

    Path(output_file_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_file_path, "w") as out_fh:
        for line in template_lines:
            out_fh.write(line)
            if line.strip() == marker.strip():
                writer.outfile = out_fh
                writer.write()


if __name__ == "__main__":  # pragma: no cover
    gen_regfile_cov_sv()
