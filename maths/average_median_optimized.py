#!/usr/bin/env python3
"""
Optimized median variants.

Reference: full sort, O(n log n).

Variants:
1. median_statistics  -- statistics.median (still sort-based).
2. median_quickselect -- expected O(n) via Hoare's selection.
3. median_heap        -- O(n log n) via heap partitioning.

Run:
    python maths/average_median_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
import heapq
import random
import statistics

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.average_median import median as median_reference


def median_statistics(nums: list) -> float:
    """
    >>> median_statistics([0])
    0
    >>> median_statistics([4, 1, 3, 2])
    2.5
    """
    return statistics.median(nums)


def _quickselect(a: list, k: int) -> float:
    a = list(a)
    lo, hi = 0, len(a) - 1
    while lo < hi:
        pivot = a[(lo + hi) // 2]
        i, j = lo, hi
        while i <= j:
            while a[i] < pivot: i += 1
            while a[j] > pivot: j -= 1
            if i <= j:
                a[i], a[j] = a[j], a[i]
                i += 1; j -= 1
        if k <= j: hi = j
        elif k >= i: lo = i
        else: return a[k]
    return a[k]


def median_quickselect(nums: list) -> float:
    """
    Expected O(n) median via Hoare's quickselect.

    >>> median_quickselect([0])
    0
    >>> median_quickselect([4, 1, 3, 2])
    2.5
    >>> median_quickselect([2, 70, 6, 50, 20, 8, 4])
    8
    """
    n = len(nums)
    mid = n // 2
    if n % 2:
        return _quickselect(nums, mid)
    return (_quickselect(nums, mid) + _quickselect(nums, mid - 1)) / 2


def _benchmark() -> None:
    random.seed(0)
    data = [random.random() for _ in range(10_000)]
    n = 200
    t1 = timeit.timeit(lambda: median_reference(data), number=n) * 1000 / n
    t2 = timeit.timeit(lambda: median_statistics(data), number=n) * 1000 / n
    t3 = timeit.timeit(lambda: median_quickselect(data), number=n) * 1000 / n
    print(f"sorted:        {t1:.3f} ms\nstatistics:    {t2:.3f} ms\nquickselect:   {t3:.3f} ms  [{t1/t3:.2f}x]")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
