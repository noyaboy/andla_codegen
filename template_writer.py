from typing import Iterable, Dict
from jinja2 import Template


class TemplateWriter:
    """Base writer using Jinja2 templates for output generation."""

    template_file: str = ""

    def __init__(self, outfile, dict_lines):
        self.outfile = outfile
        self.lines = dict_lines
        self._template_cache: Template | None = None

    def load_template(self) -> Template:
        if self._template_cache is None:
            with open(self.template_file, "r") as f:
                self._template_cache = Template(f.read())
        return self._template_cache

    # ---- Hooks to override ----
    def records(self) -> Iterable[Dict[str, str]]:
        for line in self.lines:
            yield {}

    def prepare_context(self, record: Dict[str, str]) -> Dict[str, str]:
        return record

    def postprocess(self, lines: Iterable[str]) -> Iterable[str]:
        return lines

    # ---------------------------

    def write(self):
        template = self.load_template()
        rendered_lines = [template.render(**self.prepare_context(r)) for r in self.records()]
        for line in self.postprocess(rendered_lines):
            self.outfile.write(line)
