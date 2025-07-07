#!/usr/bin/env python3

"""Generate ``andla.h`` using dictionary data and template markers."""

from pathlib import Path
import re

from utils import BaseWriter, WRITER_MAP, load_dictionary_lines, register_writer

# File paths
input_filename = 'input/andla.tmp.h'
output_filename = 'output/andla.h'
dictionary_filename = 'output/regfile_dictionary.log'


########################################################################
# Writer implementations
########################################################################

@register_writer('idx')
class IdxWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

    def render(self):
        current = None
        seen = set()
        buf = []
        for row in self.lines:
            self.fetch_terms(row)

            entry = self.doublet_upper
            if self.subregister_upper in ('MSB', 'LSB'):
                entry += '_' + self.subregister_upper

            if self.item_upper != current:
                if buf:
                    self.render_buffer.append(
                        f"SMART_ENUM({current}\n" + '\n'.join(buf) + '\n);\n'
                    )
                    buf = []
                    seen = set()
                current = self.item_upper

            if entry not in seen:
                buf.append(f"    ,{entry}")
                seen.add(entry)

        if buf:
            self.render_buffer.append(
                f"SMART_ENUM({current}\n" + '\n'.join(buf) + '\n);\n'
            )
        return self.render_buffer


@register_writer('reg')
class RegWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

    def render(self):
        current = None
        seen = set()
        buf = []
        for row in self.lines:
            self.fetch_terms(row)

            entry = self.register_lower
            if self.subregister_lower in ('lsb', 'msb'):
                entry += f"_{self.subregister_lower}"

            if self.item_lower != current:
                if buf:
                    self.render_buffer.append(
                        f"typedef struct andla_{current}_reg_t {{\n" + '\n'.join(buf) + f"\n}} andla_{current}_reg_s;\n"
                    )
                    buf = []
                    seen = set()
                current = self.item_lower

            if entry not in seen:
                buf.append(f"    __IO uint32_t {entry};")
                seen.add(entry)

        if buf:
            self.render_buffer.append(
                f"typedef struct andla_{current}_reg_t {{\n" + '\n'.join(buf) + f"\n}} andla_{current}_reg_s;\n"
            )
        return self.render_buffer


@register_writer('base')
class BaseaddrWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

    def render(self):
        items = sorted(list(self.iter_items()), key=lambda x: x[2])
        for item_lower, item_upper, _ in items:
            for row in self.lines:
                if row.item == item_lower:
                    base = row.raw.get('Physical Address', '')
                    if base:
                        self.render_buffer.append(
                            f"#define ANDLA_{item_upper}_REG_BASE (ANDLA_REG_BASE + 0x{base[-3:]})\n"
                        )
                    break
        return self.render_buffer


@register_writer('dest')
class DestWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

    def render(self):
        items = sorted(list(self.iter_items()), key=lambda x: x[2])
        prev = -1
        for item_lower, item_upper, idx in items:
            if idx - prev > 1 and prev != -1:
                for r in range(prev + 1, idx):
                    self.render_buffer.append(
                        f"#define RESERVED_{r}_DEST               (0x1 <<  {r})\n"
                    )
            self.render_buffer.append(
                f"#define {item_upper}_DEST               (0x1 <<  {idx})\n"
            )
            prev = idx
        return self.render_buffer


@register_writer('item')
class ItemWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

    def render(self):
        items = sorted(list(self.iter_items()), key=lambda x: x[2])
        prev = -1
        self.render_buffer.append("SMART_ENUM(ITEM")
        for item_lower, item_upper, idx in items:
            if idx - prev > 1 and prev != -1:
                for r in range(prev + 1, idx):
                    self.render_buffer.append(f"   ,RESERVED_{r}")
            self.render_buffer.append(f"   ,{item_upper}")
            prev = idx
        self.render_buffer.append(");")
        return [line + "\n" for line in self.render_buffer]


@register_writer('devreg')
class DevregWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

    def render(self):
        for item_lower, item_upper, _ in sorted(self.iter_items(), key=lambda x: x[2]):
            self.render_buffer.append(
                f"#define DEV_ANDLA_{item_upper}_REG     ((andla_{item_lower}_reg_s*)      ANDLA_{item_upper}_REG_BASE  )\n"
            )
        return self.render_buffer


@register_writer('extreg')
class ExtregWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

    def render(self):
        for item_lower, _ , _ in sorted(self.iter_items(), key=lambda x: x[2]):
            self.render_buffer.append(
                f"extern andla_{item_lower}_reg_s        *andla_{item_lower}_reg_p;\n"
            )
        return self.render_buffer


########################################################################
# Main generation workflow
########################################################################

def gen_h():
    with open(input_filename, 'r') as in_fh:
        lines = in_fh.readlines()

    Path(output_filename).parent.mkdir(parents=True, exist_ok=True)

    patterns = {key: re.compile(rf'^//\s*autogen_{key}_start') for key in WRITER_MAP}
    dict_lines = load_dictionary_lines(dictionary_filename)
    writers = {key: cls(None, dict_lines) for key, cls in WRITER_MAP.items()}
    found = {key: False for key in WRITER_MAP}

    with open(output_filename, 'w') as out_fh:
        for key in writers:
            writers[key].outfile = out_fh

        for line in lines:
            out_fh.write(line)
            for key, pattern in patterns.items():
                if not found[key] and pattern.match(line):
                    writers[key].write()
                    found[key] = True


if __name__ == "__main__":
    gen_h()
