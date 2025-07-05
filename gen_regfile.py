#!/usr/bin/env python3
# coding: utf-8
"""
generate_andla_regfile.py
使用方法:
    python generate_andla_regfile.py
輸出:
    output/andla_regfile.v   # 與既有檔案逐字一致
"""
import ast
import os
import re
from pathlib import Path
from collections import defaultdict
import pandas as pd

# ---------- 基本路徑 ----------
INPUT_TMP   = Path('input/andla_regfile.tmp.v')
DICT_LOG    = Path('output/regfile_dictionary.log')
OUTPUT_RTL  = Path('output/andla_regfile.v')

# ---------- Writer 基底 ----------
class BaseWriter:
    """所有子 Writer 的共同基底（不含流程控制）"""
    # ↓↓↓ 供各子類覆寫 ↓↓↓
    template: list[str]      = []      # 產生文字樣板
    iter_item: bool          = False   # 逐 Item 迴圈
    iter_register: bool      = False   # 逐 Register 迴圈
    except_keys: list[str]   = []      # 例外排除
    # ↑↑↑ 不要增加流程語法 ↑↑↑

# ---------- 各自動產區段 Writer ----------
class InterruptWriter(BaseWriter):
    template = ['                          ({item_lower}_except & {item_lower}_except_mask) |']
    iter_item = True

class BitwidthWriter(BaseWriter):
    template = ['localparam {reg_upper}_BITWIDTH{suffix:25} = {bitwidth};']
    iter_register = True

class NxWriter(BaseWriter):
    template = [
        'assign {reg_lower}_nx{suffix:47} = '
        '(issue_rf_riuwe && issue_rf_riurwaddr == {index}) ? '
        'issue_rf_riuwdata[{reg_upper}_BITWIDTH-1:0] : {reg_lower}_reg;'
    ]
    iter_register = True

class StatusnxWriter(BaseWriter):
    template = [
        'assign {reg_lower}_nx{suffix:47} = '
        'issue_rf_riuwe ? '
        '((issue_rf_riuwdata[{reg_upper}_BITWIDTH-1:0] & {reg_lower}_we_mask) | '
        '({reg_lower}_reg & ~{reg_lower}_we_mask)) : {reg_lower}_reg;'
    ]
    iter_register = True

class SfenceWriter(BaseWriter):
    template = ['assign {item_lower}_sfence_block = csr_{item_lower}_sfence_reg[0];']
    iter_item = True

# 其餘 Writer 只要仿照上面再加進來即可 …
# class SomethingWriter(BaseWriter): ...

# ---------- GeneralWriter ----------
class GeneralWriter:
    """唯一含流程控制的類別，負責統整輸出"""
    def __init__(self, df: pd.DataFrame):
        self.df = df
        # block 鍵值對應到 writer 類別
        self.block_writer = {
            'interrupt' : InterruptWriter,
            'bitwidth'  : BitwidthWriter,
            'nx'        : NxWriter,
            'statusnx'  : StatusnxWriter,
            'sfence'    : SfenceWriter,
            # '...'      : SomethingWriter,
        }

    # ---- 依區段產生文字 ----
    def render_block(self, block: str) -> str:
        writer_cls = self.block_writer.get(block)
        if writer_cls is None:
            return ''
        tmpl_lines = writer_cls.template
        lines_out  = []

        # 逐 Item
        if writer_cls.iter_item:
            for item in sorted(self.df['Item'].unique()):
                ctx = self._ctx_from_item(item)
                for t in tmpl_lines:
                    lines_out.append(t.format(**ctx))

        # 逐 Register
        elif writer_cls.iter_register:
            for _, row in self.df.iterrows():
                ctx = self._ctx_from_row(row)
                for t in tmpl_lines:
                    lines_out.append(t.format(**ctx))

        # 既非 item 亦非 register，視為靜態樣板
        else:
            lines_out = tmpl_lines.copy()

        return '\n'.join(lines_out)

    # ---- 輔助：由 Item 取得格式化欄位 ----
    def _ctx_from_item(self, item: str) -> dict:
        return {
            'item'       : item,
            'item_lower' : item.lower(),
            'item_upper' : item.upper(),
        }

    # ---- 輔助：由單列 (register) 取得格式化欄位 ----
    def _ctx_from_row(self, row) -> dict:
        bit_lo, bit_hi = 0, 0
        m = re.match(r'\[(\d+):(\d+)\]', str(row['Bit Locate']))
        if m:
            bit_hi, bit_lo = map(int, m.groups())
        bitwidth = bit_hi - bit_lo + 1
        reg       = row['Register']
        suffix    = ''  # 統一做成齊行排版用
        return {
            'item_lower': row['Item'].lower(),
            'reg_lower' : reg.lower(),
            'reg_upper' : reg.upper(),
            'index'     : int(row['Index']),
            'bitwidth'  : bitwidth,
            'suffix'    : suffix,
        }

    # ---- 主函式：組合 tmp.v 與 auto-gen 內容 ----
    def emit(self, tmp_v_path: Path, out_path: Path):
        with tmp_v_path.open() as f_in, out_path.open('w') as f_out:
            inside_block = None
            for line in f_in:
                m_start = re.match(r'\s*//\s*autogen_(\w+)_start', line)
                m_stop  = re.match(r'\s*//\s*autogen_(\w+)_stop',  line)
                # 區段開始
                if m_start:
                    inside_block = m_start.group(1)
                    f_out.write(line)  # keep the start comment
                    f_out.write(self.render_block(inside_block) + '\n')
                    continue
                # 區段結束
                if m_stop:
                    inside_block = None
                f_out.write(line)

# ---------- 將 log 轉成 DataFrame ----------
def parse_log_to_df(log: Path) -> pd.DataFrame:
    records = []
    with log.open() as f:
        for ln in f:
            ln = ln.strip()
            if ln and ln.startswith('{'):
                # 使用 eval 以支援未帶引號的 nan
                rec = eval(ln, {"__builtins__": None, "nan": float('nan')})
                records.append(rec)
    return pd.DataFrame(records)

# ---------- main ----------
def main():
    os.makedirs(OUTPUT_RTL.parent, exist_ok=True)
    df = parse_log_to_df(DICT_LOG)
    writer = GeneralWriter(df)
    writer.emit(INPUT_TMP, OUTPUT_RTL)
    print(f'[OK] 產生 {OUTPUT_RTL}')

if __name__ == '__main__':
    main()
