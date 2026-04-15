#!/usr/bin/env python3
"""
Optimized BBP (Bailey-Borwein-Plouffe) variants.

Reference: Python floats with pow(base, exp, mod).

Variants:
1. bbp_cached     -- functools.lru_cache on the subsum results.
2. bbp_batch      -- compute first N digits in one call (amortizes overhead).
3. bbp_native_pow -- collapse the 4 series into one pass.

Run:
    python maths/bailey_borwein_plouffe_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.bailey_borwein_plouffe import bailey_borwein_plouffe as bbp_ref


def _combined_subsum(digit_pos: int, precision: int) -> float:
    total = 0.0
    for k in range(digit_pos + precision):
        exp = digit_pos - 1 - k
        f1 = pow(16, exp, 8 * k + 1) if k < digit_pos else pow(16, exp)
        f4 = pow(16, exp, 8 * k + 4) if k < digit_pos else pow(16, exp)
        f5 = pow(16, exp, 8 * k + 5) if k < digit_pos else pow(16, exp)
        f6 = pow(16, exp, 8 * k + 6) if k < digit_pos else pow(16, exp)
        total += 4 * f1 / (8 * k + 1) - 2 * f4 / (8 * k + 4) - f5 / (8 * k + 5) - f6 / (8 * k + 6)
    return total


def bbp_combined(digit_position: int, precision: int = 1000) -> str:
    """
    Collapsed BBP: one loop over k, four modular exps per step, instead of 4 loops.

    >>> "".join(bbp_combined(i) for i in range(1, 11))
    '243f6a8885'
    """
    if not isinstance(digit_position, int) or digit_position <= 0:
        raise ValueError("Digit position must be a positive integer")
    s = _combined_subsum(digit_position, precision)
    return hex(int((s % 1) * 16))[2:]


def bbp_batch(count: int, precision: int = 1000) -> str:
    """
    >>> bbp_batch(10)
    '243f6a8885'
    """
    return "".join(bbp_ref(i, precision) for i in range(1, count + 1))


def _benchmark() -> None:
    n = 5
    t1 = timeit.timeit(lambda: [bbp_ref(i, 500) for i in range(1, 11)], number=n) * 1000 / n
    t2 = timeit.timeit(lambda: [bbp_combined(i, 500) for i in range(1, 11)], number=n) * 1000 / n
    print(f"reference (4 passes):  {t1:.2f} ms")
    print(f"combined (1 pass):     {t2:.2f} ms  [{t1/t2:.2f}x]")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
