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
from typing import Dict, Iterable

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

# ----------------------------------------------------------------------
# Mapping of simple template writers originally implemented via ``SimpleWriter``.
SIMPLE_TEMPLATES: Dict[str, list[str]] = {
    "interrupt": [
        "                          ({{item}}_except & {{item}}_except_mask) |\n",
    ],
    "exceptwire": [
        "wire {{item}}_except        = csr_status_reg[`{{item_upper}}_ID + 8];\n",
        "wire {{item}}_except_mask   = csr_control_reg[`{{item_upper}}_ID + 8];\n",
    ],
    "exceptio": [
        "input                 rf_{{item}}_except_trigger;\n",
    ],
    "exceptport": [
        ",rf_{{item}}_except_trigger\n",
    ],
    "baseaddrselbitwidth": [
        "localparam {{item_upper}}_BASE_ADDR_SELECT_BITWIDTH = 3;\n",
    ],
    "baseaddrselio": [
        "output [{{item_upper}}_BASE_ADDR_SELECT_BITWIDTH-           1:0] {{item}}_base_addr_select;\n",
    ],
    "baseaddrselport": [
        ",{{item}}_base_addr_select\n",
    ],
}


# ----------------------------------------------------------------------
# Configuration for the new generic writer engine.  Each entry encodes the
# behaviour of a former ``XXXWriter`` class.
WRITER_CONFIG = {
    "interrupt": {
        "selector": "iter_items",
        "templates": SIMPLE_TEMPLATES["interrupt"],
    },
    "exceptwire": {
        "selector": "iter_items",
        "templates": SIMPLE_TEMPLATES["exceptwire"],
    },
    "exceptio": {
        "selector": "iter_items",
        "templates": SIMPLE_TEMPLATES["exceptio"],
    },
    "exceptport": {
        "selector": "iter_items",
        "templates": SIMPLE_TEMPLATES["exceptport"],
    },
    "baseaddrselbitwidth": {
        "selector": "iter_dma_items",
        "templates": SIMPLE_TEMPLATES["baseaddrselbitwidth"],
    },
    "baseaddrselio": {
        "selector": "iter_dma_items",
        "templates": SIMPLE_TEMPLATES["baseaddrselio"],
    },
    "baseaddrselport": {
        "selector": "iter_dma_items",
        "templates": SIMPLE_TEMPLATES["baseaddrselport"],
    },
    "riurwaddr": {
        "selector": "iter_items",
        "templates": [
            "wire riurwaddr_bit{{id}}                      = {% if item == 'csr' %}1'b0{% else %}(issue_rf_riurwaddr[(RF_ADDR_BITWIDTH-1) -: ITEM_ID_BITWIDTH] == `{{item_upper}}_ID){% endif %};\n",
        ],
        "zero_fill": True,
        "zero_template": "wire riurwaddr_bit{idx}                      = 1'b0;\n",
    },
    "statusnx": {
        "selector": "iter_items",
        "templates": [
            "assign csr_status_nx[{% if item == 'csr' %}0{% else %}`{{item_upper}}_ID{% endif %}]                = {% if item == 'csr' %}(wr_taken & sfence_en[0]  ) ? 1'b1 : scoreboard[0]{% else %}(wr_taken & sfence_en[`{{item_upper}}_ID]  ) ? 1'b1 : scoreboard[`{{item_upper}}_ID]{% endif %};\n",
            "assign csr_status_nx[{% if item == 'csr' %}8{% else %}`{{item_upper}}_ID + 8{% endif %}]     = {% if item == 'csr' %}1'b0{% elif item == 'ldma2' %}rf_ldma_except_trigger ? 1'b1 : (wr_taken & csr_status_en) ? issue_rf_riuwdata[`{{item_upper}}_ID + 8] : csr_status_reg[`{{item_upper}}_ID + 8]{% else %}rf_{{item}}_except_trigger ? 1'b1 : (wr_taken & csr_status_en) ? issue_rf_riuwdata[`{{item_upper}}_ID + 8] : csr_status_reg[`{{item_upper}}_ID + 8]{% endif %};\n",
        ],
        "zero_fill": True,
        "zero_templates": [
            "assign csr_status_nx[{idx}]                = 1'b0;\n",
            "assign csr_status_nx[{idx} + 8]                = 1'b0;\n",
        ],
    },
    "sfenceen": {
        "selector": "iter_items",
        "templates": ["               {% if item == 'csr' %}1'b0{% elif item == 'ldma2' %}1'b0,{% else %}{{item}}_sfence_en,{% endif %}\n"],
        "zero_fill": True,
        "zero_template": "               1'b0,\n",
    },
    "scoreboard": {
        "selector": "iter_items",
        "templates": [
            "assign scoreboard{{'['}}{{id}}{{']'}}               = {% if item == 'csr' %}(ip_rf_status_clr[0]) ? 1'b0 : csr_status_reg[0]{% else %}(ip_rf_status_clr[`{{item_upper}}_ID]) ? 1'b0 : csr_status_reg[`{{item_upper}}_ID]{% endif %};\n",
        ],
        "zero_fill": True,
        "zero_template": "assign scoreboard[{idx}]               = 1'b0;\n",
    },
    "baseaddrsel": {
        "selector": "iter_dma_items",
        "templates": [
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
        ],
        "extra_context": lambda ctx: {"zero_init": f"{{({ctx['item_upper']}_BASE_ADDR_SELECT_BITWIDTH){{1'd0}}}}"},
    },
}


class ConfigurableWriter(ZeroFillMixin, AlignMixin, SkipMixin, BaseWriter):
    """Generic writer driven entirely by ``WRITER_CONFIG``."""

    def __init__(self, key: str, cfg: dict, dict_lines, outfile):
        super().__init__(outfile, dict_lines)
        self.key = key
        self.cfg = cfg

    # Selection helpers -------------------------------------------------
    def select_rows(self):
        sel = self.cfg.get("selector", "all_rows")
        if sel == "all_rows":
            return list(self.lines)
        return list(getattr(self, sel)())

    def should_skip(self, row):
        item = row.item if isinstance(row, DictRow) else row[0]
        typ = row.type if isinstance(row, DictRow) else None
        if item in self.cfg.get("skip_items", []):
            return True
        if typ and typ in self.cfg.get("skip_types", []):
            return True
        if isinstance(row, DictRow):
            return self.should_skip_item(row)
        return False

    def make_context(self, row, row_id=None):
        if isinstance(row, DictRow):
            ctx = {
                "item": row.item,
                "item_upper": row.item_upper,
                "register": row.register,
                "register_upper": row.register_upper,
                "subregister": row.subregister,
                "subregister_upper": row.subregister_upper,
                "default_value": row.default_value,
                "id": row.id if row_id is None else row_id,
            }
        else:
            item, row_id = row if isinstance(row, tuple) else (row, row_id)
            ctx = {"item": item, "item_upper": item.upper(), "id": row_id}

        if callable(self.cfg.get("extra_context")):
            ctx.update(self.cfg["extra_context"](ctx))
        return ctx

    # Rendering ---------------------------------------------------------
    def render(self):
        rows = self.select_rows()
        templates = self.cfg.get("templates", [])
        zero_fill = self.cfg.get("zero_fill", False)
        zero_templates = self.cfg.get("zero_templates")
        if zero_templates is None:
            zt = self.cfg.get("zero_template")
            zero_templates = [zt] * len(templates) if zt else [None] * len(templates)

        output_lines = []
        for tmpl_idx, tmpl in enumerate(templates):
            prev_id = None
            ztmpl = zero_templates[tmpl_idx]
            for row in rows:
                if isinstance(row, tuple):
                    item, row_id = row
                    cur_row = DictRow(item=item, type="rw", id=row_id)
                elif isinstance(row, DictRow):
                    cur_row = row
                    row_id = row.id
                else:  # plain item name
                    item = row
                    row_id = None
                    cur_row = DictRow(item=item, type="rw", id=row_id)
                if self.should_skip(cur_row):
                    continue
                if zero_fill and ztmpl and prev_id is not None and row_id is not None and prev_id - row_id > 1:
                    self.zero_template = ztmpl
                    output_lines.extend(self.zeros(prev_id, row_id))
                ctx = self.make_context(cur_row, row_id)
                output_lines.append(self.render_template(tmpl, ctx))
                prev_id = row_id

        align_sep = self.cfg.get("align_sep")
        if align_sep:
            return self.align_lines(output_lines, align_sep)
        return output_lines





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
        patterns = {key: re.compile(rf'^// autogen_{key}_start') for key in WRITER_CONFIG}
        writers = {key: ConfigurableWriter(key, cfg, dict_lines, out_fh) for key, cfg in WRITER_CONFIG.items()}
        found = {key: False for key in WRITER_CONFIG}
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
