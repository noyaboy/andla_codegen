#!/usr/bin/env python3

from pathlib import Path
import re

from utils import BaseWriter, load_dictionary_lines, register_writer

# File path configuration
log_file_path = "output/regfile_dictionary.log"
template_file_path = "input/andla_regfile_cov.tmp.sv"
output_file_path = "output/andla_regfile_cov.sv"

@register_writer("cov")
class CovWriter(BaseWriter):
    """Writer generating coverpoints for FME0 registers."""

    def skip_rule(self) -> bool:
        if self.item_upper != "FME0":
            return True
        if self.register_upper.endswith("_ADDR_INIT"):
            return False
        return not self.subregister_lower or not self.usecase

    def render(self):  # noqa: D401 - short description from BaseWriter
        for row in self.lines:
            self.fetch_terms(row)
            if self.skip():
                continue

            if 'ADDR_INIT' in self.register_upper:
                self.usecase = "range(0, 2**22)"

            parsed = self._parse_bins_str(self.usecase)
            if isinstance(parsed, tuple):
                self.bins_str = f"[ {parsed[1]} : {parsed[2]} ]"
            elif isinstance(parsed, list):
                self.bins_str = f"{{ {', '.join(map(str, parsed))} }}"

            self.bit_locate = "[21:0]" if 'ADDR_INIT' in self.register_upper else self.bit_locate

            if 'ADDR_INIT' in self.register_upper:
                self.render_buffer.append(f"        {self.item_upper}_{self.register_upper}_CP\n")
            else:
                self.render_buffer.append(f"        {self.item_upper}_{self.register_upper}_{self.subregister_upper}_CP\n")

            self.render_buffer.append(f"        : coverpoint andla_regfile.{self.doublet_lower} {self.bit_locate} {{ bins b[] = {self.bins_str}; }}\n")
            self.render_buffer.append("\n")


        return self.render_buffer


def gen_regfile_cov_sv():
    template_lines = Path(template_file_path).read_text().splitlines(True)
    dict_lines = load_dictionary_lines(log_file_path)
    writer = CovWriter(None, dict_lines)

    Path(output_file_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_file_path, "w") as out_fh:
        for line in template_lines:
            out_fh.write(line)
            if line.strip() == "// auto_gen_fme0":
                writer.outfile = out_fh
                writer.write()


if __name__ == "__main__":  # pragma: no cover
    gen_regfile_cov_sv()
