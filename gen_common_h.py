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

@register_writer("common")
class CommonWriter(BaseWriter):
    def skip_rule(self) -> bool:  # pragma: no cover - interface requirement
        return self.subregister_upper and self.subregister_upper not in ("LSB", "MSB") and self.seen(self.doublet_upper)

    def render(self):
        self.render_buffer_tmp = []
        group_idx: list[int] = []

        # ------------------------------------------------------------------
        # Register information
        # ------------------------------------------------------------------
        for row in self.lines:
            self.fetch_terms(row)

            if self.skip():
                continue

            self.render_buffer_tmp.append(f"    reg_file->item[{self.item_upper}].reg[{self.item_upper}_{self.entry_upper}].bitwidth = {self._calc_bitwidth()};")
            self.render_buffer_tmp.append(f"    reg_file->item[{self.item_upper}].reg[{self.item_upper}_{self.entry_upper}].index = {self.item_upper}_{self.entry_upper};")
            self.render_buffer_tmp.append(f"    reg_file->item[{self.item_upper}].reg[{self.item_upper}_{self.entry_upper}].phy_addr = &(andla_{self.item_lower}_reg_p->{self.entry_lower});")

        # ------------------------------------------------------------------
        # Item level information
        # ------------------------------------------------------------------

        for self.item_lower, self.item_upper, _ in self.iter_items(decrease=False):
            self.render_buffer_tmp.append(f"    reg_file->item[{self.item_upper}].id = {self.item_upper};")
            self.render_buffer_tmp.append(f"    reg_file->item[{self.item_upper}].base_addr_ptr = andla_{self.item_lower}_reg_p;")
            self.render_buffer_tmp.append(f"    reg_file->item[{self.item_upper}].reg_num = 0;")

        return self.align_on(self.render_buffer_tmp, '=', sep=' = ', strip=True)

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

