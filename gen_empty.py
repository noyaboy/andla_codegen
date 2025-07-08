#!/usr/bin/env python3
"""Generate item-specific empty modules from template."""

from pathlib import Path
import re

from utils import BaseWriter, WRITER_MAP, load_dictionary_lines, register_writer

input_filename = 'input/andla_empty.tmp.v'
output_filename_template = 'output/andla_{item}.empty.v'
dictionary_filename = 'output/regfile_dictionary.log'

class ItemBaseWriter(BaseWriter):
    """Base writer that filters dictionary rows by item."""
    def __init__(self, outfile, dict_lines, item: str):
        super().__init__(outfile, dict_lines)
        self.target_item = item

    def iter_rows(self):
        for row in self.lines:
            if row.item == self.target_item:
                yield row

@register_writer('exceptport')
class ExceptportWriter(ItemBaseWriter):
    def skip_rule(self) -> bool:
        return self.target_item in ('ldma2', 'csr')

    def render(self):
        if self.skip_rule():
            return []
        return [f",rf_{self.target_item}_except_trigger\n"]

@register_writer('port')
class PortWriter(ItemBaseWriter):
    def skip_rule(self) -> bool:
        return self.item_lower == 'csr' or self.seen(self.doublet_lower)

    def render(self):
        for row in self.iter_rows():
            self.fetch_terms(row)
            if self.skip_rule():
                continue
            self.render_buffer.append(f", rf_{self.doublet_lower}\n")
        return self.render_buffer

@register_writer('bitwidth')
class BitwidthWriter(ItemBaseWriter):
    def skip_rule(self) -> bool:
        return (
            (
                self.subregister_upper
                and (
                    (
                        self.subregister_upper not in ('MSB', 'LSB')
                        and self.seen(self.doublet_upper)
                    )
                    or (
                        self.subregister_upper in ('MSB', 'LSB')
                        and self.seen(self.triplet_upper)
                    )
                )
            )
            or (
                not self.subregister_upper
                and self.register_upper
                and self.seen(self.doublet_upper)
            )
        )

    def render(self):
        for row in self.iter_rows():
            self.fetch_terms(row)
            if self.skip_rule():
                continue
            if self.subregister_upper:
                if self.subregister_upper not in ('MSB', 'LSB'):
                    self.render_buffer.append(
                        f"localparam {self.doublet_upper}_BITWIDTH = `{self.doublet_upper}_BITWIDTH;"
                    )
                else:
                    self.render_buffer.append(
                        f"localparam {self.triplet_upper}_BITWIDTH = `{self.triplet_upper}_BITWIDTH;"
                    )
                    if self.subregister_upper == 'MSB':
                        self.render_buffer.append(
                            f"localparam {self.doublet_upper}_BITWIDTH = `{self.doublet_upper}_BITWIDTH;"
                        )
            elif self.register_upper:
                if self.register_upper == 'CREDIT':
                    self.render_buffer.append(
                        f"localparam {self.doublet_upper}_BITWIDTH = 22;"
                    )
                else:
                    self.render_buffer.append(
                        f"localparam {self.doublet_upper}_BITWIDTH = `{self.doublet_upper}_BITWIDTH;"
                    )

        return self.align_on(self.render_buffer, '=', sep=' = ', strip=True)

@register_writer('io')
class IOWriter(ItemBaseWriter):
    def skip_rule(self) -> bool:
        return (
            (
                self.item_lower == 'csr'
                and (self.typ != 'rw' or 'exram_based_addr' not in self.register_lower)
            )
            or self.seen(self.doublet_lower)
        )

    def render(self):
        for row in self.iter_rows():
            self.fetch_terms(row)
            if self.skip_rule():
                continue
            if self.typ == 'ro':
                self.render_buffer.append(
                    f"output\t [{self.doublet_upper}_BITWIDTH-1:0] rf_{self.doublet_lower};"
                )
            else:
                if self.item_lower == 'csr' and 'exram_based_addr' in self.register_lower:
                    self.render_buffer.append(
                        f"input\t [{self.doublet_upper}_BITWIDTH-1:0] rf_{self.doublet_lower};"
                    )
                elif self.register_lower == 'sfence':
                    self.render_buffer.append(
                        f"input\t [1-1:0] rf_{self.doublet_lower};"
                    )
                else:
                    self.render_buffer.append(
                        f"input\t [{self.doublet_upper}_BITWIDTH-1:0] rf_{self.doublet_lower};"
                    )

        return self.align_on(self.render_buffer, '\t', sep='\t')

@register_writer('exceptio')
class ExceptioWriter(ItemBaseWriter):
    def skip_rule(self) -> bool:
        return self.target_item in ('ldma2', 'csr')

    def render(self):
        if self.skip_rule():
            return []
        return [f"output                 rf_{self.target_item}_except_trigger;\n"]

def gen_empty_item(item: str, lines, dict_lines):
    output_filename = output_filename_template.format(item=item)
    Path(output_filename).parent.mkdir(parents=True, exist_ok=True)

    patterns = {key: re.compile(rf'^//\s*autogen_{key}_start') for key in WRITER_MAP}
    writers = {key: cls(None, dict_lines, item) for key, cls in WRITER_MAP.items()}
    found = {key: False for key in WRITER_MAP}

    with open(output_filename, 'w') as out_fh:
        for key in writers:
            writers[key].outfile = out_fh

        for line in lines:
            if line.lstrip().startswith('module andla_empty'):
                line = line.replace('andla_empty', f'andla_{item}')
            out_fh.write(line)
            for key, pattern in patterns.items():
                if not found[key] and pattern.match(line):
                    writers[key].write()
                    found[key] = True


def gen_empty():
    with open(input_filename, 'r') as in_fh:
        lines = in_fh.readlines()

    dict_lines = load_dictionary_lines(dictionary_filename)
    items = [item for item, _, _ in ItemBaseWriter(None, dict_lines, '').iter_items() if item != 'csr']

    for item in items:
        gen_empty_item(item, lines, dict_lines)

if __name__ == '__main__':
    gen_empty()
