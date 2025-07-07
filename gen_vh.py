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
            self.emit_zero_gap(
                self.id,
                "`define RESERVED_{idx}_ID  `ANDLA_RF_ID_BITWIDTH'd{idx}\n",
                decrease=False,
            )
            self.render_buffer.append(
                f"`define {self.item_upper}_ID  `ANDLA_RF_ID_BITWIDTH'd{self.id}\n"
            )

        pat = re.compile(r"(`define\s+\S+)\s+(.*)")
        pairs = []
        for line in self.render_buffer:
            m = pat.match(line.strip())
            if m:
                pairs.append((m.group(1), m.group(2)))

        return self.align_pairs(pairs, '  ')


@register_writer('bitwidth')
class BitwidthWriter(BaseWriter):
    """Emit `define *_BITWIDTH macros."""

    def skip_rule(self) -> bool:
        return False

    @staticmethod
    def _calc_width(bitloc: str) -> int:
        if not bitloc or bitloc == '':
            return 0
        if ':' in bitloc:
            hi, lo = map(int, bitloc.strip('[]').split(':'))
            return hi - lo + 1
        return 1

    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if not self.register_upper:
                continue

            width = row.bitwidth_configuare or self._calc_width(row.bit_locate)
            if self.subregister_upper:
                macro = f"{self.triplet_upper}_BITWIDTH"
                self.render_buffer.append(f"`define {macro}  {width}\n")
                if self.subregister_upper == 'MSB':
                    total = (
                        f"`{{{self.doublet_upper}_LSB_BITWIDTH+"
                        f"{self.doublet_upper}_MSB_BITWIDTH}}"
                    )
                    self.render_buffer.append(
                        f"`define {self.doublet_upper}_BITWIDTH  {total}\n"
                    )
            else:
                self.render_buffer.append(
                    f"`define {self.doublet_upper}_BITWIDTH  {width}\n"
                )

        pat = re.compile(r"(`define\s+\S+)\s+(.*)")
        pairs = []
        for line in self.render_buffer:
            m = pat.match(line.strip())
            if m:
                pairs.append((m.group(1), m.group(2)))

        return self.align_pairs(pairs, '  ')


@register_writer('idx')
class IndexWriter(BaseWriter):
    """Emit `define *_IDX macros."""

    def skip_rule(self) -> bool:
        return False

    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if not self.register_upper:
                continue
            macro = (
                f"{self.triplet_upper}_IDX"
                if self.subregister_upper
                else f"{self.doublet_upper}_IDX"
            )
            self.render_buffer.append(
                f"`define {macro}  `ANDLA_RF_INDEX_BITWIDTH'd{row.index}\n"
            )
        pat = re.compile(r"(`define\s+\S+)\s+(.*)")
        pairs = []
        for line in self.render_buffer:
            m = pat.match(line.strip())
            if m:
                pairs.append((m.group(1), m.group(2)))

        return self.align_pairs(pairs, '  ')


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
