#!/usr/bin/env python3
"""
Optimized factorial variants.

Variants:
1. fact_builtin     -- math.factorial; C, fastest.
2. fact_prod        -- math.prod(range(1, n+1)).
3. fact_divide_conq -- balanced product tree (helps for huge n / big-int mult).

Run:
    python maths/factorial_optimized.py
"""

from __future__ import annotations

import sys
import os
import math
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.factorial import factorial as ref_iter, factorial_recursive as ref_rec


def fact_builtin(n: int) -> int:
    """
    >>> fact_builtin(0)
    1
    >>> fact_builtin(6)
    720
    """
    return math.factorial(n)


def fact_prod(n: int) -> int:
    """
    >>> fact_prod(0)
    1
    >>> fact_prod(6)
    720
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("bad n")
    return math.prod(range(1, n + 1)) if n > 0 else 1


def fact_divide_conq(n: int) -> int:
    """
    Balanced binary product tree — faster big-int multiplication for huge n.

    >>> fact_divide_conq(6)
    720
    >>> fact_divide_conq(0)
    1
    """
    if n <= 1:
        return 1

    def prod(lo: int, hi: int) -> int:
        if hi - lo == 1:
            return lo
        mid = (lo + hi) // 2
        return prod(lo, mid) * prod(mid, hi)
    return prod(1, n + 1)


def _benchmark() -> None:
    n = 2000
    for k in (20, 200, 2000):
        t1 = timeit.timeit(lambda: ref_iter(k), number=n) * 1000 / n
        t2 = timeit.timeit(lambda: fact_builtin(k), number=n) * 1000 / n
        t3 = timeit.timeit(lambda: fact_divide_conq(k), number=n) * 1000 / n
        print(f"n={k:>5}: iter={t1:.4f} math={t2:.4f} divconq={t3:.4f} ms  [math {t1/t2:.0f}x]")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    _benchmark()
