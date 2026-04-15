#!/usr/bin/env python3
"""
Optimized euclidean_distance variants.

Reference already has numpy and pure-python versions.

Variants:
1. ed_math_hypot  -- math.hypot(*(a-b for a,b in zip)) — C-level, accurate.
2. ed_dot         -- sqrt(sum((a-b)**2)) with pre-subtracted list.
3. ed_numpy_opt   -- np.linalg.norm(a-b).

Run:
    python maths/euclidean_distance_optimized.py
"""

from __future__ import annotations

import sys
import os
import math
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.euclidean_distance import euclidean_distance as ed_np, euclidean_distance_no_np as ed_nonp


def ed_math_hypot(v1, v2) -> float:
    """
    math.hypot handles overflow better than sum-of-squares.

    >>> round(ed_math_hypot((0, 0), (2, 2)), 10)
    2.8284271247
    >>> round(ed_math_hypot([1, 2, 3, 4], [5, 6, 7, 8]), 10)
    8.0
    """
    return math.hypot(*(a - b for a, b in zip(v1, v2)))


def ed_dist(v1, v2) -> float:
    """
    math.dist (Python 3.8+) — C-level, best for pure python.

    >>> round(ed_dist((0, 0), (2, 2)), 10)
    2.8284271247
    """
    return math.dist(v1, v2)


def _benchmark() -> None:
    a = list(range(100))
    b = list(range(100, 200))
    n = 10000
    t1 = timeit.timeit(lambda: ed_nonp(a, b), number=n) * 1000 / n
    t2 = timeit.timeit(lambda: ed_math_hypot(a, b), number=n) * 1000 / n
    t3 = timeit.timeit(lambda: ed_dist(a, b), number=n) * 1000 / n
    print(f"reference (no-np): {t1:.4f} ms")
    print(f"math.hypot:        {t2:.4f} ms  [{t1/t2:.2f}x]")
    print(f"math.dist:         {t3:.4f} ms  [{t1/t3:.2f}x]")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    _benchmark()
