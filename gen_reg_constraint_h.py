#!/usr/bin/env python3
"""Generate ``reg_constraint.h`` using dictionary data.

This rewrite leverages :class:`utils.BaseWriter` to handle parsing and
alignment of generated lines, mirroring the approach used by ``dest``
writer in ``gen_h.py``.
"""

from pathlib import Path
import ast
import re

from utils import BaseWriter, load_dictionary_lines, register_writer

# File path configuration
input_filename = "output/regfile_dictionary.log"
output_filename = "output/reg_constraint.h"

# Header preamble
include_lines = [
    "#ifndef _REG_CONSTRAINT_H",
    "#define _REG_CONSTRAINT_H",
    "",
    "#include <stdint.h> // For uint32_t",
    "",
]


def parse_value_expression(expr: str) -> int:
    """Evaluate a simple numeric expression used in ``Usecase`` fields."""
    expr = str(expr).strip()

    if expr.isdigit() or (expr.startswith("-") and expr[1:].isdigit()):
        return int(expr)

    pow_match_alt = re.match(r"(\d+)\s*\*\*\s*(\d+)\s*(-?\s*\d+)?", expr)
    if pow_match_alt:
        base = int(pow_match_alt.group(1))
        exp = int(pow_match_alt.group(2))
        offset = int(pow_match_alt.group(3).replace(" ", "")) if pow_match_alt.group(3) else 0
        return base ** exp + offset

    pow_match = re.match(r"pow\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*(-?\s*\d+)?", expr, re.IGNORECASE)
    if pow_match:
        base = int(pow_match.group(1))
        exp = int(pow_match.group(2))
        offset = int(pow_match.group(3).replace(" ", "")) if pow_match.group(3) else 0
        return base ** exp + offset

    return int(expr)


def format_c_value_expression(expr: str) -> str:
    """Convert an expression into its C representation."""
    expr = str(expr).strip()

    pow_match_alt = re.match(r"(\d+)\s*\*\*\s*(\d+)\s*(-?\s*\d+)?", expr)
    if pow_match_alt:
        base, exp = pow_match_alt.group(1), pow_match_alt.group(2)
        if pow_match_alt.group(3):
            offset = int(pow_match_alt.group(3).replace(" ", ""))
            return str(int(base) ** int(exp) + offset)
        if base != "2":
            return str(pow(int(base), int(exp)))
        return f"1 << {exp}"

    pow_match = re.match(r"pow\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*(-?\s*\d+)?", expr, re.IGNORECASE)
    if pow_match:
        base, exp = pow_match.group(1), pow_match.group(2)
        if pow_match.group(3):
            offset = int(pow_match.group(3).replace(" ", ""))
            return str(int(base) ** int(exp) + offset)
        if base != "2":
            return str(pow(int(base), int(exp)))
        return f"1 << {exp}"

    int(expr)  # validate number
    return expr


@register_writer("constraint")
class ConstraintWriter(BaseWriter):
    """Writer that emits constraint arrays for each register usecase."""

    def skip_rule(self) -> bool:
        return not self.usecase

    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip():
                continue

            parts = [self.item_upper, self.register_upper]
            if self.subregister_upper and self.subregister_upper != "NULL":
                parts.append(self.subregister_upper)
            var_name = "_".join(parts) + "_CONSTRAINT"

            usecase_str = self.usecase
            range_match = re.match(r"range\s*\(\s*(.*?)\s*,\s*(.*?)\s*\)", usecase_str, re.IGNORECASE)
            list_match = re.match(r"\[(.*)\]", usecase_str)

            size = 0
            c_values_str = "{}"

            if range_match:
                min_expr = range_match.group(1)
                max_expr = range_match.group(2)
                min_val = parse_value_expression(min_expr)
                max_val_limit = parse_value_expression(max_expr)
                count = max_val_limit - min_val
                if count < 0:
                    continue
                if count >= 32:
                    size = 3
                    c_min = format_c_value_expression(min_expr)
                    c_max = format_c_value_expression(max_expr)
                    c_values_str = f"{{0xffffffff, {c_min}, {c_max}}}"
                elif count > 0:
                    vals = list(range(min_val, max_val_limit))
                    size = len(vals)
                    c_values_str = "{" + ",".join(map(str, vals)) + "}"
                else:
                    size = 0
                    c_values_str = "{}"
            elif list_match:
                list_content = list_match.group(1).strip()
                if list_content:
                    raw_vals = ast.literal_eval(f"[{list_content}]")
                    vals = [int(v) for v in raw_vals]
                else:
                    vals = []

                size = len(vals)
                if size >= 32:
                    size = 3
                    if vals:
                        c_values_str = f"{{0xffffffff, {min(vals)}, {max(vals)}}}"
                    else:
                        c_values_str = "{0xffffffff, 0, 0}"
                elif size > 0:
                    c_values_str = "{" + ",".join(map(str, vals)) + "}"
                else:
                    size = 0
                    c_values_str = "{}"
            else:
                continue

            self.render_buffer.append(f"uint32_t {var_name}[{size}] = {c_values_str};")

        return self.align_on(self.render_buffer, "=", sep=" = ", strip=True)


########################################################################
# Main generation workflow
########################################################################

def gen_reg_constraint_h():
    Path(output_filename).parent.mkdir(parents=True, exist_ok=True)

    dict_lines = load_dictionary_lines(input_filename, c_code=True)
    writer = ConstraintWriter(None, dict_lines)

    with open(output_filename, "w") as out_fh:
        for line in include_lines:
            out_fh.write(line + "\n")
        out_fh.write("\n")
        writer.outfile = out_fh
        writer.write()
        out_fh.write("\n#endif /* _REG_CONSTRAINT_H  */\n")


if __name__ == "__main__":  # pragma: no cover
    gen_reg_constraint_h()
