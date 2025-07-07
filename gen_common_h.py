#!/usr/bin/env python3

"""Generate ``andla_common.h`` from template.

This rewrite mirrors the original script but leverages ``utils.BaseWriter``
to handle dictionary parsing and common helper routines.
"""

from pathlib import Path
import re

from utils import BaseWriter, WRITER_MAP, load_dictionary_lines, register_writer


# File paths
input_filename = "input/andla_common.tmp.h"
output_filename = "output/andla_common.h"
dictionary_filename = "output/regfile_dictionary.log"


########################################################################
# Helper utilities (ported from the original implementation)
########################################################################

_EQ_ALIGN_COL = 82


def _format_line(prefix: str, value: str) -> str:
    """Return ``prefix = value;`` with ``=`` roughly aligned."""

    spaces_needed = max(1, _EQ_ALIGN_COL - len(prefix))
    return f"{prefix}{' ' * spaces_needed}= {value};\n"


def _replace_clog2(expr: str) -> str:
    """Replace ``$clog2(<num>)`` with its value."""

    def repl(match: re.Match) -> str:
        num = int(match.group(1))
        if num <= 0 or num & (num - 1):
            raise ValueError(f"'{num}' \u4e0d\u662f 2 \u7684\u6b21\u65b9!")
        return str(num.bit_length() - 1)

    return re.sub(r"\$clog2\((\d+)\)", repl, expr)


def _parse_defines(*files: str) -> dict[str, str]:
    """Parse simple ``\`define`` macros from ``files``."""

    defines: dict[str, str] = {}
    for fname in files:
        with open(fname, "r") as fh:
            for line in fh:
                m = re.match(r"^`define\s+(\w+)\s+(\d+)\b", line)
                if m:
                    defines[m.group(1)] = m.group(2)
    return defines


########################################################################
# Writer implementation
########################################################################


@register_writer("common")
class CommonWriter(BaseWriter):
    """Emit register initialization information for ``andla_common.h``."""

    def skip_rule(self) -> bool:  # pragma: no cover - interface requirement
        return False

    def _calc_bitwidth(self) -> str:
        """Return the bitwidth string for the current row."""

        if self.bitwidth_configuare:
            expr = self.bitwidth_configuare
            if expr and expr[0] in ("`", "$"):
                defs = _parse_defines("./output/andla.vh", "./output/andla_config.vh")
                keys_rx = "|".join(map(re.escape, defs.keys()))

                if keys_rx:
                    expr = re.sub(rf"`?({keys_rx})", lambda m: defs.get(m.group(1), m.group(0)), expr)

                expr = _replace_clog2(expr)

                if re.fullmatch(r"[\d+\-*/]+", expr):
                    expr = str(eval(expr))  # nosec - controlled content

            return expr

        if re.search(r"\[[0-9]+:[0-9]+\]", self.bit_locate):
            hi, lo = map(int, re.findall(r"\[([0-9]+):([0-9]+)\]", self.bit_locate)[0])
            return str(hi - lo + 1)

        return "0"

    def render(self):
        seen_sub: dict[str, int] = {}
        pairs: list[tuple[str, str]] = []
        group_idx: list[int] = []

        # ------------------------------------------------------------------
        # Register information
        # ------------------------------------------------------------------
        for row in self.lines:
            self.fetch_terms(row)

            key = f"{self.item_upper}_{self.register_upper}"
            seen_sub.setdefault(key, 0)
            if self.subregister_upper and self.subregister_upper not in ("LSB", "MSB"):
                if seen_sub[key] == 1:
                    continue
                seen_sub[key] = 1

            final_reg = self.doublet_upper if not self.subregister_upper or self.subregister_upper not in ("LSB", "MSB") else self.triplet_upper

            pairs.append((f"    reg_file->item[{self.item_upper}].reg[{final_reg}].bitwidth", f"{self._calc_bitwidth()};"))
            pairs.append((f"    reg_file->item[{self.item_upper}].reg[{final_reg}].index", f"{final_reg};"))

            reg_field = self.register_lower
            if self.subregister_lower and self.subregister_lower in ("lsb", "msb"):
                reg_field = f"{self.register_lower}_{self.subregister_lower}"

            pairs.append((
                f"    reg_file->item[{self.item_upper}].reg[{final_reg}].phy_addr",
                f"&(andla_{self.item_lower}_reg_p->{reg_field});",
            ))

            group_idx.append(len(pairs))

        lines = self.align_pairs(pairs, " = ")
        self.render_buffer.extend(self._insert_blank(lines, group_idx))

        # ------------------------------------------------------------------
        # Item level information
        # ------------------------------------------------------------------
        seen_item: set[str] = set()
        pairs.clear()
        group_idx.clear()

        for row in self.lines:
            item_u = row.item.upper()
            if item_u in seen_item:
                continue
            seen_item.add(item_u)

            item_l = row.item.lower()

            pairs.append((f"    reg_file->item[{item_u}].id", f"{item_u};"))
            pairs.append((f"    reg_file->item[{item_u}].base_addr_ptr", f"andla_{item_l}_reg_p;"))
            pairs.append((f"    reg_file->item[{item_u}].reg_num", "0;"))
            group_idx.append(len(pairs))

        lines = self.align_pairs(pairs, " = ")
        self.render_buffer.extend(self._insert_blank(lines, group_idx))

        return self.render_buffer

    @staticmethod
    def _insert_blank(lines: list[str], idx: list[int]) -> list[str]:
        """Insert blank lines according to ``idx`` boundaries."""

        result: list[str] = []
        prev = 0
        for i in idx:
            result.extend(lines[prev:i])
            result.append("\n")
            prev = i
        return result


########################################################################
# Main generation workflow
########################################################################


def gen_common_h():
    with open(input_filename, "r") as in_fh:
        lines = in_fh.readlines()

    Path(output_filename).parent.mkdir(parents=True, exist_ok=True)

    dict_lines = load_dictionary_lines(dictionary_filename, c_code=True)
    writer = CommonWriter(None, dict_lines)

    with open(output_filename, "w") as out_fh:
        for line in lines:
            if re.match(r"^//\s*autogen_start\s*$", line):
                out_fh.write(line)
                writer.outfile = out_fh
                writer.write()
            elif re.match(r"^//\s*autogen_stop\s*$", line):
                out_fh.write(line)
            else:
                out_fh.write(line)


if __name__ == "__main__":  # pragma: no cover
    gen_common_h()

