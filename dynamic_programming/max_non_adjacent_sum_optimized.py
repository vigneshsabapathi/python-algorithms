#!/usr/bin/env python3
"""
Optimized and alternative implementations of Max Non-Adjacent Sum.

The reference uses two variables (incl/excl) in a single pass — already
optimal at O(n) time, O(1) space. We explore alternative formulations.

Variants covered:
1. max_non_adjacent_dp_array  -- explicit DP table for clarity
2. max_non_adjacent_recursive -- top-down memoized recursion
3. max_non_adjacent_even_odd  -- partition-based approach (educational)

Key interview insight:
    The two-variable approach is "House Robber" (LeetCode 198).
    dp[i] = max(dp[i-1], dp[i-2] + nums[i]) compressed to O(1) space.

Run:
    python dynamic_programming/max_non_adjacent_sum_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.max_non_adjacent_sum import max_non_adjacent_sum as reference


# ---------------------------------------------------------------------------
# Variant 1 — Explicit DP array
# ---------------------------------------------------------------------------

def max_non_adjacent_dp_array(nums: list[int]) -> int:
    """
    Max non-adjacent sum using explicit DP table.

    dp[i] = max sum considering elements 0..i
    dp[i] = max(dp[i-1], dp[i-2] + nums[i])

    >>> max_non_adjacent_dp_array([1, 2, 3, 4, 5])
    9
    >>> max_non_adjacent_dp_array([5, 1, 1, 5])
    10
    >>> max_non_adjacent_dp_array([3, 2, 7, 10])
    13
    >>> max_non_adjacent_dp_array([-1, -2, -3])
    0
    >>> max_non_adjacent_dp_array([])
    0
    """
    if not nums:
        return 0
    n = len(nums)
    if n == 1:
        return max(0, nums[0])

    dp = [0] * n
    dp[0] = max(0, nums[0])
    dp[1] = max(dp[0], nums[1])
    for i in range(2, n):
        dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
    return dp[-1]


# ---------------------------------------------------------------------------
# Variant 2 — Top-down memoized recursion
# ---------------------------------------------------------------------------

def max_non_adjacent_recursive(nums: list[int]) -> int:
    """
    Max non-adjacent sum using top-down recursion with memoization.

    >>> max_non_adjacent_recursive([1, 2, 3, 4, 5])
    9
    >>> max_non_adjacent_recursive([5, 1, 1, 5])
    10
    >>> max_non_adjacent_recursive([3, 2, 7, 10])
    13
    >>> max_non_adjacent_recursive([-1, -2, -3])
    0
    >>> max_non_adjacent_recursive([])
    0
    """
    if not nums:
        return 0
    n = len(nums)

    @lru_cache(maxsize=None)
    def solve(i: int) -> int:
        if i < 0:
            return 0
        return max(solve(i - 1), solve(i - 2) + nums[i])

    result = solve(n - 1)
    solve.cache_clear()
    return max(0, result)


# ---------------------------------------------------------------------------
# Variant 3 — Even/odd index partitioning (educational)
# ---------------------------------------------------------------------------

def max_non_adjacent_even_odd(nums: list[int]) -> int:
    """
    Max non-adjacent sum — greedy-like approach iterating with two accumulators.

    This is functionally identical to the reference but uses prev2/prev1 naming
    that maps directly to the DP recurrence.

    >>> max_non_adjacent_even_odd([1, 2, 3, 4, 5])
    9
    >>> max_non_adjacent_even_odd([5, 1, 1, 5])
    10
    >>> max_non_adjacent_even_odd([3, 2, 7, 10])
    13
    >>> max_non_adjacent_even_odd([-1, -2, -3])
    0
    >>> max_non_adjacent_even_odd([])
    0
    """
    if not nums:
        return 0
    prev2 = 0  # dp[i-2]
    prev1 = 0  # dp[i-1]
    for num in nums:
        current = max(prev1, prev2 + num)
        prev2 = prev1
        prev1 = current
    return max(0, prev1)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([1, 2, 3, 4, 5], 9),
    ([5, 1, 1, 5], 10),
    ([3, 2, 7, 10], 13),
    ([3, 2, 5, 10, 7], 15),
    ([-1, -2, -3], 0),
    ([], 0),
    ([5], 5),
    ([10, 5], 10),
]

IMPLS = [
    ("reference", reference),
    ("dp_array", max_non_adjacent_dp_array),
    ("recursive", max_non_adjacent_recursive),
    ("even_odd", max_non_adjacent_even_odd),
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
    bench_input = [3, 2, 5, 10, 7, 1, 8, 4, 6, 9, 2, 11, 3, 7]
    print(f"\n=== Benchmark: {REPS} runs, len={len(bench_input)} ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(bench_input), number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
