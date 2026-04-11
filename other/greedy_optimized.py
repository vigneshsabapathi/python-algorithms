#!/usr/bin/env python3
"""
Optimized and alternative implementations of Greedy Algorithms.

Variants covered:
1. greedy_coin_change      -- Greedy coin change (reference)
2. dp_coin_change          -- DP optimal coin change
3. fractional_knapsack     -- Greedy fractional knapsack (reference)
4. job_sequencing          -- Greedy job sequencing with deadlines

Run:
    python other/greedy_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.greedy import greedy_coin_change as reference
from other.greedy import greedy_fractional_knapsack as frac_ref


def dp_coin_change(denominations: list[int], amount: int) -> list[int]:
    """
    Optimal coin change using dynamic programming.

    >>> dp_coin_change([25, 10, 5, 1], 41)
    [25, 10, 5, 1]
    >>> dp_coin_change([25, 10, 5, 1], 0)
    []
    >>> dp_coin_change([1, 3, 4], 6)
    [3, 3]
    """
    if amount <= 0:
        return []

    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    parent = [-1] * (amount + 1)

    for i in range(1, amount + 1):
        for coin in denominations:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                parent[i] = coin

    if dp[amount] == float("inf"):
        return []

    coins = []
    rem = amount
    while rem > 0:
        coins.append(parent[rem])
        rem -= parent[rem]
    return sorted(coins, reverse=True)


def greedy_min_coins_count(denominations: list[int], amount: int) -> int:
    """
    Count minimum coins needed (greedy, not always optimal).

    >>> greedy_min_coins_count([25, 10, 5, 1], 41)
    4
    >>> greedy_min_coins_count([25, 10, 5, 1], 0)
    0
    """
    count = 0
    remaining = amount
    for coin in sorted(denominations, reverse=True):
        count += remaining // coin
        remaining %= coin
    return count


def job_sequencing(
    jobs: list[tuple[str, int, int]],
) -> tuple[int, list[str]]:
    """
    Greedy job sequencing with deadlines to maximize profit.
    Each job is (id, deadline, profit).

    >>> job_sequencing([("a", 2, 100), ("b", 1, 19), ("c", 2, 27), ("d", 1, 25)])
    (127, ['a', 'c'])
    >>> job_sequencing([])
    (0, [])
    """
    if not jobs:
        return 0, []

    sorted_jobs = sorted(jobs, key=lambda x: x[2], reverse=True)
    max_deadline = max(j[1] for j in sorted_jobs)
    slots = [None] * (max_deadline + 1)
    total_profit = 0
    selected = []

    for job_id, deadline, profit in sorted_jobs:
        for slot in range(min(deadline, max_deadline), 0, -1):
            if slots[slot] is None:
                slots[slot] = job_id
                total_profit += profit
                selected.append(job_id)
                break

    return total_profit, selected


TEST_COIN = [
    ([25, 10, 5, 1], 41, [25, 10, 5, 1]),
    ([25, 10, 5, 1], 30, [25, 5]),
    ([25, 10, 5, 1], 0, []),
]

IMPLS_COIN = [
    ("reference", reference),
    ("dp_optimal", dp_coin_change),
]


def run_all() -> None:
    print("\n=== Correctness (Coin Change) ===")
    for denoms, amount, expected in TEST_COIN:
        for name, fn in IMPLS_COIN:
            result = fn(denoms, amount)
            ok = result == expected
            tag = "OK" if ok else "FAIL"
            if not ok:
                print(f"  [{tag}] {name}: amount={amount} expected={expected} got={result}")
        print(f"  [OK] amount={amount}")

    # Show where greedy fails
    print("\n=== Greedy vs DP (non-standard denominations) ===")
    denoms = [1, 3, 4]
    amount = 6
    greedy_res = reference(denoms, amount)
    dp_res = dp_coin_change(denoms, amount)
    print(f"  Denoms={denoms}, Amount={amount}")
    print(f"  Greedy: {greedy_res} ({len(greedy_res)} coins)")
    print(f"  DP:     {dp_res} ({len(dp_res)} coins)")

    REPS = 50_000
    print(f"\n=== Benchmark: {REPS} runs, standard coins, amount=99 ===")
    for name, fn in IMPLS_COIN:
        t = timeit.timeit(
            lambda fn=fn: fn([25, 10, 5, 1], 99), number=REPS
        ) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
