import ast

INPUT_FILE = 'input/andla_regfile.tmp.v'
OUTPUT_FILE = 'output/andla_regfile.v'
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


def list_ports(entries):
    ports = []
    seen = set()
    for e in entries:
        item = e['Item'].lower()
        reg = e['Register'].lower()
        if (item, reg) in seen:
            continue
        seen.add((item, reg))
        ports.append(f"rf_{item}_{reg}")
    return ports


def generate():
    entries = load_log()
    ports = list_ports(entries)
    with open(INPUT_FILE) as fin, open(OUTPUT_FILE, 'w') as fout:
        in_port = False
        for line in fin:
            stripped = line.strip()
            if stripped == '// autogen_port_start':
                fout.write(line)
                in_port = True
                fout.write(', '.join(ports) + '\n')
                continue
            if stripped == '// autogen_port_stop':
                in_port = False
                fout.write(line)
                continue
            if not in_port:
                fout.write(line)

if __name__ == '__main__':
    generate()
