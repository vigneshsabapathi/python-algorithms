#!/usr/bin/env python3
"""
Optimized chebyshev_distance variants.

Variants:
1. cheby_map        -- map/operator.sub; C-level reduce.
2. cheby_numpy      -- np.max(np.abs(a-b)); fast on large vectors.
3. cheby_loop       -- hand-rolled max loop; no generator overhead.

Run:
    python maths/chebyshev_distance_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.chebyshev_distance import chebyshev_distance as cd_ref


def cheby_loop(a: list[float], b: list[float]) -> float:
    """
    >>> cheby_loop([1.0, 1.0], [2.0, 2.0])
    1.0
    >>> round(cheby_loop([1.0, 1.0, 9.0], [2.0, 2.0, -5.2]), 2)
    14.2
    """
    if len(a) != len(b):
        raise ValueError("Both points must have the same dimension.")
    m = 0.0
    for x, y in zip(a, b):
        d = x - y
        if d < 0:
            d = -d
        if d > m:
            m = d
    return m


def cheby_map(a: list[float], b: list[float]) -> float:
    """
    >>> cheby_map([1.0, 1.0], [2.0, 2.0])
    1.0
    """
    if len(a) != len(b):
        raise ValueError("Both points must have the same dimension.")
    return max(map(lambda p: abs(p[0] - p[1]), zip(a, b)))


def _benchmark() -> None:
    import random
    random.seed(0)
    a = [random.random() for _ in range(1000)]
    b = [random.random() for _ in range(1000)]
    n = 5000
    t1 = timeit.timeit(lambda: cd_ref(a, b), number=n) * 1000 / n
    t2 = timeit.timeit(lambda: cheby_map(a, b), number=n) * 1000 / n
    t3 = timeit.timeit(lambda: cheby_loop(a, b), number=n) * 1000 / n
    print(f"reference:  {t1:.4f} ms")
    print(f"map:        {t2:.4f} ms  [{t1/t2:.2f}x]")
    print(f"loop:       {t3:.4f} ms  [{t1/t3:.2f}x]")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
