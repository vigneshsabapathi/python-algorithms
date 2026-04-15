#!/usr/bin/env python3
"""
Optimized combinations variants.

Reference: multiplicative formula, already O(k).

Variants:
1. comb_math        -- math.comb; C-level.
2. comb_symmetric   -- exploit C(n,k) == C(n,n-k); halves the loop.
3. comb_factorial   -- n!/(k!(n-k)!); big but direct.

Run:
    python maths/combinations_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.combinations import combinations as ref


def comb_math(n: int, k: int) -> int:
    """
    >>> comb_math(10, 5)
    252
    >>> comb_math(52, 5)
    2598960
    """
    if n < k or k < 0:
        raise ValueError("Please enter positive integers for n and k where n >= k")
    return math.comb(n, k)


def comb_symmetric(n: int, k: int) -> int:
    """
    >>> comb_symmetric(10, 5)
    252
    >>> comb_symmetric(100, 98)
    4950
    """
    if n < k or k < 0:
        raise ValueError("Please enter positive integers for n and k where n >= k")
    k = min(k, n - k)
    r = 1
    for i in range(k):
        r = r * (n - i) // (i + 1)
    return r


def _benchmark() -> None:
    n = 50000
    t1 = timeit.timeit(lambda: ref(52, 5), number=n) * 1000 / n
    t2 = timeit.timeit(lambda: comb_math(52, 5), number=n) * 1000 / n
    t3 = timeit.timeit(lambda: comb_symmetric(52, 5), number=n) * 1000 / n
    print(f"reference:   {t1:.5f} ms")
    print(f"math.comb:   {t2:.5f} ms  [{t1/t2:.2f}x]")
    print(f"symmetric:   {t3:.5f} ms  [{t1/t3:.2f}x]")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
