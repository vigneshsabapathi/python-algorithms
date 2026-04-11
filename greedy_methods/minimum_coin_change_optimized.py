#!/usr/bin/env python3
"""
Optimized and alternative implementations of Minimum Coin Change.

The reference uses greedy: sort denominations descending, take largest first.

Variants covered:
1. greedy_list     -- greedy, returns list of coins (reference)
2. greedy_count    -- greedy, returns count only (lighter)
3. dp_optimal      -- dynamic programming for arbitrary denominations
4. greedy_vs_dp    -- demonstrates greedy failure case

Key interview insight:
    Greedy works for canonical coin systems (US: 1,5,10,25) but FAILS for
    arbitrary denominations. Example: coins=[1,3,4], amount=6.
    Greedy gives [4,1,1] (3 coins), DP gives [3,3] (2 coins).
    Interviewers LOVE this trap. Always ask: "are the denominations canonical?"

Run:
    python greedy_methods/minimum_coin_change_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from greedy_methods.minimum_coin_change import minimum_coin_change as reference


# ---------------------------------------------------------------------------
# Variant 1 — greedy list (reference)
# ---------------------------------------------------------------------------

def greedy_list(denominations: list[int], amount: int) -> list[int]:
    """
    Greedy: sort descending, take largest coin repeatedly.

    >>> greedy_list([1, 5, 10, 25], 36)
    [25, 10, 1]
    >>> greedy_list([1, 5, 10, 25], 0)
    []
    >>> greedy_list([1], 7)
    [1, 1, 1, 1, 1, 1, 1]
    """
    coins: list[int] = []
    remaining = amount
    for coin in sorted(denominations, reverse=True):
        while remaining >= coin:
            remaining -= coin
            coins.append(coin)
    return coins


# ---------------------------------------------------------------------------
# Variant 2 — greedy count only (no list allocation)
# ---------------------------------------------------------------------------

def greedy_count(denominations: list[int], amount: int) -> int:
    """
    Greedy: returns just the count (no coin list).
    Uses divmod for efficiency — no inner while loop.

    >>> greedy_count([1, 5, 10, 25], 36)
    3
    >>> greedy_count([1, 5, 10, 25], 0)
    0
    >>> greedy_count([1, 5, 10, 25], 99)
    9
    """
    count = 0
    remaining = amount
    for coin in sorted(denominations, reverse=True):
        if remaining <= 0:
            break
        num_coins, remaining = divmod(remaining, coin)
        count += num_coins
    return count


# ---------------------------------------------------------------------------
# Variant 3 — DP optimal (handles non-canonical denominations)
# ---------------------------------------------------------------------------

def dp_optimal(denominations: list[int], amount: int) -> list[int]:
    """
    Dynamic programming: guaranteed optimal for ANY denomination set.
    Returns the actual coins used (backtrack from DP table).

    >>> dp_optimal([1, 5, 10, 25], 36)
    [25, 10, 1]
    >>> dp_optimal([1, 3, 4], 6)
    [3, 3]
    >>> dp_optimal([1, 5, 10, 25], 0)
    []
    >>> dp_optimal([2], 3)
    []
    """
    if amount == 0:
        return []

    # dp[i] = min coins to make amount i; -1 = impossible
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    parent = [-1] * (amount + 1)  # which coin was used

    for i in range(1, amount + 1):
        for coin in denominations:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                parent[i] = coin

    if dp[amount] == float("inf"):
        return []

    # Backtrack to find coins
    coins: list[int] = []
    current = amount
    while current > 0:
        coins.append(parent[current])
        current -= parent[current]

    return sorted(coins, reverse=True)


# ---------------------------------------------------------------------------
# Variant 4 — greedy vs DP comparison (demonstrates failure)
# ---------------------------------------------------------------------------

def greedy_vs_dp(denominations: list[int], amount: int) -> dict:
    """
    Compare greedy and DP results side by side.

    >>> result = greedy_vs_dp([1, 3, 4], 6)
    >>> result['greedy_coins']
    [4, 1, 1]
    >>> result['dp_coins']
    [3, 3]
    >>> result['greedy_optimal']
    False
    """
    greedy_coins = greedy_list(denominations, amount)
    dp_coins = dp_optimal(denominations, amount)
    return {
        "greedy_coins": greedy_coins,
        "dp_coins": dp_coins,
        "greedy_count": len(greedy_coins),
        "dp_count": len(dp_coins),
        "greedy_optimal": len(greedy_coins) == len(dp_coins),
    }


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([1, 5, 10, 25], 36, [25, 10, 1]),
    ([1, 5, 10, 25], 0, []),
    ([1, 5, 10, 25], 5, [5]),
    ([1, 5, 10, 25], 30, [25, 5]),
    ([1, 5, 10, 25], 99, [25, 25, 25, 10, 10, 1, 1, 1, 1]),
    ([1], 7, [1, 1, 1, 1, 1, 1, 1]),
]

# Cases where greedy fails
GREEDY_FAIL_CASES = [
    ([1, 3, 4], 6, [4, 1, 1], [3, 3]),  # greedy=3 coins, dp=2 coins
    ([1, 5, 6, 9], 11, [9, 1, 1], [6, 5]),  # greedy=3, dp=2
]

IMPLS = [
    ("reference",    reference),
    ("greedy_list",  greedy_list),
    ("dp_optimal",   dp_optimal),
]


def run_all() -> None:
    print("\n=== Correctness (canonical coins) ===")
    for denoms, amount, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(denoms, amount)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] amount={amount:<5} coins={expected}")

    print("\n=== Greedy vs DP (non-canonical coins) ===")
    for denoms, amount, greedy_exp, dp_exp in GREEDY_FAIL_CASES:
        result = greedy_vs_dp(denoms, amount)
        g_ok = result["greedy_coins"] == greedy_exp
        d_ok = result["dp_coins"] == dp_exp
        print(
            f"  denoms={denoms} amount={amount}\n"
            f"    greedy={result['greedy_coins']} ({result['greedy_count']} coins) {'OK' if g_ok else 'FAIL'}\n"
            f"    dp    ={result['dp_coins']} ({result['dp_count']} coins) {'OK' if d_ok else 'FAIL'}\n"
            f"    greedy_optimal={result['greedy_optimal']}"
        )

    REPS = 50_000
    denoms = [1, 5, 10, 25]
    print(f"\n=== Benchmark (US coins, amount=99): {REPS} runs ===")
    print(f"  {'greedy_list':<14} ", end="")
    t = timeit.timeit(lambda: greedy_list(denoms, 99), number=REPS) * 1000 / REPS
    print(f"{t:>7.4f} ms")
    print(f"  {'greedy_count':<14} ", end="")
    t = timeit.timeit(lambda: greedy_count(denoms, 99), number=REPS) * 1000 / REPS
    print(f"{t:>7.4f} ms")
    print(f"  {'dp_optimal':<14} ", end="")
    t = timeit.timeit(lambda: dp_optimal(denoms, 99), number=REPS) * 1000 / REPS
    print(f"{t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
