#!/usr/bin/env python3
"""
Optimized and alternative implementations of Max Subarray Sum (Kadane's).

The reference is already O(n)/O(1) Kadane's. We explore alternatives
that appear in interviews at different difficulty levels.

Variants covered:
1. max_subarray_divide_conquer  -- O(n log n) divide-and-conquer
2. max_subarray_prefix_sum      -- prefix sum approach
3. max_subarray_with_indices    -- Kadane's that also returns start/end indices

Run:
    python dynamic_programming/max_subarray_sum_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.max_subarray_sum import max_subarray_sum as reference


# ---------------------------------------------------------------------------
# Variant 1 — Divide and conquer O(n log n)
# ---------------------------------------------------------------------------

def max_subarray_divide_conquer(nums: list[int]) -> int:
    """
    Max subarray sum using divide and conquer.

    Splits array in half, recursively finds max in left, right,
    and crossing subarrays.

    >>> max_subarray_divide_conquer([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    6
    >>> max_subarray_divide_conquer([1])
    1
    >>> max_subarray_divide_conquer([-1, -2, -3])
    -1
    >>> max_subarray_divide_conquer([5, 4, -1, 7, 8])
    23
    >>> max_subarray_divide_conquer([])
    0
    """
    if not nums:
        return 0

    def helper(lo: int, hi: int) -> int:
        if lo == hi:
            return nums[lo]
        mid = (lo + hi) // 2

        # Max crossing subarray
        left_sum = float("-inf")
        s = 0
        for i in range(mid, lo - 1, -1):
            s += nums[i]
            left_sum = max(left_sum, s)

        right_sum = float("-inf")
        s = 0
        for i in range(mid + 1, hi + 1):
            s += nums[i]
            right_sum = max(right_sum, s)

        cross = left_sum + right_sum
        return max(helper(lo, mid), helper(mid + 1, hi), cross)

    return helper(0, len(nums) - 1)


# ---------------------------------------------------------------------------
# Variant 2 — Prefix sum approach
# ---------------------------------------------------------------------------

def max_subarray_prefix_sum(nums: list[int]) -> int:
    """
    Max subarray sum using prefix sums.

    max_subarray = max over all j of (prefix[j] - min prefix[0..j-1])

    >>> max_subarray_prefix_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    6
    >>> max_subarray_prefix_sum([1])
    1
    >>> max_subarray_prefix_sum([-1, -2, -3])
    -1
    >>> max_subarray_prefix_sum([5, 4, -1, 7, 8])
    23
    >>> max_subarray_prefix_sum([])
    0
    """
    if not nums:
        return 0
    max_sum = nums[0]
    prefix = 0
    min_prefix = 0
    for num in nums:
        prefix += num
        max_sum = max(max_sum, prefix - min_prefix)
        min_prefix = min(min_prefix, prefix)
    return max_sum


# ---------------------------------------------------------------------------
# Variant 3 — Kadane's with indices
# ---------------------------------------------------------------------------

def max_subarray_with_indices(nums: list[int]) -> tuple[int, int, int]:
    """
    Kadane's algorithm returning (max_sum, start_index, end_index).

    >>> max_subarray_with_indices([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    (6, 3, 6)
    >>> max_subarray_with_indices([1])
    (1, 0, 0)
    >>> max_subarray_with_indices([-1, -2, -3])
    (-1, 0, 0)
    >>> max_subarray_with_indices([5, 4, -1, 7, 8])
    (23, 0, 4)
    >>> max_subarray_with_indices([])
    (0, -1, -1)
    """
    if not nums:
        return (0, -1, -1)

    max_sum = nums[0]
    current_sum = nums[0]
    start = end = temp_start = 0

    for i in range(1, len(nums)):
        if current_sum + nums[i] < nums[i]:
            current_sum = nums[i]
            temp_start = i
        else:
            current_sum += nums[i]
        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i

    return (max_sum, start, end)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
    ([1], 1),
    ([-1, -2, -3], -1),
    ([5, 4, -1, 7, 8], 23),
    ([-2, -3, 4, -1, -2, 1, 5, -3], 7),
    ([], 0),
]

IMPLS = [
    ("reference", reference),
    ("divide_conquer", max_subarray_divide_conquer),
    ("prefix_sum", max_subarray_prefix_sum),
    ("with_indices", lambda nums: max_subarray_with_indices(nums)[0]),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for nums, expected in TEST_CASES:
        results = {name: fn(list(nums)) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] nums={nums!r}  expected={expected}  " +
              "  ".join(f"{n}={v}" for n, v in results.items()))

    REPS = 50_000
    bench_input = list(range(-10, 20)) + list(range(-5, 15))
    print(f"\n=== Benchmark: {REPS} runs, len={len(bench_input)} ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(bench_input), number=REPS) * 1000 / REPS
        print(f"  {name:<16} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
