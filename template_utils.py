from typing import List


def align_by_delimiter(lines: List[str], delimiter: str) -> List[str]:
    """Align the left part of lines split by delimiter."""
    parts = [line.split(delimiter, 1) for line in lines]
    width = max(len(p[0]) for p in parts)
    return [f"{p[0]:<{width}}{delimiter}{p[1]}" for p in parts]


def zero_pad(value: int, width: int) -> str:
    """Return zero filled string of given width."""
    return str(value).zfill(width)
