#!/usr/bin/env python3
"""
Optimized and alternative implementations of Longest Palindromic Subsequence.

Three variants:
  lcs_reverse       — LCS(s, reverse(s)) approach (reference)
  dp_direct         — direct DP on string itself (no reverse)
  space_optimized   — O(n) space rolling array

Run:
    python dynamic_programming/longest_palindromic_subsequence_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.longest_palindromic_subsequence import (
    longest_palindromic_subsequence as reference,
)


# ---------------------------------------------------------------------------
# Variant 1 — lcs_reverse (same as reference)
# ---------------------------------------------------------------------------

def lcs_reverse(s: str) -> int:
    """
    >>> lcs_reverse("bbbab")
    4
    """
    return reference(s)


# ---------------------------------------------------------------------------
# Variant 2 — dp_direct: Direct interval DP
# ---------------------------------------------------------------------------

def dp_direct(s: str) -> int:
    """
    dp[i][j] = length of longest palindromic subsequence in s[i..j]

    >>> dp_direct("bbbab")
    4
    >>> dp_direct("bbabcbcab")
    7
    >>> dp_direct("a")
    1
    >>> dp_direct("")
    0
    """
    n = len(s)
    if n == 0:
        return 0

    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

    return dp[0][n - 1]


# ---------------------------------------------------------------------------
# Variant 3 — space_optimized: O(n) space
# ---------------------------------------------------------------------------

def space_optimized(s: str) -> int:
    """
    >>> space_optimized("bbbab")
    4
    >>> space_optimized("bbabcbcab")
    7
    >>> space_optimized("")
    0
    """
    n = len(s)
    if n == 0:
        return 0

    rev = s[::-1]
    prev = [0] * (n + 1)
    for i in range(1, n + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if s[i - 1] == rev[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr
    return prev[n]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ("bbbab", 4),
    ("bbabcbcab", 7),
    ("abcba", 5),
    ("cbbd", 2),
    ("a", 1),
    ("", 0),
    ("abcdefgfedcba", 13),
]

IMPLS = [
    ("lcs_reverse", lcs_reverse),
    ("dp_direct", dp_direct),
    ("space_optimized", space_optimized),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for s, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(s)
            ok = result == expected
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}({s!r}) = {result}")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    REPS = 10_000
    inputs = ["bbabcbcab", "abcdefghgfedcbaxy"]
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(s) for s in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
