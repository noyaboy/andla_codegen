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
from typing import Callable

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

class BaseWriter:
    """
    通用 Writer，實作 data → template → output 的流程，
    並提供取得欄位、排序 items 及過濾 DMA items 的方法。
    """
    def __init__(self, outfile, dict_lines):
        self.outfile = outfile
        self.lines = dict_lines
        # shared state for subclasses
        self.seen_set                   = {}
        self.render_buffer              = []
        self.render_buffer_tmp          = []
        self.item_lower                 = ''
        self.register_lower             = ''
        self.subregister_lower          = ''
        self.doublet_lower              = ''
        self.triplet_lower              = ''
        self.item_upper                 = ''
        self.register_upper             = ''
        self.subregister_upper          = ''
        self.doublet_upper              = ''
        self.triplet_upper              = ''
        self.id                         = ''
        self.typ                        = ''
        self.default_value              = ''
        self.seq_default_value          = ''
        self.seq_default_value_width    = ''
        self.ignore_pair                = {
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

    # Mapping of rule names to their skip handlers.  Individual rules
    # encapsulate commonly used `continue` conditions across writers.
    _SKIP_HANDLERS: dict[str, Callable[["BaseWriter"], bool]] = {}

    def seen(self, key):
        """Return True if ``key`` has been seen; otherwise mark it and return False."""
        if key in self.seen_set:
            return True
        self.seen_set[key] = 1
        return False

    def skip(
        self,
        *rules: str,
        extra: Callable[["BaseWriter"], bool] | None = None,
    ) -> bool:
        """Return ``True`` if any named rule (or ``extra``) evaluates to ``True``."""
        for name in rules:
            try:
                if self._SKIP_HANDLERS[name](self):
                    return True
            except KeyError as exc:
                raise ValueError(f'Unknown skip rule: {name}') from exc

        if extra is not None and extra(self):
            return True
        return False

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

    def iter_items(self, *, dma_only: bool = False, sfence_only: bool = False):
        """Iterate over dictionary items with optional filters.

        Parameters
        ----------
        dma_only : bool, optional
            If ``True``, only yield items whose name contains ``"dma"`` and
            that are not equal to ``"ldma2"``.
        sfence_only : bool, optional
            If ``True``, only yield items whose register field equals
            ``"sfence"``.

        Yields
        ------
        tuple[str, str, int]
            ``(item_lower, item_upper, id)`` sorted by ``id`` in descending
            order. ``item_upper`` is the upper-case form of ``item_lower``.
        """
        items = {}
        for row in self.lines:
            if dma_only and not (
                row.item and "dma" in row.item and row.item != "ldma2"
            ):
                continue
            if sfence_only and row.register != "sfence":
                continue

            item = row.item
            _id = row.id
            if item and _id is not None:
                items[item] = _id

        for key in sorted(items, key=items.get, reverse=True):
            yield key, key.upper(), items[key]

    def fetch_terms(self, row: DictRow):
        """Populate commonly used case variants from a ``DictRow``."""
        self.item_lower        = row.item
        self.register_lower    = row.register
        self.subregister_lower = row.subregister

        if self.item_lower and self.register_lower:
            self.doublet_lower = f"{self.item_lower}_{self.register_lower}"
        else:
            self.doublet_lower = ''

        if self.item_lower and self.register_lower and self.subregister_lower:
            self.triplet_lower = (
                f"{self.item_lower}_{self.register_lower}_{self.subregister_lower}"
            )
        else:
            self.triplet_lower = ''

        self.item_upper        = self.item_lower.upper() if self.item_lower else ''
        self.register_upper    = self.register_lower.upper() if self.register_lower else ''
        self.subregister_upper = self.subregister_lower.upper() if self.subregister_lower else ''

        if self.item_upper and self.register_upper:
            self.doublet_upper = f"{self.item_upper}_{self.register_upper}"
        else:
            self.doublet_upper = ''

        if self.item_upper and self.register_upper and self.subregister_upper:
            self.triplet_upper = (
                f"{self.item_upper}_{self.register_upper}_{self.subregister_upper}"
            )
        else:
            self.triplet_upper = ''

        self.id  = row.id
        self.typ = row.type
        self.default_value = row.default_value

        if not self.default_value.startswith('0x'):
                self.seq_default_value_width = int(row.default_value).bit_length() or 1

        if self.default_value.startswith('0x'):
            self.seq_default_value = self.default_value.replace('0x', "32'h")
        elif self.subregister_lower in ('msb','lsb'):
            self.seq_default_value = f"{{ {{({self.triplet_upper}_BITWIDTH-{self.seq_default_value_width}){{1'd0}}}}, {self.seq_default_value_width}'d{self.default_value} }}"
        else:
            self.seq_default_value = f"{{ {{({self.doublet_upper}_BITWIDTH-{self.seq_default_value_width}){{1'd0}}}}, {self.seq_default_value_width}'d{self.default_value} }}"
        
    def fill_zero(self, start, end, template):
        return [template.format(idx=idx) for idx in range(start - 1, end, -1)]

    def align_pairs(self, pairs, sep=' '):
        """Align a sequence of ``(left, right)`` pairs by the length of ``left``."""
        if not pairs:
            return []
        max_len = max(len(left) for left, _ in pairs)
        return [f"{left:<{max_len}}{sep}{right}\n" for left, right in pairs]

    def align_on(
        self,
        lines,
        delimiter,
        *,
        sep=None,
        include_delim_in_right=False,
        reappend_left='',
        strip=False,
    ):
        """Split each line on ``delimiter`` and align the two halves.

        Parameters
        ----------
        lines : iterable of str
            Lines to align.
        delimiter : str
            Delimiter to split on. Only the first occurrence is considered.
        sep : str | None
            Separator used when joining the aligned halves. Defaults to
            ``delimiter`` if not provided.
        include_delim_in_right : bool
            When ``True``, ``delimiter`` is kept at the start of the right
            half.
        reappend_left : str
            Text appended to the left half after splitting. Useful when the
            delimiter should stay attached to the left side (e.g. ``'] '``).
        strip : bool
            Whether to strip whitespace from each half before alignment.
        """

        pairs = []
        for line in lines:
            left, right = line.split(delimiter, 1)
            left += reappend_left
            if include_delim_in_right:
                right = delimiter + right
            if strip:
                left = left.strip()
                right = right.strip()
            pairs.append((left, right))

        if sep is None:
            sep = delimiter
        return self.align_pairs(pairs, sep)

########################################################################
# InterruptWriter
########################################################################
class InterruptWriter(BaseWriter):
    def render(self):
        for self.item_lower, _ , _ in self.iter_items():
            if self.skip('interrupt'):
                continue
            self.render_buffer.append(f"                          ({self.item_lower}_except & {self.item_lower}_except_mask) |\n")
        return self.render_buffer

########################################################################
# ExceptwireWriter
########################################################################
class ExceptwireWriter(BaseWriter):
    def render(self):
        for self.item_lower, self.item_upper, _ in self.iter_items():
            if self.skip('exceptwire'):
                continue
            self.render_buffer.append(f"wire {self.item_lower}_except = csr_status_reg[`{self.item_upper}_ID + 8];\n")
            self.render_buffer.append(f"wire {self.item_lower}_except_mask = csr_control_reg[`{self.item_upper}_ID + 8];\n")
        return self.align_on(self.render_buffer, '=', sep=' = ', strip=True)

########################################################################
# ExceptioWriter
########################################################################
class ExceptioWriter(BaseWriter):
    def render(self):
        for self.item_lower, _ , _ in self.iter_items():
            if self.skip('exceptio'):
                continue
            self.render_buffer.append(f"input rf_{self.item_lower}_except_trigger;\n")
        return self.render_buffer

########################################################################
# ExceptportWriter
########################################################################
class ExceptportWriter(BaseWriter):
    def render(self):
        for self.item_lower, _ , _ in self.iter_items():
            if self.skip('exceptport'):
                continue
            self.render_buffer.append(f",rf_{self.item_lower}_except_trigger\n")
        return self.render_buffer

########################################################################
# RiurwaddrWriter
########################################################################
class RiurwaddrWriter(BaseWriter):
    def render(self):
        prev_id = None
        for self.item_lower, self.item_upper, self.id in self.iter_items():
            if prev_id is not None and prev_id - self.id > 1:
                self.render_buffer.extend(self.fill_zero( prev_id, self.id, "wire riurwaddr_bit{idx} = 1'b0;\n", ))
            if self.item_lower == 'csr':
                self.render_buffer.append(f"wire riurwaddr_bit{self.id} = 1'b0;\n")
            else:
                self.render_buffer.append(f"wire riurwaddr_bit{self.id} = (issue_rf_riurwaddr[(RF_ADDR_BITWIDTH-1) -: ITEM_ID_BITWIDTH] == `{self.item_upper}_ID);\n")
            prev_id = self.id

        return self.align_on(self.render_buffer, '=', sep=' = ', strip=True)

########################################################################
# StatusnxWriter
########################################################################
class StatusnxWriter(BaseWriter):
    def render(self):
        prev_id = None
        for self.item_lower, self.item_upper, self.id in self.iter_items():
            if prev_id is not None and prev_id - self.id > 1:
                self.render_buffer.extend(self.fill_zero(prev_id, self.id, "assign csr_status_nx[{idx}] = 1'b0;\n"))
                self.render_buffer.extend(self.fill_zero(prev_id, self.id, "assign csr_status_nx[{idx} + 8] = 1'b0;\n"))

            if self.item_lower == 'ldma2':
                self.render_buffer.append(f"assign csr_status_nx[`{self.item_upper}_ID] = (wr_taken & sfence_en[`{self.item_upper}_ID]  ) ? 1'b1 : scoreboard[`{self.item_upper}_ID];\n")
                self.render_buffer.append(f"assign csr_status_nx[`{self.item_upper}_ID + 8] = rf_ldma_except_trigger ? 1'b1 : (wr_taken & csr_status_en) ? issue_rf_riuwdata[`{self.item_upper}_ID + 8] : csr_status_reg[`{self.item_upper}_ID + 8];\n")
            else:
                self.render_buffer.append(f"assign csr_status_nx[`{self.item_upper}_ID] = (wr_taken & sfence_en[`{self.item_upper}_ID]  ) ? 1'b1 : scoreboard[`{self.item_upper}_ID];\n")
                if self.item_lower == 'csr':
                    self.render_buffer.append(f"assign csr_status_nx[`{self.item_upper}_ID + 8] = 1'b0;\n")
                else:
                    self.render_buffer.append(f"assign csr_status_nx[`{self.item_upper}_ID + 8] = rf_{self.item_lower}_except_trigger ? 1'b1 : (wr_taken & csr_status_en) ? issue_rf_riuwdata[`{self.item_upper}_ID + 8] : csr_status_reg[`{self.item_upper}_ID + 8];\n")
            prev_id = self.id

        return self.align_on(self.render_buffer, '=', sep=' = ', strip=True)
########################################################################
# SfenceenWriter
########################################################################
class SfenceenWriter(BaseWriter):
    def render(self):
        prev_id = None
        for self.item_lower, self.item_upper, self.id in self.iter_items():
            if prev_id is not None and prev_id - self.id > 1:
                self.render_buffer.extend(self.fill_zero(prev_id, self.id, "               1'b0,\n"))

            if self.item_lower == 'csr':
                self.render_buffer.append("               1'b0\n")
            elif self.item_lower == 'ldma2':
                self.render_buffer.append("               1'b0,\n")
            else:
                self.render_buffer.append(f"               {self.item_lower}_sfence_en,\n")
            prev_id = self.id

        return self.render_buffer

########################################################################
# ScoreboardWriter
########################################################################
class ScoreboardWriter(BaseWriter):
    def render(self):
        prev_id = None
        for self.item_lower, self.item_upper, self.id in self.iter_items():
            if prev_id is not None and prev_id - self.id > 1:
                self.render_buffer.extend(self.fill_zero(prev_id, self.id, "assign scoreboard[{idx}] = 1'b0;\n"))

            self.render_buffer.append(f"assign scoreboard[{self.id}] = (ip_rf_status_clr[`{self.item_upper}_ID]) ? 1'b0 : csr_status_reg[`{self.item_upper}_ID];\n")
            prev_id = self.id

        return self.align_on(self.render_buffer, '=', sep=' = ', strip=True)

########################################################################
# BaseaddrselbitwidthWriter
########################################################################
class BaseaddrselbitwidthWriter(BaseWriter):
    def render(self):
        for self.item_lower, self.item_upper, _ in self.iter_items(dma_only=True):
            self.render_buffer.append(f"localparam {self.item_upper}_BASE_ADDR_SELECT_BITWIDTH = 3;\n")
        return self.render_buffer

########################################################################
# BaseaddrselWriter
########################################################################
class BaseaddrselWriter(BaseWriter):
    def render(self):
        for self.item_lower, self.item_upper, _ in self.iter_items(dma_only=True):
            self.render_buffer.append(
f"""
wire [{self.item_upper}_BASE_ADDR_SELECT_BITWIDTH-1:0] {self.item_lower}_base_addr_select_nx;
assign  {self.item_lower}_base_addr_select_nx           = {self.item_lower}_sfence_nx[20:18];
wire {self.item_lower}_base_addr_select_en           = wr_taken & {self.item_lower}_sfence_en;
reg  [{self.item_upper}_BASE_ADDR_SELECT_BITWIDTH-1:0] {self.item_lower}_base_addr_select_reg;
always @(posedge clk or negedge rst_n) begin
    if (~rst_n)                        {self.item_lower}_base_addr_select_reg <= {{({self.item_upper}_BASE_ADDR_SELECT_BITWIDTH){{1'd0}}}};
    else if ({self.item_lower}_base_addr_select_en) {self.item_lower}_base_addr_select_reg <= {self.item_lower}_base_addr_select_nx;
end
wire [3-1: 0] {self.item_lower}_base_addr_select;
assign {self.item_lower}_base_addr_select            = {self.item_lower}_base_addr_select_reg;\n\n"""
            )
        return self.render_buffer


########################################################################
# SfenceWriter
########################################################################
class SfenceWriter(BaseWriter):
    def render(self):
        for self.item_lower, _, _ in self.iter_items(sfence_only=True):
            self.render_buffer.append(
f"""wire {self.item_lower}_start_reg_nx = wr_taken & {self.item_lower}_sfence_en;
reg  {self.item_lower}_start_reg;
wire {self.item_lower}_start_reg_en = {self.item_lower}_start_reg ^ {self.item_lower}_start_reg_nx;
always @(posedge clk or negedge rst_n) begin
    if (~rst_n) {self.item_lower}_start_reg <= 1'b0;
    else if ({self.item_lower}_start_reg_en) {self.item_lower}_start_reg <= {self.item_lower}_start_reg_nx;
end
assign rf_{self.item_lower}_sfence = {self.item_lower}_start_reg;\n\n"""
            )
        return self.render_buffer


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
            self.fetch_terms(row)
            if self.skip('port'):
                continue
            self.render_buffer.append(f", rf_{self.doublet_lower}\n")
        return self.render_buffer


########################################################################
# BitwidthWriter
########################################################################
class BitwidthWriter(BaseWriter):
    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip('bitwidth'):
                continue
            if self.subregister_upper:
                if self.subregister_upper not in ('MSB', 'LSB'):
                    self.render_buffer.append(f"localparam {self.doublet_upper}_BITWIDTH = `{self.doublet_upper}_BITWIDTH;")
                else:
                    self.render_buffer.append(f"localparam {self.triplet_upper}_BITWIDTH = `{self.triplet_upper}_BITWIDTH;")
                    if self.subregister_upper == 'MSB':
                        self.render_buffer.append(f"localparam {self.doublet_upper}_BITWIDTH = `{self.doublet_upper}_BITWIDTH;")
            elif self.register_upper:
                if self.register_upper == 'CREDIT':
                    self.render_buffer.append(f"localparam {self.doublet_upper}_BITWIDTH = 22;")
                else:
                    self.render_buffer.append(f"localparam {self.doublet_upper}_BITWIDTH = `{self.doublet_upper}_BITWIDTH;")

        return self.align_on(self.render_buffer, '=', sep=' = ', strip=True)


########################################################################
# IOWriter
########################################################################
class IOWriter(BaseWriter):
    def render(self):
        # Process each line, applying skip and render logic inline
        for row in self.lines:
            self.fetch_terms(row)

            if self.skip('io'):
                continue

            # Render logic
            if self.typ == 'ro':
                self.render_buffer.append(f"input\t [{self.doublet_upper}_BITWIDTH-1:0] rf_{self.doublet_lower};")
            else:
                if self.item_lower == 'csr' and 'exram_based_addr' in self.register_lower:
                    self.render_buffer.append(f"wire\t [{self.doublet_upper}_BITWIDTH-1:0] {self.doublet_lower};")
                elif self.register_lower == 'sfence':
                    self.render_buffer.append(f"output\t [1-1:0] rf_{self.doublet_lower};")
                else:
                    self.render_buffer.append(f"output\t [{self.doublet_upper}_BITWIDTH-1:0] rf_{self.doublet_lower};")

        # Align and return all buffered lines
        return self.align_on(self.render_buffer, '\t', sep='\t')

########################################################################
# RegWriter
########################################################################
class RegWriter(BaseWriter):
    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip('reg'):
                continue
            if self.subregister_lower:
                if self.subregister_lower in ('lsb','msb'):
                    self.render_buffer.append(f"reg\t[{self.triplet_upper}_BITWIDTH-1:0] {self.triplet_lower}_reg;")
                else:
                    self.render_buffer.append(f"reg\t[{self.doublet_upper}_BITWIDTH-1:0] {self.doublet_lower}_reg;")
            elif self.register_lower:
                self.render_buffer.append(f"reg\t[{self.doublet_upper}_BITWIDTH-1:0] {self.doublet_lower}_reg;")

        return self.align_on(self.render_buffer, '] ', sep='\t', reappend_left=']',)

########################################################################
# WireNxWriter
########################################################################
class WireNxWriter(BaseWriter):
    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip('wire_nx'):
                continue
            self.seen(self.doublet_lower)

            if self.subregister_lower:
                if self.subregister_lower in ('msb','lsb'):
                    self.render_buffer.append(f"wire\t[{self.triplet_upper}_BITWIDTH-1:0] {self.triplet_lower}_nx;")
                else:
                    self.render_buffer.append(f"wire\t[{self.doublet_upper}_BITWIDTH-1:0] {self.doublet_lower}_nx;")
            elif self.register_lower:
                self.render_buffer.append(f"wire\t[{self.doublet_upper}_BITWIDTH-1:0] {self.doublet_lower}_nx;")

        return self.align_on(self.render_buffer, '] ', sep='   ', reappend_left=']',)


########################################################################
# WireEnWriter
########################################################################
class WireEnWriter(BaseWriter):
    def render(self):
        self.seen_set = {}
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip('wire_en'):
                continue
            if self.subregister_lower in ('msb','lsb'):
                self.render_buffer.append(f"wire   {self.triplet_lower}_en;\n")
            else:
                self.render_buffer.append(f"wire   {self.doublet_lower}_en;\n")
        return self.render_buffer


########################################################################
# SeqWriter
########################################################################
class SeqWriter(BaseWriter):
    def render(self):
        self.render_buffer = ["always @(posedge clk or negedge rst_n) begin\n    if(~rst_n) begin\n"]

        for row in self.lines:
            self.fetch_terms(row)
            if self.skip('seq'):
                continue

            if self.subregister_lower in ('msb','lsb'):
                self.render_buffer_tmp.append(f"\t\t{self.triplet_lower}_reg <= {self.seq_default_value};")
            else:
                self.render_buffer_tmp.append(f"\t\t{self.doublet_lower}_reg <= {self.seq_default_value};")

        self.render_buffer.extend(self.align_on(self.render_buffer_tmp, "<=", sep='', include_delim_in_right=True,))

        self.render_buffer.append("    end else begin\n")

        self.render_buffer_tmp  = []
        self.seen_set           = {}

        for row in self.lines:
            self.fetch_terms(row)
            if self.skip('seq'):
                continue

            if self.subregister_lower in ('msb','lsb'):
                self.render_buffer_tmp.append(f"\t\t{self.triplet_lower}_reg <= {self.triplet_lower}_nx;")
            else:
                self.render_buffer_tmp.append(f"\t\t{self.doublet_lower}_reg <= {self.doublet_lower}_nx;")

        self.render_buffer.extend(self.align_on(self.render_buffer_tmp, "<=", sep='', include_delim_in_right=True,))

        self.render_buffer.append("    end\n")
        self.render_buffer.append("end\n")
        return self.render_buffer


########################################################################
# EnWriter
########################################################################
class EnWriter(BaseWriter):
    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip('en'):
                continue
            self.seen(self.doublet_lower)
            if self.subregister_lower in ('msb','lsb'):
                self.render_buffer.append(f"assign {self.triplet_lower}_en = (issue_rf_riurwaddr == {{`{self.item_upper}_ID,`{self.triplet_upper}_IDX}});\n")
            else:
                self.render_buffer.append(f"assign {self.doublet_lower}_en = (issue_rf_riurwaddr == {{`{self.item_upper}_ID,`{self.doublet_upper}_IDX}});\n")
        return self.align_on(self.render_buffer, '=', sep=' = ', strip=True)

########################################################################
# NxWriter
########################################################################
class NxWriter(BaseWriter):
    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip('nx'):
                continue
            if self.typ == 'ro' and self.register_lower:
                self.seen(self.doublet_lower)
                if self.register_lower == 'credit' and self.item_lower == 'csr':
                    self.render_buffer.append("assign csr_credit_nx = sqr_credit;")
                else:
                    self.render_buffer.append(f"assign {self.doublet_lower}_nx = {{ {{ (32 - {self.register_upper}_DATA.bit_length()) {{ 1'b0 }} }}, {self.register_upper}_DATA}};")
            elif self.subregister_lower:
                self.seen(self.doublet_lower)
                if self.register_lower in ('const_value','ram_padding_value'):
                    self.render_buffer.append(f"assign {self.doublet_lower}_nx[{self.doublet_upper}_BITWIDTH-1:{self.doublet_upper}_BITWIDTH-2] = (wr_taken & {self.doublet_lower}_en) ? issue_rf_riuwdata[RF_WDATA_BITWIDTH-1:RF_WDATA_BITWIDTH-2] : {self.doublet_lower}_reg[{self.doublet_upper}_BITWIDTH-1:{self.doublet_upper}_BITWIDTH-2];")
                    self.render_buffer.append(f"assign {self.doublet_lower}_nx[{self.doublet_upper}_BITWIDTH-3:0] = (wr_taken & {self.doublet_lower}_en) ? issue_rf_riuwdata[{self.doublet_upper}_BITWIDTH-3:0]: {self.doublet_lower}_reg[{self.doublet_upper}_BITWIDTH-3:0];")
                elif self.subregister_lower in ('msb','lsb'):
                    self.render_buffer.append(f"assign {self.triplet_lower}_nx = (wr_taken & {self.triplet_lower}_en) ? issue_rf_riuwdata[{self.triplet_upper}_BITWIDTH-1:0] : {self.triplet_lower}_reg;")
                else:
                    self.render_buffer.append(f"assign {self.doublet_lower}_nx = (wr_taken & {self.doublet_lower}_en) ? issue_rf_riuwdata[{self.doublet_upper}_BITWIDTH-1:0] : {self.doublet_lower}_reg;")
            elif self.register_lower:
                self.seen(self.doublet_lower)
                self.render_buffer.append(f"assign {self.doublet_lower}_nx = (wr_taken & {self.doublet_lower}_en) ? issue_rf_riuwdata[{self.doublet_upper}_BITWIDTH-1:0] : {self.doublet_lower}_reg;")

        return self.align_on(self.render_buffer, '=', sep=' = ', strip=True)


########################################################################
# CTRLWriter
########################################################################
class CTRLWriter(BaseWriter):
    def render(self):
        self.render_buffer = ["assign issue_rf_riurdata =\n"]
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip('control'):
                continue
            self.seen(self.doublet_lower)
            if self.subregister_lower in ('msb','lsb'):
                self.render_buffer_tmp.append(f"\t\t\t\t  ({{RF_RDATA_BITWIDTH{{({self.triplet_lower}_en)}}}} & {{{{(RF_RDATA_BITWIDTH-{self.triplet_upper}_BITWIDTH){{1'b0}}}}, {self.triplet_lower}_reg}}) |")
            elif self.register_lower in ('ldma_chsum_data','sdma_chsum_data'):
                self.render_buffer_tmp.append(f"\t\t\t\t  ({{RF_RDATA_BITWIDTH{{({self.doublet_lower}_en)}}}} & {{{{(RF_RDATA_BITWIDTH-{self.doublet_upper}_BITWIDTH){{1'b0}}}}, {self.doublet_lower}}}) |")
            else:
                self.render_buffer_tmp.append(f"\t\t\t\t  ({{RF_RDATA_BITWIDTH{{({self.doublet_lower}_en)}}}} & {{{{(RF_RDATA_BITWIDTH-{self.doublet_upper}_BITWIDTH){{1'b0}}}}, {self.doublet_lower}_reg}}) |")

        self.render_buffer.extend(self.align_on(self.render_buffer_tmp, "1'b0", sep='', include_delim_in_right=True,))
        return self.render_buffer

########################################################################
# OutputWriter
########################################################################
class OutputWriter(BaseWriter):
    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip('output'):
                continue
            if self.register_lower:
                if self.item_lower == 'csr' and self.register_lower.startswith('exram_based_addr_'):
                    self.render_buffer.append(f"assign {self.item_lower}_{self.register_lower} = {{ {self.doublet_lower}_msb_reg, {self.doublet_lower}_lsb_reg }};")
                elif self.subregister_lower in ('msb','lsb'):
                    self.render_buffer.append(f"assign rf_{self.doublet_lower} = {{ {self.doublet_lower}_msb_reg, {self.doublet_lower}_lsb_reg }};")
                else:
                    self.render_buffer.append(f"assign rf_{self.doublet_lower} = {self.doublet_lower}_reg;")

        return self.align_on(self.render_buffer, '=', sep=' = ', strip=True)

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

# Skip handler mapping populates rule functions for ``skip``.
BaseWriter._SKIP_HANDLERS = {
    'ipnum': lambda self: False,
    'port': lambda self: (
        not self.item_lower or not self.register_lower
        or (
            self.item_lower == 'csr'
            and (self.typ != 'rw' or 'exram_based_addr' in self.register_lower)
        )
        or self.seen(self.doublet_lower)
    ),
    'bitwidth': lambda self: (
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
            not self.subregister_upper and self.register_upper and self.seen(self.doublet_upper)
        )
    ),
    'io': lambda self: (
        (
            self.item_lower == 'csr'
            and (self.typ != 'rw' or 'exram_based_addr' not in self.register_lower)
        )
        or self.seen(self.doublet_lower)
    ),
    'reg': lambda self: (
        self.typ != 'rw'
        or (
            self.subregister_lower
            and self.subregister_lower not in ('lsb', 'msb')
            and self.seen(self.doublet_lower)
        )
    ),
    'wire_nx': lambda self: (
        self.typ != 'rw'
        or (
            self.subregister_lower not in ('msb', 'lsb')
            and self.seen(self.doublet_lower)
        )
    ),
    'wire_en': lambda self: (
        self.typ != 'rw'
        or (
            self.subregister_lower not in ('msb', 'lsb')
            and self.seen(self.doublet_lower)
        )
    ),
    'seq': lambda self: (
        self.typ != 'rw'
        or (
            self.subregister_lower not in ('msb', 'lsb')
            and self.seen(self.doublet_lower)
        )
    ),
    'en': lambda self: (
        self.typ != 'rw'
        or (
            self.subregister_lower not in ('msb', 'lsb')
            and self.seen(self.doublet_lower)
        )
    ),
    'nx': lambda self: (
        self.typ != 'rw'
        or self.register_lower == 'status'
        or (
            self.subregister_lower not in ('msb', 'lsb')
            and self.seen(self.doublet_lower)
        )
    ),
    'control': lambda self: (
        self.typ != 'rw'
        or (
            self.subregister_lower not in ('msb', 'lsb')
            and self.seen(self.doublet_lower)
        )
    ),
    'output': lambda self: (
        not self.register_lower
        or self.doublet_lower in self.ignore_pair
        or self.seen(self.doublet_lower)
        or self.register_lower == 'exram_addr'
    ),
    'sfence': lambda self: False,
    'baseaddrsel': lambda self: False,
    'baseaddrselbitwidth': lambda self: False,
    'scoreboard': lambda self: False,
    'sfenceen': lambda self: False,
    'statusnx': lambda self: False,
    'riurwaddr': lambda self: False,
    'exceptport': lambda self: self.item_lower in ('ldma2', 'csr'),
    'exceptio': lambda self: self.item_lower in ('ldma2', 'csr'),
    'interrupt': lambda self: self.item_lower in ('ldma2', 'csr'),
    'exceptwire': lambda self: self.item_lower in ('ldma2', 'csr'),
}

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
