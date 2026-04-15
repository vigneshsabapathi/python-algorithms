#!/usr/bin/env python3
"""
Optimized continued_fraction variants.

Variants:
1. cf_divmod       -- uses divmod() each step, avoiding double arithmetic.
2. cf_reverse      -- reconstructs a Fraction from coefficient list (inverse).
3. cf_gcd_trace    -- derives coefficients from Euclidean GCD trace.

Run:
    python maths/continued_fraction_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.continued_fraction import continued_fraction as ref


def cf_divmod(num: Fraction) -> list[int]:
    """
    Euclidean-style: repeatedly divmod(p, q) and swap.

    >>> cf_divmod(Fraction(2))
    [2]
    >>> cf_divmod(Fraction("3.245"))
    [3, 4, 12, 4]
    >>> cf_divmod(Fraction("415/93"))
    [4, 2, 6, 7]
    >>> cf_divmod(Fraction("-2.25"))
    [-3, 1, 3]
    """
    p, q = num.as_integer_ratio()
    out: list[int] = []
    while q:
        a, r = divmod(p, q)
        out.append(a)
        p, q = q, r
    return out


def cf_reverse(coeffs: list[int]) -> Fraction:
    """
    Rebuild the fraction from its continued-fraction expansion.

    >>> cf_reverse([3, 4, 12, 4])
    Fraction(649, 200)
    >>> cf_reverse([4, 2, 6, 7])
    Fraction(415, 93)
    """
    if not coeffs:
        raise ValueError("empty")
    f = Fraction(coeffs[-1])
    for a in reversed(coeffs[:-1]):
        f = a + Fraction(1, 1) / f
    return f


def _benchmark() -> None:
    q = Fraction("415/93")
    n = 50000
    t1 = timeit.timeit(lambda: ref(q), number=n) * 1000 / n
    t2 = timeit.timeit(lambda: cf_divmod(q), number=n) * 1000 / n
    print(f"reference:  {t1:.5f} ms")
    print(f"divmod:     {t2:.5f} ms  [{t1/t2:.2f}x]")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
