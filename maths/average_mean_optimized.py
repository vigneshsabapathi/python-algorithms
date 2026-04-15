#!/usr/bin/env python3
"""
Optimized mean variants.

Variants:
1. mean_fmean       -- statistics.fmean; C-level, handles floats properly.
2. mean_statistics  -- statistics.mean; uses Fractions, exact but slower.
3. mean_running     -- numerically stable online update (Welford-style).

Run:
    python maths/average_mean_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
import statistics

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.average_mean import mean as mean_reference


def mean_fmean(nums: list) -> float:
    """
    >>> mean_fmean([3, 6, 9, 12, 15, 18, 21])
    12.0
    """
    if not nums:
        raise ValueError("List is empty")
    return statistics.fmean(nums)


def mean_running(nums: list) -> float:
    """
    Numerically stable running mean.  Avoids overflow/precision loss from
    summing a large list.

    >>> mean_running([3, 6, 9, 12, 15, 18, 21])
    12.0
    >>> mean_running([2.0, 4.0, 6.0])
    4.0
    """
    if not nums:
        raise ValueError("List is empty")
    mu = 0.0
    for i, x in enumerate(nums, start=1):
        mu += (x - mu) / i
    return mu


def _benchmark() -> None:
    data = list(range(100_000))
    n = 500
    t1 = timeit.timeit(lambda: mean_reference(data), number=n) * 1000 / n
    t2 = timeit.timeit(lambda: mean_fmean(data), number=n) * 1000 / n
    t3 = timeit.timeit(lambda: statistics.mean(data), number=n) * 1000 / n
    t4 = timeit.timeit(lambda: mean_running(data), number=n) * 1000 / n
    print(f"sum/len: {t1:.3f} ms  fmean: {t2:.3f} ms  stats.mean: {t3:.3f} ms  running: {t4:.3f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
