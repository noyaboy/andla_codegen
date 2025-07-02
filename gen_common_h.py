import ast

INPUT_FILE = 'input/andla_common.tmp.h'
OUTPUT_FILE = 'output/andla_common.h'
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


def bitwidth_from_loc(loc):
    if not loc:
        return 0
    if '[' in loc and ':' in loc:
        loc = loc.split('~')[0].strip()
        hi, lo = loc.strip('[]').split(':')
        return int(hi) - int(lo) + 1
    return 1


def gen_lines(entries):
    lines = []
    for d in entries:
        item = d['Item']
        reg = d['Register']
        sub = d['SubRegister']
        idx_name = f"{item}_{reg}"
        if sub and sub not in [None, 'nan'] and sub not in ['LSB','MSB']:
            idx_name = f"{item}_{reg}_{sub}"
        bitwidth = bitwidth_from_loc(d.get('Bit Locate'))
        lines.append(f"    reg_file->item[{item}].reg[{idx_name}].bitwidth\n  = {bitwidth};")
        lines.append(f"    reg_file->item[{item}].reg[{idx_name}].index\n  = {idx_name};\n")
    return lines


def gen_item_init(entries):
    seen = set()
    lines = []
    for d in entries:
        item = d['Item']
        if item in seen:
            continue
        seen.add(item)
        lines.append(f"    reg_file->item[{item}].id\n  = {item};")
        lc = item.lower()
        lines.append(f"    reg_file->item[{item}].base_addr_ptr\n  = andla_{lc}_reg_p;")
        lines.append(f"    reg_file->item[{item}].reg_num\n  = 0;\n")
    return lines


def main():
    entries = parse_entries()
    auto_lines = gen_lines(entries)
    item_lines = gen_item_init(entries)

    with open(INPUT_FILE) as fin, open(OUTPUT_FILE,'w') as fout:
        in_auto = False
        for line in fin:
            if line.strip() == '// autogen_start':
                fout.write(line)
                for l in auto_lines:
                    fout.write(l + "\n")
                in_auto = True
            elif in_auto and line.strip() == '// autogen_stop':
                for l in item_lines:
                    fout.write(l + "\n")
                fout.write(line)
                in_auto = False
            elif not in_auto:
                fout.write(line)

if __name__ == '__main__':
    main()
