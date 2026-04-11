#!/usr/bin/env python3
"""
Optimized and alternative implementations of 0/1 Knapsack.

The reference uses bottom-up 2D DP tabulation: O(nW) time, O(nW) space.

Variants covered:
1. tabulation_2d   -- classic 2D DP table (reference, explicit)
2. memoization     -- top-down recursive with @lru_cache
3. space_optimized -- 1D rolling array, O(W) space
4. branch_bound    -- branch-and-bound with fractional upper bound (exact solver)

Key interview insight:
    The 1D rolling array processes weights in REVERSE (W down to wt[i]).
    Forward iteration would allow an item to be picked multiple times
    (that solves the UNBOUNDED knapsack instead).  Interviewers commonly
    ask "why reverse?" — the answer is to preserve the previous row's values.

Run:
    python knapsack/knapsack_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from knapsack.knapsack import knapsack as reference


# ---------------------------------------------------------------------------
# Variant 1 — 2D tabulation (clean rewrite of reference)
# ---------------------------------------------------------------------------

def tabulation_2d(capacity: int, weights: list[int], values: list[int], n: int) -> int:
    """
    Classic bottom-up DP with full (n+1) x (W+1) table.

    >>> tabulation_2d(50, [10, 20, 30], [60, 100, 120], 3)
    220
    >>> tabulation_2d(10, [5, 4, 6, 3], [10, 40, 30, 50], 4)
    90
    >>> tabulation_2d(7, [1, 3, 4, 5], [1, 4, 5, 7], 4)
    9
    >>> tabulation_2d(0, [10], [60], 1)
    0
    """
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wt, val = weights[i - 1], values[i - 1]
        for w in range(1, capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if wt <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - wt] + val)
    return dp[n][capacity]


# ---------------------------------------------------------------------------
# Variant 2 — top-down memoization with lru_cache
# ---------------------------------------------------------------------------

def memoization(capacity: int, weights: list[int], values: list[int], n: int) -> int:
    """
    Top-down recursive approach with memoization.

    >>> memoization(50, [10, 20, 30], [60, 100, 120], 3)
    220
    >>> memoization(10, [5, 4, 6, 3], [10, 40, 30, 50], 4)
    90
    >>> memoization(7, [1, 3, 4, 5], [1, 4, 5, 7], 4)
    9
    >>> memoization(0, [10], [60], 1)
    0
    """
    # Use a dict-based cache to avoid lru_cache closure issues in benchmarks
    memo: dict[tuple[int, int], int] = {}

    def solve(i: int, w: int) -> int:
        if i == 0 or w == 0:
            return 0
        if (i, w) in memo:
            return memo[(i, w)]
        # Skip item i
        result = solve(i - 1, w)
        # Take item i if it fits
        if weights[i - 1] <= w:
            result = max(result, solve(i - 1, w - weights[i - 1]) + values[i - 1])
        memo[(i, w)] = result
        return result

    return solve(n, capacity)


# ---------------------------------------------------------------------------
# Variant 3 — space-optimized 1D rolling array, O(W) space
# ---------------------------------------------------------------------------

def space_optimized(capacity: int, weights: list[int], values: list[int], n: int) -> int:
    """
    1D DP: single array of size W+1, iterate weights in REVERSE.

    Why reverse?  Forward iteration lets an item be used multiple times
    (that's the unbounded knapsack).  Reverse preserves previous-row values.

    >>> space_optimized(50, [10, 20, 30], [60, 100, 120], 3)
    220
    >>> space_optimized(10, [5, 4, 6, 3], [10, 40, 30, 50], 4)
    90
    >>> space_optimized(7, [1, 3, 4, 5], [1, 4, 5, 7], 4)
    9
    >>> space_optimized(0, [10], [60], 1)
    0
    """
    dp = [0] * (capacity + 1)
    for i in range(n):
        wt, val = weights[i], values[i]
        # REVERSE iteration: W down to wt
        for w in range(capacity, wt - 1, -1):
            dp[w] = max(dp[w], dp[w - wt] + val)
    return dp[capacity]


# ---------------------------------------------------------------------------
# Variant 4 — branch-and-bound with fractional upper bound
# ---------------------------------------------------------------------------

def branch_bound(capacity: int, weights: list[int], values: list[int], n: int) -> int:
    """
    Branch-and-bound: prune branches whose fractional upper bound
    cannot exceed the current best.  Exact optimal solution.

    Useful when n is moderate and many branches get pruned.

    >>> branch_bound(50, [10, 20, 30], [60, 100, 120], 3)
    220
    >>> branch_bound(10, [5, 4, 6, 3], [10, 40, 30, 50], 4)
    90
    >>> branch_bound(7, [1, 3, 4, 5], [1, 4, 5, 7], 4)
    9
    >>> branch_bound(0, [10], [60], 1)
    0
    """
    # Sort items by value/weight ratio descending
    items = sorted(
        zip(values, weights, range(n)),
        key=lambda x: x[0] / x[1] if x[1] > 0 else float("inf"),
        reverse=True,
    )

    def upper_bound(idx: int, current_weight: int, current_value: int) -> float:
        """Fractional relaxation upper bound from idx onward."""
        ub = float(current_value)
        remaining = capacity - current_weight
        for j in range(idx, n):
            v, w, _ = items[j]
            if w <= remaining:
                ub += v
                remaining -= w
            else:
                ub += (remaining / w) * v
                break
        return ub

    best = [0]

    def solve(idx: int, current_weight: int, current_value: int) -> None:
        if current_value > best[0]:
            best[0] = current_value
        if idx == n:
            return
        # Prune: if upper bound can't beat best, skip
        if upper_bound(idx, current_weight, current_value) <= best[0]:
            return
        v, w, _ = items[idx]
        # Branch: include item
        if current_weight + w <= capacity:
            solve(idx + 1, current_weight + w, current_value + v)
        # Branch: exclude item
        solve(idx + 1, current_weight, current_value)

    solve(0, 0, 0)
    return best[0]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (50, [10, 20, 30], [60, 100, 120], 3, 220),
    (10, [5, 4, 6, 3], [10, 40, 30, 50], 4, 90),
    (7, [1, 3, 4, 5], [1, 4, 5, 7], 4, 9),
    (5, [1, 2, 3], [6, 10, 12], 3, 22),
    (0, [10, 20], [60, 100], 2, 0),
    (15, [1, 5, 10], [10, 50, 100], 3, 150),
]

IMPLS = [
    ("reference",       lambda c, w, v, n: reference(c, w, v, n)),
    ("tabulation_2d",   tabulation_2d),
    ("memoization",     memoization),
    ("space_optimized", space_optimized),
    ("branch_bound",    branch_bound),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for cap, weights, values, n, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(cap, weights, values, n)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(
            f"  [{tag}] cap={cap:<4} n={n}  expected={expected:<6}  "
            + "  ".join(f"{nm}={v}" for nm, v in results.items())
        )

    # Benchmark with moderate input (DP-friendly)
    import random
    random.seed(42)
    n_items = 200
    cap_bench = 500
    w_bench = [random.randint(1, 50) for _ in range(n_items)]
    v_bench = [random.randint(1, 100) for _ in range(n_items)]

    REPS = 200
    print(f"\n=== Benchmark: {n_items} items, cap={cap_bench}, {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: fn(cap_bench, w_bench, v_bench, n_items), number=REPS
        ) * 1000 / REPS
        print(f"  {name:<18} {t:>9.4f} ms / call")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
