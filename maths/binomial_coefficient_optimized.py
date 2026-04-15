#!/usr/bin/env python3
"""
Optimized binomial_coefficient variants.

Reference: Pascal row-rebuild, O(n*r) time, O(r) space.

Variants:
1. binom_math_comb   -- math.comb (Python 3.8+); C-implementation, fastest.
2. binom_multiplicative -- C(n,k) = prod((n-i+1)/i), O(min(k, n-k)) time, O(1) space.
3. binom_factorial   -- n!/(k!(n-k)!) via math.factorial; O(n) mul but big ints.

Run:
    python maths/binomial_coefficient_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.binomial_coefficient import binomial_coefficient as binom_ref


def binom_math_comb(n: int, r: int) -> int:
    """
    >>> binom_math_comb(10, 5)
    252
    >>> binom_math_comb(52, 5)
    2598960
    >>> binom_math_comb(5, 6)
    0
    """
    if n < 0 or r < 0:
        raise ValueError("n and r must be non-negative integers")
    if r > n:
        return 0
    return math.comb(n, r)


def binom_multiplicative(n: int, r: int) -> int:
    """
    C(n,r) = prod_{i=1..k}((n-k+i)/i) with k = min(r, n-r).

    >>> binom_multiplicative(10, 5)
    252
    >>> binom_multiplicative(52, 5)
    2598960
    """
    if n < 0 or r < 0:
        raise ValueError("n and r must be non-negative integers")
    if r > n:
        return 0
    k = min(r, n - r)
    num = 1
    for i in range(1, k + 1):
        num = num * (n - k + i) // i
    return num


def binom_factorial(n: int, r: int) -> int:
    """
    >>> binom_factorial(10, 5)
    252
    """
    if n < 0 or r < 0:
        raise ValueError("n and r must be non-negative integers")
    if r > n:
        return 0
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))


def _benchmark() -> None:
    cases = [(50, 25), (100, 50), (200, 100)]
    n = 2000
    for (x, y) in cases:
        t1 = timeit.timeit(lambda: binom_ref(x, y), number=n) * 1000 / n
        t2 = timeit.timeit(lambda: binom_math_comb(x, y), number=n) * 1000 / n
        t3 = timeit.timeit(lambda: binom_multiplicative(x, y), number=n) * 1000 / n
        print(f"C({x},{y}):  pascal={t1:.4f} math.comb={t2:.4f} mult={t3:.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
