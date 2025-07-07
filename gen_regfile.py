#!/usr/bin/env python3

import re
from pathlib import Path

from utils import DictRow, WRITER_MAP, load_dictionary_lines, register_writer

# File path configuration
input_filename       = 'input/andla_regfile.tmp.v'
output_filename      = 'output/andla_regfile.v'
dictionary_filename  = 'output/regfile_dictionary.log'



class BaseWriter:
    """
    Generic writer implementing the data-to-template-to-output flow and
    providing helpers for column retrieval, item ordering and DMA item filtering.
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

    # subclasses override ``skip_rule`` to implement per-writer logic.  The
    # ``skip`` method simply delegates to that hook.

    def seen(self, key):
        """Return True if ``key`` has been seen; otherwise mark it and return False."""
        if key in self.seen_set:
            return True
        self.seen_set[key] = 1
        return False

    def skip(self) -> bool:
        """Return ``True`` when ``skip_rule`` signals to skip the current row."""
        return self.skip_rule()

    def skip_rule(self) -> bool:
        """Per-writer skip logic. Subclasses MUST override."""
        raise NotImplementedError

    def render(self):
        """Return an iterable of strings for the output file. Subclasses may override this."""
        raise NotImplementedError

    def write(self):
        """Write each line produced by ``render`` to ``outfile``."""
        for line in self.render():
            self.outfile.write(line)

    def get_columns(self, row: DictRow, columns):
        """Extract fields from ``row`` (case-insensitive with spaces replaced by underscores) and return those with values."""
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
        
    def emit_zero_gap(self, prev_id, cur_id, template):
        """If IDs are not contiguous, emit 1'b0 lines using the provided template."""
        if prev_id is not None and prev_id - cur_id > 1:
            self.render_buffer.extend([template.format(idx=idx) for idx in range(prev_id - 1, cur_id, -1)])

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
@register_writer('interrupt')
class InterruptWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return self.item_lower in ('ldma2', 'csr')

    def render(self):
        for self.item_lower, _ , _ in self.iter_items():
            if self.skip():
                continue
            self.render_buffer.append(f"                          ({self.item_lower}_except & {self.item_lower}_except_mask) |\n")
        return self.render_buffer

########################################################################
# ExceptwireWriter
########################################################################
@register_writer('exceptwire')
class ExceptwireWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return self.item_lower in ('ldma2', 'csr')

    def render(self):
        for self.item_lower, self.item_upper, _ in self.iter_items():
            if self.skip():
                continue
            self.render_buffer.append(f"wire {self.item_lower}_except = csr_status_reg[`{self.item_upper}_ID + 8];\n")
            self.render_buffer.append(f"wire {self.item_lower}_except_mask = csr_control_reg[`{self.item_upper}_ID + 8];\n")
        return self.align_on(self.render_buffer, '=', sep=' = ', strip=True)

########################################################################
# ExceptioWriter
########################################################################
@register_writer('exceptio')
class ExceptioWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return self.item_lower in ('ldma2', 'csr')

    def render(self):
        for self.item_lower, _ , _ in self.iter_items():
            if self.skip():
                continue
            self.render_buffer.append(f"input rf_{self.item_lower}_except_trigger;\n")
        return self.render_buffer

########################################################################
# ExceptportWriter
########################################################################
@register_writer('exceptport')
class ExceptportWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return self.item_lower in ('ldma2', 'csr')

    def render(self):
        for self.item_lower, _ , _ in self.iter_items():
            if self.skip():
                continue
            self.render_buffer.append(f",rf_{self.item_lower}_except_trigger\n")
        return self.render_buffer

########################################################################
# RiurwaddrWriter
########################################################################
@register_writer('riurwaddr')
class RiurwaddrWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

    def render(self):
        prev_id = None
        for self.item_lower, self.item_upper, self.id in self.iter_items():
            self.emit_zero_gap(prev_id, self.id,"wire riurwaddr_bit{idx} = 1'b0;\n")
            if self.item_lower == 'csr':
                self.render_buffer.append(f"wire riurwaddr_bit{self.id} = 1'b0;\n")
            else:
                self.render_buffer.append(f"wire riurwaddr_bit{self.id} = (issue_rf_riurwaddr[(RF_ADDR_BITWIDTH-1) -: ITEM_ID_BITWIDTH] == `{self.item_upper}_ID);\n")
            prev_id = self.id

        return self.align_on(self.render_buffer, '=', sep=' = ', strip=True)

########################################################################
# StatusnxWriter
########################################################################
@register_writer('statusnx')
class StatusnxWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

    def render(self):
        prev_id = None
        for self.item_lower, self.item_upper, self.id in self.iter_items():
            self.emit_zero_gap(prev_id, self.id, "assign csr_status_nx[{idx}] = 1'b0;\n")
            self.emit_zero_gap(prev_id, self.id, "assign csr_status_nx[{idx} + 8] = 1'b0;\n")

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
@register_writer('sfenceen')
class SfenceenWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

    def render(self):
        prev_id = None
        for self.item_lower, self.item_upper, self.id in self.iter_items():
            self.emit_zero_gap(prev_id, self.id, "               1'b0,\n")
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
@register_writer('scoreboard')
class ScoreboardWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

    def render(self):
        prev_id = None
        for self.item_lower, self.item_upper, self.id in self.iter_items():
            self.emit_zero_gap(prev_id, self.id, "assign scoreboard[{idx}] = 1'b0;\n")
            self.render_buffer.append(f"assign scoreboard[{self.id}] = (ip_rf_status_clr[`{self.item_upper}_ID]) ? 1'b0 : csr_status_reg[`{self.item_upper}_ID];\n")
            prev_id = self.id

        return self.align_on(self.render_buffer, '=', sep=' = ', strip=True)

########################################################################
# BaseaddrselbitwidthWriter
########################################################################
@register_writer('baseaddrselbitwidth')
class BaseaddrselbitwidthWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

    def render(self):
        for self.item_lower, self.item_upper, _ in self.iter_items(dma_only=True):
            self.render_buffer.append(f"localparam {self.item_upper}_BASE_ADDR_SELECT_BITWIDTH = 3;\n")
        return self.render_buffer

########################################################################
# BaseaddrselWriter
########################################################################
@register_writer('baseaddrsel')
class BaseaddrselWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

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
@register_writer('sfence')
class SfenceWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

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
@register_writer('ipnum')
class IpnumWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

    def render(self):
        return ["localparam ITEM_ID_NUM = `ITEM_ID_NUM;\n"]

########################################################################
# PortWriter
########################################################################
@register_writer('port')
class PortWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return (
            ( self.item_lower == 'csr' and (self.typ != 'rw' or 'exram_based_addr' in self.register_lower) )
            or self.seen(self.doublet_lower)
        )

    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip():
                continue
            self.render_buffer.append(f", rf_{self.doublet_lower}\n")
        return self.render_buffer


########################################################################
# BitwidthWriter
########################################################################
@register_writer('bitwidth')
class BitwidthWriter(BaseWriter):
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
                not self.subregister_upper and self.register_upper and self.seen(self.doublet_upper)
            )
        )

    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip():
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
@register_writer('io')
class IOWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return (
            (
                self.item_lower == 'csr'
                and (self.typ != 'rw' or 'exram_based_addr' not in self.register_lower)
            )
            or self.seen(self.doublet_lower)
        )

    def render(self):
        # Process each line, applying skip and render logic inline
        for row in self.lines:
            self.fetch_terms(row)

            if self.skip():
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
@register_writer('reg')
class RegWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return (
            self.typ != 'rw'
            or (
                self.subregister_lower
                and self.subregister_lower not in ('lsb', 'msb')
                and self.seen(self.doublet_lower)
            )
        )

    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip():
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
@register_writer('wire_nx')
class WireNxWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return (
            self.typ != 'rw'
            or (
                self.subregister_lower not in ('msb', 'lsb')
                and self.seen(self.doublet_lower)
            )
        )

    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip():
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
@register_writer('wire_en')
class WireEnWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return (
            self.typ != 'rw'
            or (
                self.subregister_lower not in ('msb', 'lsb')
                and self.seen(self.doublet_lower)
            )
        )

    def render(self):
        self.seen_set = {}
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip():
                continue
            if self.subregister_lower in ('msb','lsb'):
                self.render_buffer.append(f"wire   {self.triplet_lower}_en;\n")
            else:
                self.render_buffer.append(f"wire   {self.doublet_lower}_en;\n")
        return self.render_buffer


########################################################################
# SeqWriter
########################################################################
@register_writer('seq')
class SeqWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return (
            self.typ != 'rw'
            or (
                self.subregister_lower not in ('msb', 'lsb') and self.seen(self.doublet_lower)
            )
        )

    def render(self):
        self.render_buffer = ["always @(posedge clk or negedge rst_n) begin\n    if(~rst_n) begin\n"]

        for row in self.lines:
            self.fetch_terms(row)
            if self.skip():
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
            if self.skip():
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
@register_writer('en')
class EnWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return (
            self.typ != 'rw'
            or (
                self.subregister_lower not in ('msb', 'lsb')
                and self.seen(self.doublet_lower)
            )
        )

    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip():
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
@register_writer('nx')
class NxWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return (
            self.typ != 'rw'
            or self.register_lower == 'status'
            or (
                self.subregister_lower not in ('msb', 'lsb')
                and self.seen(self.doublet_lower)
            )
        )

    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip():
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
@register_writer('control')
class CTRLWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return (
            self.typ != 'rw'
            or (
                self.subregister_lower not in ('msb', 'lsb')
                and self.seen(self.doublet_lower)
            )
        )

    def render(self):
        self.render_buffer = ["assign issue_rf_riurdata =\n"]
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip():
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
@register_writer('output')
class OutputWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return (
            self.seen(self.doublet_lower)
            or self.typ != 'rw'
            or ( self.item_lower == 'csr' and 'exram_based_addr' not in self.register_lower )
            or self.register_lower in ['exram_addr', 'sfence']
        )

    def render(self):
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip():
                continue
            if self.register_lower:
                if self.item_lower == 'csr' and self.register_lower.startswith('exram_based_addr_'):
                    self.render_buffer.append(f"assign {self.item_lower}_{self.register_lower} = {{ {self.doublet_lower}_msb_reg, {self.doublet_lower}_lsb_reg }};")
                elif self.subregister_lower in ('msb','lsb'):
                    self.render_buffer.append(f"assign rf_{self.doublet_lower} = {{ {self.doublet_lower}_msb_reg, {self.doublet_lower}_lsb_reg }};")
                else:
                    self.render_buffer.append(f"assign rf_{self.doublet_lower} = {self.doublet_lower}_reg;")

        return self.align_on(self.render_buffer, '=', sep=' = ', strip=True)

# ``WRITER_MAP`` is automatically populated by the ``@register_writer``
# decorator applied to each writer class above.


########################################################################
# Main generation workflow
########################################################################
def gen_regfile():
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
    gen_regfile()
