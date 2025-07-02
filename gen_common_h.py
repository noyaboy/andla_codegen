import ast

INPUT_FILE = 'input/andla_common.tmp.h'
OUTPUT_FILE = 'output/andla_common.h'
REG_LOG = 'output/regfile_dictionary.log'
TARGET_COL = 82


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


def format_line(prefix, value):
    spaces = max(1, TARGET_COL - len(prefix))
    return prefix + (' ' * spaces) + '= ' + str(value) + ';\n'


def bitwidth_from_loc(loc):
    if loc and isinstance(loc, str):
        import re
        m = re.match(r'\[(\d+):(\d+)\]', loc)
        if m:
            h, l = int(m.group(1)), int(m.group(2))
            return h - l + 1
    return 0


def build_sections(entries):
    reg_lines = []
    item_lines = []

    seen_sub = set()
    for e in entries:
        item = e['Item']
        reg = e['Register']
        sub = e['SubRegister']
        bitloc = e.get('Bit Locate')
        bitwidth = bitwidth_from_loc(bitloc)
        if isinstance(sub, str) and sub not in ('LSB','MSB'):
            key = f"{item}_{reg}"
            if key in seen_sub:
                continue
            seen_sub.add(key)
        final_reg = f"{item}_{reg}" if not isinstance(sub, str) or sub in ('LSB','MSB') else f"{item}_{reg}_{sub}"
        reg_name = final_reg
        reg_lines.append(format_line(f"    reg_file->item[{item}].reg[{reg_name}].bitwidth", bitwidth))
        reg_lines.append(format_line(f"    reg_file->item[{item}].reg[{reg_name}].index", reg_name))
        reg_lines.append("\n")

    seen_item = set()
    for e in entries:
        item = e['Item']
        if item in seen_item:
            continue
        seen_item.add(item)
        low_key = item.lower()
        item_lines.append(format_line(f"    reg_file->item[{item}].id", item))
        item_lines.append(format_line(f"    reg_file->item[{item}].base_addr_ptr", f"andla_{low_key}_reg_p"))
        item_lines.append(format_line(f"    reg_file->item[{item}].reg_num", '0'))
        item_lines.append("\n")

    return reg_lines + item_lines


def generate():
    entries = load_log()
    lines = build_sections(entries)
    with open(INPUT_FILE) as fin, open(OUTPUT_FILE, 'w') as fout:
        in_auto = False
        for line in fin:
            stripped = line.strip()
            if stripped == '// autogen_start':
                fout.write(line)
                in_auto = True
                for l in lines:
                    fout.write(l)
                continue
            if stripped == '// autogen_stop':
                in_auto = False
                fout.write(line)
                continue
            if not in_auto:
                fout.write(line)

if __name__ == '__main__':
    generate()
