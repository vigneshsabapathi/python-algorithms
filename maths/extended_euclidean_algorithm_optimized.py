#!/usr/bin/env python3
"""
Optimized extended_euclidean_algorithm variants.

Reference: iterative w/ sign correction.

Variants:
1. eea_recursive  -- textbook recursive form.
2. eea_with_gcd   -- returns (gcd, x, y) rather than just (x, y).
3. eea_pow_inv    -- pow(a, -1, n) for modular inverse only (Py 3.8+).

Run:
    python maths/extended_euclidean_algorithm_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
from math import gcd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.extended_euclidean_algorithm import extended_euclidean_algorithm as ref


def eea_recursive(a: int, b: int) -> tuple[int, int, int]:
    """
    Returns (g, x, y) with a*x + b*y = g = gcd(a, b).

    >>> eea_recursive(240, 46)
    (2, -9, 47)
    >>> eea_recursive(8, 14)
    (2, 2, -1)
    """
    if b == 0:
        return (a, 1, 0) if a >= 0 else (-a, -1, 0)
    g, x1, y1 = eea_recursive(b, a % b)
    return g, y1, x1 - (a // b) * y1


def eea_with_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Iterative version returning (g, x, y).

    >>> eea_with_gcd(240, 46)
    (2, -9, 47)
    """
    old_r, r = abs(a), abs(b)
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    if a < 0:
        old_s = -old_s
    if b < 0:
        old_t = -old_t
    return old_r, old_s, old_t


def _benchmark() -> None:
    pairs = [(240, 46), (1234567, 7654321), (100003, 99991)]
    n = 50000
    t1 = timeit.timeit(lambda: [ref(a, b) for a, b in pairs], number=n) * 1000 / n
    t2 = timeit.timeit(lambda: [eea_recursive(a, b) for a, b in pairs], number=n) * 1000 / n
    t3 = timeit.timeit(lambda: [eea_with_gcd(a, b) for a, b in pairs], number=n) * 1000 / n
    print(f"reference:   {t1:.5f} ms")
    print(f"recursive:   {t2:.5f} ms  [{t1/t2:.2f}x]")
    print(f"iterative:   {t3:.5f} ms  [{t1/t3:.2f}x]")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    _benchmark()
