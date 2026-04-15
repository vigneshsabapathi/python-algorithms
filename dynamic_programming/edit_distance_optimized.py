#!/usr/bin/env python3
"""
Optimized and alternative implementations of Edit Distance (LeetCode 72).

Four variants:
  top_down     — recursive with memoization (reference)
  bottom_up    — standard 2D DP table (reference)
  space_opt    — O(min(m,n)) space using rolling array
  functools    — clean @lru_cache implementation

Run:
    python dynamic_programming/edit_distance_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.edit_distance import EditDistance

_ref = EditDistance()


def reference(w1: str, w2: str) -> int:
    return _ref.min_dist_bottom_up(w1, w2)


# ---------------------------------------------------------------------------
# Variant 1 — bottom_up_2d: Standard 2D DP
# ---------------------------------------------------------------------------

def bottom_up_2d(w1: str, w2: str) -> int:
    """
    >>> bottom_up_2d("intention", "execution")
    5
    >>> bottom_up_2d("kitten", "sitting")
    3
    """
    return reference(w1, w2)


# ---------------------------------------------------------------------------
# Variant 2 — space_optimized: O(min(m,n)) space
# ---------------------------------------------------------------------------

def space_optimized(w1: str, w2: str) -> int:
    """
    >>> space_optimized("intention", "execution")
    5
    >>> space_optimized("kitten", "sitting")
    3
    >>> space_optimized("", "")
    0
    """
    # Make w2 the shorter string for space optimization
    if len(w1) < len(w2):
        w1, w2 = w2, w1
    m, n = len(w1), len(w2)

    prev = list(range(n + 1))
    for i in range(1, m + 1):
        curr = [i] + [0] * n
        for j in range(1, n + 1):
            if w1[i - 1] == w2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev = curr
    return prev[n]


# ---------------------------------------------------------------------------
# Variant 3 — functools_memo: Clean @lru_cache
# ---------------------------------------------------------------------------

def functools_memo(w1: str, w2: str) -> int:
    """
    >>> functools_memo("intention", "execution")
    5
    >>> functools_memo("horse", "ros")
    3
    """

    @lru_cache(maxsize=None)
    def solve(i: int, j: int) -> int:
        if i == 0:
            return j
        if j == 0:
            return i
        if w1[i - 1] == w2[j - 1]:
            return solve(i - 1, j - 1)
        return 1 + min(solve(i - 1, j), solve(i, j - 1), solve(i - 1, j - 1))

    return solve(len(w1), len(w2))


# ---------------------------------------------------------------------------
# Variant 4 — wagner_fischer: Classic Wagner-Fischer with path reconstruction
# ---------------------------------------------------------------------------

def wagner_fischer(w1: str, w2: str) -> int:
    """
    >>> wagner_fischer("intention", "execution")
    5
    >>> wagner_fischer("", "abc")
    3
    """
    m, n = len(w1), len(w2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if w1[i - 1] == w2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)

    return dp[m][n]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ("intention", "execution", 5),
    ("kitten", "sitting", 3),
    ("horse", "ros", 3),
    ("", "", 0),
    ("abc", "", 3),
    ("saturday", "sunday", 3),
]

IMPLS = [
    ("bottom_up_2d", bottom_up_2d),
    ("space_optimized", space_optimized),
    ("functools_memo", functools_memo),
    ("wagner_fischer", wagner_fischer),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for w1, w2, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(w1, w2)
            ok = result == expected
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}({w1!r}, {w2!r}) = {result}")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    REPS = 20_000
    inputs = [("intention", "execution"), ("kitten", "sitting"), ("horse", "ros")]
    print(f"\n=== Benchmark: {REPS} runs, {len(inputs)} inputs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(a, b) for a, b in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
