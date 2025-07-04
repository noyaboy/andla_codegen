#!/usr/bin/env python3
"""Generic register file generator using YAML and Jinja2 templates."""

import re
import math
import yaml
import jinja2
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, Dict, Any

input_filename = 'input/andla_regfile.tmp.v'
output_filename = 'output/andla_regfile.v'
dictionary_filename = 'output/regfile_dictionary.log'
config_filename = 'config/regfile_templates.yml'

def align_pairs(pairs: Iterable[tuple[str, str]], sep: str = ' '):
    pairs = list(pairs)
    if not pairs:
        return ''
    max_len = max(len(left) for left, _ in pairs)
    return "\n".join(f"{left:<{max_len}}{sep}{right}" for left, right in pairs) + "\n"

@dataclass
class DictRow:
    item: str = ''
    register: str = ''
    subregister: str = ''
    type: str = ''
    id: int | None = None
    default_value: str = ''
    raw: Dict[str, Any] | None = None

    @classmethod
    def from_line(cls, line: str) -> "DictRow":
        data = eval(line, {"__builtins__": None, "nan": float('nan')})
        item = str(data.get('Item', '')).lower()
        register = str(data.get('Register', '')).lower()
        sub = data.get('SubRegister')
        if isinstance(sub, float) and math.isnan(sub):
            subreg = ''
        else:
            subreg = str(sub).lower() if sub is not None else ''
        typ = str(data.get('Type', '')).lower()
        _id = data.get('ID')
        if _id is None or (isinstance(_id, float) and math.isnan(_id)):
            parsed_id = None
        else:
            parsed_id = int(_id)
        dv = data.get('Default Value')
        dv_str = '' if dv is None or (isinstance(dv, float) and math.isnan(dv)) else str(dv)
        return cls(item, register, subreg, typ, parsed_id, dv_str, data)

def load_dictionary() -> list[DictRow]:
    with open(dictionary_filename, 'r') as fh:
        rows = [DictRow.from_line(line.rstrip('\n')) for line in fh]
    return [row for row in rows if row.type != 'nan']

def iter_items(rows: Iterable[DictRow]):
    items: Dict[str, int] = {}
    for row in rows:
        if row.item and row.id is not None:
            items[row.item] = row.id
    return sorted(items.items(), key=lambda kv: kv[1], reverse=True)

def iter_dma_items(rows: Iterable[DictRow]):
    result: list[str] = []
    for row in rows:
        item = row.item
        if item and 'dma' in item and item != 'ldma2' and item not in result:
            result.append(item)
    return result

def load_config() -> dict[str, str]:
    with open(config_filename, 'r') as fh:
        cfg = yaml.safe_load(fh)
    return cfg.get('placeholders', {})

def render_template(env: jinja2.Environment, template_path: str, context: dict[str, Any]):
    template = env.get_template(template_path)
    return template.render(context)

def gen_regfile():
    rows = load_dictionary()
    context = {
        'rows': [asdict(r) for r in rows],
        'item_pairs': iter_items(rows),
        'dma_items': iter_dma_items(rows),
        'align': align_pairs,
    }
    templates = load_config()
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('.'),
        keep_trailing_newline=True,
        autoescape=False,
        extensions=['jinja2.ext.do']
    )
    env.filters['align'] = align_pairs

    with open(input_filename, 'r') as in_fh:
        lines = in_fh.readlines()
    Path(output_filename).parent.mkdir(parents=True, exist_ok=True)
    with open(output_filename, 'w') as out_fh:
        for line in lines:
            out_fh.write(line)
            for key, tpl in templates.items():
                if re.match(rf'^// autogen_{key}_start', line):
                    out_fh.write(render_template(env, tpl, context))
                    break

if __name__ == '__main__':
    gen_regfile()
