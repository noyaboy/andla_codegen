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
            cls._normalize_str(data.get('Index')),
            cls._normalize_str(data.get('Bit Locate')),
            cls._normalize_str(data.get('Physical Address')),
            cls._normalize_str(data.get('Bitwidth configuare')),
            cls._normalize_str(data.get('Min')),
            cls._normalize_str(data.get('Max')),
            cls._normalize_str(data.get('Usecase')),
            cls._normalize_str(data.get('Constraint')),
            data,
        )


def load_dictionary_lines(dictionary_filename: str):
    """Read dictionary file and parse each line into :class:`DictRow` objects."""

    with open(dictionary_filename, 'r') as dict_fh:
        rows = [DictRow.from_line(line.rstrip('\n')) for line in dict_fh]

    return [row for row in rows if row.type != '']


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

    def fetch_terms(self, row: DictRow):
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

        if self.item_upper and self.register_upper:
            self.doublet_upper = f"{self.item_upper}_{self.register_upper}"
        else:
            self.doublet_upper = ''

        if self.item_upper and self.register_upper and self.subregister_upper:
            self.triplet_upper = (
                f"{self.item_upper}_{self.register_upper}_{self.subregister_upper}"
            )
        else:
            self.triplet_upper = ''

        self.id  = row.id
        self.typ = row.type
        self.default_value = row.default_value
        self.index               = row.index
        self.bit_locate          = row.bit_locate
        self.physical_address    = row.physical_address
        self.bitwidth_configuare = row.bitwidth_configuare
        self.min_val             = row.min_val
        self.max_val             = row.max_val
        self.usecase             = row.usecase
        self.constraint          = row.constraint

        if not self.default_value.startswith('0x'):
            self.seq_default_value_width = int(row.default_value).bit_length() or 1

        if self.default_value.startswith('0x'):
            self.seq_default_value = self.default_value.replace('0x', "32'h")
        elif self.subregister_lower in ('msb','lsb'):
            self.seq_default_value = f"{{ {{({self.triplet_upper}_BITWIDTH-{self.seq_default_value_width}){{1'd0}}}}, {self.seq_default_value_width}'d{self.default_value} }}"
        else:
            self.seq_default_value = f"{{ {{({self.doublet_upper}_BITWIDTH-{self.seq_default_value_width}){{1'd0}}}}, {self.seq_default_value_width}'d{self.default_value} }}"

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
