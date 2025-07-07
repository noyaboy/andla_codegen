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
