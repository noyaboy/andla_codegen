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


class BaseWriter:
    """
    通用 Writer，實作 data → template → output 的流程，
    並提供取得欄位、排序 items 及過濾 DMA items 的方法。
    """
    def __init__(self, outfile, dict_lines):
        self.outfile = outfile
        self.lines = dict_lines
        # shared state for subclasses
        self.seen_set_item      = {}
        self.seen_set           = {}
        self.render_buffer      = []
        self.item_lower         = ''
        self.register_lower     = ''
        self.subregister_lower  = ''
        self.key_lower          = ''
        self.item_upper         = ''
        self.register_upper     = ''
        self.subregister_upper  = ''
        self.key_upper          = ''
        self.typ                = ''
        self.ignore_pair        = {
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

    def render(self):
        """回傳要寫入檔案的字串 iterable；子類別或實例可 override 以輸出不同格式"""
        raise NotImplementedError

    def write(self):
        """把 render() 產生的每一行寫到 outfile"""
        for line in self.render():
            self.outfile.write(line)

    def get_columns(self, row: DictRow, columns):
        """
        從一個 DictRow 擷取多個欄位（不區分大小寫、空格轉底線），
        僅回傳有值的那些欄位。
        """
        result = {}
        for col in columns:
            attr = col.lower().replace(' ', '_')
            if hasattr(row, attr):
                val = getattr(row, attr)
                if val is not None:
                    result[col] = val
        return result

    def iter_items(self):
        """
        產生 (item, id) pair，並依照 id 做遞減排序後回傳 key。
        """
        items = {}
        for row in self.lines:
            item = row.item
            _id = row.id
            if item and _id is not None:
                items[item] = _id
        for key in sorted(items, key=items.get, reverse=True):
            yield key, items[key]

    def iter_dma_items(self):
        """
        回傳所有包含 'dma'、不等於 'ldma2'，且去除重複的 item 名稱。
        """
        result = []
        for row in self.lines:
            item = row.item
            if item and 'dma' in item and item != 'ldma2' and item not in result:
                result.append(item)
        return result

    def fetch_terms(self, row: DictRow):
        """Populate commonly used case variants from a ``DictRow``."""
        self.item_lower        = row.item
        self.register_lower    = row.register
        self.subregister_lower = row.subregister
        if self.item_lower and self.register_lower:
            self.key_lower = f"{self.item_lower}_{self.register_lower}"
        else:
            self.key_lower = ''

        self.item_upper        = self.item_lower.upper() if self.item_lower else ''
        self.register_upper    = self.register_lower.upper() if self.register_lower else ''
        self.subregister_upper = self.subregister_lower.upper() if self.subregister_lower else ''
        if self.item_upper and self.register_upper:
            self.key_upper = f"{self.item_upper}_{self.register_upper}"
        else:
            self.key_upper = ''

        self.typ = row.type

########################################################################
# InterruptWriter
########################################################################
class InterruptWriter(BaseWriter):
    def render(self):
        output = []
        for key, _ in self.iter_items():
            if key in ('ldma2', 'csr'):
                continue
            output.append(f"                          ({key}_except & {key}_except_mask) |\n")
        return output


########################################################################
# ExceptwireWriter
########################################################################
class ExceptwireWriter(BaseWriter):
    def render(self):
        output = []
        for key, _ in self.iter_items():
            if key in ('ldma2', 'csr'):
                continue
            uckey = key.upper()
            output.append(f"wire {key}_except        = csr_status_reg[`{uckey}_ID + 8];\n")
            output.append(f"wire {key}_except_mask   = csr_control_reg[`{uckey}_ID + 8];\n")
        return output


########################################################################
# ExceptioWriter
########################################################################
class ExceptioWriter(BaseWriter):
    def render(self):
        output = []
        for key, _ in self.iter_items():
            if key in ('ldma2', 'csr'):
                continue
            output.append(f"input                 rf_{key}_except_trigger;\n")
        return output


########################################################################
# ExceptportWriter
########################################################################
class ExceptportWriter(BaseWriter):
    def render(self):
        output = []
        for key, _ in self.iter_items():
            if key in ('ldma2', 'csr'):
                continue
            output.append(f",rf_{key}_except_trigger\n")
        return output


########################################################################
# RiurwaddrWriter
########################################################################
class RiurwaddrWriter(ZeroFillMixin, BaseWriter):
    def render(self):
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


########################################################################
        return output
# StatusnxWriter
########################################################################
class StatusnxWriter(ZeroFillMixin, BaseWriter):
    def render(self):
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
########################################################################
# SfenceenWriter
########################################################################
class SfenceenWriter(ZeroFillMixin, BaseWriter):
    def render(self):
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

########################################################################
# ScoreboardWriter
########################################################################
class ScoreboardWriter(ZeroFillMixin, BaseWriter):
    def render(self):
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

########################################################################
# BaseaddrselbitwidthWriter
########################################################################
class BaseaddrselbitwidthWriter(BaseWriter):
    def render(self):
        output = []
        for keys in self.iter_dma_items():
            uckeys = keys.upper()
            output.append(f"localparam {uckeys}_BASE_ADDR_SELECT_BITWIDTH = 3;\n")
        return output


########################################################################
# BaseaddrselioWriter
########################################################################
class BaseaddrselioWriter(BaseWriter):
    def render(self):
        output = []
        for keys in self.iter_dma_items():
            uckeys = keys.upper()
            output.append(f"output [{uckeys}_BASE_ADDR_SELECT_BITWIDTH-           1:0] {keys}_base_addr_select;\n")
        return output


########################################################################
# BaseaddrselportWriter
########################################################################
class BaseaddrselportWriter(BaseWriter):
    def render(self):
        output = []
        for keys in self.iter_dma_items():
            output.append(f",{keys}_base_addr_select\n")
        return output


########################################################################
# BaseaddrselWriter
########################################################################
class BaseaddrselWriter(BaseWriter):
    def render(self):
        output = []
        for keys in self.iter_dma_items():
            uckeys = keys.upper()
            output.append(
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
        return output


########################################################################
# SfenceWriter
########################################################################
class SfenceWriter(BaseWriter):
    def render(self):
        for row in self.lines:
            item = row.item
            register = row.register
            if item and register == 'sfence':
                self.seen_set[item] = 1
        output = []
        for keys in self.seen_set:
            output.append(
f"""wire {keys}_start_reg_nx = wr_taken & {keys}_sfence_en;
reg  {keys}_start_reg;
wire {keys}_start_reg_en = {keys}_start_reg ^ {keys}_start_reg_nx;
always @(posedge clk or negedge rst_n) begin
    if (~rst_n) {keys}_start_reg <= 1'b0;
    else if ({keys}_start_reg_en) {keys}_start_reg <= {keys}_start_reg_nx;
end
assign rf_{keys}_sfence = {keys}_start_reg;\n\n"""
            )
        return output


########################################################################
# IpnumWriter
########################################################################
class IpnumWriter(BaseWriter):
    def render(self):
        return ["localparam ITEM_ID_NUM = `ITEM_ID_NUM;\n"]


########################################################################
# PortWriter
########################################################################
class PortWriter(BaseWriter):
    def render(self):
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
            if key in self.seen_set_item:
                continue
            self.seen_set_item[key] = 1
            yield f", rf_{item}_{register}\n"


########################################################################
# BitwidthWriter
########################################################################
class BitwidthWriter(AlignMixin, BaseWriter):
    """
    直接對照 Perl 程式；所有重複與原始邏輯完整保留，不做結構化優化
    """

    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self.subregister_upper:
                if self.subregister_upper not in ('MSB', 'LSB'):
                    if (self.item_upper, self.register_upper) in self.seen_set:
                        continue
                    self.render_buffer.append(f"localparam {self.item_upper}_{self.register_upper}_BITWIDTH = `{self.item_upper}_{self.register_upper}_BITWIDTH;")
                    self.seen_set[(self.item_upper, self.register_upper)] = 1
                else:
                    sub_key = f"{self.key_upper}_{self.subregister_upper}"
                    if sub_key not in self.seen_set_item:
                        self.render_buffer.append(f"localparam {self.item_upper}_{self.register_upper}_{self.subregister_upper}_BITWIDTH = `{self.item_upper}_{self.register_upper}_{self.subregister_upper}_BITWIDTH;")
                        self.seen_set_item[sub_key] = 1
                        if self.subregister_upper == 'MSB':
                            self.render_buffer.append(f"localparam {self.item_upper}_{self.register_upper}_BITWIDTH = `{self.item_upper}_{self.register_upper}_BITWIDTH;")
            elif self.register_upper:
                if self.key_upper in self.seen_set_item:
                    continue
                if self.register_upper == 'CREDIT':
                    self.render_buffer.append(f"localparam {self.item_upper}_{self.register_upper}_BITWIDTH = 22;")
                else:
                    self.render_buffer.append(f"localparam {self.item_upper}_{self.register_upper}_BITWIDTH = `{self.item_upper}_{self.register_upper}_BITWIDTH;")
                self.seen_set_item[self.key_upper] = 1

        pairs = []
        for l in self.render_buffer:
            left, right = l.split('=', 1)
            pairs.append((left.strip(), right.strip()))
        return self.align_pairs(pairs, ' = ')


########################################################################
# IOWriter
########################################################################
class IOWriter(AlignMixin, BaseWriter):

    def _skip(self):
        if self.item_lower == 'csr' and (self.typ != 'rw' or self.register_lower in ('counter','counter_mask','status','control')):
            return True
        if self.key_lower in self.seen_set_item:
            return True
        return False

    def _process(self):
        if self._skip():
            return
        if self.typ == 'ro':
            self.render_buffer.append(f"input\t [{self.item_upper}_{self.register_upper}_BITWIDTH-1:0] rf_{self.item_lower}_{self.register_lower};")
        else:
            if self.item_lower == 'csr' and 'exram_based_addr' in self.register_lower:
                self.render_buffer.append(f"wire\t [{self.item_upper}_{self.register_upper}_BITWIDTH-1:0] {self.item_lower}_{self.register_lower};")
            elif self.register_lower == 'sfence':
                self.render_buffer.append(f"output\t [1-1:0] rf_{self.item_lower}_{self.register_lower};")
            else:
                self.render_buffer.append(f"output\t [{self.item_upper}_{self.register_upper}_BITWIDTH-1:0] rf_{self.item_lower}_{self.register_lower};")
        self.seen_set_item[self.key_lower] = 1

    def render(self):
        for row in self.lines:
                self.fetch_terms(row)
                self._process()

        pairs = []
        for l in self.render_buffer:
            left, right = l.split('\t', 1)
            pairs.append((left, right))
        return self.align_pairs(pairs, '\t')


########################################################################
# RegWriter
########################################################################
class RegWriter(AlignMixin, BaseWriter):

    def _skip(self):
        return self.typ != 'rw'

    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self._skip():
                continue
            if self.subregister_lower:
                if self.subregister_lower in ('lsb','msb'):
                    self.render_buffer.append(
                        f"reg\t[{self.item_upper}_{self.register_upper}_{self.subregister_upper}_BITWIDTH-1:0] {self.item_lower}_{self.register_lower}_{self.subregister_lower}_reg;"
                    )
                else:
                    if self.key_lower not in self.seen_set_item:
                        self.render_buffer.append(
                            f"reg\t[{self.item_upper}_{self.register_upper}_BITWIDTH-1:0] {self.item_lower}_{self.register_lower}_reg;"
                        )
                        self.seen_set_item[self.key_lower] = 1
            elif self.register_lower:
                self.render_buffer.append(
                    f"reg\t[{self.item_upper}_{self.register_upper}_BITWIDTH-1:0] {self.item_lower}_{self.register_lower}_reg;"
                )

        pairs = []
        for l in self.render_buffer:
            left, right = l.split('] ', 1)
            pairs.append((left + ']', right))
        return self.align_pairs(pairs, '\t')


########################################################################
# WireNxWriter
########################################################################
class WireNxWriter(AlignMixin, BaseWriter):

    def _skip(self):
        if self.typ != 'rw':
            return True
        if self.subregister_lower not in ('msb','lsb') and self.key_lower in self.seen_set_item:
            return True
        self.seen_set_item[self.key_lower] = 1
        return False

    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self._skip():
                continue
            if self.subregister_lower:
                if self.subregister_lower in ('msb','lsb'):
                    self.render_buffer.append(
                        f"wire\t[{self.item_upper}_{self.register_upper}_{self.subregister_upper}_BITWIDTH-1:0] {self.item_lower}_{self.register_lower}_{self.subregister_lower}_nx;"
                    )
                else:
                    self.render_buffer.append(
                        f"wire\t[{self.item_upper}_{self.register_upper}_BITWIDTH-1:0] {self.item_lower}_{self.register_lower}_nx;"
                    )
            elif self.register_lower:
                self.render_buffer.append(
                    f"wire\t[{self.item_upper}_{self.register_upper}_BITWIDTH-1:0] {self.item_lower}_{self.register_lower}_nx;"
                )

        pairs = []
        for l in self.render_buffer:
            left, right = l.split('] ', 1)
            pairs.append((left + ']', right))
        return self.align_pairs(pairs, '   ')


########################################################################
# WireEnWriter
########################################################################
class WireEnWriter(BaseWriter):

    def _skip(self):
        if self.typ != 'rw':
            return True
        if self.subregister_lower not in ('msb','lsb'):
            if self.key_lower in self.seen_set_item:
                return True
            self.seen_set_item[self.key_lower] = 1
        return False

    def render(self):
        self.seen_set_item = {}
        for row in self.lines:
                self.fetch_terms(row)
                if self._skip():
                    continue

                if self.subregister_lower in ('msb','lsb'):
                    wire_name = f"{self.item_lower}_{self.register_lower}_{self.subregister_lower}_en"
                else:
                    wire_name = f"{self.item_lower}_{self.register_lower}_en"
                yield f"wire   {wire_name};\n"


########################################################################
# SeqWriter
########################################################################
class SeqWriter(BaseWriter):

    def _skip(self):
        if self.typ != 'rw':
            return True
        if self.key_lower in self.seen_set_item and self.subregister_lower not in ('msb','lsb'):
            return True
        self.seen_set_item[self.key_lower] = 1
        return False


    def render(self):
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
            elif self.subregister_lower in ('msb','lsb'):
                bit = "1'b1" if default == '1' else "1'b0"
                final_assignment = f"{{ {{({self.item_upper}_{self.register_upper}_{self.subregister_upper}_BITWIDTH-1){{1'd0}}}}, {bit} }}"
            else:
                bit = "1'b1" if default == '1' else "1'b0"
                final_assignment = f"{{ {{({self.item_upper}_{self.register_upper}_BITWIDTH-1){{1'd0}}}}, {bit} }}"

            if self.subregister_lower in ('msb','lsb'):
                self.render_buffer.append(f"\t\t{self.item_lower}_{self.register_lower}_{self.subregister_lower}_reg{' '*(50-len(self.item_lower+self.register_lower+self.subregister_lower)+2)}<= {final_assignment};")
            else:
                self.render_buffer.append(f"\t\t{self.item_lower}_{self.register_lower}_reg{' '*(50-len(self.item_lower+self.register_lower)+3)}<= {final_assignment};")

        for l in self.render_buffer:
            output.append(f"{l}\n")

        output.append("    end else begin\n")
        for l in self.render_buffer:
            if '<=' in l:
                reg_name = l.split('<=')[0].strip()
                wire_name = reg_name.replace('_reg', '_nx')
                output.append(f"\t\t{reg_name:<48}<= {wire_name};\n")
        output.append("    end\n")
        output.append("end\n")
        return output


########################################################################
# EnWriter
########################################################################
class EnWriter(AlignMixin, BaseWriter):

    def _skip(self):
        if self.typ != 'rw':
            return True
        if self.key_lower in self.seen_set_item and self.subregister_lower not in ('msb','lsb'):
            return True
        self.seen_set_item[self.key_lower] = 1
        return False

    def render(self):
        for row in self.lines:
                self.fetch_terms(row)
                if self._skip():
                    continue

                if self.subregister_lower in ('msb','lsb'):
                    assignment = (
                        f"assign {self.item_lower}_{self.register_lower}_{self.subregister_lower}_en"
                        f" = (issue_rf_riurwaddr == {{`{self.item_upper}_ID,`{self.item_upper}_{self.register_upper}_{self.subregister_upper}_IDX}});"
                    )
                else:
                    assignment = (
                        f"assign {self.item_lower}_{self.register_lower}_en"
                        f" = (issue_rf_riurwaddr == {{`{self.item_upper}_ID,`{self.item_upper}_{self.register_upper}_IDX}});"
                    )

                left = assignment.split('=')[0]
                right= assignment[len(left):]
                yield from self.align_pairs([(left, right)], '')


########################################################################
# NxWriter
########################################################################
class NxWriter(AlignMixin, BaseWriter):
    """
    照原樣轉寫；重複邏輯不加抽象
    """


    def _skip(self):
        if self.typ != 'rw':
            return True
        if self.register_lower == 'status':
            return True
        if self.key_lower in self.seen_set_item and self.subregister_lower not in ('msb','lsb'):
            return True
        self.seen_set_item[self.key_lower] = 1
        return False

    def _process_ro(self):
        if self._skip():
            return
        if self.register_lower == 'credit' and self.item_lower == 'csr':
            self.render_buffer.append("assign csr_credit_nx = sqr_credit;")
        else:
            self.render_buffer.append(f"assign {self.item_lower}_{self.register_lower}_nx = {{ {{ (32 - {self.register_upper}_DATA.bit_length()) {{ 1'b0 }} }}, {self.register_upper}_DATA}};")

    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self.typ == 'ro' and self.register_lower:
                self._process_ro()
            elif self.subregister_lower:
                if self._skip():
                    continue
                if self.register_lower in ('const_value','ram_padding_value'):
                    self.render_buffer.append(
                        f"assign {self.item_lower}_{self.register_lower}_nx[{self.item_upper}_{self.register_upper}_BITWIDTH-1:{self.item_upper}_{self.register_upper}_BITWIDTH-2] = "
                        f"(wr_taken & {self.item_lower}_{self.register_lower}_en) ? issue_rf_riuwdata[RF_WDATA_BITWIDTH-1:RF_WDATA_BITWIDTH-2] : "
                        f"{self.item_lower}_{self.register_lower}_reg[{self.item_upper}_{self.register_upper}_BITWIDTH-1:{self.item_upper}_{self.register_upper}_BITWIDTH-2];"
                    )
                    self.render_buffer.append(
                        f"assign {self.item_lower}_{self.register_lower}_nx[{self.item_upper}_{self.register_upper}_BITWIDTH-3:0] = "
                        f"(wr_taken & {self.item_lower}_{self.register_lower}_en) ? issue_rf_riuwdata[{self.item_upper}_{self.register_upper}_BITWIDTH-3:0]: "
                        f"{self.item_lower}_{self.register_lower}_reg[{self.item_upper}_{self.register_upper}_BITWIDTH-3:0];"
                    )
                elif self.subregister_lower in ('msb','lsb'):
                    self.render_buffer.append(
                        f"assign {self.item_lower}_{self.register_lower}_{self.subregister_lower}_nx = "
                        f"(wr_taken & {self.item_lower}_{self.register_lower}_{self.subregister_lower}_en) ? "
                        f"issue_rf_riuwdata[{self.item_upper}_{self.register_upper}_{self.subregister_upper}_BITWIDTH-1:0] : "
                        f"{self.item_lower}_{self.register_lower}_{self.subregister_lower}_reg;"
                    )
                else:
                    self.render_buffer.append(
                        f"assign {self.item_lower}_{self.register_lower}_nx = "
                        f"(wr_taken & {self.item_lower}_{self.register_lower}_en) ? "
                        f"issue_rf_riuwdata[{self.item_upper}_{self.register_upper}_BITWIDTH-1:0] : "
                        f"{self.item_lower}_{self.register_lower}_reg;"
                    )
            elif self.register_lower:
                if self._skip():
                    continue
                self.render_buffer.append(
                    f"assign {self.item_lower}_{self.register_lower}_nx = "
                    f"(wr_taken & {self.item_lower}_{self.register_lower}_en) ? "
                    f"issue_rf_riuwdata[{self.item_upper}_{self.register_upper}_BITWIDTH-1:0] : "
                    f"{self.item_lower}_{self.register_lower}_reg;"
                )

        pairs = []
        for a in self.render_buffer:
            left, right = a.split('=', 1)
            pairs.append((left.strip(), right.strip()))
        return self.align_pairs(pairs, ' = ')


########################################################################
# CTRLWriter
########################################################################
class CTRLWriter(AlignMixin, BaseWriter):
    """
    依原 Perl 寫法轉成 Python
    """

    def _skip(self):
        if self.typ != 'rw':
            return True
        if self.subregister_lower not in ('msb','lsb'):
            if self.key_lower in self.seen_set:
                return True
            self.seen_set[self.key_lower] = 1
        return False

    def _build_output(self, signal_name, reg_name, bitwidth):
        return f"\t\t\t\t  ({{RF_RDATA_BITWIDTH{{({signal_name})}}}} & {{{{(RF_RDATA_BITWIDTH-{bitwidth}){{1'b0}}}}, {reg_name}}}) |"


    def render(self):
        output = ["assign issue_rf_riurdata =\n"]
        for row in self.lines:
            self.fetch_terms(row)
            if self._skip():
                continue
            if self.subregister_lower in ('msb','lsb'):
                signal = f"{self.item_lower}_{self.register_lower}_{self.subregister_lower}_en"
                reg_nm = f"{self.item_lower}_{self.register_lower}_{self.subregister_lower}_reg"
                bw = f"{self.item_upper}_{self.register_upper}_{self.subregister_upper}_BITWIDTH"
            else:
                signal = f"{self.item_lower}_{self.register_lower}_en"
                reg_nm = f"{self.item_lower}_{self.register_lower}_reg"
                bw = f"{self.item_upper}_{self.register_upper}_BITWIDTH"

            if self.subregister_lower:
                self.render_buffer.append(self._build_output(signal, reg_nm, bw))
            else:
                if self.register_lower in ('ldma_chsum_data','sdma_chsum_data'):
                    reg_nm = f"{self.item_lower}_{self.register_lower}"
                self.render_buffer.append(self._build_output(signal, reg_nm, bw))

        pairs = []
        for l in self.render_buffer:
            left, right = l.split("1'b0", 1)
            pairs.append((left, "1'b0" + right))
        output.extend(self.align_pairs(pairs, ''))
        return output


########################################################################
# OutputWriter
########################################################################
class OutputWriter(AlignMixin, BaseWriter):

    def _skip(self):
        key = f"{self.item_lower}_{self.register_lower}"
        if key in self.ignore_pair:
            return True
        if key in self.seen_set:
            return True
        if self.register_lower == 'exram_addr':
            return True
        self.seen_set[key] = 1
        return False

    def _process(self):
        if self._skip():
            return
        if self.subregister_lower:
            if self.item_lower == 'csr' and self.register_lower.startswith('exram_based_addr_'):
                out_reg = self.register_lower.replace('_based_', '_based_')  # 同 Perl 保留
                self.render_buffer.append(f"assign {self.item_lower}_{out_reg} = {{ {self.item_lower}_{self.register_lower}_msb_reg, {self.item_lower}_{self.register_lower}_lsb_reg }};")
            elif self.subregister_lower in ('msb','lsb'):
                self.render_buffer.append(f"assign rf_{self.item_lower}_{self.register_lower} = {{ {self.item_lower}_{self.register_lower}_msb_reg, {self.item_lower}_{self.register_lower}_lsb_reg }};")
            else:
                self.render_buffer.append(f"assign rf_{self.item_lower}_{self.register_lower} = {self.item_lower}_{self.register_lower}_reg;")
        else:
            self.render_buffer.append(f"assign rf_{self.item_lower}_{self.register_lower} = {self.item_lower}_{self.register_lower}_reg;")

    def render(self):
        for row in self.lines:
                self.fetch_terms(row)
                if self.register_lower:
                    self._process()

        pairs = []
        for l in self.render_buffer:
            left, right = l.split('=', 1)
            pairs.append((left.strip(), right.strip()))
        return self.align_pairs(pairs, ' = ')


# Mapping of pattern keywords to their corresponding writer classes
WRITER_MAP = [
    ('ipnum', IpnumWriter),
    ('port', PortWriter),
    ('bitwidth', BitwidthWriter),
    ('io', IOWriter),
    ('reg', RegWriter),
    ('wire_nx', WireNxWriter),
    ('wire_en', WireEnWriter),
    ('seq', SeqWriter),
    ('en', EnWriter),
    ('nx', NxWriter),
    ('control', CTRLWriter),
    ('output', OutputWriter),
    ('sfence', SfenceWriter),
    ('baseaddrsel', BaseaddrselWriter),
    ('baseaddrselport', BaseaddrselportWriter),
    ('baseaddrselio', BaseaddrselioWriter),
    ('baseaddrselbitwidth', BaseaddrselbitwidthWriter),
    ('scoreboard', ScoreboardWriter),
    ('sfenceen', SfenceenWriter),
    ('statusnx', StatusnxWriter),
    ('riurwaddr', RiurwaddrWriter),
    ('exceptport', ExceptportWriter),
    ('exceptio', ExceptioWriter),
    ('interrupt', InterruptWriter),
    ('exceptwire', ExceptwireWriter),
]

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
        key: re.compile(rf'^// autogen_{key}_start') for key, _ in WRITER_MAP
    }
    dict_lines = load_dictionary_lines()
    writers = {
        key: cls(None, dict_lines) for key, cls in WRITER_MAP
    }
    found = {key: False for key, _ in WRITER_MAP}

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
