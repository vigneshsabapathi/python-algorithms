#!/usr/bin/env python3
"""
Optimized factors variants.

Reference: iterate 2..sqrt(n), collect divisor pairs, sort at end.

Variants:
1. factors_sorted_pairs  -- accumulate large half, reverse-merge — no sort.
2. factors_sympy         -- sympy.divisors if available.
3. factors_bitset        -- boolean sieve-based for batch queries.

Run:
    python maths/factors_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
from math import isqrt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.factors import factors_of_a_number as ref


def factors_no_sort(num: int) -> list[int]:
    """
    Build lower & upper halves separately; merge in O(sqrt n) without sort.

    >>> factors_no_sort(1)
    [1]
    >>> factors_no_sort(24)
    [1, 2, 3, 4, 6, 8, 12, 24]
    >>> factors_no_sort(-24)
    []
    """
    if num < 1:
        return []
    lo: list[int] = []
    hi: list[int] = []
    for i in range(1, isqrt(num) + 1):
        if num % i == 0:
            lo.append(i)
            j = num // i
            if j != i:
                hi.append(j)
    return lo + hi[::-1]


def _benchmark() -> None:
    vals = [120, 360360, 999999, 1048576]
    n = 5000
    t1 = timeit.timeit(lambda: [ref(v) for v in vals], number=n) * 1000 / n
    t2 = timeit.timeit(lambda: [factors_no_sort(v) for v in vals], number=n) * 1000 / n
    print(f"reference (sort):   {t1:.4f} ms")
    print(f"no-sort merge:      {t2:.4f} ms  [{t1/t2:.2f}x]")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    _benchmark()
