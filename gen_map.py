import ast

INPUT_FILE = 'input/regfile_map.tmp.h'
OUTPUT_FILE = 'output/regfile_map.h'
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


def main():
    entries = parse_entries()
    dest_entries = gen_dest(entries)
    with open(INPUT_FILE) as fin, open(OUTPUT_FILE, 'w') as fout:
        in_dest = False
        for line in fin:
            if line.strip() == '// autogen_dest_start':
                fout.write(line)
                for l in dest_entries:
                    fout.write(l + "\n")
                in_dest = True
            elif in_dest and line.strip() == '// autogen_dest_stop':
                fout.write(line)
                in_dest = False
            elif not in_dest:
                fout.write(line)

if __name__ == '__main__':
    main()
