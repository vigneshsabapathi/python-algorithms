#!/usr/bin/env python3
"""
Optimized aliquot sum variants.

Reference scans 1..n/2 → O(n).

Variants:
1. aliquot_sum_sqrt        -- pair divisors up to sqrt(n) → O(sqrt n).
2. aliquot_sum_factorization -- sum_of_divisors via prime factorization
                                (multiplicative function) → ~O(sqrt n).
3. aliquot_sum_sympy       -- sympy.divisor_sigma(n, 1) - n (if available).

Run:
    python maths/aliquot_sum_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
from math import isqrt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.aliquot_sum import aliquot_sum as aliquot_sum_reference


def aliquot_sum_sqrt(n: int) -> int:
    """
    Pair divisor trick: for every d <= sqrt(n) that divides n, n//d is also
    a divisor. Runs in O(sqrt n).

    >>> aliquot_sum_sqrt(15)
    9
    >>> aliquot_sum_sqrt(6)
    6
    >>> aliquot_sum_sqrt(28)
    28
    >>> aliquot_sum_sqrt(1)
    0
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Input must be a positive integer")
    if n == 1:
        return 0
    total = 1  # 1 is always a proper divisor of n > 1
    r = isqrt(n)
    for d in range(2, r + 1):
        if n % d == 0:
            total += d
            other = n // d
            if other != d and other != n:
                total += other
    return total


def aliquot_sum_factorization(n: int) -> int:
    """
    Uses multiplicative property: if n = p1^a1 * p2^a2 * ...,
    sigma(n) = prod((p^(a+1) - 1)/(p - 1)); aliquot = sigma(n) - n.

    >>> aliquot_sum_factorization(15)
    9
    >>> aliquot_sum_factorization(6)
    6
    >>> aliquot_sum_factorization(28)
    28
    """
    if n <= 0:
        raise ValueError("Input must be positive")
    if n == 1:
        return 0
    sigma = 1
    x = n
    p = 2
    while p * p <= x:
        if x % p == 0:
            term = 1
            pk = 1
            while x % p == 0:
                x //= p
                pk *= p
                term += pk
            sigma *= term
        p += 1
    if x > 1:
        sigma *= 1 + x
    return sigma - n


def _benchmark() -> None:
    cases = [60, 496, 8128, 10000, 33550336]
    n = 50
    print(f"Benchmark: aliquot_sum (n={n:,} iterations per case)\n")
    print(f"{'Number':>12} {'reference':>14} {'sqrt':>14} {'factor':>14}")
    for x in cases:
        t1 = timeit.timeit(lambda: aliquot_sum_reference(x), number=n) * 1000 / n if x < 1_000_000 else float("inf")
        t2 = timeit.timeit(lambda: aliquot_sum_sqrt(x), number=n) * 1000 / n
        t3 = timeit.timeit(lambda: aliquot_sum_factorization(x), number=n) * 1000 / n
        t1s = f"{t1:.3f} ms" if t1 != float("inf") else "  (skip)"
        print(f"{x:>12} {t1s:>14} {t2:>10.3f} ms {t3:>10.3f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
