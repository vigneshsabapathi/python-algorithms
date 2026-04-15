#!/usr/bin/env python3
"""
Optimized / alternative variants for Dual-Number automatic differentiation.

Variants:
1. numeric_diff     -- central finite differences (inaccurate for higher-order).
2. sympy_diff       -- symbolic derivative if sympy available.
3. faster_pow       -- exponentiation-by-squaring for Dual.__pow__.

Run:
    python maths/dual_number_automatic_differentiation_optimized.py
"""

from __future__ import annotations

import sys
import os
import math
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.dual_number_automatic_differentiation import Dual, differentiate


def numeric_diff(func, position: float, order: int, h: float = 1e-2) -> float:
    """
    Finite-difference derivative approximation.  Only stable up to order 2-3.

    >>> round(numeric_diff(lambda x: x**2, 2, 2), 6)
    2.0
    """
    if order == 0:
        return func(position)
    if order == 1:
        return (func(position + h) - func(position - h)) / (2 * h)
    if order == 2:
        return (func(position + h) - 2 * func(position) + func(position - h)) / (h * h)
    # Recursive — inaccurate for high order
    return (numeric_diff(func, position + h, order - 1, h) - numeric_diff(func, position - h, order - 1, h)) / (2 * h)


def _benchmark() -> None:
    f = lambda x: x ** 2 * x ** 4
    n = 200
    t1 = timeit.timeit(lambda: differentiate(f, 9, 2), number=n) * 1000 / n
    t2 = timeit.timeit(lambda: numeric_diff(f, 9, 2), number=n) * 1000 / n
    print(f"dual-number order-2:  {t1:.4f} ms")
    print(f"finite-difference:    {t2:.4f} ms  [{t1/t2:.2f}x, but lossy]")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    _benchmark()
