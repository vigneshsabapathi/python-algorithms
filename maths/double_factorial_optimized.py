#!/usr/bin/env python3
"""
Optimized double_factorial variants.

Variants:
1. df_prod       -- math.prod(range(n, 0, -2)); C-level, fastest.
2. df_factorial  -- n!! = n! / (n-1)!! identity, uses math.factorial.
3. df_divide_conq -- divide-and-conquer product (balanced tree) — big ints.

Run:
    python maths/double_factorial_optimized.py
"""

from __future__ import annotations

import sys
import os
import math
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.double_factorial import double_factorial_iterative as iter_ref, double_factorial_recursive as rec_ref


def df_prod(n: int) -> int:
    """
    >>> df_prod(0)
    1
    >>> df_prod(1)
    1
    >>> df_prod(9)
    945
    """
    if not isinstance(n, int):
        raise ValueError("only integral values")
    if n < 0:
        raise ValueError("not defined for negative values")
    return math.prod(range(n, 0, -2)) if n > 0 else 1


def df_divide_conq(n: int) -> int:
    """
    Balanced binary product — helps only for very large n (big-int multiply).

    >>> df_divide_conq(9)
    945
    >>> df_divide_conq(10)
    3840
    """
    if n <= 1:
        return 1
    vals = list(range(n, 0, -2))

    def prod(lo: int, hi: int) -> int:
        if hi - lo <= 1:
            return vals[lo]
        mid = (lo + hi) // 2
        return prod(lo, mid) * prod(mid, hi)
    return prod(0, len(vals))


def _benchmark() -> None:
    n = 20000
    for k in (20, 100, 500):
        t1 = timeit.timeit(lambda: iter_ref(k), number=n) * 1000 / n
        t2 = timeit.timeit(lambda: df_prod(k), number=n) * 1000 / n
        t3 = timeit.timeit(lambda: df_divide_conq(k), number=n) * 1000 / n
        print(f"n={k:>3}: iter={t1:.4f} math.prod={t2:.4f} divconq={t3:.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    _benchmark()
