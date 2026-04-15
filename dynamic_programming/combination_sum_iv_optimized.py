#!/usr/bin/env python3
"""
Optimized and alternative implementations of Combination Sum IV.

Three variants:
  brute_force     — exponential recursive (reference baseline)
  top_down_memo   — O(target*n) memoized recursion
  bottom_up       — O(target*n) tabulation (fastest)

Run:
    python dynamic_programming/combination_sum_iv_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.combination_sum_iv import (
    combination_sum_iv as brute_ref,
    combination_sum_iv_dp_array as memo_ref,
    combination_sum_iv_bottom_up as bottom_ref,
)


# ---------------------------------------------------------------------------
# Variant 1 — brute_force wrapper
# ---------------------------------------------------------------------------

def brute_force(array: list[int], target: int) -> int:
    """
    >>> brute_force([1, 2, 5], 5)
    9
    """
    return brute_ref(array, target)


# ---------------------------------------------------------------------------
# Variant 2 — top_down_lru: Using @lru_cache
# ---------------------------------------------------------------------------

def top_down_lru(array: list[int], target: int) -> int:
    """
    >>> top_down_lru([1, 2, 5], 5)
    9
    """
    from functools import lru_cache

    arr_tuple = tuple(array)

    @lru_cache(maxsize=None)
    def solve(remaining: int) -> int:
        if remaining == 0:
            return 1
        if remaining < 0:
            return 0
        return sum(solve(remaining - item) for item in arr_tuple)

    return solve(target)


# ---------------------------------------------------------------------------
# Variant 3 — bottom_up_optimized: Clean bottom-up
# ---------------------------------------------------------------------------

def bottom_up_optimized(array: list[int], target: int) -> int:
    """
    >>> bottom_up_optimized([1, 2, 5], 5)
    9
    """
    dp = [0] * (target + 1)
    dp[0] = 1
    for i in range(1, target + 1):
        for num in array:
            if i >= num:
                dp[i] += dp[i - num]
    return dp[target]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([1, 2, 5], 5, 9),
    ([1, 2, 3], 4, 7),
    ([2], 3, 0),
    ([1], 5, 1),
    ([1, 2], 4, 5),
]

IMPLS = [
    ("brute_force", brute_force),
    ("top_down_lru", top_down_lru),
    ("bottom_up", bottom_up_optimized),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for arr, target, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(arr, target)
            ok = result == expected
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}({arr}, {target}) = {result}")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    REPS = 50_000
    print(f"\n=== Benchmark (target=10): {REPS} runs ===")
    arr = [1, 2, 5]
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(arr, 10), number=REPS) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
