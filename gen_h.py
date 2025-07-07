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
        return self.seen(f"{self.item_upper}_{self.entry_upper}")

    def render(self):
        for self.item_upper, enum_list in self.iter_enums():
            self.render_buffer_tmp = []
            for self.entry_upper in enum_list:
                if self.skip():
                    continue
                self.render_buffer_tmp.append(f"    ,{self.item_upper}_{self.entry_upper}")

            self.render_buffer.append(f"SMART_ENUM({self.item_upper}\n" + "\n".join(self.render_buffer_tmp) + "\n);\n")

        return self.render_buffer

@register_writer('reg')
class RegWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return self.seen(f"{self.item_upper}_{self.entry_upper}")

    def render(self):
        for self.item_upper, enum_list in self.iter_enums():
            self.render_buffer_tmp = []
            for self.entry_upper in enum_list:
                if self.skip():
                    continue
                self.render_buffer_tmp.append(f"    __IO uint32_t {self.entry_upper.lower()};")

            self.render_buffer.append(
                f"typedef struct andla_{self.item_upper.lower()}_reg_t {{\n"
                + "\n".join(self.render_buffer_tmp)
                + f"\n}} andla_{self.item_upper.lower()}_reg_s;\n"
            )

        return self.render_buffer

@register_writer('base')
class BaseaddrWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

    def render(self):
        for item_lower, item_upper, _ in self.iter_items():
            for row in self.lines:
                self.fetch_terms(row)
                if self.item_lower == item_lower:
                    self.render_buffer.append(f"#define ANDLA_{item_upper}_REG_BASE (ANDLA_REG_BASE + 0x{self.physical_address[-3:]})\n")
                    break
        return self.align_on(self.render_buffer, '(ANDLA_REG_BASE', sep=' (ANDLA_REG_BASE ', strip=True)


@register_writer('dest')
class DestWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

    def render(self):
        self.prev_id = -1
        for _, self.item_upper, self.id in self.iter_items():
            self.emit_zero_gap(self.id, "#define RESERVED_{idx}_DEST (0x1 <<   {idx})\n")
            self.render_buffer.append(f"#define {self.item_upper}_DEST (0x1 <<   {self.id})\n")
        return self.align_on(self.render_buffer, '(0x1', sep=' (0x1 ', strip=True)

@register_writer('item')
class ItemWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

    def render(self):
        self.render_buffer.append("SMART_ENUM(ITEM\n")
        for _, self.item_upper, self.id in self.iter_items(decrease=False):
            self.emit_zero_gap(self.id, "   ,RESERVED_{idx}\n", decrease=False)
            self.render_buffer.append(f"   ,{self.item_upper}\n")
        self.render_buffer.append(");\n")
        return self.render_buffer

@register_writer('devreg')
class DevregWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

    def render(self):
        for self.item_lower, self.item_upper, self.id in self.iter_items(decrease=False):
            self.render_buffer.append(f"#define DEV_ANDLA_{self.item_upper}_REG     ((andla_{self.item_lower}_reg_s*)      ANDLA_{self.item_upper}_REG_BASE  )\n")
        return self.align_on(self.render_buffer, '((andla_', sep='   ((andla_', strip=True)


@register_writer('extreg')
class ExtregWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

    def render(self):
        for self.item_lower, _ , self.id in self.iter_items(decrease=False):
            self.render_buffer.append(
                f"extern andla_{self.item_lower}_reg_s *andla_{self.item_lower}_reg_p;\n"
            )
        return self.align_on(self.render_buffer, '*andla_', sep='   *andla_', strip=True)


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
