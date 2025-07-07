#!/usr/bin/env python3
"""Generate the andla.vh header using dictionary data."""

import re
from pathlib import Path

from utils import (
    BaseWriter,
    WRITER_MAP,
    load_dictionary_lines,
    register_writer,
)

# File path configuration
input_filename = 'input/andla.tmp.vh'
output_filename = 'output/andla.vh'
dictionary_filename = 'output/regfile_dictionary.log'


########################################################################
# Writer implementations
########################################################################

@register_writer('itemid')
class ItemidWriter(BaseWriter):
    """Emit `define ITEM_ID macros."""
    def skip_rule(self) -> bool:
        return False

    def render(self):
        self.prev_id = -1
        for _, self.item_upper, self.id in self.iter_items(decrease=False):
            self.emit_zero_gap(self.id, "`define RESERVED_{idx}_ID  `ANDLA_RF_ID_BITWIDTH'd{idx}\n", decrease=False)
            self.render_buffer.append(f"`define {self.item_upper}_ID  `ANDLA_RF_ID_BITWIDTH'd{self.id}\n")

        return self.align_on(self.render_buffer, '`ANDLA', sep=' `ANDLA', strip=True)


@register_writer('bitwidth')
class BitwidthWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return self.subregister_upper not in ('MSB', 'LSB') and self.seen(self.doublet_upper) and self.subregister_upper 

    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip():
                continue

            if self.subregister_upper in ('MSB', 'LSB'):
                self.render_buffer.append(f"`define {self.triplet_upper}_BITWIDTH   {self.bitwidth}\n")
                if self.subregister_upper == 'MSB':
                    self.render_buffer.append(f"`define {self.doublet_upper}_BITWIDTH   `{self.doublet_upper}_LSB_BITWIDTH+`{self.doublet_upper}_MSB_BITWIDTH\n")
            else:
                self.render_buffer.append(f"`define {self.doublet_upper}_BITWIDTH   {self.bitwidth}\n")
        
        return self.align_on(self.render_buffer, '   ', sep='   ', strip=True)

@register_writer('idx')
class IndexWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return self.subregister_upper not in ('MSB', 'LSB') and self.seen(self.doublet_upper) and self.subregister_upper 

    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip():
                continue

            if self.subregister_upper in ('MSB', 'LSB'):
                self.render_buffer.append(f"`define {self.triplet_upper}_IDX  `ANDLA_RF_INDEX_BITWIDTH'd{row.index}\n")
            else:
                self.render_buffer.append(f"`define {self.doublet_upper}_IDX  `ANDLA_RF_INDEX_BITWIDTH'd{row.index}\n")

        return self.align_on(self.render_buffer, '`ANDLA', sep='  `ANDLA', strip=True)


########################################################################
# Main generation workflow
########################################################################

def gen_vh():
    with open(input_filename, 'r') as in_fh:
        lines = in_fh.readlines()

    Path(output_filename).parent.mkdir(parents=True, exist_ok=True)

    patterns = {key: re.compile(rf'^//\s*autogen_{key}_start') for key in WRITER_MAP}
    dict_lines = load_dictionary_lines(dictionary_filename)
    writers = {key: cls(None, dict_lines) for key, cls in WRITER_MAP.items()}
    found = {key: False for key in WRITER_MAP}

    with open(output_filename, 'w') as out_fh:
        for key in writers:
            writers[key].outfile = out_fh

        for line in lines:
            out_fh.write(line)
            for key, pattern in patterns.items():
                if not found[key] and pattern.match(line):
                    writers[key].write()
                    found[key] = True


if __name__ == '__main__':
    gen_vh()
