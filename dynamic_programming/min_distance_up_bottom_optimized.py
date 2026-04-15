#!/usr/bin/env python3
"""
Optimized and alternative implementations of Min Edit Distance (top-down).

Variants covered:
1. min_distance_bottom_up      -- classic O(mn) tabulation
2. min_distance_space_opt      -- O(min(m,n)) space with two rows
3. min_distance_weighted       -- weighted operations (educational)

Run:
    python dynamic_programming/min_distance_up_bottom_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.min_distance_up_bottom import min_distance as reference


# ---------------------------------------------------------------------------
# Variant 1 — Bottom-up tabulation
# ---------------------------------------------------------------------------

def min_distance_bottom_up(word1: str, word2: str) -> int:
    """
    Edit distance using bottom-up DP table.

    >>> min_distance_bottom_up("horse", "ros")
    3
    >>> min_distance_bottom_up("intention", "execution")
    5
    >>> min_distance_bottom_up("", "abc")
    3
    >>> min_distance_bottom_up("abc", "abc")
    0
    >>> min_distance_bottom_up("", "")
    0
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[m][n]


# ---------------------------------------------------------------------------
# Variant 2 — Space-optimized (two rows)
# ---------------------------------------------------------------------------

def min_distance_space_opt(word1: str, word2: str) -> int:
    """
    Edit distance using O(min(m,n)) space with two rolling rows.

    >>> min_distance_space_opt("horse", "ros")
    3
    >>> min_distance_space_opt("intention", "execution")
    5
    >>> min_distance_space_opt("", "abc")
    3
    >>> min_distance_space_opt("abc", "abc")
    0
    >>> min_distance_space_opt("", "")
    0
    """
    if len(word1) < len(word2):
        word1, word2 = word2, word1
    m, n = len(word1), len(word2)

    prev = list(range(n + 1))
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev, curr = curr, prev

    return prev[n]


# ---------------------------------------------------------------------------
# Variant 3 — Weighted operations
# ---------------------------------------------------------------------------

def min_distance_weighted(word1: str, word2: str,
                          insert_cost: int = 1,
                          delete_cost: int = 1,
                          replace_cost: int = 1) -> int:
    """
    Edit distance with configurable operation costs.

    With default costs (all 1), matches standard Levenshtein.

    >>> min_distance_weighted("horse", "ros")
    3
    >>> min_distance_weighted("intention", "execution")
    5
    >>> min_distance_weighted("ab", "cd", replace_cost=2)
    4
    >>> min_distance_weighted("", "abc")
    3
    >>> min_distance_weighted("", "")
    0
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i * delete_cost
    for j in range(n + 1):
        dp[0][j] = j * insert_cost

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i - 1][j] + delete_cost,
                    dp[i][j - 1] + insert_cost,
                    dp[i - 1][j - 1] + replace_cost,
                )

    return dp[m][n]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ("horse", "ros", 3),
    ("intention", "execution", 5),
    ("", "abc", 3),
    ("abc", "", 3),
    ("abc", "abc", 0),
    ("kitten", "sitting", 3),
    ("", "", 0),
]

IMPLS = [
    ("reference", reference),
    ("bottom_up", min_distance_bottom_up),
    ("space_opt", min_distance_space_opt),
    ("weighted", min_distance_weighted),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for w1, w2, expected in TEST_CASES:
        results = {name: fn(w1, w2) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] ({w1!r}, {w2!r})  expected={expected}  " +
              "  ".join(f"{n}={v}" for n, v in results.items()))

    REPS = 10_000
    w1, w2 = "algorithm", "altruistic"
    print(f"\n=== Benchmark: {REPS} runs, ({w1!r}, {w2!r}) ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(w1, w2), number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
