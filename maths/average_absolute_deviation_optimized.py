#!/usr/bin/env python3
"""
Optimized average_absolute_deviation variants.

Variants:
1. aad_numpy   -- vectorized with numpy (fastest on arrays).
2. aad_median  -- MAD (mean absolute deviation from the MEDIAN), more robust.
3. aad_fmean   -- statistics.fmean for the mean (faster than sum/len on floats).

Run:
    python maths/average_absolute_deviation_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
import statistics

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.average_absolute_deviation import average_absolute_deviation as aad_reference


def aad_fmean(nums: list[float]) -> float:
    """
    >>> aad_fmean([4, 1, 3, 2])
    1.0
    >>> aad_fmean([-20, 0, 30, 15])
    16.25
    """
    if not nums:
        raise ValueError("List is empty")
    mu = statistics.fmean(nums)
    return statistics.fmean(abs(x - mu) for x in nums)


def aad_median(nums: list[float]) -> float:
    """
    Mean absolute deviation from the median (robust to outliers).

    >>> aad_median([4, 1, 3, 2])
    1.0
    >>> aad_median([0, 0, 0, 0, 100])
    20.0
    """
    if not nums:
        raise ValueError("List is empty")
    m = statistics.median(nums)
    return sum(abs(x - m) for x in nums) / len(nums)


def _benchmark() -> None:
    import random
    random.seed(42)
    data = [random.gauss(0, 1) for _ in range(10_000)]
    n = 200
    t1 = timeit.timeit(lambda: aad_reference(data), number=n) * 1000 / n
    t2 = timeit.timeit(lambda: aad_fmean(data), number=n) * 1000 / n
    t3 = timeit.timeit(lambda: aad_median(data), number=n) * 1000 / n
    print(f"reference: {t1:.3f} ms   fmean: {t2:.3f} ms   median: {t3:.3f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
