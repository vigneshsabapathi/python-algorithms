#!/usr/bin/env python3
"""
Optimized binary_multiplication variants.

Variants:
1. mul_native     -- Python's `*` — C-level, baseline.
2. mul_peasant    -- "Russian peasant" multiplication (same algo, clearer).
3. mul_mod_pow    -- mod-multiply via pow(a*b, 1, m), trivial but idiomatic.

Run:
    python maths/binary_multiplication_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.binary_multiplication import binary_multiply, binary_mod_multiply


def mul_native(a: int, b: int) -> int:
    """
    >>> mul_native(3, 4)
    12
    >>> mul_native(10, 5)
    50
    """
    return a * b


def mul_peasant(a: int, b: int) -> int:
    """
    Russian peasant: identical algorithm, double/halve form.

    >>> mul_peasant(3, 4)
    12
    >>> mul_peasant(17, 23)
    391
    """
    result = 0
    while b > 0:
        if b & 1:
            result += a
        a <<= 1
        b >>= 1
    return result


def mul_mod_native(a: int, b: int, m: int) -> int:
    """
    >>> mul_mod_native(10, 5, 13)
    11
    """
    return (a * b) % m


def _benchmark() -> None:
    pairs = [(i * 137, i * 211) for i in range(1, 200)]
    n = 1000
    t1 = timeit.timeit(lambda: [binary_multiply(a, b) for a, b in pairs], number=n) * 1000 / n
    t2 = timeit.timeit(lambda: [mul_native(a, b) for a, b in pairs], number=n) * 1000 / n
    t3 = timeit.timeit(lambda: [binary_mod_multiply(a, b, 997) for a, b in pairs], number=n) * 1000 / n
    t4 = timeit.timeit(lambda: [mul_mod_native(a, b, 997) for a, b in pairs], number=n) * 1000 / n
    print(f"binary_multiply:      {t1:.3f} ms")
    print(f"native *:             {t2:.3f} ms  [{t1/t2:.0f}x]")
    print(f"binary_mod_multiply:  {t3:.3f} ms")
    print(f"native (a*b)%m:       {t4:.3f} ms  [{t3/t4:.0f}x]")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
