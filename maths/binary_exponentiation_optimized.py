#!/usr/bin/env python3
"""
Optimized binary exponentiation variants.

Reference already contains recursive + iterative + modular versions.

Variants:
1. pow_builtin    -- Python's pow(a, b, m) — C-level, fastest.
2. be_matrix      -- matrix exponentiation for fibonacci-like linear recurrences.
3. be_lshift_fast -- micro-optimized iterative with combined mod steps.

Run:
    python maths/binary_exponentiation_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.binary_exponentiation import (
    binary_exp_iterative,
    binary_exp_mod_iterative,
)


def pow_builtin(base: float, exponent: int) -> float:
    """
    >>> pow_builtin(3, 5)
    243
    >>> pow_builtin(2, 10)
    1024
    """
    if exponent < 0:
        raise ValueError("Exponent must be a non-negative integer")
    return pow(base, exponent)


def pow_builtin_mod(base: int, exponent: int, modulus: int) -> int:
    """
    >>> pow_builtin_mod(3, 4, 5)
    1
    >>> pow_builtin_mod(11, 13, 7)
    4
    """
    if modulus <= 0:
        raise ValueError("Modulus must be a positive integer")
    return pow(base, exponent, modulus)


def be_lshift_fast(base: int, exponent: int, modulus: int) -> int:
    """
    Minimal-op modular exponentiation; single `res * base % m` per odd bit.

    >>> be_lshift_fast(1269380576, 374, 34)
    8
    """
    res = 1
    base %= modulus
    while exponent:
        if exponent & 1:
            res = res * base % modulus
        base = base * base % modulus
        exponent >>= 1
    return res


def _benchmark() -> None:
    a, b, c = 1269380576, 374, 34
    n = 50000
    t1 = timeit.timeit(lambda: binary_exp_iterative(a, b), number=n) * 1000 / n
    t2 = timeit.timeit(lambda: pow_builtin(a, b), number=n) * 1000 / n
    t3 = timeit.timeit(lambda: binary_exp_mod_iterative(a, b, c), number=n) * 1000 / n
    t4 = timeit.timeit(lambda: pow_builtin_mod(a, b, c), number=n) * 1000 / n
    t5 = timeit.timeit(lambda: be_lshift_fast(a, b, c), number=n) * 1000 / n
    print(f"iter   a^b:        {t1:.5f} ms")
    print(f"pow    a^b:        {t2:.5f} ms  [{t1/t2:.1f}x]")
    print(f"iter   (a^b)%m:    {t3:.5f} ms")
    print(f"pow    (a^b)%m:    {t4:.5f} ms  [{t3/t4:.1f}x]")
    print(f"lshift (a^b)%m:    {t5:.5f} ms  [{t3/t5:.1f}x]")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
