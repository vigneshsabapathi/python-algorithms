"""
Power Sum — Optimized implementations.

Variants:
1. Subset-sum DP (bottom-up) — count ways using unbounded candidates
2. Memoized backtracking — same logic, cached
3. itertools combination approach — enumerate all valid subsets

Reference: https://www.hackerrank.com/challenges/the-power-sum/problem
"""

from __future__ import annotations

import math
from functools import lru_cache
from itertools import combinations


def _get_candidates(x: int, n: int) -> list[int]:
    """Return list of i^n values where i >= 1 and i^n <= x."""
    max_base = int(x ** (1 / n))
    return [i**n for i in range(1, max_base + 1)]


# ── Variant 1: Subset-sum DP (0/1 knapsack) ──────────────────────────────


def solve_dp(x: int, n: int) -> int:
    """
    Count ways to express x as sum of unique n-th powers using 0/1 knapsack DP.

    dp[s] = number of ways to reach sum s using candidates considered so far.
    For each candidate c, update dp in reverse: dp[s] += dp[s - c].
    Reverse iteration ensures each candidate is used at most once.

    >>> solve_dp(13, 2)
    1
    >>> solve_dp(10, 2)
    1
    >>> solve_dp(100, 2)
    3
    >>> solve_dp(1000, 2)
    1269
    >>> solve_dp(10, 3)
    0
    """
    candidates = _get_candidates(x, n)
    dp = [0] * (x + 1)
    dp[0] = 1
    for c in candidates:
        for s in range(x, c - 1, -1):
            dp[s] += dp[s - c]
    return dp[x]


# ── Variant 2: Memoized backtracking ─────────────────────────────────────


def solve_memo(x: int, n: int) -> int:
    """
    Memoized backtracking: at each candidate index, either include it or skip it.

    State: (index, remaining_sum) → count of valid ways from here.

    >>> solve_memo(13, 2)
    1
    >>> solve_memo(10, 2)
    1
    >>> solve_memo(100, 2)
    3
    >>> solve_memo(1000, 2)
    1269
    >>> solve_memo(10, 3)
    0
    """
    candidates = _get_candidates(x, n)

    @lru_cache(maxsize=None)
    def count(idx: int, remaining: int) -> int:
        if remaining == 0:
            return 1
        if idx == len(candidates) or remaining < 0:
            return 0
        # Include candidates[idx] or skip it
        return count(idx + 1, remaining - candidates[idx]) + count(idx + 1, remaining)

    return count(0, x)


# ── Variant 3: itertools combinations ─────────────────────────────────────


def solve_itertools(x: int, n: int) -> int:
    """
    Enumerate all subsets of n-th power candidates and count those summing to x.
    Correct but exponential — only practical for small candidate lists.

    >>> solve_itertools(13, 2)
    1
    >>> solve_itertools(10, 2)
    1
    >>> solve_itertools(100, 2)
    3
    >>> solve_itertools(10, 3)
    0
    """
    candidates = _get_candidates(x, n)
    total = 0
    for size in range(1, len(candidates) + 1):
        for combo in combinations(candidates, size):
            if sum(combo) == x:
                total += 1
    return total


# ── Variant 4: Also return the actual combinations ────────────────────────


def solve_with_combinations(x: int, n: int) -> list[list[int]]:
    """
    Return all ways to express x as sum of unique n-th powers,
    showing the actual bases (not the powered values).

    >>> solve_with_combinations(13, 2)
    [[2, 3]]
    >>> solve_with_combinations(100, 2)
    [[1, 3, 4, 5, 7], [6, 8], [10]]
    """
    max_base = int(x ** (1 / n))
    results: list[list[int]] = []

    def find(idx: int, remaining: int, path: list[int]) -> None:
        if remaining == 0:
            results.append(path[:])
            return
        if idx > max_base or remaining < 0:
            return
        val = idx**n
        if val <= remaining:
            path.append(idx)
            find(idx + 1, remaining - val, path)
            path.pop()
        find(idx + 1, remaining, path)

    find(1, x, [])
    return results


if __name__ == "__main__":
    import time

    cases = [
        (13, 2), (100, 2), (200, 2), (500, 2), (1000, 2),
        (100, 3), (800, 3), (64, 6),
    ]

    print(f"{'X':>5} {'N':>3} {'DP':>6} {'Memo':>6} {'Itools':>6} | {'t_dp':>10} {'t_memo':>10}")
    print("-" * 65)
    for x, n in cases:
        t = time.perf_counter()
        r_dp = solve_dp(x, n)
        t_dp = time.perf_counter() - t

        t = time.perf_counter()
        r_memo = solve_memo(x, n)
        t_memo = time.perf_counter() - t

        # itertools only for small cases
        r_it = "-"
        if x <= 200:
            t = time.perf_counter()
            r_it = solve_itertools(x, n)
            t_it = time.perf_counter() - t
        else:
            t_it = 0

        print(f"{x:>5} {n:>3} {r_dp:>6} {r_memo:>6} {str(r_it):>6} | {t_dp:>9.4f}s {t_memo:>9.4f}s")

    print("\n=== Actual combinations (100, 2) ===")
    combos = solve_with_combinations(100, 2)
    for c in combos:
        powers = [f"{b}^2={b**2}" for b in c]
        print(f"  {c} → {' + '.join(powers)} = {sum(b**2 for b in c)}")

    import doctest
    doctest.testmod()
