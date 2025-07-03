#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

# Define file paths
input_file = 'input/regfile_map.tmp.h'
# output_file = '../../../../andes_vip/patterns/andeshape/andla/common/program/andla.h'
output_file = 'output/regfile_map.h'
reg_file = 'output/regfile_dictionary.log'

# Open input and output files
try:
    in_fh = open(input_file, 'r')
except IOError as e:
    sys.stderr.write(f"Cannot open {input_file}: {e}\n")
    sys.exit(1)

try:
    out_fh = open(output_file, 'w')
except IOError as e:
    sys.stderr.write(f"Cannot open {output_file}: {e}\n")
    sys.exit(1)

dest_entries = []
buffer_dest = []
seen_entries = {}

# (8) 針對 dest 的部分
try:
    dest_reg = open(reg_file, 'r')
except IOError as e:
    sys.stderr.write(f"Cannot open {reg_file}: {e}\n")
    sys.exit(1)

current_item = ''
dest = None
subdest = None
current_id = 0

for line in dest_reg:
    line = line.rstrip('\n')

    # 只處理同時具有 Item、Register、SubRegister 的行
    m = re.search(
        r"'Item':\s*'(\w+)',\s*'Register':\s*'(\w+)',\s*'SubRegister':\s*(?:'(\w+)'|nan)",
        line,
    )

    if m:
        item, register, subreg = m.group(1), m.group(2), m.group(3)

        # 忽略同一 item 已經處理過的第一筆
        if item in seen_entries:
            continue
        seen_entries[item] = seen_entries.get(item, 0) + 1  # 模擬 $seen_entries{$item}++

        # 取得 ID 欄位
        id_match = re.search(r"'ID':\s*(\d+)", line)
        id_val = int(id_match.group(1)) if id_match else None

        # 如果是新 item，先 flush 掉上一個 item 的 buffer
        if item != current_item:
            if buffer_dest:
                dest_entries.append(
                    f"#define {current_item}_DEST               (0x1 <<  {current_id})\n"
                )
                if (
                    id_val is not None
                    and current_id is not None
                    and id_val - current_id > 1
                ):
                    for idx in range(current_id + 1, id_val):
                        dest_entries.append(
                            f"#define RESERVED_{idx}_DEST               (0x1 <<  {idx})\n"
                        )

                buffer_dest = []

            current_item = item
            seen_entries = {}  # 為下一個 item 重置 duplicate 判斷

            # 現在才抓這個新 item 的第一個 Physical Address
            p_match = re.search(r"'Physical Address':\s*'(\w+)'", line)
            if p_match:
                dest = p_match.group(1)
                subdest = dest[-3:]

        buffer_dest.append(item)
        current_id = id_val

# 迴圈結束後，別忘了把最後一個 item flush 出來
if buffer_dest:
    dest_entries.append(
        f"#define {current_item}_DEST               (0x1 <<  {current_id})\n"
    )

dest_reg.close()

# -------------------------------
# 9 input/andla.tmp.h，將原檔內容與自動生成區段結合
# -------------------------------
in_dest_autogen = 0

for line in in_fh:
    if re.match(r'^//\s*autogen_dest_start\s*$', line):
        out_fh.write(line)
        in_dest_autogen = 1
        for entry in dest_entries:
            out_fh.write(entry)
    elif in_dest_autogen and re.match(r'^//\s*autogen_dest_stop\s*$', line):
        out_fh.write(line)
        in_dest_autogen = 0
    else:
        out_fh.write(line)

# Close filehandles
in_fh.close()
out_fh.close()
