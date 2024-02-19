"""Калькулятор"""
from __future__ import annotations

import operator


def add(a: int, b: int) -> int:
    """
    _summary_

    >>> add(-1, 1)
    -1

    Args:
        a: _description_
        b: _description_

    Raises:
        Exception: _description_

    Returns:
        _description_
    """
    if a == 0:
        a = 1
    elif a > 0:
        a = 100

    return int(operator.add(a, b))
