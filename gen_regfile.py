#!/usr/bin/env python3
# ─┐
# │  Author Information
# │  Author      : Hao Chun (Noah) Liang   (translated to Python)
# │  Affiliation : Bachelor of EE, National Tsing Hua University
# │  Position    : CA Group RD-CA-CAA Intern
# │  Email       : science103555@gmail.com
# │  Date        : 2024/12/31 (Tuesday)
# │  Description : Automatic Code Generation for the AnDLA
# │                Register File RTL code.  (Perl → Python port, no optimisation)
# └────────────────────────────────────────────────────────────────────

import os
import re
import ast
import math
from dataclasses import dataclass
from pathlib import Path

from registry import WRITER_REGISTRY, register_writer

# 檔案路徑設定
input_filename       = 'input/andla_regfile.tmp.v'
output_filename      = 'output/andla_regfile.v'
dictionary_filename  = 'output/regfile_dictionary.log'

@dataclass
class DictRow:
    item: str = ''
    register: str = ''
    subregister: str = ''
    type: str = ''
    id: int | None = None
    default_value: str = ''
    raw: dict = None

    @classmethod
    def from_line(cls, line: str) -> "DictRow":
        data = eval(line, {"__builtins__": None, "nan": float('nan')})
        item = str(data.get('Item', '')).lower()
        register = str(data.get('Register', '')).lower()
        sub = data.get('SubRegister')
        if isinstance(sub, float) and math.isnan(sub):
            subreg = ''
        elif sub is None:
            subreg = ''
        else:
            subreg = str(sub).lower()
        typ = str(data.get('Type', '')).lower()
        _id = data.get('ID')
        if _id is None or (isinstance(_id, float) and math.isnan(_id)):
            parsed_id = None
        else:
            parsed_id = int(_id)
        dv = data.get('Default Value')
        if dv is None or (isinstance(dv, float) and math.isnan(dv)):
            dv_str = ''
        else:
            dv_str = str(dv)
        return cls(item, register, subreg, typ, parsed_id, dv_str, data)

def load_dictionary_lines():
    """Read dictionary file and parse each line into DictRow objects.

    Any rows where the ``Type`` field evaluates to ``nan`` are ignored so
    that subsequent generation stages do not process them.
    """
    with open(dictionary_filename, 'r') as dict_fh:
        rows = [DictRow.from_line(line.rstrip('\n')) for line in dict_fh]

    # Filter out entries whose type is represented as ``nan``.  ``from_line``
    # already lower-cases the value so a simple string comparison suffices.
    return [row for row in rows if row.type != 'nan']


class TemplateWriter:
    """Base class implementing the data → template → output pipeline."""
    def __init__(self, outfile, dict_lines):
        self.outfile = outfile
        self.lines = dict_lines

    def render(self):
        """Return an iterable of strings to be written to the file."""
        raise NotImplementedError

    def write(self):
        for line in self.render():
            self.outfile.write(line)


class AlignMixin:
    """Mixin providing alignment helpers for generated code."""

    def align_pairs(self, pairs, sep=' '):
        if not pairs:
            return []
        max_len = max(len(left) for left, _ in pairs)
        return [f"{left:<{max_len}}{sep}{right}\n" for left, right in pairs]


class ZeroFillMixin:
    """Mixin to generate zero assignment lines for ID gaps."""

    def fill_zero(self, start, end, template):
        return [template.format(idx=idx) for idx in range(start - 1, end, -1)]


class BaseWriter(TemplateWriter):
    """Common base writer holding the output file and dictionary content."""

    def get_columns(self, row: DictRow, columns):
        """Return a mapping of requested columns from a DictRow."""
        result = {}
        for col in columns:
            attr = col.lower().replace(' ', '_')
            if hasattr(row, attr):
                val = getattr(row, attr)
                if val is not None:
                    result[col] = val
        return result

    def iter_items(self):
        """Yield (item, id) pairs sorted by id descending."""
        items = {}
        for row in self.lines:
            item = row.item
            _id = row.id
            if item and _id is not None:
                items[item] = _id
        for key in sorted(items, key=items.get, reverse=True):
            yield key, items[key]

    def iter_dma_items(self):
        """Return unique DMA item names excluding ldma2."""
        result = []
        for row in self.lines:
            item = row.item
            if item and 'dma' in item and item != 'ldma2' and item not in result:
                result.append(item)
        return result

    def write(self):
        """Write rendered lines to outfile."""
        for line in self.render():
            self.outfile.write(line)

########################################################################
# InterruptWriter
########################################################################
@register_writer("interrupt")
class InterruptWriter(BaseWriter):
    def write_interrupt(self):
        for key, _ in self.iter_items():
            if key in ('ldma2', 'csr'):
                continue
            self.outfile.write(f"                          ({key}_except & {key}_except_mask) |\n")

    write = write_interrupt

########################################################################
# ExceptwireWriter
########################################################################
@register_writer("exceptwire")
class ExceptwireWriter(BaseWriter):
    def write_exceptwire(self):
        for key, _ in self.iter_items():
            if key in ('ldma2', 'csr'):
                continue
            uckey = key.upper()
            self.outfile.write(f"wire {key}_except        = csr_status_reg[`{uckey}_ID + 8];\n")
            self.outfile.write(f"wire {key}_except_mask   = csr_control_reg[`{uckey}_ID + 8];\n")

    write = write_exceptwire

########################################################################
# ExceptioWriter
########################################################################
@register_writer("exceptio")
class ExceptioWriter(BaseWriter):
    def write_exceptio(self):
        for key, _ in self.iter_items():
            if key in ('ldma2', 'csr'):
                continue
            self.outfile.write(f"input                 rf_{key}_except_trigger;\n")

    write = write_exceptio

########################################################################
# ExceptportWriter
########################################################################
@register_writer("exceptport")
class ExceptportWriter(BaseWriter):
    def write_exceptport(self):
        for key, _ in self.iter_items():
            if key in ('ldma2', 'csr'):
                continue
            self.outfile.write(f",rf_{key}_except_trigger\n")

    write = write_exceptport

########################################################################
# RiurwaddrWriter
########################################################################
@register_writer("riurwaddr")
class RiurwaddrWriter(ZeroFillMixin, BaseWriter):
    def render_riurwaddr(self):
        output = []
        prev_id = None
        for key, value in self.iter_items():
            if prev_id is not None and prev_id - value > 1:
                output.extend(self.fill_zero(prev_id, value, "wire riurwaddr_bit{idx}                      = 1'b0;\n"))
            uckey = key.upper()
            if key == 'csr':
                output.append(f"wire riurwaddr_bit{value}                      = 1'b0;\n")
            else:
                output.append(f"wire riurwaddr_bit{value}                      = (issue_rf_riurwaddr[(RF_ADDR_BITWIDTH-1) -: ITEM_ID_BITWIDTH] == `{uckey}_ID);\n")
            prev_id = value
        return output

    render = render_riurwaddr

########################################################################
# StatusnxWriter
########################################################################
@register_writer("statusnx")
class StatusnxWriter(ZeroFillMixin, BaseWriter):
    def render_statusnx(self):
        items = list(self.iter_items())
        
        output = []
        prev_id = None
        for key, value in items:
            uckey = key.upper()
            if prev_id is not None and prev_id - value > 1:
                output.extend(self.fill_zero(prev_id, value, "assign csr_status_nx[{idx}]                = 1'b0;\n"))
            if key == 'csr':
                output.append("assign csr_status_nx[0]                = (wr_taken & sfence_en[0]  ) ? 1'b1 : scoreboard[0];\n")
            else:
                output.append(f"assign csr_status_nx[`{uckey}_ID]         = (wr_taken & sfence_en[`{uckey}_ID]  ) ? 1'b1 : scoreboard[`{uckey}_ID];\n")
            prev_id = value

        prev_id = None
        for key, value in items:
            uckey = key.upper()
            if prev_id is not None and prev_id - value > 1:
                output.extend(self.fill_zero(prev_id, value, "assign csr_status_nx[{idx} + 8]                = 1'b0;\n"))
            if key == 'csr':
                output.append("assign csr_status_nx[8]                           = 1'b0;\n")
            elif key == 'ldma2':
                output.append(f"assign csr_status_nx[`{uckey}_ID + 8]                = rf_ldma_except_trigger ? 1'b1 : (wr_taken & csr_status_en) ? issue_rf_riuwdata[`{uckey}_ID + 8] : csr_status_reg[`{uckey}_ID + 8];\n")
            else:
                output.append(f"assign csr_status_nx[`{uckey}_ID + 8]                = rf_{key}_except_trigger ? 1'b1 : (wr_taken & csr_status_en) ? issue_rf_riuwdata[`{uckey}_ID + 8] : csr_status_reg[`{uckey}_ID + 8];\n")
            prev_id = value
        return output

    render = render_statusnx

########################################################################
# SfenceenWriter
########################################################################
@register_writer("sfenceen")
class SfenceenWriter(ZeroFillMixin, BaseWriter):
    def render_sfenceen(self):
        output = []
        prev_id = None
        for key, value in self.iter_items():
            uckey = key.upper()
            if prev_id is not None and prev_id - value > 1:
                output.extend(self.fill_zero(prev_id, value, "               1'b0,\n"))

            if key == 'csr':
                output.append("               1'b0\n")
            elif key == 'ldma2':
                output.append("               1'b0,\n")
            else:
                output.append(f"               {key}_sfence_en,\n")
            prev_id = value
        return output

    render = render_sfenceen

########################################################################
# ScoreboardWriter
########################################################################
@register_writer("scoreboard")
class ScoreboardWriter(ZeroFillMixin, BaseWriter):
    def render_scoreboard(self):
        output = []
        prev_id = None
        for key, value in self.iter_items():
            uckey = key.upper()
            if prev_id is not None and prev_id - value > 1:
                output.extend(self.fill_zero(prev_id, value, "assign scoreboard[{idx}]               = 1'b0;\n"))

            if key == 'csr':
                output.append(f"assign scoreboard[{value}]               = (ip_rf_status_clr[0]) ? 1'b0 : csr_status_reg[0];\n")
            else:
                output.append(f"assign scoreboard[{value}]               = (ip_rf_status_clr[`{uckey}_ID]) ? 1'b0 : csr_status_reg[`{uckey}_ID];\n")
            prev_id = value
        return output

    render = render_scoreboard

########################################################################
# BaseaddrselbitwidthWriter
########################################################################
@register_writer("baseaddrselbitwidth")
class BaseaddrselbitwidthWriter(BaseWriter):
    def write_baseaddrselbitwidth(self):
        for keys in self.iter_dma_items():
            uckeys = keys.upper()
            self.outfile.write(f"localparam {uckeys}_BASE_ADDR_SELECT_BITWIDTH = 3;\n")

    write = write_baseaddrselbitwidth

########################################################################
# BaseaddrselioWriter
########################################################################
@register_writer("baseaddrselio")
class BaseaddrselioWriter(BaseWriter):
    def write_baseaddrselio(self):
        for keys in self.iter_dma_items():
            uckeys = keys.upper()
            self.outfile.write(f"output [{uckeys}_BASE_ADDR_SELECT_BITWIDTH-           1:0] {keys}_base_addr_select;\n")

    write = write_baseaddrselio

########################################################################
# BaseaddrselportWriter
########################################################################
@register_writer("baseaddrselport")
class BaseaddrselportWriter(BaseWriter):
    def write_baseaddrselport(self):
        for keys in self.iter_dma_items():
            self.outfile.write(f",{keys}_base_addr_select\n")

    write = write_baseaddrselport

########################################################################
# BaseaddrselWriter
########################################################################
@register_writer("baseaddrsel")
class BaseaddrselWriter(BaseWriter):
    def write_baseaddrsel(self):
        for keys in self.iter_dma_items():
            uckeys = keys.upper()
            self.outfile.write(
f"""
wire [{uckeys}_BASE_ADDR_SELECT_BITWIDTH-1:0] {keys}_base_addr_select_nx;
assign  {keys}_base_addr_select_nx           = {keys}_sfence_nx[20:18];
wire {keys}_base_addr_select_en           = wr_taken & {keys}_sfence_en;
reg  [{uckeys}_BASE_ADDR_SELECT_BITWIDTH-1:0] {keys}_base_addr_select_reg;
always @(posedge clk or negedge rst_n) begin
    if (~rst_n)                        {keys}_base_addr_select_reg <= {{({uckeys}_BASE_ADDR_SELECT_BITWIDTH){{1'd0}}}};
    else if ({keys}_base_addr_select_en) {keys}_base_addr_select_reg <= {keys}_base_addr_select_nx;
end
wire [3-1: 0] {keys}_base_addr_select;
assign {keys}_base_addr_select            = {keys}_base_addr_select_reg;\n\n"""
            )

    write = write_baseaddrsel

########################################################################
# SfenceWriter
########################################################################
@register_writer("sfence")
class SfenceWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_sfence = {}

    def write_sfence(self):
        for row in self.lines:
            item = row.item
            register = row.register
            if item and register == 'sfence':
                self.seen_sfence[item] = 1
        for keys in self.seen_sfence:
            self.outfile.write(
f"""wire {keys}_start_reg_nx = wr_taken & {keys}_sfence_en;
reg  {keys}_start_reg;
wire {keys}_start_reg_en = {keys}_start_reg ^ {keys}_start_reg_nx;
always @(posedge clk or negedge rst_n) begin
    if (~rst_n) {keys}_start_reg <= 1'b0;
    else if ({keys}_start_reg_en) {keys}_start_reg <= {keys}_start_reg_nx;
end
assign rf_{keys}_sfence = {keys}_start_reg;\n\n"""
            )

    write = write_sfence

########################################################################
# IpnumWriter
########################################################################
@register_writer("ipnum")
class IpnumWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_items = {}

    def write_ipnum(self):
        for row in self.lines:
            item = row.item
            if item and item not in self.seen_items:
                self.seen_items[item] = 1
        # 與原 Perl 保持一致：直接輸出 ITEM_ID_NUM 巨集
        self.outfile.write("localparam ITEM_ID_NUM = `ITEM_ID_NUM;\n")

    write = write_ipnum

########################################################################
# PortWriter
########################################################################
@register_writer("port")
class PortWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_items = {}

    def write_port(self):
        for row in self.lines:
            item = row.item
            register = row.register
            typ = row.type
            if not item or not register:
                continue

            if item == 'csr' and (typ != 'rw' or register in ('counter', 'counter_mask', 'status', 'control')):
                continue
            if item == 'csr' and re.search(r'exram_based_addr', register):
                continue

            key = f"{item}_{register}"
            if key in self.seen_items:
                continue
            self.outfile.write(f", rf_{item}_{register}\n")
            self.seen_items[key] = 1

    write = write_port

########################################################################
# BitwidthWriter
########################################################################
@register_writer("bitwidth")
class BitwidthWriter(AlignMixin, BaseWriter):
    """
    直接對照 Perl 程式；所有重複與原始邏輯完整保留，不做結構化優化
    """
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_items      = {}
        self.seen_cases      = {}
        self.bitwidth_lines  = []
        self.item            = ''
        self.register        = ''
        self.subregister     = ''
        self.key             = ''

    def fetch_terms(self, row: DictRow):
        self.item        = row.item.upper()
        self.register    = row.register.upper()
        self.subregister = row.subregister.upper() if row.subregister else ''
        self.key         = f"{self.item}_{self.register}"

    def render_bitwidth(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self.subregister:
                if self.subregister not in ('MSB', 'LSB'):
                    if (self.item, self.register) in self.seen_cases:
                        continue
                    self.bitwidth_lines.append(f"localparam {self.item}_{self.register}_BITWIDTH = `{self.item}_{self.register}_BITWIDTH;")
                    self.seen_cases[(self.item, self.register)] = 1
                else:
                    sub_key = f"{self.key}_{self.subregister}"
                    if sub_key not in self.seen_items:
                        self.bitwidth_lines.append(f"localparam {self.item}_{self.register}_{self.subregister}_BITWIDTH = `{self.item}_{self.register}_{self.subregister}_BITWIDTH;")
                        self.seen_items[sub_key] = 1
                        if self.subregister == 'MSB':
                            self.bitwidth_lines.append(f"localparam {self.item}_{self.register}_BITWIDTH = `{self.item}_{self.register}_BITWIDTH;")
            elif self.register:
                if self.key in self.seen_items:
                    continue
                if self.register == 'CREDIT':
                    self.bitwidth_lines.append(f"localparam {self.item}_{self.register}_BITWIDTH = 22;")
                else:
                    self.bitwidth_lines.append(f"localparam {self.item}_{self.register}_BITWIDTH = `{self.item}_{self.register}_BITWIDTH;")
                self.seen_items[self.key] = 1

        pairs = []
        for l in self.bitwidth_lines:
            left, right = l.split('=', 1)
            pairs.append((left.strip(), right.strip()))
        return self.align_pairs(pairs, ' = ')

    render = render_bitwidth

########################################################################
# IOWriter
########################################################################
@register_writer("io")
class IOWriter(AlignMixin, BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_items = {}
        self.io_lines   = []
        self.item       = ''
        self.register   = ''
        self.key        = ''
        self.typ        = ''

    def fetch_terms(self, row: DictRow):
        self.item     = row.item
        self.register = row.register
        self.key      = f"{self.item}_{self.register}"
        self.typ      = row.type

    def _skip(self):
        if self.item == 'csr' and (self.typ != 'rw' or self.register in ('counter','counter_mask','status','control')):
            return True
        if self.key in self.seen_items:
            return True
        return False

    def _process(self):
        if self._skip():
            return
        if self.typ == 'ro':
            self.io_lines.append(f"input\t [{self.item.upper()}_{self.register.upper()}_BITWIDTH-1:0] rf_{self.item}_{self.register};")
        else:
            if self.item == 'csr' and 'exram_based_addr' in self.register:
                self.io_lines.append(f"wire\t [{self.item.upper()}_{self.register.upper()}_BITWIDTH-1:0] {self.item}_{self.register};")
            elif self.register == 'sfence':
                self.io_lines.append(f"output\t [1-1:0] rf_{self.item}_{self.register};")
            else:
                self.io_lines.append(f"output\t [{self.item.upper()}_{self.register.upper()}_BITWIDTH-1:0] rf_{self.item}_{self.register};")
        self.seen_items[self.key] = 1

    def render_io(self):
        for row in self.lines:
                self.fetch_terms(row)
                self._process()

        pairs = []
        for l in self.io_lines:
            left, right = l.split('\t', 1)
            pairs.append((left, right))
        return self.align_pairs(pairs, '\t')

    render = render_io

########################################################################
# RegWriter
########################################################################
@register_writer("reg")
class RegWriter(AlignMixin, BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.reg_lines  = []
        self.seen_items = {}
        self.seen_cases = {}
        self.item       = ''
        self.register   = ''
        self.subregister= ''
        self.key        = ''
        self.typ        = ''

    def fetch_terms(self, row: DictRow):
        self.item       = row.item
        self.register   = row.register
        self.subregister= row.subregister
        self.key        = f"{self.item}_{self.register}"
        self.typ        = row.type

    def _skip(self):
        return self.typ != 'rw'

    def render_reg(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self._skip():
                continue
            if self.subregister:
                if self.subregister in ('lsb','msb'):
                    self.reg_lines.append(f"reg\t[{self.item.upper()}_{self.register.upper()}_{self.subregister.upper()}_BITWIDTH-1:0] {self.item}_{self.register}_{self.subregister}_reg;")
                else:
                    if self.key not in self.seen_items:
                        self.reg_lines.append(f"reg\t[{self.item.upper()}_{self.register.upper()}_BITWIDTH-1:0] {self.item}_{self.register}_reg;")
                        self.seen_items[self.key] = 1
            elif self.register:
                self.reg_lines.append(f"reg\t[{self.item.upper()}_{self.register.upper()}_BITWIDTH-1:0] {self.item}_{self.register}_reg;")

        pairs = []
        for l in self.reg_lines:
            left, right = l.split('] ', 1)
            pairs.append((left + ']', right))
        return self.align_pairs(pairs, '\t')

    render = render_reg

########################################################################
# WireNxWriter
########################################################################
@register_writer("wire_nx")
class WireNxWriter(AlignMixin, BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.wire_lines       = []
        self.seen_items       = {}
        self.item             = ''
        self.register         = ''
        self.subregister      = ''
        self.key              = ''
        self.item_upper       = ''
        self.register_upper   = ''
        self.subregister_upper= ''
        self.typ              = ''

    def fetch_terms(self, row: DictRow):
        self.item        = row.item
        self.register    = row.register
        self.subregister = row.subregister
        self.key = f"{self.item}_{self.register}"
        self.item_upper       = self.item.upper()
        self.register_upper   = self.register.upper()
        self.subregister_upper= self.subregister.upper() if self.subregister else ''
        self.typ = row.type

    def _skip(self):
        if self.typ != 'rw':
            return True
        if self.subregister not in ('msb','lsb') and self.key in self.seen_items:
            return True
        self.seen_items[self.key] = 1
        return False

    def render_wire_nx(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self._skip():
                continue
            if self.subregister:
                if self.subregister in ('msb','lsb'):
                    self.wire_lines.append(f"wire\t[{self.item_upper}_{self.register_upper}_{self.subregister_upper}_BITWIDTH-1:0] {self.item}_{self.register}_{self.subregister}_nx;")
                else:
                    self.wire_lines.append(f"wire\t[{self.item_upper}_{self.register_upper}_BITWIDTH-1:0] {self.item}_{self.register}_nx;")
            elif self.register:
                self.wire_lines.append(f"wire\t[{self.item_upper}_{self.register_upper}_BITWIDTH-1:0] {self.item}_{self.register}_nx;")

        pairs = []
        for l in self.wire_lines:
            left, right = l.split('] ', 1)
            pairs.append((left + ']', right))
        return self.align_pairs(pairs, '   ')

    render = render_wire_nx

########################################################################
# WireEnWriter
########################################################################
@register_writer("wire_en")
class WireEnWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_items       = {}
        self.outfile          = outfile
        self.item             = ''
        self.register         = ''
        self.subregister      = ''
        self.key              = ''
        self.wire_name        = ''
        self.typ              = ''

    def fetch_terms(self, row: DictRow):
        self.item        = row.item
        self.register    = row.register
        self.subregister = row.subregister
        self.key = f"{self.item}_{self.register}"
        self.typ = row.type

    def _skip(self):
        if self.typ != 'rw':
            return True
        if self.subregister not in ('msb','lsb'):
            if self.key in self.seen_items:
                return True
            self.seen_items[self.key] = 1
        return False

    def render_wire_en(self):
        self.seen_items = {}
        for row in self.lines:
                self.fetch_terms(row)
                if self._skip():
                    continue

                if self.subregister in ('msb','lsb'):
                    self.wire_name = f"{self.item}_{self.register}_{self.subregister}_en"
                else:
                    self.wire_name = f"{self.item}_{self.register}_en"
                yield f"wire   {self.wire_name};\n"

    render = render_wire_en

########################################################################
# SeqWriter
########################################################################
@register_writer("seq")
class SeqWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.reg_lines  = []
        self.seen_items = {}
        self.item       = ''
        self.register   = ''
        self.subregister= ''
        self.key        = ''
        self.typ        = ''

    def fetch_terms(self, row: DictRow):
        self.item       = row.item
        self.register   = row.register
        self.subregister= row.subregister
        self.key        = f"{self.item}_{self.register}"
        self.typ        = row.type

    def _skip(self):
        if self.typ != 'rw':
            return True
        if self.key in self.seen_items and self.subregister not in ('msb','lsb'):
            return True
        self.seen_items[self.key] = 1
        return False


    def render_seq(self):
        output = []
        output.append("always @(posedge clk or negedge rst_n) begin\n")
        output.append("    if(~rst_n) begin\n")
        for row in self.lines:
            self.fetch_terms(row)
            if self._skip():
                continue
            default = row.default_value
            if default.startswith('0x'):
                final_assignment = default.replace('0x', "32'h")
            elif self.subregister in ('msb','lsb'):
                bit = "1'b1" if default == '1' else "1'b0"
                final_assignment = f"{{ {{({self.item.upper()}_{self.register.upper()}_{self.subregister.upper()}_BITWIDTH-1){{1'd0}}}}, {bit} }}"
            else:
                bit = "1'b1" if default == '1' else "1'b0"
                final_assignment = f"{{ {{({self.item.upper()}_{self.register.upper()}_BITWIDTH-1){{1'd0}}}}, {bit} }}"

            if self.subregister in ('msb','lsb'):
                self.reg_lines.append(f"\t\t{self.item}_{self.register}_{self.subregister}_reg{' '*(50-len(self.item+self.register+self.subregister)+2)}<= {final_assignment};")
            else:
                self.reg_lines.append(f"\t\t{self.item}_{self.register}_reg{' '*(50-len(self.item+self.register)+3)}<= {final_assignment};")

        for l in self.reg_lines:
            output.append(f"{l}\n")

        output.append("    end else begin\n")
        for l in self.reg_lines:
            if '<=' in l:
                reg_name = l.split('<=')[0].strip()
                wire_name = reg_name.replace('_reg', '_nx')
                output.append(f"\t\t{reg_name:<48}<= {wire_name};\n")
        output.append("    end\n")
        output.append("end\n")
        return output

    render = render_seq

########################################################################
# EnWriter
########################################################################
@register_writer("en")
class EnWriter(AlignMixin, BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.outfile    = outfile
        self.seen_items = {}
        self.item       = ''
        self.register   = ''
        self.subregister= ''
        self.key        = ''
        self.typ        = ''

    def fetch_term(self, row: DictRow):
        self.item       = row.item
        self.register   = row.register
        self.subregister= row.subregister
        self.key        = f"{self.item}_{self.register}"
        self.typ        = row.type

    def _skip(self):
        if self.typ != 'rw':
            return True
        if self.key in self.seen_items and self.subregister not in ('msb','lsb'):
            return True
        self.seen_items[self.key] = 1
        return False

    def render_en(self):
        for row in self.lines:
                self.fetch_term(row)
                if self._skip():
                    continue

                if self.subregister in ('msb','lsb'):
                    assignment = (f"assign {self.item}_{self.register}_{self.subregister}_en"
                                  f" = (issue_rf_riurwaddr == {{`{self.item.upper()}_ID,`{self.item.upper()}_{self.register.upper()}_{self.subregister.upper()}_IDX}});")
                else:
                    assignment = (f"assign {self.item}_{self.register}_en"
                                  f" = (issue_rf_riurwaddr == {{`{self.item.upper()}_ID,`{self.item.upper()}_{self.register.upper()}_IDX}});")

                left = assignment.split('=')[0]
                right= assignment[len(left):]
                yield from self.align_pairs([(left, right)], '')

    render = render_en

########################################################################
# NxWriter
########################################################################
@register_writer("nx")
class NxWriter(AlignMixin, BaseWriter):
    """
    照原樣轉寫；重複邏輯不加抽象
    """
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.assignments = []
        self.seen_items  = {}
        self.item        = ''
        self.register    = ''
        self.subregister = ''
        self.typ         = ''
        self.key         = ''

    def fetch_terms(self, row: DictRow):
        self.item        = row.item
        self.register    = row.register
        self.subregister = row.subregister
        self.key = f"{self.item}_{self.register}"
        self.typ = row.type

    def _skip(self):
        if self.typ != 'rw':
            return True
        if self.register == 'status':
            return True
        if self.key in self.seen_items and self.subregister not in ('msb','lsb'):
            return True
        self.seen_items[self.key] = 1
        return False

    def _process_ro(self):
        if self._skip():
            return
        if self.register == 'credit' and self.item == 'csr':
            self.assignments.append("assign csr_credit_nx = sqr_credit;")
        else:
            self.assignments.append(f"assign {self.item}_{self.register}_nx = {{ {{ (32 - {self.register.upper()}_DATA.bit_length()) {{ 1'b0 }} }}, {self.register.upper()}_DATA}};")

    def render_nx(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self.typ == 'ro' and self.register:
                self._process_ro()
            elif self.subregister:
                if self._skip():
                    continue
                if self.register in ('const_value','ram_padding_value'):
                    self.assignments.append(
                        f"assign {self.item}_{self.register}_nx[{self.item.upper()}_{self.register.upper()}_BITWIDTH-1:{self.item.upper()}_{self.register.upper()}_BITWIDTH-2] = "
                        f"(wr_taken & {self.item}_{self.register}_en) ? issue_rf_riuwdata[RF_WDATA_BITWIDTH-1:RF_WDATA_BITWIDTH-2] : "
                        f"{self.item}_{self.register}_reg[{self.item.upper()}_{self.register.upper()}_BITWIDTH-1:{self.item.upper()}_{self.register.upper()}_BITWIDTH-2];"
                    )
                    self.assignments.append(
                        f"assign {self.item}_{self.register}_nx[{self.item.upper()}_{self.register.upper()}_BITWIDTH-3:0] = "
                        f"(wr_taken & {self.item}_{self.register}_en) ? issue_rf_riuwdata[{self.item.upper()}_{self.register.upper()}_BITWIDTH-3:0]: "
                        f"{self.item}_{self.register}_reg[{self.item.upper()}_{self.register.upper()}_BITWIDTH-3:0];"
                    )
                elif self.subregister in ('msb','lsb'):
                    self.assignments.append(
                        f"assign {self.item}_{self.register}_{self.subregister}_nx = "
                        f"(wr_taken & {self.item}_{self.register}_{self.subregister}_en) ? "
                        f"issue_rf_riuwdata[{self.item.upper()}_{self.register.upper()}_{self.subregister.upper()}_BITWIDTH-1:0] : "
                        f"{self.item}_{self.register}_{self.subregister}_reg;"
                    )
                else:
                    self.assignments.append(
                        f"assign {self.item}_{self.register}_nx = "
                        f"(wr_taken & {self.item}_{self.register}_en) ? "
                        f"issue_rf_riuwdata[{self.item.upper()}_{self.register.upper()}_BITWIDTH-1:0] : "
                        f"{self.item}_{self.register}_reg;"
                    )
            elif self.register:
                if self._skip():
                    continue
                self.assignments.append(
                    f"assign {self.item}_{self.register}_nx = "
                    f"(wr_taken & {self.item}_{self.register}_en) ? "
                    f"issue_rf_riuwdata[{self.item.upper()}_{self.register.upper()}_BITWIDTH-1:0] : "
                    f"{self.item}_{self.register}_reg;"
                )

        pairs = []
        for a in self.assignments:
            left, right = a.split('=', 1)
            pairs.append((left.strip(), right.strip()))
        return self.align_pairs(pairs, ' = ')

    render = render_nx

########################################################################
# CTRLWriter
########################################################################
@register_writer("control")
class CTRLWriter(AlignMixin, BaseWriter):
    """
    依原 Perl 寫法轉成 Python
    """
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.io_lines   = []
        self.seen_pair  = {}
        self.item       = ''
        self.register   = ''
        self.subregister= ''
        self.key        = ''
        self.typ        = ''

    def fetch_terms(self, row: DictRow):
        self.item       = row.item
        self.register   = row.register
        self.subregister= row.subregister
        self.key        = f"{self.item}_{self.register}"
        self.typ        = row.type

    def _skip(self):
        if self.typ != 'rw':
            return True
        if self.subregister not in ('msb','lsb'):
            if self.key in self.seen_pair:
                return True
            self.seen_pair[self.key] = 1
        return False

    def _build_output(self, signal_name, reg_name, bitwidth):
        return f"\t\t\t\t  ({{RF_RDATA_BITWIDTH{{({signal_name})}}}} & {{{{(RF_RDATA_BITWIDTH-{bitwidth}){{1'b0}}}}, {reg_name}}}) |"


    def render_control(self):
        output = ["assign issue_rf_riurdata =\n"]
        for row in self.lines:
            self.fetch_terms(row)
            if self._skip():
                continue
            if self.subregister in ('msb','lsb'):
                signal = f"{self.item}_{self.register}_{self.subregister}_en"
                reg_nm = f"{self.item}_{self.register}_{self.subregister}_reg"
                bw = f"{self.item.upper()}_{self.register.upper()}_{self.subregister.upper()}_BITWIDTH"
            else:
                signal = f"{self.item}_{self.register}_en"
                reg_nm = f"{self.item}_{self.register}_reg"
                bw = f"{self.item.upper()}_{self.register.upper()}_BITWIDTH"

            if self.subregister:
                self.io_lines.append(self._build_output(signal, reg_nm, bw))
            else:
                if self.register in ('ldma_chsum_data','sdma_chsum_data'):
                    reg_nm = f"{self.item}_{self.register}"
                self.io_lines.append(self._build_output(signal, reg_nm, bw))

        pairs = []
        for l in self.io_lines:
            left, right = l.split("1'b0", 1)
            pairs.append((left, "1'b0" + right))
        output.extend(self.align_pairs(pairs, ''))
        return output

    render = render_control

########################################################################
# OutputWriter
########################################################################
@register_writer("output")
class OutputWriter(AlignMixin, BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_pair      = {}
        self.bitwidth_lines = []
        self.ignore_pair    = {
            'csr_id'           : 1,
            'csr_revision'     : 1,
            'csr_status'       : 1,
            'csr_control'      : 1,
            'csr_credit'       : 1,
            'csr_counter'      : 1,
            'csr_counter_mask' : 1,
            'csr_nop'          : 1,
            'sdma_sfence'      : 1,
            'sdma_sdma_chsum_data' : 1,
            'ldma_sfence'      : 1,
            'ldma_ldma_chsum_data' : 1,
            'cdma_sfence'      : 1,
            'cdma_exram_addr'  : 1,
            'fme0_sfence'      : 1,
        }

    def fetch_terms(self, row: DictRow):
        self.item       = row.item
        self.register   = row.register
        self.subregister= row.subregister

    def _skip(self):
        key = f"{self.item}_{self.register}"
        if key in self.ignore_pair:
            return True
        if key in self.seen_pair:
            return True
        if self.register == 'exram_addr':
            return True
        self.seen_pair[key] = 1
        return False

    def _process(self):
        if self._skip():
            return
        if self.subregister:
            if self.item == 'csr' and self.register.startswith('exram_based_addr_'):
                out_reg = self.register.replace('_based_', '_based_')  # 同 Perl 保留
                self.bitwidth_lines.append(f"assign {self.item}_{out_reg} = {{{self.item}_{self.register}_msb_reg, {self.item}_{self.register}_lsb_reg}};")
            elif self.subregister in ('msb','lsb'):
                self.bitwidth_lines.append(f"assign rf_{self.item}_{self.register} = {{{self.item}_{self.register}_msb_reg, {self.item}_{self.register}_lsb_reg}};")
            else:
                self.bitwidth_lines.append(f"assign rf_{self.item}_{self.register} = {self.item}_{self.register}_reg;")
        else:
            self.bitwidth_lines.append(f"assign rf_{self.item}_{self.register} = {self.item}_{self.register}_reg;")

    def render_output(self):
        for row in self.lines:
                self.fetch_terms(row)
                if self.register:
                    self._process()

        pairs = []
        for l in self.bitwidth_lines:
            left, right = l.split('=', 1)
            pairs.append((left.strip(), right.strip()))
        return self.align_pairs(pairs, ' = ')

    render = render_output

# The list of writers is now populated automatically via @register_writer.

########################################################################
# Main 轉檔流程
########################################################################
def gen_regfile():
    # 讀取原始 .tmp.v
    with open(input_filename, 'r') as in_fh:
        lines = in_fh.readlines()

    # 確保輸出資料夾存在
    Path(output_filename).parent.mkdir(parents=True, exist_ok=True)

    # Prepare writer instances and regex patterns
    patterns = {
        key: re.compile(rf'^// autogen_{key}_start')
        for key in WRITER_REGISTRY
    }
    dict_lines = load_dictionary_lines()
    writers = {key: cls(None, dict_lines) for key, cls in WRITER_REGISTRY.items()}
    found = {key: False for key in WRITER_REGISTRY}

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
    gen_regfile()
