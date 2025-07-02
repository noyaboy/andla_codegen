"""
╔══════════════════════════════════════════════════════════════════╗
║                         Author Information                       ║
╠══════════════════════════════════════════════════════════════════╣
║ Author      : Hao Chun (Noah) Liang                              ║
║ Affiliation : Bachelor of EE, National Tsing Hua University      ║
║ Position    : CA Group RD-CA-CAA Intern                          ║
║ Email       : science103555@gmail.com                            ║
║ Date        : 2024/12/31 (Tuesday)                               ║
║ Description : Automatic Code Generation for the AnDLA            ║
║               Register File RTL code.                            ║
╚══════════════════════════════════════════════════════════════════╝
"""

import re

input_filename = 'input/andla.tmp.vh'
output_filename = 'output/andla.vh'
dictionary_filename = 'output/regfile_dictionary.log'

class ItemidWriter:
    def __init__(self, dictionary_filename):
# {{{
        self.dictionary_filename = dictionary_filename
        self.lines_to_write = []
        self.seen_pair = set()
# }}}
    def fetch_term(self, line):
# {{{
        match_item = re.search(r"'Item': '([^']*)'", line)
        match_id = re.search(r"'ID'\s*:\s*([0-9]+)", line)
        if match_item:
            item = match_item.group(1)
        else:
            item = None

        if match_id:
            id = match_id.group(1)
        else:
            id = None
        
        return item, id
# }}}
    def _process(self, item, id):
# {{{
        define_line = f"`define {item}_ID  `ANDLA_RF_ID_BITWIDTH'd{id}\n"
        if define_line not in self.lines_to_write:
            self.lines_to_write.append(define_line)
# }}}
    def write_itemid(self, outfile):
# {{{

        with open(self.dictionary_filename, 'r') as dicfile:
            # Read the content of the dictionary file
            content = dicfile.readlines()
        
        current_id = -1
        for line in content:
            item, id = self.fetch_term(line)
            if (int(id) - int(current_id) > 1):
                for i in range (int(current_id) + 1, int(id)):
                    self._process(f"RESERVED_{i}", i)

            current_id = int(id)

                
            self._process(item, id)


        # Write aligned lines with spaces
        for line in self.lines_to_write:
            outfile.write(line)
# }}}

class BitwidthWriter:
    def __init__(self, dictionary_filename):
# {{{
        self.dictionary_filename = dictionary_filename
        self.lines_to_write = []
        self.seen_pair = set()
# }}}
    def fetch_term(self, line):
# {{{
        match_sub = re.search(r"'Item': '([^']*)', 'Register': '([^']*)', 'SubRegister': '([^']*)', .* 'Bit Locate': '\[(\d+):(\d+)\]'", line)
        single_bit_match_sub = re.search(r"'Item': '([^']*)', 'Register': '([^']*)', 'SubRegister': '([^']*)'", line)
        match_re = re.search(r"'Item': '([^']*)', 'Register': '([^']*)', .* 'Bit Locate': '\[(\d+):(\d+)\]'", line)
        single_bit_match_re = re.search(r"'Item': '([^']*)', 'Register': '([^']*)'", line)
        hard_match = re.search(r" 'Bitwidth configuare': '([^']*)'", line)
        if match_sub:
            item = match_sub.group(1)
            register = match_sub.group(2)
            subregister = match_sub.group(3)
            bitwidth = int(match_sub.group(4)) - int(match_sub.group(5)) + 1
        elif single_bit_match_sub:
            item = single_bit_match_sub.group(1)
            register = single_bit_match_sub.group(2)
            subregister = single_bit_match_sub.group(3)
            bitwidth = 1
        elif match_re:
            item = match_re.group(1)
            register = match_re.group(2)
            subregister = None
            bitwidth = int(match_re.group(3)) - int(match_re.group(4)) + 1
        elif single_bit_match_re:
            item = single_bit_match_re.group(1)
            register = single_bit_match_re.group(2)
            subregister = None
            bitwidth = 1
        else:
            item = None
            register = None
            subregister = None
            bitwidth = None


        if hard_match:
            hard = hard_match.group(1)
        else:
            hard = None

        return item, register, subregister, bitwidth, hard
# }}}
    def _process_sub(self, item, register, subregister, bitwidth, hard):
# {{{
        key = (item, register)
        if subregister not in ['LSB', 'MSB'] and key in self.seen_pair:
            return
        self.seen_pair.add(key)

        if hard is not None:
            bitwidth = hard

        if subregister not in ['LSB', 'MSB']:
            define_line = f"`define {item}_{register}_BITWIDTH  {bitwidth}\n"
            self.lines_to_write.append(define_line)
        else:
            define_line = f"`define {item}_{register}_{subregister}_BITWIDTH  {bitwidth}\n"
            self.lines_to_write.append(define_line)
            if subregister == 'MSB':
                define_line = f"`define {item}_{register}_BITWIDTH  `{item}_{register}_LSB_BITWIDTH+`{item}_{register}_MSB_BITWIDTH\n"
                self.lines_to_write.append(define_line)

# }}}
    def _process_re(self, item, register, bitwidth, hard):
# {{{
        if hard is not None:
            bitwidth = hard

        define_line = f"`define {item}_{register}_BITWIDTH  {bitwidth}\n"
        self.lines_to_write.append(define_line)
# }}}
    def write_bitwidth(self, outfile):
# {{{

        with open(self.dictionary_filename, 'r') as dicfile:
            # Read the content of the dictionary file
            content = dicfile.readlines()

        for line in content:
            item, register, subregister, bitwidth, hard = self.fetch_term(line)
            if subregister:
                self._process_sub(item, register, subregister, bitwidth, hard)
            elif register:
                self._process_re(item, register, bitwidth, hard)

        # Find the maximum length of the base part (up to the bitwidth number)
        max_base_length = max(len(line.split('_BITWIDTH  ')[0]) for line in self.lines_to_write)

        # Write aligned lines with spaces
        for line in self.lines_to_write:
            base, bitwidth = line.split('_BITWIDTH  ')
            base_with_bitwidth = f"{base}_BITWIDTH"
            padding_spaces = max_base_length - len(base)  # Calculate required spaces
            formatted_line = f"{base_with_bitwidth}{' ' * padding_spaces} {bitwidth.strip()}\n"
            outfile.write(formatted_line)
# }}}


class IndexWriter:
    def __init__(self, dictionary_filename):
# {{{
        self.dictionary_filename = dictionary_filename
        self.lines_to_write = []
        self.cur_item = None
        self.counter = -1
# }}}
    def extract_item_register_subregister(self, line):
# {{{

        match_idx = re.search(r"'Index'\s*:\s*(\d+)", line)
        if match_idx:
            index = match_idx.group(1)
        else:
            index = None

        match = re.search(r"'Item': '([^']+)', 'Register': '([^']+)', 'SubRegister': '([^']+)'", line)
        if match:
            return match.group(1), match.group(2), match.group(3), index
        match = re.search(r"'Item': '([^']+)', 'Register': '([^']+)'", line)
        if match:
            return match.group(1), match.group(2), None, index
        return None, None, None, None
# }}}
    def should_skip_entry(self, item, register, subregister, seen_pairs):
# {{{
        key = (item, register)
        skip_conditions = [
            subregister not in ['MSB', 'LSB'] and key in seen_pairs,
        ]
        return any(skip_conditions)
# }}}
    def process(self, item, register, subregister, index):
# {{{

        if subregister:
            if subregister not in ['MSB', 'LSB']:
                return f"`define {item}_{register}_IDX `ANDLA_RF_INDEX_BITWIDTH'd{index}\n"
            else:
                return f"`define {item}_{register}_{subregister}_IDX `ANDLA_RF_INDEX_BITWIDTH'd{index}\n"
        else:
            return f"`define {item}_{register}_IDX `ANDLA_RF_INDEX_BITWIDTH'd{index}\n"
# }}}
    def write_file(self, outfile):
# {{{
        # Calculate the position of the second ` in each line
        second_backtick_positions = [
            line.find("`", line.find("`") + 1) for line in self.lines_to_write
        ]
        max_position = max(second_backtick_positions)

        for line, second_pos in zip(self.lines_to_write, second_backtick_positions):

            spaces_needed = max_position - second_pos  # Calculate spaces required
            aligned_line = line[:second_pos] + " " * spaces_needed + line[second_pos:]
            outfile.write(aligned_line)
# }}}
    def write_idx(self, outfile):
# {{{
        with open(self.dictionary_filename, 'r') as dicfile:
            content = dicfile.readlines()
          
        seen_pairs = set()
        for line in content:
            item, register, subregister, index = self.extract_item_register_subregister(line)
            if not item or not register:
                continue
          
            if subregister and self.should_skip_entry(item, register, subregister, seen_pairs):
                  continue
            seen_pairs.add((item, register))

            define_line = self.process(item, register, subregister, index)
            self.lines_to_write.append(define_line)

        self.write_file(outfile)
# }}}

def gen_vh():
# {{{
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()

    # Add markers after the first lines that start with '// autogen_'
    found_itemid = False
    found_bitwidth = False
    found_idx = False

    with open(output_filename, 'w') as outfile:
        for line in lines:
            outfile.write(line)
          
            # Write port information after '// autogen_itemid_start'
            if not found_itemid and line.startswith('// autogen_itemid_start'):
                itemid_writer = ItemidWriter(dictionary_filename)
                itemid_writer.write_itemid(outfile)
                found_itemid  = True
            
            # Write port information after '// autogen_bitwidth_start'
            if not found_bitwidth and line.startswith('// autogen_bitwidth_start'):
                bitwidth_writer = BitwidthWriter(dictionary_filename)
                bitwidth_writer.write_bitwidth(outfile)
                found_bitwidth = True
              
            # Write port information after '// autogen_idx_start'
            if not found_idx and line.startswith('// autogen_idx_start'):
                idx_writer = IndexWriter(dictionary_filename)
                idx_writer.write_idx(outfile)
                found_idx = True
# }}}


if __name__ == '__main__':
    gen_vh()



