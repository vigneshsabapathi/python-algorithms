#!/usr/bin/env python3
"""
Optimized and alternative implementations of Best Time to Buy and Sell Stock.

The reference tracks min_price and max_gain in a single pass.

Variants covered:
1. single_pass    -- track min_price, update max_gain (reference)
2. kadane_style   -- transform to max subarray problem (price deltas)
3. two_pointer    -- left=buy, right=sell, slide window
4. reduce_style   -- functools.reduce one-liner

Key interview insight:
    This is LeetCode 121. The greedy single-pass is O(n) time O(1) space.
    The Kadane variant shows the connection to maximum subarray (LC 53).
    Interviewers love asking "what if you can do multiple transactions?" (LC 122).

Run:
    python greedy_methods/best_time_to_buy_and_sell_stock_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from functools import reduce

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from greedy_methods.best_time_to_buy_and_sell_stock import max_profit as reference


# ---------------------------------------------------------------------------
# Variant 1 — single pass: track min price (reference, explicit)
# ---------------------------------------------------------------------------

def single_pass(prices: list[int]) -> int:
    """
    Track minimum price seen so far, compute max profit at each step.

    >>> single_pass([7, 1, 5, 3, 6, 4])
    5
    >>> single_pass([7, 6, 4, 3, 1])
    0
    >>> single_pass([])
    0
    >>> single_pass([1])
    0
    """
    if len(prices) < 2:
        return 0
    min_price = prices[0]
    max_gain = 0
    for price in prices[1:]:
        max_gain = max(max_gain, price - min_price)
        min_price = min(min_price, price)
    return max_gain


# ---------------------------------------------------------------------------
# Variant 2 — Kadane-style: max subarray on price deltas
# ---------------------------------------------------------------------------

def kadane_style(prices: list[int]) -> int:
    """
    Convert to daily gains/losses, then find max subarray sum (Kadane).
    The max subarray of deltas = best buy-sell profit.

    >>> kadane_style([7, 1, 5, 3, 6, 4])
    5
    >>> kadane_style([7, 6, 4, 3, 1])
    0
    >>> kadane_style([])
    0
    >>> kadane_style([1])
    0
    """
    if len(prices) < 2:
        return 0
    max_profit = 0
    current = 0
    for i in range(1, len(prices)):
        current = max(0, current + prices[i] - prices[i - 1])
        max_profit = max(max_profit, current)
    return max_profit


# ---------------------------------------------------------------------------
# Variant 3 — two pointer: left=buy day, right=sell day
# ---------------------------------------------------------------------------

def two_pointer(prices: list[int]) -> int:
    """
    Slide two pointers: left (buy), right (sell).
    If price drops below buy price, move buy pointer forward.

    >>> two_pointer([7, 1, 5, 3, 6, 4])
    5
    >>> two_pointer([7, 6, 4, 3, 1])
    0
    >>> two_pointer([])
    0
    >>> two_pointer([1])
    0
    """
    if len(prices) < 2:
        return 0
    left = 0  # buy
    max_profit = 0
    for right in range(1, len(prices)):
        if prices[right] < prices[left]:
            left = right
        else:
            max_profit = max(max_profit, prices[right] - prices[left])
    return max_profit


# ---------------------------------------------------------------------------
# Variant 4 — reduce one-liner: functional style
# ---------------------------------------------------------------------------

def reduce_style(prices: list[int]) -> int:
    """
    functools.reduce tracking (min_price, max_profit) in one pass.

    >>> reduce_style([7, 1, 5, 3, 6, 4])
    5
    >>> reduce_style([7, 6, 4, 3, 1])
    0
    >>> reduce_style([])
    0
    >>> reduce_style([1])
    0
    """
    if len(prices) < 2:
        return 0
    _, profit = reduce(
        lambda acc, p: (min(acc[0], p), max(acc[1], p - acc[0])),
        prices[1:],
        (prices[0], 0),
    )
    return profit


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([7, 1, 5, 3, 6, 4], 5),
    ([7, 6, 4, 3, 1], 0),
    ([2, 4, 1], 2),
    ([1, 2], 1),
    ([1], 0),
    ([], 0),
    ([3, 3, 3], 0),
    ([1, 2, 3, 4, 5], 4),
    ([5, 4, 3, 2, 1, 10], 9),
    (list(range(1000, 0, -1)), 0),
    (list(range(1000)), 999),
]

IMPLS = [
    ("reference",    reference),
    ("single_pass",  single_pass),
    ("kadane_style", kadane_style),
    ("two_pointer",  two_pointer),
    ("reduce_style", reduce_style),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for prices, expected in TEST_CASES:
        label = str(prices) if len(prices) <= 8 else f"[...{len(prices)} items]"
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(prices)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] prices={label:<30} expected={expected}")

    REPS = 50_000
    small = [7, 1, 5, 3, 6, 4]
    large = list(range(10_000))

    print(f"\n=== Benchmark (6 prices): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(small), number=REPS) * 1000 / REPS
        print(f"  {name:<14} {t:>7.4f} ms")

    print(f"\n=== Benchmark (10k prices): {REPS // 10} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(large), number=REPS // 10) * 1000 / (REPS // 10)
        print(f"  {name:<14} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
