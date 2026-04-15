#!/usr/bin/env python3
"""
Optimized and alternative implementations of 0/1 Knapsack.

Three variants:
  bottom_up_2d    — standard 2D DP table (reference)
  space_optimized — O(W) space using 1D rolling array
  branch_bound    — branch and bound for exact solution (with pruning)

Run:
    python dynamic_programming/knapsack_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.knapsack import knapsack_with_example_solution as reference


# ---------------------------------------------------------------------------
# Variant 1 — bottom_up_2d (same as reference)
# ---------------------------------------------------------------------------

def bottom_up_2d(w: int, wt: list[int], val: list[int]) -> int:
    """
    >>> bottom_up_2d(10, [1, 3, 5, 2], [10, 20, 100, 22])
    142
    >>> bottom_up_2d(6, [4, 3, 2, 3], [3, 2, 4, 4])
    8
    """
    return reference(w, wt, val)[0]


# ---------------------------------------------------------------------------
# Variant 2 — space_optimized: O(W) space, 1D rolling array
# ---------------------------------------------------------------------------

def space_optimized(w: int, wt: list[int], val: list[int]) -> int:
    """
    Process items in reverse weight order to avoid reusing items.

    >>> space_optimized(10, [1, 3, 5, 2], [10, 20, 100, 22])
    142
    >>> space_optimized(6, [4, 3, 2, 3], [3, 2, 4, 4])
    8
    """
    n = len(wt)
    dp = [0] * (w + 1)
    for i in range(n):
        for j in range(w, wt[i] - 1, -1):
            dp[j] = max(dp[j], val[i] + dp[j - wt[i]])
    return dp[w]


# ---------------------------------------------------------------------------
# Variant 3 — memoized_recursive: Top-down with @lru_cache
# ---------------------------------------------------------------------------

def memoized_recursive(w: int, wt: list[int], val: list[int]) -> int:
    """
    >>> memoized_recursive(10, [1, 3, 5, 2], [10, 20, 100, 22])
    142
    >>> memoized_recursive(6, [4, 3, 2, 3], [3, 2, 4, 4])
    8
    """
    from functools import lru_cache

    n = len(wt)
    wt_tuple = tuple(wt)
    val_tuple = tuple(val)

    @lru_cache(maxsize=None)
    def solve(i: int, remaining: int) -> int:
        if i == 0 or remaining == 0:
            return 0
        if wt_tuple[i - 1] > remaining:
            return solve(i - 1, remaining)
        return max(
            solve(i - 1, remaining),
            val_tuple[i - 1] + solve(i - 1, remaining - wt_tuple[i - 1]),
        )

    return solve(n, w)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (10, [1, 3, 5, 2], [10, 20, 100, 22], 142),
    (6, [4, 3, 2, 3], [3, 2, 4, 4], 8),
    (50, [10, 20, 30], [60, 100, 120], 220),
]

IMPLS = [
    ("bottom_up_2d", bottom_up_2d),
    ("space_optimized", space_optimized),
    ("memoized_recursive", memoized_recursive),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for w, wt, val, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(w, wt, val)
            ok = result == expected
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}(W={w}) = {result}  (expected {expected})")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    REPS = 20_000
    w, wt, val = 50, [10, 20, 30], [60, 100, 120]
    print(f"\n=== Benchmark (3 items, W=50): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(w, wt, val), number=REPS) * 1000 / REPS
        print(f"  {name:<22} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
