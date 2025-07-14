#!/usr/bin/env python3
"""Utility functions and helpers for code generation."""

import ast
import math
import re
from dataclasses import dataclass
from typing import Callable

# Registry of writer name to class mappings.
WRITER_MAP: dict[str, type] = {}

@dataclass
class DictRow:
    """Normalized representation of a dictionary log entry."""

    item: str = ''
    register: str = ''
    subregister: str = ''
    type: str = ''
    id: int | None = None
    default_value: str = ''
    description: str = ''
    enumeration: str = ''
    index: str = ''
    bit_locate: str = ''
    physical_address: str = ''
    bitwidth_configuare: str = ''
    min_val: str = ''
    max_val: str = ''
    usecase: str = ''
    constraint: str = ''
    raw: dict | None = None

    @staticmethod
    def _normalize_str(value, *, lower: bool = True) -> str:
        """Return a string with NaN/``None`` converted to ``''``."""

        if value is None or (isinstance(value, float) and math.isnan(value)):
            return ''
        result = str(value)
        return result.lower() if lower else result

    @staticmethod
    def _normalize_int(value) -> int | None:
        """Return ``None`` when ``value`` is NaN/``None`` otherwise ``int``."""

        if value is None or (isinstance(value, float) and math.isnan(value)):
            return None
        return int(value)

    @classmethod
    def from_line(cls, line: str) -> "DictRow":
        """Parse a log line into a ``DictRow`` instance."""

        safe_line = re.sub(r':\s*nan\b(\s*[,}])', r': None\1', line)
        safe_line = re.sub(r':\s*nan\s*$', ': None', safe_line)
        data = ast.literal_eval(safe_line)
        return cls(
            cls._normalize_str(data.get('Item')),
            cls._normalize_str(data.get('Register')),
            cls._normalize_str(data.get('SubRegister')),
            cls._normalize_str(data.get('Type')),
            cls._normalize_int(data.get('ID')),
            cls._normalize_str(data.get('Default Value'), lower=False),
            data.get('Description'),
            data.get('Enumeration'),
            cls._normalize_str(data.get('Index')),
            cls._normalize_str(data.get('Bit Locate')),
            data.get('Physical Address'), # Maintain original case
            data.get('Bitwidth configuare'), # Maintain original case
            cls._normalize_str(data.get('Min')),
            cls._normalize_str(data.get('Max')),
            cls._normalize_str(data.get('Usecase')),
            cls._normalize_str(data.get('Constraint')),
            data,
        )


def load_dictionary_lines(dictionary_filename: str, c_code: bool = False):
    """Read dictionary file and parse each line into :class:`DictRow` objects."""

    with open(dictionary_filename, 'r') as dict_fh:
        rows = [DictRow.from_line(line.rstrip('\n')) for line in dict_fh]

    return [row for row in rows if (row.type != '' or c_code is True)]


def register_writer(name: str) -> Callable[[type], type]:
    """Class decorator used to register ``BaseWriter`` subclasses."""

    def decorator(cls: type) -> type:
        WRITER_MAP[name] = cls
        return cls

    return decorator


class BaseWriter:
    """Generic writer implementing the data-to-template-to-output flow.

    Provides helpers for column retrieval, item ordering, and DMA item
    filtering used by the various writer subclasses.
    """

    def __init__(self, outfile, dict_lines):
        self.outfile = outfile
        self.lines = dict_lines
        # shared state for subclasses
        self.seen_set                   = {}
        self.render_buffer              = []
        self.render_buffer_tmp          = []
        self.render_buffer_regdef       = []
        self.render_buffer_regfield     = []
        self.item_lower                 = ''
        self.register_lower             = ''
        self.subregister_lower          = ''
        self.doublet_lower              = ''
        self.triplet_lower              = ''
        self.item_upper                 = ''
        self.register_upper             = ''
        self.subregister_upper          = ''
        self.doublet_upper              = ''
        self.triplet_upper              = ''
        self.doublet_lower              = ''
        self.triplet_lower              = ''
        self.id                         = ''
        self.typ                        = ''
        self.default_value              = ''
        self.index                      = ''
        self.bit_locate                 = ''
        self.physical_address           = ''
        self.bitwidth_configuare        = ''
        self.min_val                    = ''
        self.max_val                    = ''
        self.usecase                    = ''
        self.constraint                 = ''
        self.seq_default_value          = ''
        self.seq_default_value_width    = ''
        self.prev_id                    = None
        self.entry_upper                = None
        self.entry_lower                = None
        self.bitwidth                   = ''
        self.usecase_size               = 0
        self.usecase_set                = "{}"
        self.bins_str                   = ''
        self.description                = ''
        self.enumeration                = ''

    # subclasses override ``skip_rule`` to implement per-writer logic.  The
    # ``skip`` method simply delegates to that hook.

    def seen(self, key):
        """Return True if ``key`` has been seen; otherwise mark it."""
        if key in self.seen_set:
            return True
        self.seen_set[key] = 1
        return False

    def skip(self) -> bool:
        """Return ``True`` when ``skip_rule`` signals to skip the current row."""
        return self.skip_rule()

    def skip_rule(self) -> bool:  # pragma: no cover - interface method
        """Per-writer skip logic. Subclasses MUST override."""
        raise NotImplementedError

    def render(self):  # pragma: no cover - interface method
        """Return an iterable of strings for the output file."""
        raise NotImplementedError

    def write(self):
        """Write each line produced by ``render`` to ``outfile``."""
        for line in self.render():
            self.outfile.write(line)

    def get_columns(self, row: DictRow, columns):
        """Extract fields from ``row`` and return those with values."""
        result = {}
        for col in columns:
            attr = col.lower().replace(' ', '_')
            if hasattr(row, attr):
                val = getattr(row, attr)
                if val is not None:
                    result[col] = val
        return result

    def _replace_clog2(self, expr: str) -> str:
        """Replace ``$clog2(<num>)`` with its value."""

        def repl(match: re.Match) -> str:
            num = int(match.group(1))
            if num <= 0 or num & (num - 1):
                raise ValueError(f"'{num}' \u4e0d\u662f 2 \u7684\u6b21\u65b9!")
            return str(num.bit_length() - 1)

        return re.sub(r"\$clog2\((\d+)\)", repl, expr)


    def _parse_defines(self, *files: str) -> dict[str, str]:
        defines: dict[str, str] = {}
        for fname in files:
            with open(fname, "r") as fh:
                for line in fh:
                    m = re.match(r"^`define\s+(\w+)\s+(\d+)\b", line)
                    if m:
                        defines[m.group(1)] = m.group(2)
        return defines

    def _calc_bitwidth(self) -> str:
        """Return the bitwidth string for the current row."""

        if self.bitwidth_configuare:
            expr = self.bitwidth_configuare
            if expr and expr[0] in ("`", "$"):
                defs = self._parse_defines("./output/andla.vh", "./output/andla_config.vh")
                keys_rx = "|".join(map(re.escape, defs.keys()))

                if keys_rx:
                    expr = re.sub(rf"`?({keys_rx})", lambda m: defs.get(m.group(1), m.group(0)), expr)

                expr = self._replace_clog2(expr)

                if re.fullmatch(r"[\d+\-*/]+", expr):
                    expr = str(eval(expr))  # nosec - controlled content

            return expr

        if re.search(r"\[[0-9]+:[0-9]+\]", self.bit_locate):
            hi, lo = map(int, re.findall(r"\[([0-9]+):([0-9]+)\]", self.bit_locate)[0])
            return str(hi - lo + 1)

        return "0"

    def iter_items(self, *, dma_only: bool = False, sfence_only: bool = False, decrease: bool = True):
        """Iterate over dictionary items with optional filters."""
        items = {}
        for row in self.lines:
            if dma_only and not (
                row.item and "dma" in row.item and row.item != "ldma2"
            ):
                continue
            if sfence_only and row.register != "sfence":
                continue

            item = row.item
            _id = row.id
            if item and _id is not None:
                items[item] = _id

        for key in sorted(items, key=items.get, reverse=decrease):
            yield key, key.upper(), items[key]

    def iter_enums(self):
        mapping = {}
        for row in self.lines:
            self.fetch_terms(row)
            if self.subregister_upper in ('MSB', 'LSB'):
                mapping.setdefault(self.item_upper, []).append(f"{self.register_upper}_{self.subregister_upper}")
            else:
                mapping.setdefault(self.item_upper, []).append(f"{self.register_upper}")

        return mapping.items()

    def fetch_terms(self, row: DictRow, update_bins = False):
        """Populate commonly used case variants from a ``DictRow``."""
        self.item_lower        = row.item
        self.register_lower    = row.register
        self.subregister_lower = row.subregister

        if self.item_lower and self.register_lower:
            self.doublet_lower = f"{self.item_lower}_{self.register_lower}"
        else:
            self.doublet_lower = ''

        if self.item_lower and self.register_lower and self.subregister_lower:
            self.triplet_lower = (
                f"{self.item_lower}_{self.register_lower}_{self.subregister_lower}"
            )
        else:
            self.triplet_lower = ''

        self.item_upper        = self.item_lower.upper() if self.item_lower else ''
        self.register_upper    = self.register_lower.upper() if self.register_lower else ''
        self.subregister_upper = self.subregister_lower.upper() if self.subregister_lower else ''

        self.doublet_upper = f"{self.item_upper}_{self.register_upper}"
        self.doublet_lower = f"{self.item_lower}_{self.register_lower}"

        if self.subregister_upper:
            self.triplet_upper = (f"{self.item_upper}_{self.register_upper}_{self.subregister_upper}")
            self.triplet_lower = (f"{self.item_lower}_{self.register_lower}_{self.subregister_lower}")
        else:
            self.triplet_upper = ''
            self.triplet_lower = ''

        self.id                     = row.id
        self.typ                    = row.type
        self.default_value          = row.default_value
        self.index                  = row.index
        self.bit_locate             = row.bit_locate
        self.physical_address       = row.physical_address
        self.bitwidth_configuare    = row.bitwidth_configuare
        self.min_val                = row.min_val
        self.max_val                = row.max_val
        self.usecase                = row.usecase
        self.constraint             = row.constraint

        if not self.default_value.startswith('0x') and self.typ != '':
            self.seq_default_value_width = int(row.default_value).bit_length() or 1

        if self.default_value.startswith('0x'):
            self.seq_default_value = self.default_value.replace('0x', "32'h")
        elif self.subregister_lower in ('msb','lsb'):
            self.seq_default_value = f"{{ {{({self.triplet_upper}_BITWIDTH-{self.seq_default_value_width}){{1'd0}}}}, {self.seq_default_value_width}'d{self.default_value} }}"
        else:
            self.seq_default_value = f"{{ {{({self.doublet_upper}_BITWIDTH-{self.seq_default_value_width}){{1'd0}}}}, {self.seq_default_value_width}'d{self.default_value} }}"

        if self.bitwidth_configuare:
            self.bitwidth = self.bitwidth_configuare
        else:
            if ':' in self.bit_locate and '~' not in self.bit_locate:
                hi, lo = map(int, self.bit_locate.strip('[]').split(':'))
                self.bitwidth = hi - lo + 1
            else:
                self.bitwidth = 1

        if self.subregister_upper and self.subregister_upper in ('MSB', 'LSB'):
            self.entry_upper = f"{self.register_upper}_{self.subregister_upper}"
            self.entry_lower = f"{self.register_lower}_{self.subregister_lower}"
        else:
            self.entry_upper = f"{self.register_upper}"
            self.entry_lower = f"{self.register_lower}"

        range_match = re.match(r"range\s*\(\s*(.*?)\s*,\s*(.*?)\s*\)", self.usecase, re.IGNORECASE)
        list_match = re.match(r"\[(.*)\]", self.usecase)

        self.usecase_size = 0
        self.usecase_set = "{}"
        self.description = row.description
        self.enumeration = row.enumeration

        if range_match:
            count = self._parse_value_expression(range_match.group(2)) - self._parse_value_expression(range_match.group(1))
            if count >= 32:
                self.usecase_size = 3
                self.usecase_set = f"{{0xffffffff, {self._format_c_value_expression(range_match.group(1))}, {self._format_c_value_expression(range_match.group(2))}}}"
            elif count > 0:
                self.usecase_size = len(list(range(self._parse_value_expression(range_match.group(1)), self._parse_value_expression(range_match.group(2)))))
                self.usecase_set = "{" + ",".join(map(str, list(range(self._parse_value_expression(range_match.group(1)), self._parse_value_expression(range_match.group(2)))))) + "}"

        elif list_match:
            list_content = list_match.group(1).strip()

            vals = [int(v) for v in ast.literal_eval(f"[{list_content}]")]
            self.usecase_size = len(vals)
            if self.usecase_size >= 32:
                self.usecase_size = 3
                if vals:
                    self.usecase_set = f"{{0xffffffff, {min(vals)}, {max(vals)}}}"
                else:
                    self.usecase_set = "{0xffffffff, 0, 0}"
            elif self.usecase_size > 0:
                self.usecase_set = "{" + ",".join(map(str, vals)) + "}"

        if update_bins:
            if 'ADDR_INIT' in self.register_upper:
                self.usecase = "range(0, 2**22)"
                self.bit_locate = "[21:0]"

            if isinstance(self._parse_bins_str(self.usecase), tuple):
                self.bins_str = f"[ {self._parse_bins_str(self.usecase)[1]} : {self._parse_bins_str(self.usecase)[2]} ]"
            elif isinstance(self._parse_bins_str(self.usecase), list):
                self.bins_str = f"{{ {', '.join(map(str, self._parse_bins_str(self.usecase)))} }}"

        

    def emit_zero_gap(self, cur_id, template, update=True, decrease=True):
        """If IDs are not contiguous, emit gap lines and update ``prev_id``."""
        if decrease:
            if self.prev_id is not None and self.prev_id - cur_id > 1:
                self.render_buffer.extend(
                    [template.format(idx=idx) for idx in range(self.prev_id - 1, cur_id, -1)]
                )
            if update:
                self.prev_id = cur_id
        else:
            if self.prev_id is not None and cur_id - self.prev_id > 1:
                self.render_buffer.extend(
                    [template.format(idx=idx) for idx in range(self.prev_id + 1, cur_id)]
                )
            if update:
                self.prev_id = cur_id

    def _safe_eval_num(self, num_str: str) -> int:
        """Evaluate ``num_str`` which may contain simple ``**`` expressions."""

        num_str = str(num_str).strip()
        if re.fullmatch(r"\d+", num_str):
            return int(num_str)

        power_match = re.fullmatch(r"(\d+)\s*\*\*\s*(\d+)\s*(-?\s*\d+)?", num_str)
        if power_match:
            base = int(power_match.group(1))
            exp = int(power_match.group(2))
            offset = int(power_match.group(3).replace(" ", "")) if power_match.group(3) else 0
            if exp >= 64:
                raise ValueError(f"Exponent too large in safe_eval_num: {num_str}")
            return base ** exp + offset

        if re.fullmatch(r"0x[0-9a-fA-F]+", num_str):
            return int(num_str, 16)

        return int(num_str)

    def _parse_bins_str(self, usecase_str):
        """Parse ``Usecase`` field and return a list or a ("range", start, end) tuple."""

        usecase_str = str(usecase_str).strip()
        bins_str = None
        start_val = None
        end_val = None

        match = re.fullmatch(r"range\s*\(\s*([^,]+)\s*,\s*([^)]+)\s*\)", usecase_str, re.IGNORECASE)
        if match:
            start = self._safe_eval_num(match.group(1))
            end = self._safe_eval_num(match.group(2))
            if start < end:
                bins_str = list(range(start, end))
                start_val, end_val = start, end - 1
            else:
                bins_str = []
                start_val, end_val = start, end - 1

        if bins_str is None:
            match = re.fullmatch(r"range\s*\[\s*([^,]+)\s*,\s*([^\]]+)\s*\]", usecase_str, re.IGNORECASE)
            if match:
                start = self._safe_eval_num(match.group(1))
                end = self._safe_eval_num(match.group(2))
                if start <= end:
                    bins_str = list(range(start, end + 1))
                    start_val, end_val = start, end
                else:
                    bins_str = []
                    start_val, end_val = start, end

        if bins_str is None:
            match = re.fullmatch(r"([^~]+)\s*~\s*(.+)", usecase_str)
            if match:
                start = self._safe_eval_num(match.group(1))
                end = self._safe_eval_num(match.group(2))
                if start <= end:
                    bins_str = list(range(start, end + 1))
                    start_val, end_val = start, end
                else:
                    bins_str = []
                    start_val, end_val = start, end

        if bins_str is None and usecase_str.startswith("[") and usecase_str.endswith("]"):
            content = usecase_str[1:-1].strip()
            if content:
                vals = [self._safe_eval_num(v.strip()) for v in content.split(",")]
                bins_str = vals
                if len(bins_str) >= 32:
                    start_val, end_val = min(bins_str), max(bins_str)
            else:
                bins_str = []
                start_val = end_val = None

        if bins_str is None and "," in usecase_str and not usecase_str.lower().startswith("range"):
            vals = [self._safe_eval_num(v.strip()) for v in usecase_str.split(",")]
            bins_str = vals
            if len(bins_str) >= 32:
                start_val, end_val = min(bins_str), max(bins_str)

        if bins_str is None:
            val = self._safe_eval_num(usecase_str)
            bins_str = [val]
            start_val = end_val = val

        if len(bins_str) >= 32 and start_val is not None and end_val is not None:
            is_contig = len(bins_str) == end_val - start_val + 1 and set(bins_str) == set(range(start_val, end_val + 1))
            if is_contig:
                return ("range", start_val, end_val)

        return bins_str

    def _parse_value_expression(self, expr: str) -> int:
        if expr.isdigit() or (expr.startswith("-") and expr[1:].isdigit()):
            return int(expr)

        pow_match_alt = re.match(r"(\d+)\s*\*\*\s*(\d+)\s*(-?\s*\d+)?", expr)
        if pow_match_alt:
            base = int(pow_match_alt.group(1))
            exp = int(pow_match_alt.group(2))
            offset = int(pow_match_alt.group(3).replace(" ", "")) if pow_match_alt.group(3) else 0
            return base ** exp + offset

        pow_match = re.match(r"pow\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*(-?\s*\d+)?", expr, re.IGNORECASE)
        if pow_match:
            base = int(pow_match.group(1))
            exp = int(pow_match.group(2))
            offset = int(pow_match.group(3).replace(" ", "")) if pow_match.group(3) else 0
            return base ** exp + offset

        return int(expr)


    def _format_c_value_expression(self, expr: str) -> str:
        pow_match_alt = re.match(r"(\d+)\s*\*\*\s*(\d+)\s*(-?\s*\d+)?", expr)
        if pow_match_alt:
            base, exp = pow_match_alt.group(1), pow_match_alt.group(2)
            if pow_match_alt.group(3):
                offset = int(pow_match_alt.group(3).replace(" ", ""))
                return str(int(base) ** int(exp) + offset)
            if base != "2":
                return str(pow(int(base), int(exp)))
            return f"1 << {exp}"

        pow_match = re.match(r"pow\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*(-?\s*\d+)?", expr, re.IGNORECASE)
        if pow_match:
            base, exp = pow_match.group(1), pow_match.group(2)
            if pow_match.group(3):
                offset = int(pow_match.group(3).replace(" ", ""))
                return str(int(base) ** int(exp) + offset)
            if base != "2":
                return str(pow(int(base), int(exp)))
            return f"1 << {exp}"

        int(expr)  # validate number
        return expr

    def align_pairs(self, pairs, sep=' '):
        """Align a sequence of ``(left, right)`` pairs by the length of ``left``."""
        if not pairs:
            return []
        max_len = max(len(left) for left, _ in pairs)
        return [f"{left:<{max_len}}{sep}{right}\n" for left, right in pairs]

    def align_on(
        self,
        lines,
        delimiter,
        *,
        sep=None,
        include_delim_in_right=False,
        reappend_left='',
        strip=False,
    ):
        """Split each line on ``delimiter`` and align the two halves."""

        pairs = []
        for line in lines:
            left, right = line.split(delimiter, 1)
            left += reappend_left
            if include_delim_in_right:
                right = delimiter + right
            if strip:
                left = left.strip()
                right = right.strip()
            pairs.append((left, right))

        if sep is None:
            sep = delimiter
        return self.align_pairs(pairs, sep)
