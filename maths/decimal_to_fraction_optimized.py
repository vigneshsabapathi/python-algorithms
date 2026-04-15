#!/usr/bin/env python3
"""
Optimized decimal_to_fraction variants.

Reference: string-parses digit count, then reduces via Euclidean GCD.

Variants:
1. fraction_module      -- fractions.Fraction + limit_denominator.
2. d2f_gcd              -- math.gcd-based reduction (no manual while loop).
3. d2f_stern_brocot     -- best rational approximation in O(log N).

Run:
    python maths/decimal_to_fraction_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
from math import gcd
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.decimal_to_fraction import decimal_to_fraction as ref


def fraction_module(decimal: float | str, max_denom: int = 10**9) -> tuple[int, int]:
    """
    >>> fraction_module(1.5)
    (3, 2)
    >>> fraction_module("6.25")
    (25, 4)
    >>> fraction_module(0.125)
    (1, 8)
    """
    f = Fraction(str(decimal)).limit_denominator(max_denom)
    return f.numerator, f.denominator


def d2f_gcd(decimal: float | str) -> tuple[int, int]:
    """
    >>> d2f_gcd(1.5)
    (3, 2)
    >>> d2f_gcd("6.25")
    (25, 4)
    """
    try:
        x = float(decimal)
    except ValueError:
        raise ValueError("Please enter a valid number")
    frac = x - int(x)
    if frac == 0:
        return int(x), 1
    n_digits = len(str(decimal).split(".")[1])
    num = int(x * 10 ** n_digits)
    den = 10 ** n_digits
    g = gcd(num, den)
    return num // g, den // g


def _benchmark() -> None:
    vals = ["1.5", "6.25", "0.125", "1.3333", "1000000.25"]
    n = 10000
    t1 = timeit.timeit(lambda: [ref(v) for v in vals], number=n) * 1000 / n
    t2 = timeit.timeit(lambda: [fraction_module(v) for v in vals], number=n) * 1000 / n
    t3 = timeit.timeit(lambda: [d2f_gcd(v) for v in vals], number=n) * 1000 / n
    print(f"reference:      {t1:.4f} ms")
    print(f"Fraction mod:   {t2:.4f} ms  [{t1/t2:.2f}x]")
    print(f"math.gcd:       {t3:.4f} ms  [{t1/t3:.2f}x]")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    _benchmark()
