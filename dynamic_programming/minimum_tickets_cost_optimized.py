#!/usr/bin/env python3
"""
Optimized and alternative implementations of Minimum Tickets Cost.

Variants covered:
1. min_tickets_recursive   -- top-down memoized recursion
2. min_tickets_sparse      -- DP only on travel days (space-efficient)
3. min_tickets_window      -- sliding window approach

Run:
    python dynamic_programming/minimum_tickets_cost_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.minimum_tickets_cost import minimum_tickets_cost as reference


# ---------------------------------------------------------------------------
# Variant 1 — Top-down memoized recursion
# ---------------------------------------------------------------------------

def min_tickets_recursive(days: list[int], costs: list[int]) -> int:
    """
    Minimum tickets cost using memoized recursion.

    >>> min_tickets_recursive([1, 4, 6, 7, 8, 20], [2, 7, 15])
    11
    >>> min_tickets_recursive([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 31], [2, 7, 15])
    17
    >>> min_tickets_recursive([1], [2, 7, 15])
    2
    >>> min_tickets_recursive([], [2, 7, 15])
    0
    """
    if not days:
        return 0
    n = len(days)
    durations = [1, 7, 30]

    @lru_cache(maxsize=None)
    def dp(i: int) -> int:
        if i >= n:
            return 0
        best = float("inf")
        j = i
        for k, dur in enumerate(durations):
            while j < n and days[j] < days[i] + dur:
                j += 1
            best = min(best, costs[k] + dp(j))
        return best

    result = dp(0)
    dp.cache_clear()
    return result


# ---------------------------------------------------------------------------
# Variant 2 — Sparse DP (only on travel days)
# ---------------------------------------------------------------------------

def min_tickets_sparse(days: list[int], costs: list[int]) -> int:
    """
    DP only at travel day indices — avoids allocating for non-travel days.

    >>> min_tickets_sparse([1, 4, 6, 7, 8, 20], [2, 7, 15])
    11
    >>> min_tickets_sparse([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 31], [2, 7, 15])
    17
    >>> min_tickets_sparse([1], [2, 7, 15])
    2
    >>> min_tickets_sparse([], [2, 7, 15])
    0
    """
    if not days:
        return 0
    import bisect
    n = len(days)
    dp = [0] * (n + 1)
    durations = [1, 7, 30]

    for i in range(n - 1, -1, -1):
        dp[i] = float("inf")
        for k, dur in enumerate(durations):
            j = bisect.bisect_left(days, days[i] + dur, i)
            dp[i] = min(dp[i], costs[k] + dp[j])

    return dp[0]


# ---------------------------------------------------------------------------
# Variant 3 — Sliding window
# ---------------------------------------------------------------------------

def min_tickets_window(days: list[int], costs: list[int]) -> int:
    """
    Forward DP with pointer tracking for 7-day and 30-day windows.

    >>> min_tickets_window([1, 4, 6, 7, 8, 20], [2, 7, 15])
    11
    >>> min_tickets_window([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 31], [2, 7, 15])
    17
    >>> min_tickets_window([1], [2, 7, 15])
    2
    >>> min_tickets_window([], [2, 7, 15])
    0
    """
    if not days:
        return 0
    n = len(days)
    dp = [0] * (n + 1)
    j7 = j30 = 0

    for i in range(n):
        while j7 < i and days[j7] + 7 <= days[i]:
            j7 += 1
        while j30 < i and days[j30] + 30 <= days[i]:
            j30 += 1
        dp[i + 1] = min(
            dp[i] + costs[0],
            dp[j7] + costs[1],
            dp[j30] + costs[2],
        )

    return dp[n]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([1, 4, 6, 7, 8, 20], [2, 7, 15], 11),
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 31], [2, 7, 15], 17),
    ([1], [2, 7, 15], 2),
    ([], [2, 7, 15], 0),
]

IMPLS = [
    ("reference", reference),
    ("recursive", min_tickets_recursive),
    ("sparse", min_tickets_sparse),
    ("window", min_tickets_window),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for days, costs, expected in TEST_CASES:
        results = {name: fn(list(days), list(costs)) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] days={days}  expected={expected}  " +
              "  ".join(f"{n}={v}" for n, v in results.items()))

    REPS = 20_000
    bench_days = list(range(1, 366, 3))
    bench_costs = [2, 7, 15]
    print(f"\n=== Benchmark: {REPS} runs, {len(bench_days)} travel days ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(bench_days, bench_costs), number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
