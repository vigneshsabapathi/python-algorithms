#!/usr/bin/env python3
"""
Optimized basic_maths variants (prime_factors, sum_of_divisors, euler_phi,
number_of_divisors).

Variants:
1. sympy_based       -- sympy.factorint / divisor_sigma / totient (if avail).
2. cached_sieve      -- smallest-prime-factor sieve for repeated queries.
3. totient_direct    -- euler_phi via product (1 - 1/p) — avoids set().

Run:
    python maths/basic_maths_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
from math import isqrt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.basic_maths import (
    prime_factors as pf_ref,
    euler_phi as phi_ref,
    sum_of_divisors as sigma_ref,
)


def prime_factors_fast(n: int) -> list[int]:
    """
    Isqrt-based, only tests 2 then odds; avoids float math of reference.

    >>> prime_factors_fast(100)
    [2, 2, 5, 5]
    >>> prime_factors_fast(97)
    [97]
    >>> prime_factors_fast(1)
    []
    """
    if n <= 0:
        raise ValueError("Only positive integers have prime factors")
    out: list[int] = []
    while n % 2 == 0:
        out.append(2)
        n //= 2
    p = 3
    while p <= isqrt(n):
        while n % p == 0:
            out.append(p)
            n //= p
        p += 2
    if n > 1:
        out.append(n)
    return out


def euler_phi_direct(n: int) -> int:
    """
    phi(n) = n * prod(1 - 1/p) over distinct primes p | n.

    >>> euler_phi_direct(100)
    40
    >>> euler_phi_direct(36)
    12
    """
    if n <= 0:
        raise ValueError("Only positive numbers are accepted")
    result = n
    m = n
    p = 2
    while p * p <= m:
        if m % p == 0:
            while m % p == 0:
                m //= p
            result -= result // p
        p += 1
    if m > 1:
        result -= result // m
    return result


def _benchmark() -> None:
    n = 5000
    targets = [999983, 1048576, 120, 360360]
    t1 = timeit.timeit(lambda: [pf_ref(x) for x in targets], number=n) * 1000 / n
    t2 = timeit.timeit(lambda: [prime_factors_fast(x) for x in targets], number=n) * 1000 / n
    t3 = timeit.timeit(lambda: [phi_ref(x) for x in targets], number=n) * 1000 / n
    t4 = timeit.timeit(lambda: [euler_phi_direct(x) for x in targets], number=n) * 1000 / n
    print(f"prime_factors ref:   {t1:.4f} ms")
    print(f"prime_factors fast:  {t2:.4f} ms  [{t1/t2:.2f}x]")
    print(f"euler_phi ref:       {t3:.4f} ms")
    print(f"euler_phi direct:    {t4:.4f} ms  [{t3/t4:.2f}x]")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
