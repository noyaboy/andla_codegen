import ast

INPUT_FILE = 'input/andla.tmp.h'
OUTPUT_FILE = 'output/andla.h'
REG_LOG = 'output/regfile_dictionary.log'


def load_log():
    entries = []
    with open(REG_LOG) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            line = line.replace('nan', 'None')
            entries.append(ast.literal_eval(line))
    return entries


def build_sections(entries):
    idx_entries = []
    reg_entries = []
    base_entries = []
    dest_entries = []
    item_entries = ["SMART_ENUM(ITEM"]
    devreg_entries = []
    extreg_entries = []

    # idx
    current_item = None
    buffer = []
    seen = set()
    for e in entries:
        item = e['Item']
        reg = e['Register']
        sub = e['SubRegister']
        entry = f"{item}_{reg}"
        if isinstance(sub, str) and sub in ('LSB','MSB'):
            entry += f"_{sub}"
        if item != current_item:
            if buffer:
                idx_entries.append(f"SMART_ENUM({current_item}\n" + "\n".join(buffer) + "\n);\n")
                buffer = []
            current_item = item
            seen.clear()
        if entry in seen:
            continue
        seen.add(entry)
        buffer.append(f"    ,{entry}")
    if buffer:
        idx_entries.append(f"SMART_ENUM({current_item}\n" + "\n".join(buffer) + "\n);\n")

    # reg typedefs
    current_item = None
    buffer = []
    seen.clear()
    for e in entries:
        item = e['Item']
        reg = e['Register'].lower()
        sub = e['SubRegister']
        if isinstance(sub, str) and sub in ('LSB','MSB'):
            reg += '_' + sub.lower()
        if item != current_item:
            if buffer:
                item_lc = current_item.lower()
                reg_entries.append(f"typedef struct andla_{item_lc}_reg_t {{\n" + "\n".join(buffer) + f"\n}} andla_{item_lc}_reg_s;\n")
                buffer = []
            current_item = item
            seen.clear()
        if reg in seen:
            continue
        seen.add(reg)
        buffer.append(f"    __IO uint32_t {reg};")
    if buffer:
        item_lc = current_item.lower()
        reg_entries.append(f"typedef struct andla_{item_lc}_reg_t {{\n" + "\n".join(buffer) + f"\n}} andla_{item_lc}_reg_s;\n")

    # base
    seen.clear()
    for e in entries:
        item = e['Item']
        if item in seen:
            continue
        seen.add(item)
        addr = e.get('Physical Address','0')
        sub = addr[-3:]
        base_entries.append(f"#define ANDLA_{item}_REG_BASE (ANDLA_REG_BASE + 0x{sub})\n")

    # item enum & dest
    seen.clear()
    prev_id = None
    for e in entries:
        item = e['Item']
        if item in seen:
            continue
        seen.add(item)
        idv = int(e.get('ID',0))
        if prev_id is not None and idv - prev_id > 1:
            for i in range(prev_id+1, idv):
                item_entries.append(f"   ,RESERVED_{i}")
                dest_entries.append(f"#define RESERVED_{i}_DEST               (0x1 <<  {i})\n")
        item_entries.append(f"   ,{item}")
        dest_entries.append(f"#define {item}_DEST               (0x1 <<  {idv})\n")
        prev_id = idv
    item_entries.append(");\n")

    # devreg/extreg
    seen.clear()
    for e in entries:
        item = e['Item']
        if item in seen:
            continue
        seen.add(item)
        lc = item.lower()
        uc = item.upper()
        devreg_entries.append(f"#define DEV_ANDLA_{uc}_REG     ((andla_{lc}_reg_s*)      ANDLA_{uc}_REG_BASE  )\n")
        extreg_entries.append(f"extern andla_{lc}_reg_s        *andla_{lc}_reg_p;\n")

    return idx_entries, reg_entries, base_entries, dest_entries, item_entries, devreg_entries, extreg_entries


def generate():
    entries = load_log()
    idx_entries, reg_entries, base_entries, dest_entries, item_entries, devreg_entries, extreg_entries = build_sections(entries)

    with open(INPUT_FILE) as fin, open(OUTPUT_FILE, 'w') as fout:
        idx_flag = reg_flag = base_flag = dest_flag = item_flag = False
        dev_flag = ext_flag = False
        for line in fin:
            stripped = line.strip()
            if stripped == '// autogen_idx_start':
                fout.write(line)
                for l in idx_entries:
                    fout.write(l)
                idx_flag = True
                continue
            if stripped == '// autogen_idx_stop':
                idx_flag = False
                fout.write(line)
                continue
            if stripped == '// autogen_reg_start':
                fout.write(line)
                for l in reg_entries:
                    fout.write(l)
                reg_flag = True
                continue
            if stripped == '// autogen_reg_stop':
                reg_flag = False
                fout.write(line)
                continue
            if stripped == '// autogen_base_start':
                fout.write(line)
                for l in base_entries:
                    fout.write(l)
                base_flag = True
                continue
            if stripped == '// autogen_base_stop':
                base_flag = False
                fout.write(line)
                continue
            if stripped == '// autogen_dest_start':
                fout.write(line)
                for l in dest_entries:
                    fout.write(l)
                dest_flag = True
                continue
            if stripped == '// autogen_dest_stop':
                dest_flag = False
                fout.write(line)
                continue
            if stripped == '// autogen_item_start':
                fout.write(line)
                for l in item_entries:
                    fout.write(l + "\n" if not l.endswith('\n') else l)
                item_flag = True
                continue
            if stripped == '// autogen_item_stop':
                item_flag = False
                fout.write(line)
                continue
            if stripped == '// autogen_devreg_start':
                fout.write(line)
                for l in devreg_entries:
                    fout.write(l)
                dev_flag = True
                continue
            if stripped == '// autogen_devreg_stop':
                dev_flag = False
                fout.write(line)
                continue
            if stripped == '// autogen_extreg_start':
                fout.write(line)
                for l in extreg_entries:
                    fout.write(l)
                ext_flag = True
                continue
            if stripped == '// autogen_extreg_stop':
                ext_flag = False
                fout.write(line)
                continue
            if not any([idx_flag, reg_flag, base_flag, dest_flag, item_flag, dev_flag, ext_flag]):
                fout.write(line)

if __name__ == '__main__':
    generate()
