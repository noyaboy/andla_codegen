#!/usr/bin/env python3
import re

# Define file paths
input_file = 'input/andla_common.tmp.h'
# output_file = '../../../../andes_vip/patterns/andeshape/andla/common/program/andla_common.c'
output_file = 'output/andla_common.h'
reg_file = 'output/regfile_dictionary.log'

# Flag to track if we're between autogen_start and autogen_stop
in_autogen = False

# 用來統計各個 item 出現的次數
item_count = {}

# 設定 "=" 的目標對齊位置
target_equal_pos = 82

# Function: 將 `=` 之前的字串對齊到 target_equal_pos
def format_line(prefix, value):
    prefix_length = len(prefix)
    spaces_needed = target_equal_pos - prefix_length
    if spaces_needed < 1:
        spaces_needed = 1  # 確保至少有 1 個空格
    return f"{prefix}{' ' * spaces_needed}= {value};\n"

def replace_clog2(s):
    def repl(match):
        num = int(match.group(1))
        return str(_calc_clog2(num))
    return re.sub(r'\$clog2\((\d+)\)', repl, s)

# 輔助函數：輸入必是 2 的次方，回傳對應的指數
def _calc_clog2(n):
    if not (n > 0 and (n & (n - 1)) == 0):
        raise ValueError(f"'{n}' 不是 2 的次方！")
    exp = 0
    while n > 1:
        n >>= 1
        exp += 1
    return exp

# 讀取檔案並解析 define
def parse(file1, file2):
    defines = {}
    for fname in (file1, file2):
        with open(fname, 'r') as fh:
            for line in fh:
                m = re.match(r'^`define\s+(\w+)\s+(\d+)\b', line)
                if m:
                    name, val = m.group(1), m.group(2)
                    defines[name] = val
    return defines  # 回傳 dict

# Process the input file line by line
with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
    for line in fin:
        if re.match(r'^//\s*autogen_start\s*$', line):
            # Write the autogen_start line
            fout.write(line)
            in_autogen = True

            seen_sub = {}

            # Insert contents of regfile_dictionary.log in the new format
            with open(reg_file, 'r') as reg:
                for reg_line in reg:
                    reg_line = reg_line.rstrip('\n')

                    # 解析 Python 字典格式
                    data = {k: v for k, v in re.findall(r"'([^']+)': '([^']+)'", reg_line)}

                    # 提取必要的字段
                    item = data.get('Item', 'UNKNOWN')
                    register = data.get('Register', 'UNKNOWN')
                    subregister = data.get('SubRegister', 'nan')  # 讀取 SubRegister
                    index_name = (
                        f"{item}_{register}"
                        if (subregister == 'nan' or (subregister != 'nan' and (subregister != 'LSB' and subregister != 'MSB')))
                        else f"{item}_{register}_{subregister}"
                    )
                    bitwidth = 0

                    if f"{item}_{register}" not in seen_sub:
                        seen_sub[f"{item}_{register}"] = 0

                    if subregister != 'nan' and subregister not in ('LSB', 'MSB'):
                        if seen_sub[f"{item}_{register}"] == 1:
                            continue
                        seen_sub[f"{item}_{register}"] = 1

                    # 計算 Bit Locate 位寬
                    if 'Bit Locate' in data and re.search(r'\[[0-9]+:[0-9]+\]', data['Bit Locate']):
                        high_bit, low_bit = map(int, re.findall(r'\[([0-9]+):([0-9]+)\]', data['Bit Locate'])[0])
                        bitwidth = high_bit - low_bit + 1

                    final_register = (
                        f"{item}_{register}"
                        if (subregister == 'nan' or (subregister != 'nan' and (subregister != 'LSB' and subregister != 'MSB')))
                        else f"{item}_{register}_{subregister}"
                    )

                    # 轉換 `item` 和 `register` 為小寫（雖然後續未使用，但保留以維持與原 Perl 程式相同結構）
                    item_lower = item.lower()
                    register_lower = (
                        register.lower()
                        if (subregister == 'nan' or (subregister != 'nan' and (subregister != 'LSB' and subregister != 'MSB')))
                        else f"{register}_{subregister}".lower()
                    )

                    if 'Bitwidth configuare' in data:
                        if data['Bitwidth configuare'] and data['Bitwidth configuare'][0] in ('`', '$'):
                            # 已經取得的定義
                            defs = parse('./output/andla.vh', './output/andla_config.vh')

                            # 原始字串
                            s = data['Bitwidth configuare']

                            # 先把所有 define key 拼成一個正規表達式
                            keys_rx = '|'.join(map(re.escape, defs.keys()))

                            # 找到首個出現的 key（可帶或不帶前導 `）並做替換
                            def repl_def(m):
                                key = m.group(1)
                                return defs.get(key, m.group(0))
                            s = re.sub(rf'`?({keys_rx})', repl_def, s)
                            s = replace_clog2(s)

                            # 如果整個 s 都是由數字和 + - * / 組成，直接計算出結果
                            if re.match(r'^[\d+\-*\/]+$', s):
                                try:
                                    result = eval(s)
                                    s = str(result)
                                except Exception as e:
                                    raise RuntimeError(f"Invalid expression '{s}': {e}")

                            fout.write(
                                format_line(
                                    f"    reg_file->item[{item}].reg[{final_register}].bitwidth",
                                    s,
                                )
                            )
                        else:
                            fout.write(
                                format_line(
                                    f"    reg_file->item[{item}].reg[{final_register}].bitwidth",
                                    bitwidth,
                                )
                            )
                    else:
                        fout.write(
                            format_line(
                                f"    reg_file->item[{item}].reg[{final_register}].bitwidth",
                                bitwidth,
                            )
                        )

                    fout.write(
                        format_line(
                            f"    reg_file->item[{item}].reg[{final_register}].index",
                            index_name,
                        )
                    )
                    fout.write(
                        format_line(
                            f"    reg_file->item[{item}].reg[{final_register}].phy_addr",
                            f"&(andla_{item_lower}_reg_p->{register_lower})",
                        )
                    )
                    fout.write("\n")

        elif in_autogen and re.match(r'^//\s*autogen_stop\s*$', line):
            seen_item = {}
            with open(reg_file, 'r') as reg:
                for reg_line in reg:
                    data = {k: v for k, v in re.findall(r"'([^']+)': '([^']+)'", reg_line)}
                    item = data.get('Item')
                    if item not in seen_item:
                        seen_item[item] = 0
                    if seen_item[item] == 1:
                        continue
                    seen_item[item] = 1

            for key in seen_item:
                low_key = key.lower()
                fout.write(format_line(f"    reg_file->item[{key}].id", key))
                fout.write(format_line(f"    reg_file->item[{key}].base_addr_ptr", f"andla_{low_key}_reg_p"))
                fout.write(format_line(f"    reg_file->item[{key}].reg_num", "0"))
                fout.write("\n")

            # Write the autogen_stop line and exit autogen section
            fout.write(line)
            in_autogen = False

        elif not in_autogen:
            # Write lines outside the autogen section
            fout.write(line)
