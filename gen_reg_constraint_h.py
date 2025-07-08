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

@register_writer("constraint")
class ConstraintWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return not self.usecase

    def render(self):
        self.render_buffer.append(f"#ifndef _REG_CONSTRAINT_H\n")
        self.render_buffer.append(f"#define _REG_CONSTRAINT_H\n")
        self.render_buffer.append(f"\n")
        self.render_buffer.append(f"#include <stdint.h> // For uint32_t\n\n")
        self.render_buffer.append(f"\n")
        
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip():
                continue

            if self.subregister_upper:
                self.render_buffer_tmp.append(f"uint32_t {self.triplet_upper}_CONSTRAINT[{self.usecase_size}] = {self.usecase_set};")
            else:
                self.render_buffer_tmp.append(f"uint32_t {self.doublet_upper}_CONSTRAINT[{self.usecase_size}] = {self.usecase_set};")

        self.render_buffer.extend(self.align_on(self.render_buffer_tmp, "=", sep=" = ", strip=True))
        self.render_buffer.append("\n#endif /* _REG_CONSTRAINT_H  */\n")
        
        return self.render_buffer


########################################################################
# Main generation workflow
########################################################################

def gen_reg_constraint_h():
    Path(output_filename).parent.mkdir(parents=True, exist_ok=True)

    dict_lines = load_dictionary_lines(input_filename, c_code=True)
    writer = ConstraintWriter(None, dict_lines)

    with open(output_filename, "w") as out_fh:
        writer.outfile = out_fh
        writer.write()

if __name__ == "__main__":  # pragma: no cover
    gen_reg_constraint_h()
