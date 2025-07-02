import ast

INPUT_FILE = 'input/andla_regfile.tmp.v'
OUTPUT_FILE = 'output/andla_regfile.v'
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


def unique_items(entries):
    seen = set()
    items = []
    for d in entries:
        item = d['Item']
        if item not in seen:
            seen.add(item)
            items.append((int(d.get('ID',0)), item))
    return sorted(items)


def gen_port(entries):
    ports = []
    seen = set()
    for d in entries:
        item = d['Item'].lower()
        reg = d['Register'].lower()
        typ = str(d.get('Type','')).lower()
        key = f"{item}_{reg}"
        if key in seen:
            continue
        seen.add(key)
        if item == 'csr' and (typ != 'rw' or reg in ['counter','counter_mask','status','control'] or reg.startswith('exram_based_addr')):
            continue
        ports.append(f", rf_{item}_{reg}")
    return ports


def gen_bitwidth(entries):
    lines = []
    seen = set()
    for d in entries:
        item = d['Item'].upper()
        reg = d['Register'].upper()
        sub = d['SubRegister']
        key = (item, reg, sub)
        if key in seen:
            continue
        seen.add(key)
        if sub and sub not in [None,'nan']:
            name = f"{item}_{reg}_{sub}_BITWIDTH"
        else:
            name = f"{item}_{reg}_BITWIDTH"
        lines.append(f"localparam {name} = `{name};")
    return lines


def write_section(lines, start_tag, stop_tag, fout, active):
    if active:
        for l in lines:
            fout.write(l + "\n")


def main():
    entries = parse_entries()
    ports = gen_port(entries)
    bitwidth_lines = gen_bitwidth(entries)
    with open(INPUT_FILE) as fin, open(OUTPUT_FILE,'w') as fout:
        in_port = in_bit = False
        for line in fin:
            if line.strip() == '// autogen_port_start':
                fout.write(line)
                write_section(ports, None, None, fout, True)
                in_port = True
            elif in_port and line.strip() == '// autogen_port_stop':
                fout.write(line)
                in_port = False
            elif line.strip() == '// autogen_bitwidth_start':
                fout.write(line)
                write_section(bitwidth_lines, None, None, fout, True)
                in_bit = True
            elif in_bit and line.strip() == '// autogen_bitwidth_stop':
                fout.write(line)
                in_bit = False
            else:
                if not in_port and not in_bit:
                    fout.write(line)

if __name__ == '__main__':
    main()
