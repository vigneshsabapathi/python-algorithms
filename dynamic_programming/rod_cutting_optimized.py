#!/usr/bin/env python3
"""
Optimized and alternative implementations of Rod Cutting.

Variants covered:
1. rod_cutting_recursive    -- top-down memoized recursion
2. rod_cutting_with_cuts    -- DP with cut reconstruction
3. rod_cutting_unbounded_kp -- formulated as unbounded knapsack

Run:
    python dynamic_programming/rod_cutting_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.rod_cutting import rod_cutting as reference


# ---------------------------------------------------------------------------
# Variant 1 — Top-down memoized recursion
# ---------------------------------------------------------------------------

def rod_cutting_recursive(prices: list[int], length: int) -> int:
    """
    Rod cutting using memoized recursion.

    >>> rod_cutting_recursive([1, 5, 8, 9, 10, 17, 17, 20], 8)
    22
    >>> rod_cutting_recursive([1, 5, 8, 9, 10, 17, 17, 20], 4)
    10
    >>> rod_cutting_recursive([1], 1)
    1
    >>> rod_cutting_recursive([], 0)
    0
    """
    if length == 0:
        return 0
    prices_t = tuple(prices)

    @lru_cache(maxsize=None)
    def dp(n: int) -> int:
        if n == 0:
            return 0
        best = 0
        for i in range(min(n, len(prices_t))):
            best = max(best, prices_t[i] + dp(n - i - 1))
        return best

    result = dp(length)
    dp.cache_clear()
    return result


# ---------------------------------------------------------------------------
# Variant 2 — DP with cut reconstruction
# ---------------------------------------------------------------------------

def rod_cutting_with_cuts(prices: list[int], length: int) -> tuple[int, list[int]]:
    """
    Returns (max_revenue, list_of_cut_lengths).

    >>> rod_cutting_with_cuts([1, 5, 8, 9, 10, 17, 17, 20], 8)
    (22, [2, 6])
    >>> rod_cutting_with_cuts([1, 5, 8, 9, 10, 17, 17, 20], 4)
    (10, [2, 2])
    >>> rod_cutting_with_cuts([], 0)
    (0, [])
    """
    if length == 0:
        return (0, [])
    dp = [0] * (length + 1)
    cut_at = [0] * (length + 1)

    for i in range(1, length + 1):
        for j in range(min(i, len(prices))):
            if prices[j] + dp[i - j - 1] > dp[i]:
                dp[i] = prices[j] + dp[i - j - 1]
                cut_at[i] = j + 1

    cuts = []
    rem = length
    while rem > 0:
        cuts.append(cut_at[rem])
        rem -= cut_at[rem]

    return (dp[length], sorted(cuts))


# ---------------------------------------------------------------------------
# Variant 3 — Unbounded knapsack formulation
# ---------------------------------------------------------------------------

def rod_cutting_unbounded_kp(prices: list[int], length: int) -> int:
    """
    Rod cutting as unbounded knapsack: items have weight=i+1, value=prices[i].

    >>> rod_cutting_unbounded_kp([1, 5, 8, 9, 10, 17, 17, 20], 8)
    22
    >>> rod_cutting_unbounded_kp([1, 5, 8, 9, 10, 17, 17, 20], 4)
    10
    >>> rod_cutting_unbounded_kp([1], 1)
    1
    >>> rod_cutting_unbounded_kp([], 0)
    0
    """
    if length == 0:
        return 0
    dp = [0] * (length + 1)
    for piece_len in range(1, min(length, len(prices)) + 1):
        price = prices[piece_len - 1]
        for cap in range(piece_len, length + 1):
            dp[cap] = max(dp[cap], dp[cap - piece_len] + price)
    return dp[length]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

PRICES = [1, 5, 8, 9, 10, 17, 17, 20]
TEST_CASES = [
    (PRICES, 8, 22), (PRICES, 4, 10), ([3, 5, 8, 9, 10, 17, 17, 20], 1, 3),
    ([1], 1, 1), ([], 0, 0),
]

IMPLS = [
    ("reference", reference),
    ("recursive", rod_cutting_recursive),
    ("with_cuts", lambda p, n: rod_cutting_with_cuts(p, n)[0]),
    ("unbounded_kp", rod_cutting_unbounded_kp),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for prices, length, expected in TEST_CASES:
        results = {name: fn(prices, length) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] length={length}  expected={expected}  " +
              "  ".join(f"{n}={v}" for n, v in results.items()))

    # Show cuts
    rev, cuts = rod_cutting_with_cuts(PRICES, 8)
    print(f"\n  Cuts for length=8: {cuts} (revenue={rev})")

    REPS = 10_000
    print(f"\n=== Benchmark: {REPS} runs, length=8 ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(PRICES, 8), number=REPS) * 1000 / REPS
        print(f"  {name:<14} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
