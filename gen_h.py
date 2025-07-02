import ast
from collections import OrderedDict

INPUT_FILE = 'input/andla.tmp.h'
OUTPUT_FILE = 'output/andla.h'
REG_FILE = 'output/regfile_dictionary.log'


def parse_entries():
    entries = []
    with open(REG_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            processed = line.replace(': nan', ': None')
            entries.append(ast.literal_eval(processed))
    return entries


def gen_idx(entries):
    idx_entries = []
    current_item = None
    buffer = []
    seen = set()
    for d in entries:
        item = d.get('Item')
        reg = d.get('Register')
        sub = d.get('SubRegister')
        entry = f"{item}_{reg}"
        if sub in ('LSB', 'MSB'):
            entry += f"_{sub}"
        if item != current_item:
            if buffer:
                idx_entries.append("SMART_ENUM(" + current_item + "\n" + "\n".join(buffer) + "\n);")
                buffer = []
            current_item = item
            seen = set()
        if entry in seen:
            continue
        seen.add(entry)
        buffer.append(f"    ,{entry}")
    if buffer:
        idx_entries.append("SMART_ENUM(" + current_item + "\n" + "\n".join(buffer) + "\n);")
    return idx_entries


def gen_reg(entries):
    reg_entries = []
    current_item = None
    buffer = []
    seen = set()
    for d in entries:
        item = d['Item']
        reg = d['Register']
        sub = d['SubRegister']
        name = reg.lower()
        if sub in ('LSB', 'MSB'):
            name += '_' + sub.lower()
        key = (item, name)
        if item != current_item:
            if buffer:
                item_lc = current_item.lower()
                reg_entries.append(f"typedef struct andla_{item_lc}_reg_t {{\n" + "\n".join(buffer) + f"\n}} andla_{item_lc}_reg_s;")
                buffer = []
            current_item = item
            seen = set()
        if name in seen:
            continue
        seen.add(name)
        buffer.append(f"    __IO uint32_t {name};")
    if buffer:
        item_lc = current_item.lower()
        reg_entries.append(f"typedef struct andla_{item_lc}_reg_t {{\n" + "\n".join(buffer) + f"\n}} andla_{item_lc}_reg_s;")
    return reg_entries


def gen_base(entries):
    base_entries = []
    seen = set()
    for d in entries:
        item = d['Item']
        if item in seen:
            continue
        seen.add(item)
        base = d.get('Physical Address', '0')
        subbase = base[-3:]
        base_entries.append(f"#define ANDLA_{item}_REG_BASE (ANDLA_REG_BASE + 0x{subbase})")
    return base_entries


def gen_dest(entries):
    dest_entries = []
    item_ids = []
    seen = set()
    for d in entries:
        item = d['Item']
        if item in seen:
            continue
        seen.add(item)
        item_ids.append((int(d.get('ID',0)), item))
    item_ids.sort()
    current_id = -1
    for id_val, item in item_ids:
        while current_id + 1 < id_val:
            current_id += 1
            dest_entries.append(f"#define RESERVED_{current_id}_DEST               (0x1 <<  {current_id})")
        dest_entries.append(f"#define {item}_DEST               (0x1 <<  {id_val})")
        current_id = id_val
    return dest_entries


def gen_item_enum(entries):
    item_ids = []
    seen = set()
    for d in entries:
        item = d['Item']
        if item in seen:
            continue
        seen.add(item)
        item_ids.append((int(d.get('ID',0)), item))
    item_ids.sort()
    lines = ["SMART_ENUM(ITEM"]
    current_id = -1
    for id_val, item in item_ids:
        while current_id + 1 < id_val:
            current_id += 1
            lines.append(f"   ,RESERVED_{current_id}")
        lines.append(f"   ,{item}")
        current_id = id_val
    lines.append(");")
    return lines


def gen_devreg(entries):
    dev_entries = []
    seen = set()
    for d in entries:
        item = d['Item']
        if item in seen:
            continue
        seen.add(item)
        lc = item.lower()
        dev_entries.append(f"#define DEV_ANDLA_{item}_REG     ((andla_{lc}_reg_s*)      ANDLA_{item}_REG_BASE  )")
    return dev_entries


def gen_extreg(entries):
    ext_entries = []
    seen = set()
    for d in entries:
        item = d['Item']
        if item in seen:
            continue
        seen.add(item)
        lc = item.lower()
        ext_entries.append(f"extern andla_{lc}_reg_s        *andla_{lc}_reg_p;")
    return ext_entries


def main():
    entries = parse_entries()
    idx_entries = gen_idx(entries)
    reg_entries = gen_reg(entries)
    base_entries = gen_base(entries)
    dest_entries = gen_dest(entries)
    item_entries = gen_item_enum(entries)
    devreg_entries = gen_devreg(entries)
    extreg_entries = gen_extreg(entries)

    with open(INPUT_FILE) as fin, open(OUTPUT_FILE, 'w') as fout:
        in_idx = in_reg = in_base = in_dest = in_item = in_dev = in_ext = False
        for line in fin:
            if line.strip() == '// autogen_idx_start':
                fout.write(line)
                for l in idx_entries:
                    fout.write(l + "\n")
                in_idx = True
            elif in_idx and line.strip() == '// autogen_idx_stop':
                fout.write(line)
                in_idx = False
            elif line.strip() == '// autogen_reg_start':
                fout.write(line)
                for l in reg_entries:
                    fout.write(l + "\n")
                in_reg = True
            elif in_reg and line.strip() == '// autogen_reg_stop':
                fout.write(line)
                in_reg = False
            elif line.strip() == '// autogen_base_start':
                fout.write(line)
                for l in base_entries:
                    fout.write(l + "\n")
                in_base = True
            elif in_base and line.strip() == '// autogen_base_stop':
                fout.write(line)
                in_base = False
            elif line.strip() == '// autogen_dest_start':
                fout.write(line)
                for l in dest_entries:
                    fout.write(l + "\n")
                in_dest = True
            elif in_dest and line.strip() == '// autogen_dest_stop':
                fout.write(line)
                in_dest = False
            elif line.strip() == '// autogen_item_start':
                fout.write(line)
                for l in item_entries:
                    fout.write(l + "\n")
                in_item = True
            elif in_item and line.strip() == '// autogen_item_stop':
                fout.write(line)
                in_item = False
            elif line.strip() == '// autogen_devreg_start':
                fout.write(line)
                for l in devreg_entries:
                    fout.write(l + "\n")
                in_dev = True
            elif in_dev and line.strip() == '// autogen_devreg_stop':
                fout.write(line)
                in_dev = False
            elif line.strip() == '// autogen_extreg_start':
                fout.write(line)
                for l in extreg_entries:
                    fout.write(l + "\n")
                in_ext = True
            elif in_ext and line.strip() == '// autogen_extreg_stop':
                fout.write(line)
                in_ext = False
            else:
                if not any([in_idx, in_reg, in_base, in_dest, in_item, in_dev, in_ext]):
                    fout.write(line)
    
if __name__ == '__main__':
    main()
