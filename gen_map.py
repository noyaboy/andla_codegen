import ast

INPUT_FILE = 'input/regfile_map.tmp.h'
OUTPUT_FILE = 'output/regfile_map.h'
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


def build_dest(entries):
    dest_entries = []
    seen = set()
    current_id = None
    for e in entries:
        item = e['Item']
        if item in seen:
            continue
        seen.add(item)
        item_id = int(e.get('ID',0))
        if current_id is not None and item_id - current_id > 1:
            for idx in range(current_id+1, item_id):
                dest_entries.append(f"#define RESERVED_{idx}_DEST               (0x1 <<  {idx})\n")
        dest_entries.append(f"#define {item}_DEST               (0x1 <<  {item_id})\n")
        current_id = item_id
    return dest_entries


def generate():
    entries = load_log()
    dest_entries = build_dest(entries)
    with open(INPUT_FILE) as fin, open(OUTPUT_FILE, 'w') as fout:
        in_dest = False
        for line in fin:
            stripped = line.strip()
            if stripped == '// autogen_dest_start':
                fout.write(line)
                in_dest = True
                for d in dest_entries:
                    fout.write(d)
                continue
            if stripped == '// autogen_dest_stop':
                in_dest = False
                fout.write(line)
                continue
            if not in_dest:
                fout.write(line)

if __name__ == '__main__':
    generate()
