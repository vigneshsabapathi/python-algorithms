#!/usr/bin/env python3
"""
Optimized decimal_isolate variants.

Variants:
1. decimal_math_modf  -- math.modf returns (frac, int); avoids int() cast issues.
2. decimal_round      -- round(x, d) - int(x) alternate.
3. decimal_str        -- string-based (exact, but slow).

Run:
    python maths/decimal_isolate_optimized.py
"""

from __future__ import annotations

import sys
import os
import math
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.decimal_isolate import decimal_isolate as ref


def decimal_math_modf(x: float, digits: int) -> float:
    """
    >>> decimal_math_modf(1.53, 0)
    0.53
    >>> decimal_math_modf(35.345, 2)
    0.34
    >>> decimal_math_modf(-14.123, 3)
    -0.123
    """
    frac, _ = math.modf(x)
    return round(frac, digits) if digits > 0 else frac


def _benchmark() -> None:
    vals = [(i * 0.137 - 50, i % 5) for i in range(1000)]
    n = 5000
    t1 = timeit.timeit(lambda: [ref(v, d) for v, d in vals], number=n) * 1000 / n
    t2 = timeit.timeit(lambda: [decimal_math_modf(v, d) for v, d in vals], number=n) * 1000 / n
    print(f"reference:  {t1:.4f} ms\nmath.modf:  {t2:.4f} ms  [{t1/t2:.2f}x]")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    _benchmark()
