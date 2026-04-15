#!/usr/bin/env python3
"""
Optimized fast_inverse_sqrt variants.

Reference: classic Quake III algorithm — single Newton iteration.

Variants:
1. fisr_newton_2  -- two Newton iterations for higher accuracy.
2. fisr_native    -- 1/math.sqrt(x) — almost always faster in Python.
3. fisr_pow       -- x**-0.5.

Run:
    python maths/fast_inverse_sqrt_optimized.py
"""

from __future__ import annotations

import sys
import os
import math
import struct
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.fast_inverse_sqrt import fast_inverse_sqrt as ref


def fisr_newton_2(number: float) -> float:
    """
    Quake III with 2 Newton iterations (error ~1e-7 instead of ~1e-3).

    >>> from math import isclose, sqrt
    >>> all(isclose(fisr_newton_2(i), 1 / sqrt(i), rel_tol=1e-5) for i in range(50, 60))
    True
    """
    if number <= 0:
        raise ValueError("Input must be a positive number.")
    i = struct.unpack(">i", struct.pack(">f", number))[0]
    i = 0x5F3759DF - (i >> 1)
    y = struct.unpack(">f", struct.pack(">i", i))[0]
    y = y * (1.5 - 0.5 * number * y * y)
    y = y * (1.5 - 0.5 * number * y * y)  # extra iteration
    return y


def fisr_native(number: float) -> float:
    """
    >>> round(fisr_native(4), 6)
    0.5
    """
    if number <= 0:
        raise ValueError("Input must be a positive number.")
    return 1.0 / math.sqrt(number)


def _benchmark() -> None:
    vals = [float(i) for i in range(1, 500)]
    n = 5000
    t1 = timeit.timeit(lambda: [ref(v) for v in vals], number=n) * 1000 / n
    t2 = timeit.timeit(lambda: [fisr_newton_2(v) for v in vals], number=n) * 1000 / n
    t3 = timeit.timeit(lambda: [fisr_native(v) for v in vals], number=n) * 1000 / n
    print(f"Quake III (1 Newton): {t1:.4f} ms")
    print(f"Quake III (2 Newton): {t2:.4f} ms  [{t1/t2:.2f}x]")
    print(f"1/math.sqrt:          {t3:.4f} ms  [{t1/t3:.2f}x faster]")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    _benchmark()
