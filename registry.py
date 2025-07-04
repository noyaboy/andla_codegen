"""Simple registry for Writer classes used by ``gen_regfile.py``.

This module defines a global dictionary mapping writer keys (strings) to the
actual writer classes.  Writers register themselves via the
``@register_writer`` decorator at import time so ``gen_regfile.py`` can create
instances dynamically without manually maintaining a list.
"""

from typing import Dict, Type


WRITER_REGISTRY: Dict[str, Type["BaseWriter"]] = {}


def register_writer(key: str):
    """Class decorator to register a writer class.

    Parameters
    ----------
    key:
        The name used in templates and command line to identify the writer.

    Raises
    ------
    ValueError
        If ``key`` has already been registered.
    """

    def decorator(cls: Type["BaseWriter"]) -> Type["BaseWriter"]:
        if key in WRITER_REGISTRY:
            raise ValueError(f"Writer '{key}' 已經註冊過了")
        WRITER_REGISTRY[key] = cls
        return cls

    return decorator


__all__ = ["WRITER_REGISTRY", "register_writer"]

