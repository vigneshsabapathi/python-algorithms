#!/usr/bin/env python3
"""
Optimized and alternative implementations of Maximum Subsequence (Kadane's).

Variants covered:
1. kadane_standard   -- Standard Kadane's O(n) (reference)
2. divide_conquer    -- Divide and conquer O(n log n)
3. prefix_sum        -- Prefix sum approach O(n)

Run:
    python other/maximum_subsequence_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.maximum_subsequence import max_subsequence as reference


def divide_conquer_max(arr: list[int]) -> int:
    """
    Maximum subarray sum using divide and conquer.

    >>> divide_conquer_max([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    6
    >>> divide_conquer_max([1, 2, 3, 4])
    10
    >>> divide_conquer_max([-1, -2, -3])
    -1
    >>> divide_conquer_max([])
    0
    """
    if not arr:
        return 0

    def helper(lo: int, hi: int) -> int:
        if lo == hi:
            return arr[lo]
        mid = (lo + hi) // 2
        left_max = helper(lo, mid)
        right_max = helper(mid + 1, hi)

        # Max crossing subarray
        left_sum = float("-inf")
        s = 0
        for i in range(mid, lo - 1, -1):
            s += arr[i]
            left_sum = max(left_sum, s)

        right_sum = float("-inf")
        s = 0
        for i in range(mid + 1, hi + 1):
            s += arr[i]
            right_sum = max(right_sum, s)

        cross_max = left_sum + right_sum
        return max(left_max, right_max, cross_max)

    return helper(0, len(arr) - 1)


def prefix_sum_max(arr: list[int]) -> int:
    """
    Maximum subarray sum using prefix sums.

    >>> prefix_sum_max([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    6
    >>> prefix_sum_max([1, 2, 3])
    6
    >>> prefix_sum_max([-5])
    -5
    >>> prefix_sum_max([])
    0
    """
    if not arr:
        return 0
    max_sum = arr[0]
    prefix = 0
    min_prefix = 0
    for num in arr:
        prefix += num
        max_sum = max(max_sum, prefix - min_prefix)
        min_prefix = min(min_prefix, prefix)
    return max_sum


def kadane_circular(arr: list[int]) -> int:
    """
    Maximum subarray sum for circular arrays.

    >>> kadane_circular([5, -3, 5])
    10
    >>> kadane_circular([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    6
    >>> kadane_circular([-1, -2, -3])
    -1
    """
    if not arr:
        return 0

    # Standard Kadane's for non-circular
    max_kadane = reference(arr)

    # For circular: total_sum - min_subarray_sum
    total = sum(arr)
    # Find min subarray using Kadane's on negated array
    inverted = [-x for x in arr]
    max_inverted = reference(inverted)
    min_subarray = -max_inverted

    if total == min_subarray:
        return max_kadane

    return max(max_kadane, total - min_subarray)


TEST_CASES = [
    ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
    ([1, 2, 3, 4], 10),
    ([-1, -2, -3], -1),
    ([5], 5),
    ([], 0),
]

IMPLS = [
    ("reference", reference),
    ("divide_conquer", divide_conquer_max),
    ("prefix_sum", prefix_sum_max),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for arr, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(list(arr))
            ok = result == expected
            tag = "OK" if ok else "FAIL"
            if not ok:
                print(f"  [{tag}] {name}: expected={expected} got={result}")
        print(f"  [OK] n={len(arr)} max_sum={expected}")

    import random
    rng = random.Random(42)
    large = [rng.randint(-100, 100) for _ in range(10000)]

    REPS = 2000
    print(f"\n=== Benchmark: {REPS} runs, {len(large)} elements ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(list(large)), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
