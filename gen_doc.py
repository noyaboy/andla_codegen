#!/usr/bin/env python3

import re
from pathlib import Path
from typing import List

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

    def regfield_cluster(self):
        new_buffer = []

        new_buffer.append(f"[regfields]\n")
        new_buffer.append(f"----\n")
        new_buffer.append(f"|Field Name   |Bits    |Type  |Reset      |Description\n")
        new_buffer.extend(self.render_buffer_regfield)            
        new_buffer.append(f"----\n\n")
        self.render_buffer_regfield = new_buffer

    def regdef_cluster(self):
        self.render_buffer_regdef = self.insert_reserved(self.render_buffer_regdef, 31)
        self.render_buffer_regdef = self.align_on(self.render_buffer_regdef, '   ', sep='   ', strip=True)
        pairs = [self.render_buffer_regdef[i:i+5]
            for i in range(0, len(self.render_buffer_regdef), 5)
        ]

        new_buffer = []
        for pair in pairs:
            new_buffer.append("[regdef]\n")
            new_buffer.append("----\n")           
            new_buffer.extend(pair)            
            new_buffer.append("----\n\n")

        self.render_buffer_regdef = new_buffer

    def insert_reserved(self, lines: List[str], max_bit: int = 31) -> List[str]:
        tok_pat = re.compile(r'^\s*(\d+)(?::(\d+))?')
        parsed = []
        for ln in lines:
            m = tok_pat.match(ln)
            if not m:
                if 'IBMC' in ln:
                    parts = ln.split()
                    hi, lo = parts[0].split(':')
                    parsed.append((hi, lo, ln))
            else:
                hi = int(m.group(1))
                lo = int(m.group(2) or hi)
                parsed.append((hi, lo, ln))

        result = []
        prev_hi = -1
        for hi, lo, ln in parsed:
            if 'IBMCBW' in str(hi):
                prev_hi = 31
                if hi == 'IBMCBW':
                    result.append(ln)
                    result.append(f"31:IBMCBW+1   Reserved\n")
                else:
                    result.append(ln)
                    result.append(f"31:IBMCBW   Reserved\n")
            else:
                if lo > prev_hi + 1:
                    gap_hi, gap_lo = lo - 1, prev_hi + 1
                    result.append(
                        f"{gap_hi}:{gap_lo}   Reserved\n" if gap_hi != gap_lo
                        else f"{gap_lo}   Reserved\n"
                    )
                prev_hi = hi
                result.append(ln)

            

        if prev_hi < max_bit:
            gap_hi, gap_lo = max_bit, prev_hi + 1
            result.append(
                f"{gap_hi}:{gap_lo}   Reserved\n" if gap_hi != gap_lo
                else f"{gap_lo}   Reserved\n"
            )
        return result

    def render(self):
        previous_item = ''
        previous_doublet = ''
        subfield_detector = False
        for row in self.lines:
            self.fetch_terms(row)

            if subfield_detector:
                if previous_doublet != self.doublet_lower:
                    self.regdef_cluster()
                    self.regfield_cluster()
                    self.render_buffer.extend(self.render_buffer_regdef)
                    self.render_buffer.extend(self.render_buffer_regfield)
                    self.render_buffer_regdef = []
                    self.render_buffer_regfield = []
                    subfield_detector = False
            
            if self.skip():
                continue

            if previous_item != self.item_lower:
                self.render_buffer.append(f"[[section:{self.item_lower}-register]]\n")
                self.render_buffer.append(f"=== {self.item_upper} Registers\n\n")
                previous_item = self.item_lower

            if self.bitwidth_configuare:
                if '`ANDLA_IBMC_ADDR_BITWIDTH+1' in self.bitwidth_configuare:
                    self.bitwidth = 'IBMCBW:0'
                elif '`ANDLA_IBMC_ADDR_BITWIDTH' in self.bitwidth_configuare:
                    self.bitwidth = 'IBMCBW-1:0'
            else:
                self.bitwidth = self.bit_locate.strip('[]')

            self.physical_address = self.physical_address[:4] + "_" + self.physical_address[4:]

            if not self.subregister_lower:
                self.render_buffer.append(f"[[section:{self.item_lower}-reg-{self.register_lower}]]\n")
                self.render_buffer.append(f"==== {self.register_upper.capitalize()} (0x{self.physical_address})\n")
                self.render_buffer.append(f"*Command ID*: {self.id} +\n")
                self.render_buffer.append(f"*Command Index*: {self.index} +\n")
                self.render_buffer.append(f"\n")
            elif self.subregister_lower:
                if self.subregister_lower in ['lsb', 'msb']:
                    self.render_buffer.append(f"[[section:{self.item_lower}-reg-{self.register_lower}]]\n")
                    self.render_buffer.append(f"==== {self.register_upper.capitalize()} {self.subregister_upper} (0x{self.physical_address})\n")
                    self.render_buffer.append(f"*Command ID*: {self.id} +\n")
                    self.render_buffer.append(f"*Command Index*: {self.index} +\n")
                    self.render_buffer.append(f"\n")
                elif not self.seen(self.doublet_lower):
                    self.render_buffer.append(f"[[section:{self.item_lower}-reg-{self.register_lower}]]\n")
                    self.render_buffer.append(f"==== {self.register_upper.capitalize()} (0x{self.physical_address})\n")
                    self.render_buffer.append(f"*Command ID*: {self.id} +\n")
                    self.render_buffer.append(f"*Command Index*: {self.index} +\n")
                    self.render_buffer.append(f"\n")
                    previous_doublet = self.doublet_lower
                    subfield_detector = True

            if self.subregister_lower:
                self.render_buffer_regdef.append(f"{self.bitwidth}   {self.subregister_upper}\n")
            else:
                self.render_buffer_regdef.append(f"{self.bitwidth}   {self.register_upper}\n")


            if self.subregister_lower and self.subregister_lower in ['lsb', 'msb']:
                self.render_buffer_regfield.append(f"\n|{self.register_upper}_{self.subregister_upper} |[{self.bitwidth}] |{self.typ.upper()} |{self.default_value} |{self.description}\n")
            elif self.subregister_lower:
                self.render_buffer_regfield.append(f"\n|{self.subregister_upper} |[{self.bitwidth}] |{self.typ.upper()} |{self.default_value} |{self.description}\n")
            else:
                self.render_buffer_regfield.append(f"\n|{self.register_upper} |[{self.bitwidth}] |{self.typ.upper()} |{self.default_value} |{self.description}\n")

            if self.enumeration:
                self.render_buffer_regfield.append('[cols="^,<3",options="header",grid="rows",frame="none",width="95%"]\n')
                self.render_buffer_regfield.append(f"!===\n")
                self.render_buffer_regfield.append(f"!Value !Meaning\n")
                for line in self.enumeration.splitlines():
                    if ':' in line:
                        key, name = [part.strip() for part in line.split(':', 1)]
                        self.render_buffer_regfield.append(f"!{key}     !{name}\n")

                self.render_buffer_regfield.append(f"!===\n")

            if not self.subregister_lower:
                self.regdef_cluster()
                self.regfield_cluster()

                self.render_buffer.extend(self.render_buffer_regdef)
                self.render_buffer.extend(self.render_buffer_regfield)
                self.render_buffer_regdef = []
                self.render_buffer_regfield = []

            if self.subregister_lower:
                if self.subregister_lower in ['lsb', 'msb']:
                    self.regdef_cluster()
                    self.regfield_cluster()

                    self.render_buffer.extend(self.render_buffer_regdef)
                    self.render_buffer.extend(self.render_buffer_regfield)
                    self.render_buffer_regdef = []
                    self.render_buffer_regfield = []

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
