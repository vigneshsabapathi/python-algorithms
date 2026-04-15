#!/usr/bin/env python3
"""
Optimized Euler's totient sieve variants.

Reference: linear sieve-like approach with primes list.

Variants:
1. totient_sieve     -- classic: phi[i]=i; for each prime p, for mults, phi[m]-=phi[m]/p.
2. totient_single    -- O(sqrt n) single-value, for when only one phi(n) is needed.
3. totient_factorint -- sympy.totient if available.

Run:
    python maths/eulers_totient_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.eulers_totient import totient as ref


def totient_sieve(n: int) -> list[int]:
    """
    Classic O(n log log n) sieve: phi[1..n].

    >>> phi = totient_sieve(10)
    >>> phi[1], phi[6], phi[9]
    (1, 2, 6)
    """
    phi = list(range(n + 1))
    for i in range(2, n + 1):
        if phi[i] == i:  # i is prime
            for j in range(i, n + 1, i):
                phi[j] -= phi[j] // i
    return phi


def totient_single(n: int) -> int:
    """
    O(sqrt n) single-value totient.

    >>> totient_single(9)
    6
    >>> totient_single(10)
    4
    >>> totient_single(100)
    40
    """
    if n <= 0:
        raise ValueError("n must be positive")
    result = n
    p = 2
    x = n
    while p * p <= x:
        if x % p == 0:
            while x % p == 0:
                x //= p
            result -= result // p
        p += 1
    if x > 1:
        result -= result // x
    return result


def _benchmark() -> None:
    n = 50
    t1 = timeit.timeit(lambda: ref(10000), number=n) * 1000 / n
    t2 = timeit.timeit(lambda: totient_sieve(10000), number=n) * 1000 / n
    t3 = timeit.timeit(lambda: [totient_single(i) for i in range(1, 10001)], number=n // 2) * 1000 / (n // 2)
    print(f"reference:     {t1:.3f} ms")
    print(f"classic sieve: {t2:.3f} ms  [{t1/t2:.2f}x]")
    print(f"per-value:     {t3:.3f} ms  [{t1/t3:.2f}x]")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    _benchmark()
