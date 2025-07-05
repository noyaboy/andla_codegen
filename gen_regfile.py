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
from typing import Dict, Type, Iterable, Callable

# 檔案路徑設定
input_filename       = 'input/andla_regfile.tmp.v'
output_filename      = 'output/andla_regfile.v'
dictionary_filename  = 'output/regfile_dictionary.log'


class RegistryMixin:
    """Mixin for registering writer subclasses automatically."""

    REGISTRY: Dict[str, Type["BaseWriter"]] = {}

    def __init_subclass__(cls, key: str | None = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if key is None:
            key = cls.__name__.removesuffix("Writer").lower()
        if key in cls.REGISTRY:
            raise ValueError(f"{key} 已註冊")
        cls.REGISTRY[key] = cls

@dataclass
class DictRow:
    item: str = ''
    register: str = ''
    subregister: str = ''
    type: str = ''
    id: int | None = None
    default_value: str = ''
    raw: dict = None

    @property
    def item_upper(self) -> str:
        return self.item.upper()

    @property
    def register_upper(self) -> str:
        return self.register.upper()

    @property
    def subregister_upper(self) -> str:
        return self.subregister.upper() if self.subregister else ''

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

    def render_template(self, template: str, context: dict) -> str:
        """Render a Jinja2 template string with the supplied context."""
        from jinja2 import Template
        return Template(template, keep_trailing_newline=True).render(**context)

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

    def align_lines(self, raw_lines, sep=' '):
        pairs = [line.split(sep, 1) for line in raw_lines]
        return self.align_pairs(pairs, sep)


class ZeroFillMixin:
    """Mixin to generate zero assignment lines for ID gaps."""

    zero_template: str = "{idx}    1'b0,\n"

    def zeros(self, start, end):
        for idx in range(start - 1, end, -1):
            yield self.zero_template.format(idx=idx)


class SkipMixin:
    """Provide default skip rules for items."""

    default_skip_items = {"ldma2", "csr"}

    def should_skip_item(self, row: DictRow) -> bool:
        return row.item in self.default_skip_items or getattr(row, "typ", "rw") != "rw"


class RowMixin:
    """Mixin supplying helpers for common DictRow field handling."""

    def load_row(self, row: DictRow):
        self.item = row.item
        self.register = row.register
        self.subregister = row.subregister
        self.key = f"{self.item}_{self.register}"
        self.typ = row.type
        self.item_upper = row.item_upper
        self.register_upper = row.register_upper
        self.subregister_upper = row.subregister_upper


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

class SimpleWriter(SkipMixin, RegistryMixin, BaseWriter):
    """Writer that renders a list of templates for selected items."""

    templates: list[str] = []
    item_selector: Callable[["SimpleWriter"], Iterable] = BaseWriter.iter_items

    def render(self):
        for item in self.item_selector():
            _item = item[0] if isinstance(item, tuple) else item
            if _item in self.default_skip_items:
                continue
            ctx = {"item": _item, "item_upper": _item.upper()}
            for tmpl in self.templates:
                yield self.render_template(tmpl, ctx)

# Mapping of simple template writers
SIMPLE_TEMPLATES: Dict[str, list[str]] = {
    "interrupt": [
        "                          ({{item}}_except & {{item}}_except_mask) |\n"
    ],
    "exceptwire": [
        "wire {{item}}_except        = csr_status_reg[`{{item_upper}}_ID + 8];\n",
        "wire {{item}}_except_mask   = csr_control_reg[`{{item_upper}}_ID + 8];\n",
    ],
    "exceptio": [
        "input                 rf_{{item}}_except_trigger;\n"
    ],
    "exceptport": [
        ",rf_{{item}}_except_trigger\n"
    ],
    "baseaddrselbitwidth": [
        "localparam {{item_upper}}_BASE_ADDR_SELECT_BITWIDTH = 3;\n"
    ],
    "baseaddrselio": [
        "output [{{item_upper}}_BASE_ADDR_SELECT_BITWIDTH-           1:0] {{item}}_base_addr_select;\n"
    ],
    "baseaddrselport": [
        ",{{item}}_base_addr_select\n"
    ],
}

# Keys that iterate over DMA items instead of regular items
DMA_KEYS = {"baseaddrselbitwidth", "baseaddrselio", "baseaddrselport"}


def register_simple_templates():
    for key, tmpls in SIMPLE_TEMPLATES.items():
        item_selector = BaseWriter.iter_dma_items if key in DMA_KEYS else BaseWriter.iter_items
        attrs = {
            "templates": tmpls,
            "item_selector": item_selector,
            "__module__": __name__,
        }
        cls = type(f"{key.title()}Writer", (SimpleWriter,), attrs)
        RegistryMixin.REGISTRY[key] = cls


register_simple_templates()


class TemplateLoopWriter(RowMixin, AlignMixin, BaseWriter):
    """Generic writer that loops over a row source and renders templates."""

    templates: list[str] = []
    row_source: Callable[["TemplateLoopWriter"], Iterable] = lambda self: self.lines
    zero_fill: bool = False
    zero_template: str | list[str] | None = None
    align_output: bool = False
    align_sep: str = " "

    def skip(self, row) -> bool:
        return False

    def context(self, row) -> dict:
        if isinstance(row, tuple):
            if len(row) >= 2:
                item, idx = row[0], row[1]
                return {"item": item, "item_upper": item.upper(), "id": idx}
            return {"item": row[0], "item_upper": row[0].upper()}
        return {
            "item": getattr(row, "item", ""),
            "item_upper": getattr(row, "item", "").upper(),
            "register": getattr(row, "register", ""),
            "register_upper": getattr(row, "register", "").upper(),
            "subregister": getattr(row, "subregister", ""),
            "subregister_upper": getattr(row, "subregister", "").upper(),
            "id": getattr(row, "id", None),
            "default_value": getattr(row, "default_value", ""),
        }

    def render(self):
        output_lines = []
        templates = list(self.templates)
        zero_templates = self.zero_template
        if zero_templates is None:
            zero_templates = [None] * len(templates)
        elif not isinstance(zero_templates, (list, tuple)):
            zero_templates = [zero_templates] * len(templates)

        for tmpl, ztmpl in zip(templates, zero_templates):
            prev_idx = None
            for row in self.row_source():
                if self.skip(row):
                    continue
                ctx = self.context(row)
                cur_idx = ctx.get("id")
                if self.zero_fill and ztmpl and cur_idx is not None and prev_idx is not None and prev_idx - cur_idx > 1:
                    for idx in range(prev_idx - 1, cur_idx, -1):
                        output_lines.append(ztmpl.format(idx=idx))
                output_lines.append(self.render_template(tmpl, ctx))
                if cur_idx is not None:
                    prev_idx = cur_idx
        if self.align_output and self.align_sep:
            if all(self.align_sep in line for line in output_lines):
                output_lines = self.align_lines(output_lines, self.align_sep)
        return output_lines



########################################################################
# RiurwaddrWriter
########################################################################
class RiurwaddrWriter(RegistryMixin, ZeroFillMixin, TemplateLoopWriter, key="riurwaddr"):
    templates = [
        "wire riurwaddr_bit{{id}}                      = "
        "{% if item == 'csr' %}1'b0{% else %}(issue_rf_riurwaddr[(RF_ADDR_BITWIDTH-1) -: ITEM_ID_BITWIDTH] == `{{item_upper}}_ID){% endif %};\n"
    ]
    zero_template = "wire riurwaddr_bit{idx}                      = 1'b0;\n"
    zero_fill = True
    row_source = BaseWriter.iter_items

    def context(self, row):
        item, value = row
        return {"item": item, "item_upper": item.upper(), "id": value}


########################################################################
# StatusnxWriter
########################################################################

class StatusnxWriter(RegistryMixin, ZeroFillMixin, TemplateLoopWriter, key="statusnx"):
    templates = [
        "assign csr_status_nx[{% if item == 'csr' %}0{% else %}`{{item_upper}}_ID{% endif %}]"
        "                = {% if item == 'csr' %}(wr_taken & sfence_en[0]  ) ? 1'b1 : scoreboard[0]{% else %}(wr_taken & sfence_en[`{{item_upper}}_ID]  ) ? 1'b1 : scoreboard[`{{item_upper}}_ID]{% endif %};\n",
        "assign csr_status_nx[{% if item == 'csr' %}8{% else %}`{{item_upper}}_ID + 8{% endif %}]     = "
        "{% if item == 'csr' %}1'b0{% elif item == 'ldma2' %}rf_ldma_except_trigger ? 1'b1 : (wr_taken & csr_status_en) ? issue_rf_riuwdata[`{{item_upper}}_ID + 8] : csr_status_reg[`{{item_upper}}_ID + 8]{% else %}rf_{{item}}_except_trigger ? 1'b1 : (wr_taken & csr_status_en) ? issue_rf_riuwdata[`{{item_upper}}_ID + 8] : csr_status_reg[`{{item_upper}}_ID + 8]{% endif %};\n",
    ]
    zero_template = [
        "assign csr_status_nx[{idx}]                = 1'b0;\n",
        "assign csr_status_nx[{idx} + 8]                = 1'b0;\n",
    ]
    zero_fill = True
    row_source = BaseWriter.iter_items

    def context(self, row):
        item, value = row
        return {"item": item, "item_upper": item.upper(), "id": value}

########################################################################
# SfenceenWriter
########################################################################

class SfenceenWriter(RegistryMixin, ZeroFillMixin, TemplateLoopWriter, key="sfenceen"):
    templates = ["               {% if item == 'csr' %}1'b0{% elif item == 'ldma2' %}1'b0,{% else %}{{item}}_sfence_en,{% endif %}\n"]
    zero_template = "               1'b0,\n"
    zero_fill = True
    row_source = BaseWriter.iter_items

    def context(self, row):
        item, value = row
        return {"item": item, "id": value}
########################################################################
# ScoreboardWriter
########################################################################
########################################################################
class ScoreboardWriter(RegistryMixin, ZeroFillMixin, BaseWriter, key="scoreboard"):
    template = (
        "assign scoreboard[{{id}}]               = "
        "{% if item == 'csr' %}(ip_rf_status_clr[0]) ? 1'b0 : csr_status_reg[0]{% else %}(ip_rf_status_clr[`{{item_upper}}_ID]) ? 1'b0 : csr_status_reg[`{{item_upper}}_ID]{% endif %};\n"
    )
    zero_template = "assign scoreboard[{idx}]               = 1'b0;\n"

    def render(self):
        output = []
        prev_id = None
        for item, value in self.iter_items():
            if prev_id is not None and prev_id - value > 1:
                output.extend(self.zeros(prev_id, value))
            ctx = {"item": item, "item_upper": item.upper(), "id": value}
            output.append(self.render_template(self.template, ctx))
            prev_id = value
        return output

########################################################################
# BaseaddrselWriter
########################################################################
class BaseaddrselWriter(SkipMixin, RegistryMixin, TemplateLoopWriter, key="baseaddrsel"):
    templates = [
        "wire [{{item_upper}}_BASE_ADDR_SELECT_BITWIDTH-1:0] {{item}}_base_addr_select_nx;\n",
        "assign  {{item}}_base_addr_select_nx           = {{item}}_sfence_nx[20:18];\n",
        "wire {{item}}_base_addr_select_en           = wr_taken & {{item}}_sfence_en;\n",
        "reg  [{{item_upper}}_BASE_ADDR_SELECT_BITWIDTH-1:0] {{item}}_base_addr_select_reg;\n",
        "always @(posedge clk or negedge rst_n) begin\n",
        "    if (~rst_n)                        {{item}}_base_addr_select_reg <= {{zero_init}};\n",
        "    else if ({{item}}_base_addr_select_en) {{item}}_base_addr_select_reg <= {{item}}_base_addr_select_nx;\n",
        "end\n",
        "wire [3-1: 0] {{item}}_base_addr_select;\n",
        "assign {{item}}_base_addr_select            = {{item}}_base_addr_select_reg;\n\n",
    ]

    row_source = BaseWriter.iter_dma_items

    def skip(self, item):
        return item in self.default_skip_items

    def context(self, item):
        def zero_init(item_upper: str) -> str:
            return f"{{({item_upper}_BASE_ADDR_SELECT_BITWIDTH){{1'd0}}}}"

        return {
            "item": item,
            "item_upper": item.upper(),
            "zero_init": zero_init(item.upper()),
        }

########################################################################
# SfenceWriter
########################################################################
class SfenceWriter(RegistryMixin, TemplateLoopWriter, key="sfence"):
    templates = [
        "wire {{item}}_start_reg_nx = wr_taken & {{item}}_sfence_en;\n"
        "reg  {{item}}_start_reg;\n"
        "wire {{item}}_start_reg_en = {{item}}_start_reg ^ {{item}}_start_reg_nx;\n"
        "always @(posedge clk or negedge rst_n) begin\n"
        "    if (~rst_n) {{item}}_start_reg <= 1'b0;\n"
        "    else if ({{item}}_start_reg_en) {{item}}_start_reg <= {{item}}_start_reg_nx;\n"
        "end\n"
        "assign rf_{{item}}_sfence = {{item}}_start_reg;\n\n"
    ]

    def row_source(self):
        seen = []
        for row in self.lines:
            if row.item and row.register == 'sfence' and row.item not in seen:
                seen.append(row.item)
        return seen

    def context(self, item):
        return {"item": item}

########################################################################
# IpnumWriter
########################################################################
class IpnumWriter(RegistryMixin, BaseWriter, key="ipnum"):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_items = {}

    def render(self):
        for row in self.lines:
            item = row.item
            if item and item not in self.seen_items:
                self.seen_items[item] = 1
        # 與原 Perl 保持一致：直接輸出 ITEM_ID_NUM 巨集
        yield "localparam ITEM_ID_NUM = `ITEM_ID_NUM;\n"

########################################################################
# PortWriter
########################################################################
class PortWriter(RegistryMixin, TemplateLoopWriter, key="port"):
    templates = [", rf_{{item}}_{{register}}\n"]
    row_source = lambda self: self.lines

    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_items = set()

    def skip(self, row: DictRow) -> bool:
        item = row.item
        register = row.register
        typ = row.type
        if not item or not register:
            return True
        if item == 'csr' and (typ != 'rw' or register in ('counter', 'counter_mask', 'status', 'control')):
            return True
        if item == 'csr' and re.search(r'exram_based_addr', register):
            return True
        key = f"{item}_{register}"
        if key in self.seen_items:
            return True
        self.seen_items.add(key)
        return False

    def context(self, row: DictRow):
        return {"item": row.item, "register": row.register}

########################################################################
# BitwidthWriter
########################################################################
class BitwidthWriter(RegistryMixin, TemplateLoopWriter, key="bitwidth"):
    """
    直接對照 Perl 程式；所有重複與原始邏輯完整保留，不做結構化優化
    """
    templates = ["{{line}}\n"]
    align_output = True
    align_sep = ' = '

    def row_source(self):
        lines = []
        seen_items = set()
        seen_cases = set()
        for row in self.lines:
            self.load_row(row)
            if self.subregister:
                if self.subregister not in ('msb', 'lsb'):
                    if (self.item, self.register) in seen_cases:
                        continue
                    lines.append(
                        f"localparam {self.item_upper}_{self.register_upper}_BITWIDTH = `{self.item_upper}_{self.register_upper}_BITWIDTH;"
                    )
                    seen_cases.add((self.item, self.register))
                else:
                    sub_key = f"{self.key}_{self.subregister}"
                    if sub_key not in seen_items:
                        lines.append(
                            f"localparam {self.item_upper}_{self.register_upper}_{self.subregister_upper}_BITWIDTH = `{self.item_upper}_{self.register_upper}_{self.subregister_upper}_BITWIDTH;"
                        )
                        seen_items.add(sub_key)
                        if self.subregister == 'msb':
                            lines.append(
                                f"localparam {self.item_upper}_{self.register_upper}_BITWIDTH = `{self.item_upper}_{self.register_upper}_BITWIDTH;"
                            )
            elif self.register:
                if self.key in seen_items:
                    continue
                if self.register == 'credit':
                    lines.append(
                        f"localparam {self.item_upper}_{self.register_upper}_BITWIDTH = 22;"
                    )
                else:
                    lines.append(
                        f"localparam {self.item_upper}_{self.register_upper}_BITWIDTH = `{self.item_upper}_{self.register_upper}_BITWIDTH;"
                    )
                seen_items.add(self.key)
        return lines

    def context(self, line):
        return {"line": line}


########################################################################
# IOWriter
########################################################################
class IOWriter(SkipMixin, RegistryMixin, TemplateLoopWriter, key="io"):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_items = {}
        self.io_lines   = []
        self.item       = ''
        self.register   = ''
        self.key        = ''
        self.typ        = ''

    def _skip(self, row: DictRow) -> bool:
        return (
            (row.item == 'csr' and row.register in ('id', 'revision', 'credit', 'nop', 'counter','counter_mask','status','control'))
            or self.key in self.seen_items
        )

    def _process(self, row: DictRow):
        if self._skip(row):
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

    templates = ["{{line}}\n"]
    align_output = True
    align_sep = '\t'

    def row_source(self):
        self.seen_items = {}
        lines = []
        for row in self.lines:
            self.load_row(row)
            if self._skip(row):
                continue
            if self.typ == 'ro':
                lines.append(f"input\t [{self.item.upper()}_{self.register_upper}_BITWIDTH-1:0] rf_{self.item}_{self.register};")
            else:
                if self.item == 'csr' and 'exram_based_addr' in self.register:
                    lines.append(f"wire\t [{self.item.upper()}_{self.register_upper}_BITWIDTH-1:0] {self.item}_{self.register};")
                elif self.register == 'sfence':
                    lines.append(f"output\t [1-1:0] rf_{self.item}_{self.register};")
                else:
                    lines.append(f"output\t [{self.item.upper()}_{self.register_upper}_BITWIDTH-1:0] rf_{self.item}_{self.register};")
            self.seen_items[self.key] = 1
        return lines

    def context(self, line):
        return {"line": line}


########################################################################
# RegWriter
########################################################################
class RegWriter(RegistryMixin, TemplateLoopWriter, key="reg"):
    templates = ["{{line}}\n"]
    align_output = True
    align_sep = '\t'

    def row_source(self):
        lines = []
        seen_items = set()
        for row in self.lines:
            self.load_row(row)
            if self.typ != 'rw':
                continue
            if self.subregister:
                if self.subregister in ('lsb','msb'):
                    lines.append(f"reg\t[{self.item.upper()}_{self.register.upper()}_{self.subregister.upper()}_BITWIDTH-1:0] {self.item}_{self.register}_{self.subregister}_reg;")
                else:
                    if self.key not in seen_items:
                        lines.append(f"reg\t[{self.item.upper()}_{self.register.upper()}_BITWIDTH-1:0] {self.item}_{self.register}_reg;")
                        seen_items.add(self.key)
            elif self.register:
                lines.append(f"reg\t[{self.item.upper()}_{self.register.upper()}_BITWIDTH-1:0] {self.item}_{self.register}_reg;")
        return lines

    def context(self, line):
        return {"line": line}


########################################################################
# WireNxWriter
########################################################################
class WireNxWriter(RegistryMixin, TemplateLoopWriter, key="wire_nx"):
    templates = ["{{line}}\n"]
    align_output = True
    align_sep = '   '

    def row_source(self):
        lines = []
        seen_items = set()
        for row in self.lines:
            self.load_row(row)
            if self.typ != 'rw':
                continue
            if self.subregister not in ('msb','lsb') and self.key in seen_items:
                continue
            seen_items.add(self.key)
            if self.subregister:
                if self.subregister in ('msb','lsb'):
                    lines.append(f"wire\t[{self.item_upper}_{self.register_upper}_{self.subregister_upper}_BITWIDTH-1:0] {self.item}_{self.register}_{self.subregister}_nx;")
                else:
                    lines.append(f"wire\t[{self.item_upper}_{self.register_upper}_BITWIDTH-1:0] {self.item}_{self.register}_nx;")
            elif self.register:
                lines.append(f"wire\t[{self.item_upper}_{self.register_upper}_BITWIDTH-1:0] {self.item}_{self.register}_nx;")
        return lines

    def context(self, line):
        return {"line": line}


########################################################################
# WireEnWriter
########################################################################
class WireEnWriter(RegistryMixin, TemplateLoopWriter, key="wire_en"):
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


    def _skip(self):
        if self.typ != 'rw':
            return True
        if self.subregister not in ('msb','lsb'):
            if self.key in self.seen_items:
                return True
            self.seen_items[self.key] = 1
        return False

    templates = ["wire   {{wire_name}};\n"]

    def row_source(self):
        self.seen_items = {}
        entries = []
        for row in self.lines:
            self.load_row(row)
            if self._skip():
                continue
            if self.subregister in ('msb','lsb'):
                wire_name = f"{self.item}_{self.register}_{self.subregister}_en"
            else:
                wire_name = f"{self.item}_{self.register}_en"
            entries.append(wire_name)
        return entries

    def context(self, wire_name):
        return {"wire_name": wire_name}


########################################################################
# SeqWriter
########################################################################
class SeqWriter(RegistryMixin, TemplateLoopWriter, key="seq"):
    templates = ["{{line}}\n"]

    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_items = {}


    def _skip(self):
        if self.typ != 'rw':
            return True
        if self.key in self.seen_items and self.subregister not in ('msb','lsb'):
            return True
        self.seen_items[self.key] = 1
        return False


    def row_source(self):
        lines = ["always @(posedge clk or negedge rst_n) begin",
                 "    if(~rst_n) begin"]
        reg_lines = []
        for row in self.lines:
            self.load_row(row)
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
                reg_lines.append(f"\t\t{self.item}_{self.register}_{self.subregister}_reg{' '*(50-len(self.item+self.register+self.subregister)+2)}<= {final_assignment};")
            else:
                reg_lines.append(f"\t\t{self.item}_{self.register}_reg{' '*(50-len(self.item+self.register)+3)}<= {final_assignment};")

        lines.extend([f"{l}" for l in reg_lines])
        lines.append("    end else begin")
        for l in reg_lines:
            if '<=' in l:
                reg_name = l.split('<=')[0].strip()
                wire_name = reg_name.replace('_reg', '_nx')
                lines.append(f"\t\t{reg_name:<48}<= {wire_name};")
        lines.append("    end")
        lines.append("end")
        return lines

    def context(self, line):
        return {"line": line}


########################################################################
# EnWriter
########################################################################
class EnWriter(RegistryMixin, TemplateLoopWriter, key="en"):
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.outfile    = outfile
        self.seen_items = {}
        self.item       = ''
        self.register   = ''
        self.subregister= ''
        self.key        = ''
        self.typ        = ''


    def _skip(self):
        if self.typ != 'rw':
            return True
        if self.key in self.seen_items and self.subregister not in ('msb','lsb'):
            return True
        self.seen_items[self.key] = 1
        return False

    templates = ["{{line}}\n"]
    align_output = True
    align_sep = ''

    def row_source(self):
        lines = []
        self.seen_items = {}
        for row in self.lines:
            self.load_row(row)
            if self._skip():
                continue
            if self.subregister in ('msb','lsb'):
                assignment = (f"assign {self.item}_{self.register}_{self.subregister}_en"
                              f" = (issue_rf_riurwaddr == {{`{self.item.upper()}_ID,`{self.item.upper()}_{self.register.upper()}_{self.subregister.upper()}_IDX}});")
            else:
                assignment = (f"assign {self.item}_{self.register}_en"
                              f" = (issue_rf_riurwaddr == {{`{self.item.upper()}_ID,`{self.item.upper()}_{self.register.upper()}_IDX}});")
            left = assignment.split('=')[0]
            right = assignment[len(left):]
            lines.extend(self.align_pairs([(left, right)], ''))
        return [line.rstrip('\n') for line in lines]

    def context(self, line):
        return {"line": line}


########################################################################
# NxWriter
########################################################################
class NxWriter(RegistryMixin, TemplateLoopWriter, key="nx"):
    """
    照原樣轉寫；重複邏輯不加抽象
    """
    templates = ["{{line}}\n"]
    align_output = True
    align_sep = ' = '

    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.seen_items  = {}


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

    def row_source(self):
        lines = []
        for row in self.lines:
            self.load_row(row)
            if self.typ == 'ro' and self.register:
                if self._skip():
                    continue
                if self.register == 'credit' and self.item == 'csr':
                    lines.append("assign csr_credit_nx = sqr_credit;")
                else:
                    lines.append(
                        f"assign {self.item}_{self.register}_nx = {{ {{ (32 - {self.register.upper()}_DATA.bit_length()) {{ 1'b0 }} }}, {self.register.upper()}_DATA}};"
                    )
            elif self.subregister:
                if self._skip():
                    continue
                if self.register in ('const_value','ram_padding_value'):
                    lines.append(
                        f"assign {self.item}_{self.register}_nx[{self.item.upper()}_{self.register.upper()}_BITWIDTH-1:{self.item.upper()}_{self.register.upper()}_BITWIDTH-2] = (wr_taken & {self.item}_{self.register}_en) ? issue_rf_riuwdata[RF_WDATA_BITWIDTH-1:RF_WDATA_BITWIDTH-2] : {self.item}_{self.register}_reg[{self.item.upper()}_{self.register.upper()}_BITWIDTH-1:{self.item.upper()}_{self.register.upper()}_BITWIDTH-2];"
                    )
                    lines.append(
                        f"assign {self.item}_{self.register}_nx[{self.item.upper()}_{self.register.upper()}_BITWIDTH-3:0] = (wr_taken & {self.item}_{self.register}_en) ? issue_rf_riuwdata[{self.item.upper()}_{self.register.upper()}_BITWIDTH-3:0]: {self.item}_{self.register}_reg[{self.item.upper()}_{self.register.upper()}_BITWIDTH-3:0];"
                    )
                elif self.subregister in ('msb','lsb'):
                    lines.append(
                        f"assign {self.item}_{self.register}_{self.subregister}_nx = (wr_taken & {self.item}_{self.register}_{self.subregister}_en) ? issue_rf_riuwdata[{self.item.upper()}_{self.register.upper()}_{self.subregister.upper()}_BITWIDTH-1:0] : {self.item}_{self.register}_{self.subregister}_reg;"
                    )
                else:
                    lines.append(
                        f"assign {self.item}_{self.register}_nx = (wr_taken & {self.item}_{self.register}_en) ? issue_rf_riuwdata[{self.item.upper()}_{self.register.upper()}_BITWIDTH-1:0] : {self.item}_{self.register}_reg;"
                    )
            elif self.register:
                if self._skip():
                    continue
                lines.append(
                    f"assign {self.item}_{self.register}_nx = (wr_taken & {self.item}_{self.register}_en) ? issue_rf_riuwdata[{self.item.upper()}_{self.register.upper()}_BITWIDTH-1:0] : {self.item}_{self.register}_reg;"
                )
        return lines

    def context(self, line):
        return {"line": line}


########################################################################
# CTRLWriter
########################################################################
class CTRLWriter(RegistryMixin, TemplateLoopWriter, key="control"):
    """
    依原 Perl 寫法轉成 Python
    """
    def __init__(self, outfile, dict_lines):
        super().__init__(outfile, dict_lines)
        self.io_lines   = []
        self.seen_pair  = {}


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


    templates = ["{{line}}\n"]

    def row_source(self):
        lines = ["assign issue_rf_riurdata ="]
        for row in self.lines:
            self.load_row(row)
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
                lines.append(self._build_output(signal, reg_nm, bw))
            else:
                if self.register in ('ldma_chsum_data','sdma_chsum_data'):
                    reg_nm = f"{self.item}_{self.register}"
                lines.append(self._build_output(signal, reg_nm, bw))
        pairs = []
        for l in lines[1:]:
            left, right = l.split("1'b0", 1)
            pairs.append((left, "1'b0" + right))
        aligned = self.align_pairs(pairs, '')
        return [lines[0]] + [line.rstrip('\n') for line in aligned]

    def context(self, line):
        return {"line": line}


########################################################################
# OutputWriter
########################################################################
class OutputWriter(RegistryMixin, TemplateLoopWriter, key="output"):
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
            'sdma_exram_addr'  : 1,
            'ldma_exram_addr'  : 1,
            'fme0_sfence'      : 1,
        }


    def _skip(self):
        key = f"{self.item}_{self.register}"

        if key in self.ignore_pair:
            return True

        if key in self.seen_pair:
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

    templates = ["{{line}}\n"]
    align_output = True
    align_sep = ' = '

    def row_source(self):
        lines = []
        self.seen_pair = {}
        for row in self.lines:
            self.load_row(row)
            if self.register:
                if self._skip():
                    continue
                if self.subregister:
                    if self.item == 'csr' and self.register.startswith('exram_based_addr_'):
                        out_reg = self.register.replace('_based_', '_based_')
                        lines.append(f"assign {self.item}_{out_reg} = {{{self.item}_{self.register}_msb_reg, {self.item}_{self.register}_lsb_reg}};")
                    elif self.subregister in ('msb','lsb'):
                        lines.append(f"assign rf_{self.item}_{self.register} = {{{self.item}_{self.register}_msb_reg, {self.item}_{self.register}_lsb_reg}};")
                    else:
                        lines.append(f"assign rf_{self.item}_{self.register} = {self.item}_{self.register}_reg;")
                else:
                    lines.append(f"assign rf_{self.item}_{self.register} = {self.item}_{self.register}_reg;")
        return lines

    def context(self, line):
        return {"line": line}


# The list of writers is now populated automatically via RegistryMixin.

########################################################################
# Main 轉檔流程
########################################################################
def gen_regfile():
    def load_input():
        with open(input_filename, 'r') as in_fh:
            return in_fh.readlines()

    def prepare_output():
        Path(output_filename).parent.mkdir(parents=True, exist_ok=True)
        return open(output_filename, 'w')

    def load_dictionary():
        return load_dictionary_lines()

    def init_writers(dict_lines, out_fh):
        patterns = {
            key: re.compile(rf'^// autogen_{key}_start')
            for key in RegistryMixin.REGISTRY
        }
        writers = {key: cls(out_fh, dict_lines) for key, cls in RegistryMixin.REGISTRY.items()}
        found = {key: False for key in RegistryMixin.REGISTRY}
        return patterns, writers, found

    def process_and_write(lines, out_fh, patterns, writers, found):
        for line in lines:
            out_fh.write(line)
            for key, pattern in patterns.items():
                if not found[key] and pattern.match(line):
                    writers[key].write()
                    found[key] = True

    lines = load_input()
    with prepare_output() as out_fh:
        dict_lines = load_dictionary()
        patterns, writers, found = init_writers(dict_lines, out_fh)
        process_and_write(lines, out_fh, patterns, writers, found)

if __name__ == "__main__":
    gen_regfile()
