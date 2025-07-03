#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

# -------------------------------
# 0. 定義檔案路徑（與 Perl 原碼保持一致）
# -------------------------------
input_file  = 'input/andla.tmp.h'
# output_file = '../../../../andes_vip/patterns/andeshape/andla/common/program/andla.h'
output_file = 'output/andla.h'
reg_file    = 'output/regfile_dictionary.log'

# -------------------------------
# 1. 開啟 input 及 output 檔案
# -------------------------------
try:
    in_fh  = open(input_file,  'r', encoding='utf-8')
except OSError as e:
    sys.exit(f"Cannot open {input_file}: {e}")

try:
    out_fh = open(output_file, 'w', encoding='utf-8')
except OSError as e:
    sys.exit(f"Cannot open {output_file}: {e}")

# -------------------------------
# 1. 解析 regfile_dictionary.log 產生 enum 與 typedef struct 的內容
# -------------------------------

idx_entries     = []
reg_entries     = []
base_entries    = []
dest_entries    = []
item_entries    = []
devreg_entries  = []
extreg_entries  = []

current_item    = ""

buffer_idx      = []
buffer_reg      = []
buffer_base     = []
buffer_dest     = []
buffer_item     = []
buffer_devreg   = []
buffer_extreg   = []

seen_entries    = {}
seen_items      = {}

# -------------------------------
# (1) 針對 enum 的部分
# -------------------------------
try:
    idx_reg_fh = open(reg_file, 'r', encoding='utf-8')
except OSError as e:
    sys.exit(f"Cannot open {reg_file}: {e}")

for line in idx_reg_fh:
    line = line.rstrip('\n')
    m = re.search(r"'Item':\s*'(\w+)',\s*'Register':\s*'(\w+)',\s*'SubRegister':\s*(?:'(\w+)'|nan)", line)
    if m:
        item, register, subreg = m.group(1), m.group(2), m.group(3)
        entry = f"{item}_{register}"

        # 紀錄 item，確保不重複
        seen_items[item] = 1

        # 若 SubRegister 為 LSB 或 MSB，則加上
        if subreg and (subreg == "LSB" or subreg == "MSB"):
            entry += f"_{subreg}"

        # 避免 enum 內部重複
        if entry in seen_entries:
            continue
        seen_entries[entry] = 1

        if item != current_item:
            # 遇到新 item 時，先把前一組輸出
            if buffer_idx:
                idx_entries.append(f"SMART_ENUM({current_item}\n" + "\n".join(buffer_idx) + "\n);\n")
                buffer_idx = []
            current_item = item
            seen_entries = {}   # 清空以免不同 enum 互相影響

        buffer_idx.append(f"    ,{entry}")

# 輸出最後一組
if buffer_idx:
    idx_entries.append(f"SMART_ENUM({current_item}\n" + "\n".join(buffer_idx) + "\n);\n")

idx_reg_fh.close()

# -------------------------------
# (2) 針對 typedef struct 的部分
# -------------------------------
try:
    reg_reg_fh = open(reg_file, 'r', encoding='utf-8')
except OSError as e:
    sys.exit(f"Cannot open {reg_file}: {e}")

seen_entries = {}
current_item = ""
buffer_reg   = []

for line in reg_reg_fh:
    line = line.rstrip('\n')
    m = re.search(r"'Item':\s*'(\w+)',\s*'Register':\s*'(\w+)',\s*'SubRegister':\s*(?:'(\w+)'|nan)", line)
    if m:
        item, register, subreg = m.group(1), m.group(2), m.group(3)
        entry = register.lower()

        if subreg and (subreg == "LSB" or subreg == "MSB"):
            subreg = subreg.lower()
            entry += f"_{subreg}"

        if entry in seen_entries:
            continue
        seen_entries[entry] = 1

        if item != current_item:
            if buffer_reg:
                item_lc = current_item.lower()
                reg_entries.append(f"typedef struct andla_{item_lc}_reg_t {{\n" +
                                   "\n".join(buffer_reg) +
                                   f"\n}} andla_{item_lc}_reg_s;\n")
                buffer_reg = []
            current_item = item
            seen_entries = {}

        buffer_reg.append(f"    __IO uint32_t {entry};")

if buffer_reg:
    item_lc = current_item.lower()
    reg_entries.append(f"typedef struct andla_{item_lc}_reg_t {{\n" +
                       "\n".join(buffer_reg) +
                       f"\n}} andla_{item_lc}_reg_s;\n")

reg_reg_fh.close()

# -------------------------------
# (3) 針對 physical base addr 的部分
# -------------------------------
try:
    base_reg_fh = open(reg_file, 'r', encoding='utf-8')
except OSError as e:
    sys.exit(f"Cannot open {reg_file}: {e}")

current_item = ''
base         = ''
subbase      = ''
buffer_base  = []
seen_entries = {}

for line in base_reg_fh:
    line = line.rstrip('\n')
    m = re.search(r"'Item':\s*'(\w+)',\s*'Register':\s*'(\w+)',\s*'SubRegister':\s*(?:'(\w+)'|nan)", line)
    if m:
        item, register, subreg = m.group(1), m.group(2), m.group(3)

        # 忽略同一 item 已經處理過的第一筆
        if seen_entries.get(item, 0):
            continue
        seen_entries[item] = 1

        # 如果是新 item，先 flush 掉上一個 item 的 buffer
        if item != current_item:
            if buffer_base:
                base_entries.append(f"#define ANDLA_{current_item}_REG_BASE (ANDLA_REG_BASE + 0x{subbase})\n")
                buffer_base = []
            current_item = item
            seen_entries = {}
            # 現在才抓這個新 item 的第一個 Physical Address
            m_ph = re.search(r"'Physical Address':\s*'(\w+)'", line)
            if m_ph:
                base    = m_ph.group(1)
                subbase = base[-3:]

        buffer_base.append(item)

# loop 結束後，別忘了把最後一個 item flush 出來
if buffer_base:
    base_entries.append(f"#define ANDLA_{current_item}_REG_BASE (ANDLA_REG_BASE + 0x{subbase})\n")

base_reg_fh.close()

# -------------------------------
# (5) 針對 item 的部分
# -------------------------------
try:
    item_reg_fh = open(reg_file, 'r', encoding='utf-8')
except OSError as e:
    sys.exit(f"Cannot open {reg_file}: {e}")

seen_entries      = {}
current_item      = ""
current_id_value  = 0
buffer_item       = []
item_entries.append("SMART_ENUM(ITEM\n")

for line in item_reg_fh:
    line = line.rstrip('\n')
    m = re.search(r"'Item':\s*'(\w+)',\s*'Register':\s*'(\w+)',\s*'SubRegister':\s*(?:'(\w+)'|nan)", line)
    if m:
        item, register, subreg = m.group(1), m.group(2), m.group(3)
        entry = register.lower()

        if item in seen_entries:
            continue
        seen_entries[item] = 1

        id_value = None
        m_id = re.search(r"'ID':\s*(\d+)", line)
        if m_id:
            id_value = int(m_id.group(1))

        if item != current_item:
            if buffer_item:
                item_entries.append(f"   ,{current_item}\n")
                if id_value is not None and (id_value - current_id_value) > 1:
                    for i in range(current_id_value + 1, id_value):
                        item_entries.append(f"   ,RESERVED_{i}\n")
                buffer_item = []

            current_id_value = id_value if id_value is not None else current_id_value
            current_item     = item
            seen_entries     = {}

        buffer_item.append(f"    __IO uint32_t {entry};")

if buffer_item:
    item_entries.append(f"   ,{current_item}\n")

item_entries.append(");\n")
item_reg_fh.close()

# -------------------------------
# (6) 針對 devreg 的部分
# -------------------------------
try:
    devreg_reg_fh = open(reg_file, 'r', encoding='utf-8')
except OSError as e:
    sys.exit(f"Cannot open {reg_file}: {e}")

seen_entries    = {}
current_item    = ""
buffer_devreg   = []

for line in devreg_reg_fh:
    line = line.rstrip('\n')
    m = re.search(r"'Item':\s*'(\w+)',\s*'Register':\s*'(\w+)',\s*'SubRegister':\s*(?:'(\w+)'|nan)", line)
    if m:
        item, register, subreg = m.group(1), m.group(2), m.group(3)
        entry = register.lower()

        if item in seen_entries:
            continue
        seen_entries[item] = 1

        if item != current_item:
            if buffer_devreg:
                item_lc = current_item.lower()
                item_uc = current_item.upper()
                devreg_entries.append(f"#define DEV_ANDLA_{item_uc}_REG     ((andla_{item_lc}_reg_s*)      ANDLA_{item_uc}_REG_BASE  )\n")
                buffer_devreg = []
            current_item  = item
            seen_entries  = {}

        buffer_devreg.append(f"    __IO uint32_t {entry};")

if buffer_devreg:
    item_lc = current_item.lower()
    item_uc = current_item.upper()
    devreg_entries.append(f"#define DEV_ANDLA_{item_uc}_REG     ((andla_{item_lc}_reg_s*)      ANDLA_{item_uc}_REG_BASE  )\n")

devreg_reg_fh.close()

# -------------------------------
# (7) 針對 extreg 的部分
# -------------------------------
try:
    extreg_reg_fh = open(reg_file, 'r', encoding='utf-8')
except OSError as e:
    sys.exit(f"Cannot open {reg_file}: {e}")

seen_entries   = {}
current_item   = ""
buffer_extreg  = []

for line in extreg_reg_fh:
    line = line.rstrip('\n')
    m = re.search(r"'Item':\s*'(\w+)',\s*'Register':\s*'(\w+)',\s*'SubRegister':\s*(?:'(\w+)'|nan)", line)
    if m:
        item, register, subreg = m.group(1), m.group(2), m.group(3)
        entry = register.lower()

        if item in seen_entries:
            continue
        seen_entries[item] = 1

        if item != current_item:
            if buffer_extreg:
                item_lc = current_item.lower()
                extreg_entries.append(f"extern andla_{item_lc}_reg_s        *andla_{item_lc}_reg_p;\n")
                buffer_extreg = []
            current_item  = item
            seen_entries  = {}

        buffer_extreg.append(f"    __IO uint32_t {entry};")

if buffer_extreg:
    item_lc = current_item.lower()
    extreg_entries.append(f"extern andla_{item_lc}_reg_s        *andla_{item_lc}_reg_p;\n")

extreg_reg_fh.close()

# -------------------------------
# (8) 針對 dest 的部分
# -------------------------------
try:
    dest_reg_fh = open(reg_file, 'r', encoding='utf-8')
except OSError as e:
    sys.exit(f"Cannot open {reg_file}: {e}")

current_item = ''
dest         = ''
subdest      = ''
buffer_dest  = []
seen_entries = {}
current_id   = 0

for line in dest_reg_fh:
    line = line.rstrip('\n')
    m = re.search(r"'Item':\s*'(\w+)',\s*'Register':\s*'(\w+)',\s*'SubRegister':\s*(?:'(\w+)'|nan)", line)
    if m:
        item, register, subreg = m.group(1), m.group(2), m.group(3)

        # 忽略同一 item 已經處理過的第一筆
        if seen_entries.get(item, 0):
            continue
        seen_entries[item] = seen_entries.get(item, 0) + 1

        id_m = re.search(r"'ID':\s*(\d+)", line)
        id_val = int(id_m.group(1)) if id_m else 0

        # 如果是新 item，先 flush 掉上一個 item 的 buffer
        if item != current_item:
            if buffer_dest:
                dest_entries.append(f"#define {current_item}_DEST               (0x1 <<  {current_id})\n")
                if (id_val - current_id) > 1:
                    for idx in range(current_id + 1, id_val):
                        dest_entries.append(f"#define RESERVED_{idx}_DEST               (0x1 <<  {idx})\n")
                buffer_dest = []
            current_item = item
            seen_entries = {}
            # 現在才抓這個新 item 的第一個 Physical Address
            ph_m = re.search(r"'Physical Address':\s*'(\w+)'", line)
            if ph_m:
                dest    = ph_m.group(1)
                subdest = dest[-3:]

        buffer_dest.append(item)
        current_id = id_val

# loop 結束後，別忘了把最後一個 item flush 出來
if buffer_dest:
    dest_entries.append(f"#define {current_item}_DEST               (0x1 <<  {current_id})\n")

dest_reg_fh.close()

# -------------------------------
# 9. input/andla.tmp.h，將原檔內容與自動生成區段結合
# -------------------------------
in_idx_autogen     = False
in_reg_autogen     = False
in_base_autogen    = False
in_dest_autogen    = False
in_item_autogen    = False
in_devreg_autogen  = False
in_extreg_autogen  = False

for line in in_fh:
    if re.match(r'^//\s*autogen_idx_start\s*$', line):
        out_fh.write(line)
        in_idx_autogen = True
        for entry in idx_entries:
            out_fh.write(f"{entry}\n")
    elif in_idx_autogen and re.match(r'^//\s*autogen_idx_stop\s*$', line):
        out_fh.write(line)
        in_idx_autogen = False

    elif re.match(r'^//\s*autogen_reg_start\s*$', line):
        out_fh.write(line)
        in_reg_autogen = True
        for entry in reg_entries:
            out_fh.write(f"{entry}\n")
    elif in_reg_autogen and re.match(r'^//\s*autogen_reg_stop\s*$', line):
        out_fh.write(line)
        in_reg_autogen = False

    elif re.match(r'^//\s*autogen_base_start\s*$', line):
        out_fh.write(line)
        in_base_autogen = True
        for entry in base_entries:
            out_fh.write(entry)
    elif in_base_autogen and re.match(r'^//\s*autogen_base_stop\s*$', line):
        out_fh.write(line)
        in_base_autogen = False

    elif re.match(r'^//\s*autogen_dest_start\s*$', line):
        out_fh.write(line)
        in_dest_autogen = True
        for entry in dest_entries:
            out_fh.write(entry)
    elif in_dest_autogen and re.match(r'^//\s*autogen_dest_stop\s*$', line):
        out_fh.write(line)
        in_dest_autogen = False

    elif re.match(r'^//\s*autogen_item_start\s*$', line):
        out_fh.write(line)
        in_item_autogen = True
        for entry in item_entries:
            out_fh.write(entry)
    elif in_item_autogen and re.match(r'^//\s*autogen_item_stop\s*$', line):
        out_fh.write(line)
        in_item_autogen = False

    elif re.match(r'^//\s*autogen_devreg_start\s*$', line):
        out_fh.write(line)
        in_devreg_autogen = True
        for entry in devreg_entries:
            out_fh.write(entry)
    elif in_devreg_autogen and re.match(r'^//\s*autogen_devreg_stop\s*$', line):
        out_fh.write(line)
        in_devreg_autogen = False

    elif re.match(r'^//\s*autogen_extreg_start\s*$', line):
        out_fh.write(line)
        in_extreg_autogen = True
        for entry in extreg_entries:
            out_fh.write(entry)
    elif in_extreg_autogen and re.match(r'^//\s*autogen_extreg_stop\s*$', line):
        out_fh.write(line)
        in_extreg_autogen = False

    else:
        out_fh.write(line)

# -------------------------------
# 10. 關閉所有檔案
# -------------------------------
in_fh.close()
out_fh.close()
