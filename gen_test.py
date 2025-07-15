#!/usr/bin/env python3

"""Generate ``andla.h`` using dictionary data and template markers."""

from pathlib import Path
import re

from utils import BaseWriter, WRITER_MAP, load_dictionary_lines, register_writer

# File paths
input_filename = 'input/test.tmp.log'
output_filename = 'output/test.log'
dictionary_filename = 'output/regfile_dictionary.log'


########################################################################
# Writer implementations
########################################################################

# @register_writer('test')
# class TestWriter(BaseWriter):
#     def skip_rule(self) -> bool:
#         # return not self.item_upper == 'SDMA'
#         return False
#         # return self.seen(f"{self.item_lower}_{self.register_lower}")
#         # return self.seen(f"{self.item_lower}_{self.register_lower}") and self.subregister_upper not in ['LSB', 'MSB']

#     def render(self):
#         for row in self.lines:
#             self.fetch_terms(row)
#             if self.skip():
#                 continue
#             self.render_buffer.append(f"Item = {self.item_lower}, Register = {self.register_lower}, Subregister = {self.subregister_lower}\n")
#             self.render_buffer.append(f"ID = {self.id}, Index = {self.index}, Bit Locate = {self.bit_locate}, Type = {self.typ}, Physical Address = {self.physical_address}\n")
#             self.render_buffer.append(f"Usecase = {self.usecase}, Default Value = {self.default_value}, Bitwidth Configure = {self.bitwidth_configuare}\n")
#             self.render_buffer.append(f"Usecase Size = {self.usecase_size}, Usecase Set = {self.usecase_set}\n")
#             self.render_buffer.append(f"Enumeration = {self.enumeration}\n\n")
#         return self.render_buffer

@register_writer('test')
class TestWriter(BaseWriter):
    def skip_rule(self) -> bool:
        return False

    def render(self):
        self.prev_id = -1
        for self.item_lower, self.item_upper, self.id in self.iter_items():
            self.emit_zero_gap(self.id, "RESERVED_{idx} = {idx}\n")
            self.render_buffer.append(f"{self.item_upper} = {self.id}\n")
        # return self.render_buffer
        return self.align_on(self.render_buffer, ' = ', sep=' = ', strip=True)

# @register_writer('test')
# class TestWriter(BaseWriter):
#     def skip_rule(self) -> bool:
#         return False
#         # return self.item_upper != 'SDMA'

#     def render(self):
#         for self.item_upper, enum_list in self.iter_enums():
#             self.render_buffer_tmp = []
#             for self.entry_upper in enum_list:
#                 if self.skip():
#                     continue
#                 self.render_buffer_tmp.append(f"    ,{self.item_upper}_{self.entry_upper}\n")

#             if self.skip():
#                 continue
#             self.render_buffer.append(f"{self.item_upper} (\n")
#             self.render_buffer.extend(self.render_buffer_tmp)
#             self.render_buffer.append(f");\n")

#         return self.render_buffer


# @register_writer('test')
# class TestWriter(BaseWriter):
#     def skip_rule(self) -> bool:
#         return not self.enumeration_dict

#     def render(self):
#         for row in self.lines:
#             self.fetch_terms(row)
#             if self.skip():
#                 continue

#             self.render_buffer.append(f"\n{self.item_upper}, {self.register_upper}: \n")
            
#             for key, name in self.enumeration_dict.items():
#                 self.render_buffer.append(f"value = {key}, meaning = {name}\n")

#         return self.render_buffer

########################################################################
# Main generation workflow
########################################################################

def gen_h():
    with open(input_filename, 'r') as in_fh:
        lines = in_fh.readlines()

    patterns = {key: re.compile(rf'^//\s*autogen_{key}_start') for key in WRITER_MAP}

    dict_lines = load_dictionary_lines(dictionary_filename)
    # dict_lines = load_dictionary_lines(dictionary_filename, c_code=True)

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
