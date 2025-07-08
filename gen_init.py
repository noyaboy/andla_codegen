#!/usr/bin/env python3

"""Generate ``regfile_init.h`` based on dictionary values.

This version mirrors the behaviour of the original script but leverages the
``utils.BaseWriter`` abstraction to parse the dictionary and render the output
using helper routines.
"""

from pathlib import Path
import re

from utils import BaseWriter, load_dictionary_lines, register_writer


# File paths
input_filename = "input/regfile_init.tmp.h"
output_filename = "output/regfile_init.h"
dictionary_filename = "output/regfile_dictionary.log"


@register_writer("init")
class InitWriter(BaseWriter):
    """Writer producing the register initialisation table."""

    def skip_rule(self) -> bool:
        # Only generate for RW registers.  When the register has a subregister
        # that is neither ``LSB`` nor ``MSB``, emit the entry only once.
        if self.typ != "rw":
            return True

        return (
            self.subregister_upper
            and self.subregister_upper not in ("LSB", "MSB")
            and self.seen(self.doublet_upper)
        )

    def render(self):
        for row in self.lines:
            self.fetch_terms(row)

            if self.skip():
                continue

            self.render_buffer.append(
                f"    regfile->item[{self.item_upper}].reg[{self.item_upper}_{self.entry_upper}].data = {self.default_value};"
            )

        return self.align_on(self.render_buffer, "=", sep=" = ", strip=True)


########################################################################
# Main generation workflow
########################################################################

def gen_init():
    with open(input_filename, "r") as in_fh:
        lines = in_fh.readlines()

    Path(output_filename).parent.mkdir(parents=True, exist_ok=True)

    dict_lines = load_dictionary_lines(dictionary_filename, c_code=True)
    writer = InitWriter(None, dict_lines)

    with open(output_filename, "w") as out_fh:
        for line in lines:
            if re.match(r"^//\s*autogen_start\s*$", line):
                out_fh.write(line)
                writer.outfile = out_fh
                writer.write()
            else:
                out_fh.write(line)


if __name__ == "__main__":  # pragma: no cover
    gen_init()

