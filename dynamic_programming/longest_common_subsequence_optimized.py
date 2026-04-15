#!/usr/bin/env python3
"""
Optimized and alternative implementations of Longest Common Subsequence.

Three variants:
  bottom_up_2d      — standard 2D DP with backtracking (reference)
  space_optimized   — O(min(m,n)) space (length only, no backtracking)
  lru_cache_memo    — top-down @lru_cache

Run:
    python dynamic_programming/longest_common_subsequence_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.longest_common_subsequence import longest_common_subsequence as reference


# ---------------------------------------------------------------------------
# Variant 1 — bottom_up_2d (same as reference)
# ---------------------------------------------------------------------------

def bottom_up_2d(x: str, y: str) -> tuple[int, str]:
    """
    >>> bottom_up_2d("programming", "gaming")
    (6, 'gaming')
    """
    return reference(x, y)


# ---------------------------------------------------------------------------
# Variant 2 — space_optimized: O(min(m,n)) space, length only
# ---------------------------------------------------------------------------

def space_optimized(x: str, y: str) -> int:
    """
    >>> space_optimized("programming", "gaming")
    6
    >>> space_optimized("abcdef", "ace")
    3
    >>> space_optimized("", "abc")
    0
    """
    if len(x) < len(y):
        x, y = y, x
    m, n = len(x), len(y)
    prev = [0] * (n + 1)
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr
    return prev[n]


# ---------------------------------------------------------------------------
# Variant 3 — lru_cache_memo: Top-down with @lru_cache
# ---------------------------------------------------------------------------

def lru_cache_memo(x: str, y: str) -> int:
    """
    >>> lru_cache_memo("programming", "gaming")
    6
    >>> lru_cache_memo("abc", "def")
    0
    """

    @lru_cache(maxsize=None)
    def solve(i: int, j: int) -> int:
        if i == 0 or j == 0:
            return 0
        if x[i - 1] == y[j - 1]:
            return 1 + solve(i - 1, j - 1)
        return max(solve(i - 1, j), solve(i, j - 1))

    return solve(len(x), len(y))


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ("programming", "gaming", 6),
    ("abcdef", "ace", 3),
    ("abc", "abc", 3),
    ("abc", "def", 0),
    ("", "abc", 0),
    ("ABCD", "ACBD", 3),
]

IMPLS = [
    ("bottom_up_2d", lambda x, y: reference(x, y)[0]),
    ("space_optimized", space_optimized),
    ("lru_cache_memo", lru_cache_memo),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for x, y, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(x, y)
            ok = result == expected
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}({x!r}, {y!r}) = {result}")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    REPS = 20_000
    inputs = [("programming", "gaming"), ("abcdefghij", "acegikmoqs")]
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(a, b) for a, b in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
