#!/usr/bin/env python3
"""
Optimized and alternative implementations of Sum of Subset (Subset Sum).

Variants covered:
1. subset_sum_1d        -- O(target) space using 1D array
2. subset_sum_bitset    -- Python int as bitset
3. subset_sum_backtrack -- backtracking with pruning

Run:
    python dynamic_programming/sum_of_subset_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.sum_of_subset import is_subset_sum as reference


# ---------------------------------------------------------------------------
# Variant 1 — 1D DP array
# ---------------------------------------------------------------------------

def subset_sum_1d(nums: list[int], target: int) -> bool:
    """
    Subset sum using O(target) space.

    >>> subset_sum_1d([3, 34, 4, 12, 5, 2], 9)
    True
    >>> subset_sum_1d([3, 34, 4, 12, 5, 2], 30)
    False
    >>> subset_sum_1d([1, 2, 3], 6)
    True
    >>> subset_sum_1d([], 0)
    True
    """
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for j in range(target, num - 1, -1):
            if dp[j - num]:
                dp[j] = True
    return dp[target]


# ---------------------------------------------------------------------------
# Variant 2 — Bitset approach
# ---------------------------------------------------------------------------

def subset_sum_bitset(nums: list[int], target: int) -> bool:
    """
    Subset sum using a single integer as a bitset.

    >>> subset_sum_bitset([3, 34, 4, 12, 5, 2], 9)
    True
    >>> subset_sum_bitset([3, 34, 4, 12, 5, 2], 30)
    False
    >>> subset_sum_bitset([1, 2, 3], 6)
    True
    >>> subset_sum_bitset([], 0)
    True
    """
    bits = 1
    for num in nums:
        bits |= bits << num
    return bool(bits & (1 << target))


# ---------------------------------------------------------------------------
# Variant 3 — Backtracking with pruning
# ---------------------------------------------------------------------------

def subset_sum_backtrack(nums: list[int], target: int) -> bool:
    """
    Subset sum using backtracking with sorting and pruning.

    >>> subset_sum_backtrack([3, 34, 4, 12, 5, 2], 9)
    True
    >>> subset_sum_backtrack([3, 34, 4, 12, 5, 2], 30)
    False
    >>> subset_sum_backtrack([1, 2, 3], 6)
    True
    >>> subset_sum_backtrack([], 0)
    True
    """
    nums_sorted = sorted(nums)

    def backtrack(idx: int, remaining: int) -> bool:
        if remaining == 0:
            return True
        if idx >= len(nums_sorted) or remaining < 0:
            return False
        if nums_sorted[idx] > remaining:
            return False
        return (backtrack(idx + 1, remaining - nums_sorted[idx]) or
                backtrack(idx + 1, remaining))

    return backtrack(0, target)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([3, 34, 4, 12, 5, 2], 9, True),
    ([3, 34, 4, 12, 5, 2], 30, False),
    ([1, 2, 3], 6, True),
    ([1, 2, 3], 7, False),
    ([], 0, True),
    ([], 1, False),
]

IMPLS = [
    ("reference", reference),
    ("1d_dp", subset_sum_1d),
    ("bitset", subset_sum_bitset),
    ("backtrack", subset_sum_backtrack),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for nums, target, expected in TEST_CASES:
        results = {name: fn(list(nums), target) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] nums={nums}, target={target}  expected={expected}  " +
              "  ".join(f"{n}={v}" for n, v in results.items()))

    REPS = 10_000
    bench_nums = [3, 34, 4, 12, 5, 2, 7, 8, 1, 15, 20, 6]
    bench_target = 50
    print(f"\n=== Benchmark: {REPS} runs, len={len(bench_nums)}, target={bench_target} ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(bench_nums, bench_target), number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
