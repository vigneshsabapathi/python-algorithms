#!/usr/bin/env python3
"""
Optimized check_polygon variants.

Reference: sorts full list, O(n log n), then compares largest vs sum-of-rest.

Variants:
1. poly_max_sum   -- O(n) single pass: max + sum, then largest < sum-largest.
2. poly_recursive -- educational reformulation.

Run:
    python maths/check_polygon_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.check_polygon import check_polygon as ref


def poly_max_sum(nums: list[float]) -> bool:
    """
    O(n) — single pass for max and sum, then `max < total - max`.

    >>> poly_max_sum([6, 10, 5])
    True
    >>> poly_max_sum([3, 7, 13, 2])
    False
    >>> poly_max_sum([1, 4.3, 5.2, 12.2])
    False
    >>> poly_max_sum([])
    Traceback (most recent call last):
        ...
    ValueError: Monogons and Digons are not polygons in the Euclidean space
    >>> poly_max_sum([-2, 5, 6])
    Traceback (most recent call last):
        ...
    ValueError: All values must be greater than 0
    """
    if len(nums) < 2:
        raise ValueError("Monogons and Digons are not polygons in the Euclidean space")
    if any(i <= 0 for i in nums):
        raise ValueError("All values must be greater than 0")
    total = 0.0
    largest = nums[0]
    for v in nums:
        total += v
        if v > largest:
            largest = v
    return largest < total - largest


def _benchmark() -> None:
    import random
    random.seed(0)
    data = [random.random() * 10 + 0.01 for _ in range(1000)]
    n = 2000
    t1 = timeit.timeit(lambda: ref(data), number=n) * 1000 / n
    t2 = timeit.timeit(lambda: poly_max_sum(data), number=n) * 1000 / n
    print(f"reference sort:  {t1:.4f} ms")
    print(f"max-sum O(n):    {t2:.4f} ms  [{t1/t2:.2f}x]")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
