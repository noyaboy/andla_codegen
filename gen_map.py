#!/usr/bin/env python3

"""Generate ``regfile_map.h`` from template using ``utils.BaseWriter``."""

from pathlib import Path
import re

from utils import BaseWriter, load_dictionary_lines, register_writer

# File path configuration
input_filename = "input/regfile_map.tmp.h"
output_filename = "output/regfile_map.h"
dictionary_filename = "output/regfile_dictionary.log"


@register_writer("dest")
class DestWriter(BaseWriter):
    """Emit ``_DEST`` macros for each item in ID order."""

    def skip_rule(self) -> bool:  # pragma: no cover - interface method
        return False

    def render(self):
        self.prev_id = -1
        for _, self.item_upper, self.id in self.iter_items(decrease=False):
            self.emit_zero_gap(
                self.id,
                "#define RESERVED_{idx}_DEST               (0x1 <<  {idx})\n",
                decrease=False,
            )
            self.render_buffer.append(
                f"#define {self.item_upper}_DEST               (0x1 <<  {self.id})\n"
            )

        return self.render_buffer


def gen_map():
    """Entry point for ``regfile_map.h`` generation."""

    with open(input_filename, "r") as in_fh:
        lines = in_fh.readlines()

    Path(output_filename).parent.mkdir(parents=True, exist_ok=True)

    dict_lines = load_dictionary_lines(dictionary_filename, c_code=True)
    writer = DestWriter(None, dict_lines)

    start_pat = re.compile(r"^//\s*autogen_dest_start")
    stop_pat = re.compile(r"^//\s*autogen_dest_stop")

    in_dest = False
    with open(output_filename, "w") as out_fh:
        for line in lines:
            if start_pat.match(line):
                out_fh.write(line)
                writer.outfile = out_fh
                writer.write()
                in_dest = True
            elif in_dest and stop_pat.match(line):
                out_fh.write(line)
                in_dest = False
            elif not in_dest:
                out_fh.write(line)


if __name__ == "__main__":  # pragma: no cover
    gen_map()
