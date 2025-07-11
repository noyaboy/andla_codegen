#!/usr/bin/env python3

import re
from pathlib import Path

from utils import (
    DictRow,
    BaseWriter,
    WRITER_MAP,
    load_dictionary_lines,
    register_writer,
)

# File path configuration
input_filename       = 'input/programming_model.tmp.adoc'
output_filename      = 'output/programming_model.adoc'
dictionary_filename  = 'output/regfile_dictionary.log'

########################################################################
# BitwidthWriter
########################################################################
@register_writer('doc')
class DocWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip():
                continue

            self.render_buffer.append(f"//[[section:{self.item_lower}-reg-{self.register_lower}]]\n")
            self.render_buffer.append(f"==== {self.register_upper} (0x{self.physical_address})\n")
            self.render_buffer.append(f"*Command ID*: {self.id} +\n")
            self.render_buffer.append(f"*Command Index*: {self.index} +\n")
            self.render_buffer.append(f"\n")
            self.render_buffer.append(f"[regdef]\n")
            self.render_buffer.append(f"----\n")
            self.render_buffer.append(f"{self.bit_locate} {self.register_upper}\n")
            self.render_buffer.append(f"----\n")
            self.render_buffer.append(f"\n")
            self.render_buffer.append(f"[regfields]\n")
            self.render_buffer.append(f"----\n")
            self.render_buffer.append(f"|Field Name |Bits |Type |Reset |Description\n")
            self.render_buffer.append(f"|{self.register_upper} |{self.bit_locate} |{self.typ.upper()} |{self.default_value} | Todo\n")
            self.render_buffer.append(f"----\n")

        return self.render_buffer


########################################################################
# Main generation workflow
########################################################################
def gen_doc():
    # Read the original .tmp.v file
    with open(input_filename, 'r') as in_fh:
        lines = in_fh.readlines()

    # Ensure the output directory exists
    Path(output_filename).parent.mkdir(parents=True, exist_ok=True)

    # Prepare writer instances and regex patterns
    patterns = {key: re.compile(rf'^// autogen_{key}_start') for key in WRITER_MAP}
    dict_lines = load_dictionary_lines(dictionary_filename)
    writers = {key: cls(None, dict_lines) for key, cls in WRITER_MAP.items()}
    found = {key: False for key in WRITER_MAP}

    with open(output_filename, 'w') as out_fh:
        # Inject file handle into each writer instance
        for key in writers:
            writers[key].outfile = out_fh

        for line in lines:
            out_fh.write(line)
            for key, pattern in patterns.items():
                if not found[key] and pattern.match(line):
                    writers[key].write()
                    found[key] = True

if __name__ == "__main__":
    gen_doc()
