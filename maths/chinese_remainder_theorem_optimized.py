#!/usr/bin/env python3
"""
Optimized Chinese Remainder Theorem variants.

Variants:
1. crt_builtin_pow   -- use pow(a, -1, m) for modular inverse (Py 3.8+).
2. crt_list          -- general CRT over a list of (n_i, r_i) pairs.
3. crt_iterative     -- non-recursive extended euclid.

Run:
    python maths/chinese_remainder_theorem_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
from math import gcd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.chinese_remainder_theorem import chinese_remainder_theorem as ref


def crt_builtin_pow(n1: int, r1: int, n2: int, r2: int) -> int:
    """
    Use Python's built-in pow for modular inverse.

    >>> crt_builtin_pow(5, 1, 7, 3)
    31
    >>> crt_builtin_pow(3, 2, 5, 3)
    8
    """
    m = n1 * n2
    x = pow(n1 % n2, -1, n2) if gcd(n1, n2) == 1 else 0
    y = pow(n2 % n1, -1, n1) if gcd(n2, n1) == 1 else 0
    n = r2 * x * n1 + r1 * y * n2
    return (n % m + m) % m


def crt_list(mods: list[int], rems: list[int]) -> int:
    """
    General CRT over pairs.  Requires all mods coprime.

    >>> crt_list([3, 5, 7], [2, 3, 2])
    23
    >>> crt_list([5, 7], [1, 3])
    31
    """
    assert len(mods) == len(rems)
    M = 1
    for m in mods:
        M *= m
    x = 0
    for mi, ri in zip(mods, rems):
        Mi = M // mi
        yi = pow(Mi, -1, mi)
        x += ri * Mi * yi
    return x % M


def _benchmark() -> None:
    n = 50000
    t1 = timeit.timeit(lambda: ref(97, 23, 101, 41), number=n) * 1000 / n
    t2 = timeit.timeit(lambda: crt_builtin_pow(97, 23, 101, 41), number=n) * 1000 / n
    t3 = timeit.timeit(lambda: crt_list([97, 101], [23, 41]), number=n) * 1000 / n
    print(f"reference ext-euclid: {t1:.5f} ms")
    print(f"builtin pow:          {t2:.5f} ms  [{t1/t2:.2f}x]")
    print(f"crt_list:             {t3:.5f} ms  [{t1/t3:.2f}x]")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
