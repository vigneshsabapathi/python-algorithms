#!/usr/bin/env python3
"""
Optimized and alternative implementations of Minimum Coin Change.

Variants covered:
1. min_coins_top_down     -- memoized recursion
2. min_coins_bfs          -- BFS shortest-path approach
3. min_coins_with_trace   -- bottom-up with coin tracking

Run:
    python dynamic_programming/minimum_coin_change_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
from collections import deque
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.minimum_coin_change import minimum_coin_change as reference


# ---------------------------------------------------------------------------
# Variant 1 — Top-down memoized recursion
# ---------------------------------------------------------------------------

def min_coins_top_down(coins: list[int], amount: int) -> int:
    """
    Minimum coin change using top-down memoization.

    >>> min_coins_top_down([1, 5, 10, 25], 30)
    2
    >>> min_coins_top_down([1, 5, 10, 25], 11)
    2
    >>> min_coins_top_down([2], 3)
    -1
    >>> min_coins_top_down([1], 0)
    0
    >>> min_coins_top_down([1, 2, 5], 11)
    3
    """
    coins_tuple = tuple(coins)

    @lru_cache(maxsize=None)
    def dp(rem: int) -> int:
        if rem == 0:
            return 0
        if rem < 0:
            return float("inf")
        best = float("inf")
        for c in coins_tuple:
            best = min(best, dp(rem - c) + 1)
        return best

    result = dp(amount)
    dp.cache_clear()
    return result if result != float("inf") else -1


# ---------------------------------------------------------------------------
# Variant 2 — BFS shortest-path
# ---------------------------------------------------------------------------

def min_coins_bfs(coins: list[int], amount: int) -> int:
    """
    Minimum coin change using BFS — models it as shortest path from amount to 0.

    >>> min_coins_bfs([1, 5, 10, 25], 30)
    2
    >>> min_coins_bfs([1, 5, 10, 25], 11)
    2
    >>> min_coins_bfs([2], 3)
    -1
    >>> min_coins_bfs([1], 0)
    0
    >>> min_coins_bfs([1, 2, 5], 11)
    3
    """
    if amount == 0:
        return 0
    visited = [False] * (amount + 1)
    visited[0] = True
    queue = deque([0])
    level = 0

    while queue:
        level += 1
        for _ in range(len(queue)):
            curr = queue.popleft()
            for coin in coins:
                nxt = curr + coin
                if nxt == amount:
                    return level
                if nxt < amount and not visited[nxt]:
                    visited[nxt] = True
                    queue.append(nxt)
    return -1


# ---------------------------------------------------------------------------
# Variant 3 — Bottom-up with coin tracking
# ---------------------------------------------------------------------------

def min_coins_with_trace(coins: list[int], amount: int) -> tuple[int, list[int]]:
    """
    Returns (min_coins, list_of_coins_used).

    >>> min_coins_with_trace([1, 5, 10, 25], 30)
    (2, [5, 25])
    >>> min_coins_with_trace([2], 3)
    (-1, [])
    >>> min_coins_with_trace([1], 0)
    (0, [])
    >>> min_coins_with_trace([1, 2, 5], 11)
    (3, [1, 5, 5])
    """
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    parent = [-1] * (amount + 1)

    for coin in sorted(coins):
        for x in range(coin, amount + 1):
            if dp[x - coin] + 1 < dp[x]:
                dp[x] = dp[x - coin] + 1
                parent[x] = coin

    if dp[amount] == float("inf"):
        return (-1, [])

    result_coins = []
    rem = amount
    while rem > 0:
        result_coins.append(parent[rem])
        rem -= parent[rem]
    return (dp[amount], sorted(result_coins))


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([1, 5, 10, 25], 30, 2),
    ([1, 5, 10, 25], 11, 2),
    ([2], 3, -1),
    ([1], 0, 0),
    ([1, 2, 5], 11, 3),
]

IMPLS = [
    ("reference", reference),
    ("top_down", min_coins_top_down),
    ("bfs", min_coins_bfs),
    ("with_trace", lambda c, a: min_coins_with_trace(c, a)[0]),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for coins, amount, expected in TEST_CASES:
        results = {name: fn(list(coins), amount) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] coins={coins}, amount={amount}  expected={expected}  " +
              "  ".join(f"{n}={v}" for n, v in results.items()))

    REPS = 5_000
    coins, amount = [1, 5, 10, 25], 100
    print(f"\n=== Benchmark: {REPS} runs, amount={amount} ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(coins, amount), number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
