#!/usr/bin/env python3
import re

# Define file paths
input_file = 'input/regfile_init.tmp.h'
# my $output_file = '../../../../andes_vip/patterns/andeshape/andla/common/program/andla_common.c';
output_file = 'output/regfile_init.h'
reg_file = 'output/regfile_dictionary.log'

# Open input and output files
with open(input_file, 'r') as in_f, open(output_file, 'w') as out_f:
    # Flag to track if we're between autogen_start and autogen_stop
    in_autogen = False

    # 設定 "=" 的目標對齊位置
    target_equal_pos = 82

    # Function: 將 `=` 之前的字串對齊到 target_equal_pos
    def format_line(prefix, value):
        prefix_length = len(prefix)
        spaces_needed = target_equal_pos - prefix_length
        if spaces_needed < 1:
            spaces_needed = 1  # 確保至少有 1 個空格
        return prefix + (' ' * spaces_needed) + "= " + value + ";\n"

    # Process the input file line by line
    for line in in_f:
        if re.match(r'^//\s*autogen_start\s*$', line):
            # Write the autogen_start line
            out_f.write(line)
            in_autogen = True

            seen_sub = {}

            # Insert contents of regfile_dictionary.log in the new format
            with open(reg_file, 'r') as reg_f:
                for reg_line in reg_f:
                    reg_line = reg_line.rstrip('\n')  # Remove newline
                    # 解析 Python 字典格式
                    data = dict(re.findall(r"'([^']+)': '([^']+)'", reg_line))
                    # 提取必要的字段
                    item = data.get('Item', 'UNKNOWN')
                    register = data.get('Register', 'UNKNOWN')
                    subregister = data.get('SubRegister', 'nan')  # 讀取 SubRegister
                    default = data.get('Default Value')
                    type_ = data.get('Type')

                    index_key = f"{item}_{register}"
                    if index_key not in seen_sub:
                        seen_sub[index_key] = 0

                    # Only process RW types
                    if type_ != 'RW':
                        continue
                    if subregister != 'nan' and subregister not in ('LSB', 'MSB'):
                        if seen_sub[index_key] == 1:
                            continue
                        seen_sub[index_key] = 1

                    # 計算 final_register
                    if subregister == 'nan' or (subregister != 'nan' and subregister not in ('LSB', 'MSB')):
                        final_register = f"{item}_{register}"
                    else:
                        final_register = f"{item}_{register}_{subregister}"

                    # 轉換 item 和 register 為小寫
                    item_lower = item.lower()
                    if subregister == 'nan' or (subregister != 'nan' and subregister not in ('LSB', 'MSB')):
                        register_lower = register.lower()
                    else:
                        register_lower = f"{register}_{subregister}".lower()

                    out_f.write(format_line(f"    regfile->item[{item}].reg[{final_register}].data", default))
        elif in_autogen and re.match(r'^//\s*autogen_stop\s*$', line):
            # Write the autogen_stop line and exit autogen section
            out_f.write(line)
            in_autogen = False
        elif not in_autogen:
            # Write lines outside the autogen section
            out_f.write(line)
