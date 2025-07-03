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
from pathlib import Path

# 檔案路徑設定
input_filename       = 'input/andla_regfile.tmp.v'
output_filename      = 'output/andla_regfile.v'
dictionary_filename  = 'output/regfile_dictionary.log'

def load_dictionary_lines():
    """Read dictionary file once and return cleaned lines."""
    with open(dictionary_filename, 'r') as dict_fh:
        return [line.rstrip('\n') for line in dict_fh]


class BaseWriter:
    """Common base writer holding the output file and dictionary content."""
    def __init__(self, outfile, dict_lines):
        self.outfile = outfile
        self.lines = dict_lines

    FIELD_PATTERNS = {
        'Item'         : re.compile(r"'Item': '([^']*)'"),
        'Register'     : re.compile(r"'Register': '([^']*)'"),
        'SubRegister'  : re.compile(r"'SubRegister': '([^']*)'"),
        'Type'         : re.compile(r"'Type': '([^']*)'"),
        'ID'           : re.compile(r"'ID':\s*(\d+)"),
        'Default Value': re.compile(r"'Default Value': '([^']*)'")
    }

    def get_columns(self, line, columns):
        """Return a mapping of requested columns parsed from a dictionary line."""
        result = {}
        for col in columns:
            pat = self.FIELD_PATTERNS.get(col)
            if not pat:
                continue
            m = pat.search(line)
            if not m:
                if col == 'SubRegister' and "'SubRegister': nan" in line:
                    result[col] = ''
                else:
                    continue
            else:
                val = m.group(1)
                if col in ('Item', 'Register', 'SubRegister', 'Type'):
                    val = val.lower()
                elif col == 'ID':
                    val = int(val)
                result[col] = val
        return result

    def write(self):
        """Virtual write method for polymorphism."""
        raise NotImplementedError

########################################################################
# InterruptWriter
########################################################################
class InterruptWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_item = {}

    def write_interrupt(self):
        current_value = None
        entrance      = 0
        for line in self.lines:
            data = self.get_columns(line, ('Item', 'ID'))
            item = data.get('Item')
            _id  = data.get('ID')
            if item is not None and _id is not None:
                self.seen_item[item] = _id

        for key in sorted(self.seen_item, key=lambda k: self.seen_item[k], reverse=True):
            value  = self.seen_item[key]
            uckey  = key.upper()
            if entrance == 0:
                entrance      = 1
                current_value = value

            if key in ('ldma2', 'csr'):
                pass
            else:
                self.outfile.write(
                    f"                          ({key}_except & {key}_except_mask) |\n"
                )
            current_value = value

    write = write_interrupt

########################################################################
# ExceptwireWriter
########################################################################
class ExceptwireWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_item = {}

    def write_exceptwire(self):
        current_value = None
        entrance      = 0
        for line in self.lines:
            data = self.get_columns(line, ('Item', 'ID'))
            item = data.get('Item')
            _id  = data.get('ID')
            if item is not None and _id is not None:
                self.seen_item[item] = _id

        # 第一段
        for key in sorted(self.seen_item, key=lambda k: self.seen_item[k], reverse=True):
            value  = self.seen_item[key]
            uckey  = key.upper()
            if entrance == 0:
                entrance      = 1
                current_value = value

            if key in ('ldma2', 'csr'):
                pass
            else:
                self.outfile.write(
                    f"wire {key}_except        = csr_status_reg[`{uckey}_ID + 8];\n"
                )
            current_value = value

        # 第二段
        for key in sorted(self.seen_item, key=lambda k: self.seen_item[k], reverse=True):
            value  = self.seen_item[key]
            uckey  = key.upper()
            if entrance == 0:
                entrance      = 1
                current_value = value

            if key in ('ldma2', 'csr'):
                pass
            else:
                self.outfile.write(
                    f"wire {key}_except_mask   = csr_control_reg[`{uckey}_ID + 8];\n"
                )
            current_value = value

    write = write_exceptwire

########################################################################
# ExceptioWriter
########################################################################
class ExceptioWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_item = {}

    def write_exceptio(self):
        current_value = None
        entrance      = 0
        for line in self.lines:
            data = self.get_columns(line, ('Item', 'ID'))
            item = data.get('Item')
            _id  = data.get('ID')
            if item is not None and _id is not None:
                self.seen_item[item] = _id

        for key in sorted(self.seen_item, key=lambda k: self.seen_item[k], reverse=True):
            value  = self.seen_item[key]
            uckey  = key.upper()
            if entrance == 0:
                entrance      = 1
                current_value = value
            if key in ('ldma2', 'csr'):
                pass
            else:
                self.outfile.write(
                    f"input                 rf_{key}_except_trigger;\n"
                )
            current_value = value

    write = write_exceptio

########################################################################
# ExceptportWriter
########################################################################
class ExceptportWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_item = {}

    def write_exceptport(self):
        current_value = None
        entrance      = 0
        for line in self.lines:
            data = self.get_columns(line, ('Item', 'ID'))
            item = data.get('Item')
            _id  = data.get('ID')
            if item is not None and _id is not None:
                self.seen_item[item] = _id

        for key in sorted(self.seen_item, key=lambda k: self.seen_item[k], reverse=True):
            value  = self.seen_item[key]
            uckey  = key.upper()
            if entrance == 0:
                entrance      = 1
                current_value = value
            if key in ('ldma2', 'csr'):
                pass
            else:
                self.outfile.write(
                    f",rf_{key}_except_trigger\n"
                )
            current_value = value

    write = write_exceptport

########################################################################
# RiurwaddrWriter
########################################################################
class RiurwaddrWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_item = {}

    def write_riurwaddr(self):
        current_value = None
        entrance      = 0
        for line in self.lines:
            data = self.get_columns(line, ('Item', 'ID'))
            item = data.get('Item')
            _id  = data.get('ID')
            if item is not None and _id is not None:
                self.seen_item[item] = _id

        for key in sorted(self.seen_item, key=lambda k: self.seen_item[k], reverse=True):
            value  = self.seen_item[key]
            uckey  = key.upper()
            if entrance == 0:
                entrance      = 1
                current_value = value

            if current_value - value > 1:
                for idx in range(current_value - 1, value, -1):
                    self.outfile.write(
                        f"wire riurwaddr_bit{idx}                      = 1'b0;\n"
                    )

            if key == 'csr':
                self.outfile.write(
                    f"wire riurwaddr_bit{value}                      = 1'b0;\n"
                )
            else:
                self.outfile.write(
                    f"wire riurwaddr_bit{value}                      = (issue_rf_riurwaddr[(RF_ADDR_BITWIDTH-1) -: ITEM_ID_BITWIDTH] == `{uckey}_ID);\n"
                )
            current_value = value

    write = write_riurwaddr

########################################################################
# StatusnxWriter
########################################################################
class StatusnxWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_item = {}

    def write_statusnx(self):
        current_value = None
        entrance      = 0
        for line in self.lines:
            data = self.get_columns(line, ('Item', 'ID'))
            item = data.get('Item')
            _id  = data.get('ID')
            if item is not None and _id is not None:
                self.seen_item[item] = _id

        # 第一段 0~7
        for key in sorted(self.seen_item, key=lambda k: self.seen_item[k], reverse=True):
            value  = self.seen_item[key]
            uckey  = key.upper()
            if entrance == 0:
                entrance      = 1
                current_value = value

            if current_value - value > 1:
                for idx in range(current_value - 1, value, -1):
                    self.outfile.write(
                        f"assign csr_status_nx[{idx}]                = 1'b0;\n"
                    )

            if key == 'csr':
                self.outfile.write(
                    "assign csr_status_nx[0]                = (wr_taken & sfence_en[0]  ) ? 1'b1 : scoreboard[0];\n"
                )
            else:
                self.outfile.write(
                    f"assign csr_status_nx[`{uckey}_ID]         = (wr_taken & sfence_en[`{uckey}_ID]  ) ? 1'b1 : scoreboard[`{uckey}_ID];\n"
                )
            current_value = value

        # 第二段 8~15
        entrance = 0
        for key in sorted(self.seen_item, key=lambda k: self.seen_item[k], reverse=True):
            value  = self.seen_item[key]
            uckey  = key.upper()
            if entrance == 0:
                entrance      = 1
                current_value = value

            if current_value - value > 1:
                for idx in range(current_value - 1, value, -1):
                    self.outfile.write(
                        f"assign csr_status_nx[{idx} + 8]                       = 1'b0;\n"
                    )

            if key == 'csr':
                self.outfile.write(
                    "assign csr_status_nx[8]                           = 1'b0;\n"
                )
            elif key == 'ldma2':
                self.outfile.write(
                    f"assign csr_status_nx[`{uckey}_ID + 8]                = rf_ldma_except_trigger ? 1'b1 : (wr_taken & csr_status_en) ? issue_rf_riuwdata[`{uckey}_ID + 8] : csr_status_reg[`{uckey}_ID + 8];\n"
                )
            else:
                self.outfile.write(
                    f"assign csr_status_nx[`{uckey}_ID + 8]                = rf_{key}_except_trigger ? 1'b1 : (wr_taken & csr_status_en) ? issue_rf_riuwdata[`{uckey}_ID + 8] : csr_status_reg[`{uckey}_ID + 8];\n"
                )
            current_value = value

    write = write_statusnx

########################################################################
# SfenceenWriter
########################################################################
class SfenceenWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_item = {}

    def write_sfenceen(self):
        current_value = None
        entrance      = 0
        for line in self.lines:
            data = self.get_columns(line, ('Item', 'ID'))
            item = data.get('Item')
            _id  = data.get('ID')
            if item is not None and _id is not None:
                self.seen_item[item] = _id

        for key in sorted(self.seen_item, key=lambda k: self.seen_item[k], reverse=True):
            value  = self.seen_item[key]
            uckey  = key.upper()
            if entrance == 0:
                entrance      = 1
                current_value = value

            if current_value - value > 1:
                for idx in range(current_value - 1, value, -1):
                    self.outfile.write("               1'b0,\n")

            if key == 'csr':
                self.outfile.write("               1'b0\n")
            elif key == 'ldma2':
                self.outfile.write("               1'b0,\n")
            else:
                self.outfile.write(f"               {key}_sfence_en,\n")
            current_value = value

    write = write_sfenceen

########################################################################
# ScoreboardWriter
########################################################################
class ScoreboardWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_item = {}

    def write_scoreboard(self):
        current_value = None
        entrance      = 0
        for line in self.lines:
            data = self.get_columns(line, ('Item', 'ID'))
            item = data.get('Item')
            _id  = data.get('ID')
            if item is not None and _id is not None:
                self.seen_item[item] = _id

        for key in sorted(self.seen_item, key=lambda k: self.seen_item[k], reverse=True):
            value  = self.seen_item[key]
            uckey  = key.upper()
            if entrance == 0:
                entrance      = 1
                current_value = value

            if current_value - value > 1:
                for idx in range(current_value - 1, value, -1):
                    self.outfile.write(
                        f"assign scoreboard[{idx}]               = 1'b0;\n"
                    )

            if key == 'csr':
                self.outfile.write(
                    f"assign scoreboard[{value}]               = (ip_rf_status_clr[0]) ? 1'b0 : csr_status_reg[0];\n"
                )
            else:
                self.outfile.write(
                    f"assign scoreboard[{value}]               = (ip_rf_status_clr[`{uckey}_ID]) ? 1'b0 : csr_status_reg[`{uckey}_ID];\n"
                )
            current_value = value

    write = write_scoreboard

########################################################################
# BaseaddrselbitwidthWriter
########################################################################
class BaseaddrselbitwidthWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_dma = {}

    def write_baseaddrselbitwidth(self):
        for line in self.lines:
            data = self.get_columns(line, ('Item',))
            item = data.get('Item')
            if item and 'dma' in item and item != 'ldma2':
                self.seen_dma[item] = 1
        for keys in self.seen_dma:
            uckeys = keys.upper()
            self.outfile.write(
                f"localparam {uckeys}_BASE_ADDR_SELECT_BITWIDTH = 3;\n"
            )

    write = write_baseaddrselbitwidth

########################################################################
# BaseaddrselioWriter
########################################################################
class BaseaddrselioWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_dma = {}

    def write_baseaddrselio(self):
        for line in self.lines:
            data = self.get_columns(line, ('Item',))
            item = data.get('Item')
            if item and 'dma' in item and item != 'ldma2':
                self.seen_dma[item] = 1
        for keys in self.seen_dma:
            uckeys = keys.upper()
            self.outfile.write(
                f"output [{uckeys}_BASE_ADDR_SELECT_BITWIDTH-           1:0] {keys}_base_addr_select;\n"
            )

    write = write_baseaddrselio

########################################################################
# BaseaddrselportWriter
########################################################################
class BaseaddrselportWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_dma = {}

    def write_baseaddrselport(self):
        for line in self.lines:
            data = self.get_columns(line, ('Item',))
            item = data.get('Item')
            if item and 'dma' in item and item != 'ldma2':
                self.seen_dma[item] = 1
        for keys in self.seen_dma:
            self.outfile.write(f",{keys}_base_addr_select\n")

    write = write_baseaddrselport

########################################################################
# BaseaddrselWriter
########################################################################
class BaseaddrselWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_dma = {}

    def write_baseaddrsel(self):
        for line in self.lines:
            data = self.get_columns(line, ('Item',))
            item = data.get('Item')
            if item and 'dma' in item and item != 'ldma2':
                self.seen_dma[item] = 1
        for keys in self.seen_dma:
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
class SfenceWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_sfence = {}

    def write_sfence(self):
        for line in self.lines:
            data = self.get_columns(line, ('Item', 'Register'))
            item = data.get('Item')
            register = data.get('Register')
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
class IpnumWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_items = {}

    def write_ipnum(self):
        for line in self.lines:
            data = self.get_columns(line, ('Item',))
            item = data.get('Item')
            if item and item not in self.seen_items:
                self.seen_items[item] = 1
        # 與原 Perl 保持一致：直接輸出 ITEM_ID_NUM 巨集
        self.outfile.write("localparam ITEM_ID_NUM = `ITEM_ID_NUM;\n")

    write = write_ipnum

########################################################################
# PortWriter
########################################################################
class PortWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_items = {}

    def write_port(self):
        for line in self.lines:
            data = self.get_columns(line, ('Item', 'Register', 'Type'))
            item = data.get('Item')
            register = data.get('Register')
            typ = data.get('Type', '')
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
class BitwidthWriter(BaseWriter):
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

    def fetch_terms(self, line:str):
        data = self.get_columns(line, ('Item', 'Register', 'SubRegister'))
        if 'Item' in data and 'Register' in data:
            self.item        = data['Item'].upper()
            self.register    = data['Register'].upper()
            self.subregister = data.get('SubRegister', '').upper()
            self.key         = f"{self.item}_{self.register}"

    def _process_sub(self):
        if self.subregister not in ('MSB', 'LSB'):
            if (self.item, self.register) in self.seen_cases:
                return
            self.bitwidth_lines.append(
                f"localparam {self.item}_{self.register}_BITWIDTH = `{self.item}_{self.register}_BITWIDTH;"
            )
            self.seen_cases[(self.item, self.register)] = 1
        else:
            sub_key = f"{self.key}_{self.subregister}"
            if sub_key not in self.seen_items:
                self.bitwidth_lines.append(
                    f"localparam {self.item}_{self.register}_{self.subregister}_BITWIDTH = `{self.item}_{self.register}_{self.subregister}_BITWIDTH;"
                )
                self.seen_items[sub_key] = 1
                if self.subregister == 'MSB':
                    self.bitwidth_lines.append(
                        f"localparam {self.item}_{self.register}_BITWIDTH = `{self.item}_{self.register}_BITWIDTH;"
                    )

    def _process_re(self):
        if self.key in self.seen_items:
            return
        if self.register == 'CREDIT':
            self.bitwidth_lines.append(
                f"localparam {self.item}_{self.register}_BITWIDTH = 22;"
            )
        else:
            self.bitwidth_lines.append(
                f"localparam {self.item}_{self.register}_BITWIDTH = `{self.item}_{self.register}_BITWIDTH;"
            )
        self.seen_items[self.key] = 1

    def write_bitwidth(self):
        for line in self.lines:
                self.fetch_terms(line)
                if self.subregister:
                    self._process_sub()
                elif self.register:
                    self._process_re()

        max_len = 0
        for l in self.bitwidth_lines:
            left = l.split('=')[0]
            max_len = max(max_len, len(left))


        for l in self.bitwidth_lines:
            left, right = l.split('=', 1)
            self.outfile.write(f"{left:<{max_len}} = {right.strip()}\n")




    write = write_bitwidth

########################################################################
# IOWriter
########################################################################
class IOWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_items = {}
        self.io_lines   = []
        self.item       = ''
        self.register   = ''
        self.key        = ''
        self.typ        = ''

    def fetch_terms(self, line:str):
        data = self.get_columns(line, ('Item', 'Register', 'Type'))
        if 'Item' in data and 'Register' in data:
            self.item     = data['Item']
            self.register = data['Register']
            self.key      = f"{self.item}_{self.register}"
        if 'Type' in data:
            self.typ = data['Type']

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
            self.io_lines.append(
                f"input\t [{self.item.upper()}_{self.register.upper()}_BITWIDTH-1:0] rf_{self.item}_{self.register};"
            )
        else:
            if self.item == 'csr' and 'exram_based_addr' in self.register:
                self.io_lines.append(
                    f"wire\t [{self.item.upper()}_{self.register.upper()}_BITWIDTH-1:0] {self.item}_{self.register};"
                )
            elif self.register == 'sfence':
                self.io_lines.append(
                    f"output\t [1-1:0] rf_{self.item}_{self.register};"
                )
            else:
                self.io_lines.append(
                    f"output\t [{self.item.upper()}_{self.register.upper()}_BITWIDTH-1:0] rf_{self.item}_{self.register};"
                )
        self.seen_items[self.key] = 1

    def write_io(self):
        for line in self.lines:
                self.fetch_terms(line)
                self._process()

        max_len = 0
        for l in self.io_lines:
            left = l.split('\t')[0]
            max_len = max(max_len, len(left))

        for l in self.io_lines:
            left, right = l.split('\t', 1)
            self.outfile.write(f"{left:<{max_len}}\t{right}\n")

    write = write_io

########################################################################
# RegWriter
########################################################################
class RegWriter(BaseWriter):
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

    def fetch_terms(self, line:str):
        data = self.get_columns(line, ('Item', 'Register', 'SubRegister', 'Type'))
        if 'Item' in data and 'Register' in data:
            self.item       = data['Item']
            self.register   = data['Register']
            self.subregister= data.get('SubRegister', '')
            self.key        = f"{self.item}_{self.register}"
        if 'Type' in data:
            self.typ = data['Type']

    def _skip(self):
        return self.typ != 'rw'

    def _process_sub(self):
        if self._skip():
            return
        if self.subregister in ('lsb','msb'):
            self.reg_lines.append(
                f"reg\t[{self.item.upper()}_{self.register.upper()}_{self.subregister.upper()}_BITWIDTH-1:0] {self.item}_{self.register}_{self.subregister}_reg;"
            )
        else:
            if self.key not in self.seen_items:
                self.reg_lines.append(
                    f"reg\t[{self.item.upper()}_{self.register.upper()}_BITWIDTH-1:0] {self.item}_{self.register}_reg;"
                )
                self.seen_items[self.key] = 1

    def _process_re(self):
        if self._skip():
            return
        self.reg_lines.append(
            f"reg\t[{self.item.upper()}_{self.register.upper()}_BITWIDTH-1:0] {self.item}_{self.register}_reg;"
        )

    def write_reg(self):
        for line in self.lines:
                self.fetch_terms(line)
                if self.subregister:
                    self._process_sub()
                elif self.register:
                    self._process_re()

        max_len = 0
        for l in self.reg_lines:
            left = l.split('] ')[0]
            max_len = max(max_len, len(left))

        for l in self.reg_lines:
            left, right = l.split('] ', 1)
            self.outfile.write(f"{left:<{max_len}}] \t{right}\n")

    write = write_reg

########################################################################
# WireNxWriter
########################################################################
class WireNxWriter(BaseWriter):
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

    def fetch_terms(self, line:str):
        data = self.get_columns(line, ('Item', 'Register', 'SubRegister', 'Type'))
        self.item        = data.get('Item', '')
        self.register    = data.get('Register', '')
        self.subregister = data.get('SubRegister', '')
        self.key = f"{self.item}_{self.register}"
        self.item_upper       = self.item.upper()
        self.register_upper   = self.register.upper()
        self.subregister_upper= self.subregister.upper() if self.subregister else ''
        if 'Type' in data:
            self.typ = data['Type']

    def _skip(self):
        if self.typ != 'rw':
            return True
        if self.subregister not in ('msb','lsb') and self.key in self.seen_items:
            return True
        self.seen_items[self.key] = 1
        return False

    def _process_sub(self):
        if self._skip():
            return
        if self.subregister in ('msb','lsb'):
            self.wire_lines.append(
                f"wire\t[{self.item_upper}_{self.register_upper}_{self.subregister_upper}_BITWIDTH-1:0] {self.item}_{self.register}_{self.subregister}_nx;"
            )
        else:
            self.wire_lines.append(
                f"wire\t[{self.item_upper}_{self.register_upper}_BITWIDTH-1:0] {self.item}_{self.register}_nx;"
            )

    def _process_re(self):
        if self._skip():
            return
        self.wire_lines.append(
            f"wire\t[{self.item_upper}_{self.register_upper}_BITWIDTH-1:0] {self.item}_{self.register}_nx;"
        )

    def write_wire_nx(self):
        for line in self.lines:
                self.fetch_terms(line)
                if self.subregister:
                    self._process_sub()
                elif self.register:
                    self._process_re()

        max_len = 0
        for l in self.wire_lines:
            left = l.split('] ')[0]
            max_len = max(max_len, len(left))
        for l in self.wire_lines:
            left, right = l.split('] ', 1)
            self.outfile.write(f"{left:<{max_len}}]   {right}\n")

    write = write_wire_nx

########################################################################
# WireEnWriter
########################################################################
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

    def fetch_terms(self, line:str):
        data = self.get_columns(line, ('Item', 'Register', 'SubRegister', 'Type'))
        self.item        = data.get('Item', '')
        self.register    = data.get('Register', '')
        self.subregister = data.get('SubRegister', '')
        self.key = f"{self.item}_{self.register}"
        if 'Type' in data:
            self.typ = data['Type']

    def _skip(self):
        if self.typ != 'rw':
            return True
        if self.subregister not in ('msb','lsb'):
            if self.key in self.seen_items:
                return True
            self.seen_items[self.key] = 1
        return False

    def write_wire_en(self):
        self.seen_items = {}
        for line in self.lines:
                self.fetch_terms(line)
                if self._skip():
                    continue

                if self.subregister in ('msb','lsb'):
                    self.wire_name = f"{self.item}_{self.register}_{self.subregister}_en"
                else:
                    self.wire_name = f"{self.item}_{self.register}_en"
                self.outfile.write(f"wire   {self.wire_name};\n")

    write = write_wire_en

########################################################################
# SeqWriter
########################################################################
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

    def fetch_terms(self, line:str):
        data = self.get_columns(line, ('Item', 'Register', 'SubRegister', 'Type'))
        if 'Item' in data and 'Register' in data:
            self.item       = data['Item']
            self.register   = data['Register']
            self.subregister= data.get('SubRegister', '')
            self.key        = f"{self.item}_{self.register}"
        if 'Type' in data:
            self.typ = data['Type']

    def _skip(self):
        if self.typ != 'rw':
            return True
        if self.key in self.seen_items and self.subregister not in ('msb','lsb'):
            return True
        self.seen_items[self.key] = 1
        return False

    def _process_sub(self, line:str):
        if self._skip():
            return
        default = self.get_columns(line, ('Default Value',)).get('Default Value', '')

        if default.startswith('0x'):
            final_assignment = default.replace('0x', '32\'h')
        elif self.subregister in ('msb','lsb'):
            bit = "1'b1" if default == '1' else "1'b0"
            final_assignment = f"{{ {{({self.item.upper()}_{self.register.upper()}_{self.subregister.upper()}_BITWIDTH-1){{1'd0}}}}, {bit} }}"
        else:
            bit = "1'b1" if default == '1' else "1'b0"
            final_assignment = f"{{ {{({self.item.upper()}_{self.register.upper()}_BITWIDTH-1){{1'd0}}}}, {bit} }}"

        if self.subregister in ('msb','lsb'):
            self.reg_lines.append(
                f"\t\t{self.item}_{self.register}_{self.subregister}_reg{' '*(50-len(self.item+self.register+self.subregister)+2)}<= {final_assignment};"
            )
        else:
            self.reg_lines.append(
                f"\t\t{self.item}_{self.register}_reg{' '*(50-len(self.item+self.register)+3)}<= {final_assignment};"
            )

    def _process_re(self, line:str):
        if self._skip():
            return
        default = self.get_columns(line, ('Default Value',)).get('Default Value', '')
        if default.startswith('0x'):
            final_assignment = default.replace('0x', '32\'h')
        else:
            bit = "1'b1" if default == '1' else "1'b0"
            final_assignment = f"{{ {{({self.item.upper()}_{self.register.upper()}_BITWIDTH-1){{1'd0}}}}, {bit} }}"
        self.reg_lines.append(
            f"\t\t{self.item}_{self.register}_reg{' '*(50-len(self.item+self.register)+3)}<= {final_assignment};"
        )

    def write_seq(self):
        self.outfile.write("always @(posedge clk or negedge rst_n) begin\n")
        self.outfile.write("    if(~rst_n) begin\n")
        for line in self.lines:
            self.fetch_terms(line)
            if self.subregister:
                self._process_sub(line)
            elif self.register:
                self._process_re(line)

        for l in self.reg_lines:
            self.outfile.write(f"{l}\n")

        self.outfile.write("    end else begin\n")
        for l in self.reg_lines:
            if '<=' in l:
                reg_name = l.split('<=')[0].strip()
                wire_name = reg_name.replace('_reg', '_nx')
                self.outfile.write(f"\t\t{reg_name:<48}<= {wire_name};\n")
        self.outfile.write("    end\n")
        self.outfile.write("end\n")

    write = write_seq

########################################################################
# EnWriter
########################################################################
class EnWriter(BaseWriter):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.outfile    = outfile
        self.seen_items = {}
        self.item       = ''
        self.register   = ''
        self.subregister= ''
        self.key        = ''
        self.typ        = ''

    def fetch_term(self, line:str):
        data = self.get_columns(line, ('Item', 'Register', 'SubRegister', 'Type'))
        if 'Item' in data and 'Register' in data:
            self.item       = data['Item']
            self.register   = data['Register']
            self.subregister= data.get('SubRegister', '')
            self.key        = f"{self.item}_{self.register}"
        if 'Type' in data:
            self.typ = data['Type']

    def _skip(self):
        if self.typ != 'rw':
            return True
        if self.key in self.seen_items and self.subregister not in ('msb','lsb'):
            return True
        self.seen_items[self.key] = 1
        return False

    def write_en(self):
        for line in self.lines:
                self.fetch_term(line)
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
                self.outfile.write(f"{left:<50s}{right}\n")

    write = write_en

########################################################################
# NxWriter
########################################################################
class NxWriter(BaseWriter):
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

    def fetch_terms(self, line:str):
        data = self.get_columns(line, ('Item', 'Register', 'SubRegister', 'Type'))
        self.item        = data.get('Item', '')
        self.register    = data.get('Register', '')
        self.subregister = data.get('SubRegister', '')
        self.key = f"{self.item}_{self.register}"
        self.typ = data.get('Type', '')

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
            self.assignments.append(
                "assign csr_credit_nx = sqr_credit;"
            )
        else:
            self.assignments.append(
                f"assign {self.item}_{self.register}_nx = {{ {{ (32 - {self.register.upper()}_DATA.bit_length()) {{ 1'b0 }} }}, {self.register.upper()}_DATA}};"
            )

    def _process_sub(self):
        if self._skip():
            return
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

    def _process_re(self):
        if self._skip():
            return
        self.assignments.append(
            f"assign {self.item}_{self.register}_nx = "
            f"(wr_taken & {self.item}_{self.register}_en) ? "
            f"issue_rf_riuwdata[{self.item.upper()}_{self.register.upper()}_BITWIDTH-1:0] : "
            f"{self.item}_{self.register}_reg;"
        )

    def write_nx(self):
        for line in self.lines:
            self.fetch_terms(line)
            if self.typ == 'ro' and self.register:
                self._process_ro()
            elif self.subregister:
                self._process_sub()
            elif self.register:
                self._process_re()

        max_len = 0
        for a in self.assignments:
            left = a.split('=')[0]
            max_len = max(max_len, len(left))

        for a in self.assignments:
            left, right = a.split('=', 1)
            self.outfile.write(f"{left:<{max_len}} = {right.strip()}\n")

    write = write_nx

########################################################################
# CTRLWriter
########################################################################
class CTRLWriter(BaseWriter):
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

    def fetch_terms(self, line:str):
        data = self.get_columns(line, ('Item', 'Register', 'SubRegister', 'Type'))
        if 'Item' in data and 'Register' in data:
            self.item       = data['Item']
            self.register   = data['Register']
            self.subregister= data.get('SubRegister', '')
            self.key        = f"{self.item}_{self.register}"
        if 'Type' in data:
            self.typ = data['Type']

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

    def _process_sub(self):
        if self._skip():
            return
        if self.subregister in ('msb','lsb'):
            signal = f"{self.item}_{self.register}_{self.subregister}_en"
            reg_nm = f"{self.item}_{self.register}_{self.subregister}_reg"
            bw     = f"{self.item.upper()}_{self.register.upper()}_{self.subregister.upper()}_BITWIDTH"
        else:
            signal = f"{self.item}_{self.register}_en"
            reg_nm = f"{self.item}_{self.register}_reg"
            bw     = f"{self.item.upper()}_{self.register.upper()}_BITWIDTH"

        self.io_lines.append(self._build_output(signal, reg_nm, bw))

    def _process_re(self):
        if self._skip():
            return
        if self.register in ('ldma_chsum_data','sdma_chsum_data'):
            signal = f"{self.item}_{self.register}_en"
            reg_nm = f"{self.item}_{self.register}"
        else:
            signal = f"{self.item}_{self.register}_en"
            reg_nm = f"{self.item}_{self.register}_reg"
        bw = f"{self.item.upper()}_{self.register.upper()}_BITWIDTH"

        self.io_lines.append(self._build_output(signal, reg_nm, bw))

    def write_control(self):
        self.outfile.write("assign issue_rf_riurdata =\n")
        for line in self.lines:
            self.fetch_terms(line)
            if self.subregister:
                self._process_sub()
            elif self.register:
                self._process_re()

        max_len = 0
        for l in self.io_lines:
            left = l.split("1'b0")[0]
            max_len = max(max_len, len(left))

        for l in self.io_lines:
            left, right = l.split("1'b0", 1)
            self.outfile.write(f"{left:<{max_len}}1'b0{right}\n")

    write = write_control

########################################################################
# OutputWriter
########################################################################
class OutputWriter(BaseWriter):
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

    def fetch_terms(self, line:str):
        data = self.get_columns(line, ('Item', 'Register', 'SubRegister'))
        if 'Item' in data and 'Register' in data:
            self.item       = data['Item']
            self.register   = data['Register']
            self.subregister= data.get('SubRegister', '')

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
                self.bitwidth_lines.append(
                    f"assign {self.item}_{out_reg} = {{{self.item}_{self.register}_msb_reg, {self.item}_{self.register}_lsb_reg}};"
                )
            elif self.subregister in ('msb','lsb'):
                self.bitwidth_lines.append(
                    f"assign rf_{self.item}_{self.register} = {{{self.item}_{self.register}_msb_reg, {self.item}_{self.register}_lsb_reg}};"
                )
            else:
                self.bitwidth_lines.append(
                    f"assign rf_{self.item}_{self.register} = {self.item}_{self.register}_reg;"
                )
        else:
            self.bitwidth_lines.append(
                f"assign rf_{self.item}_{self.register} = {self.item}_{self.register}_reg;"
            )

    def write_output(self):
        for line in self.lines:
                self.fetch_terms(line)
                if self.register:
                    self._process()

        max_len = 0
        for l in self.bitwidth_lines:
            left = l.split('=')[0]
            max_len = max(max_len, len(left))
        for l in self.bitwidth_lines:
            left, right = l.split('=', 1)
            self.outfile.write(f"{left:<{max_len}} = {right.strip()}\n")
    write = write_output

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
