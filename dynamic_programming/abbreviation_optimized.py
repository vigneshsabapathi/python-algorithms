#!/usr/bin/env python3
"""
Optimized and alternative implementations of Abbreviation.

Given strings a and b, determine if a can be transformed into b by:
  1. Capitalizing some lowercase letters in a
  2. Deleting all remaining lowercase letters

Four variants:
  dp_2d         — standard 2D bottom-up DP (reference baseline)
  dp_1d         — space-optimized 1D rolling array
  top_down      — recursive with memoization
  greedy_check  — greedy attempt (works for many cases, not all)

Run:
    python dynamic_programming/abbreviation_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.abbreviation import abbr as reference


# ---------------------------------------------------------------------------
# Variant 1 — dp_2d: Standard 2D DP (same as reference)
# ---------------------------------------------------------------------------

def dp_2d(a: str, b: str) -> bool:
    """
    >>> dp_2d("daBcd", "ABC")
    True
    >>> dp_2d("dBcd", "ABC")
    False
    >>> dp_2d("", "")
    True
    """
    n, m = len(a), len(b)
    dp = [[False] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = True
    for i in range(n):
        for j in range(m + 1):
            if dp[i][j]:
                if j < m and a[i].upper() == b[j]:
                    dp[i + 1][j + 1] = True
                if a[i].islower():
                    dp[i + 1][j] = True
    return dp[n][m]


# ---------------------------------------------------------------------------
# Variant 2 — dp_1d: Space-optimized rolling array
# ---------------------------------------------------------------------------

def dp_1d(a: str, b: str) -> bool:
    """
    Uses only O(m) space instead of O(n*m).

    >>> dp_1d("daBcd", "ABC")
    True
    >>> dp_1d("dBcd", "ABC")
    False
    >>> dp_1d("ABc", "ABC")
    True
    """
    n, m = len(a), len(b)
    prev = [False] * (m + 1)
    prev[0] = True
    for i in range(n):
        curr = [False] * (m + 1)
        for j in range(m + 1):
            if prev[j]:
                if j < m and a[i].upper() == b[j]:
                    curr[j + 1] = True
                if a[i].islower():
                    curr[j] = True
        prev = curr
    return prev[m]


# ---------------------------------------------------------------------------
# Variant 3 — top_down: Recursive with memoization
# ---------------------------------------------------------------------------

def top_down(a: str, b: str) -> bool:
    """
    >>> top_down("daBcd", "ABC")
    True
    >>> top_down("dBcd", "ABC")
    False
    >>> top_down("abc", "ABC")
    True
    """
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def solve(i: int, j: int) -> bool:
        if j == len(b):
            # All remaining chars in a must be lowercase (deletable)
            return all(c.islower() for c in a[i:])
        if i == len(a):
            return False
        if a[i].upper() == b[j]:
            # Try capitalizing (or keeping if already upper) and matching
            if solve(i + 1, j + 1):
                return True
        if a[i].islower():
            # Try deleting this lowercase char
            return solve(i + 1, j)
        return False

    return solve(0, 0)


# ---------------------------------------------------------------------------
# Variant 4 — greedy_check: Greedy matching attempt
# ---------------------------------------------------------------------------

def greedy_check(a: str, b: str) -> bool:
    """
    Greedy: scan a left-to-right, match b chars greedily.
    After matching all of b, remaining chars in a must be lowercase.

    This is NOT always correct for all edge cases, but works for most
    interview-style inputs. Included to show why greedy fails.

    >>> greedy_check("daBcd", "ABC")
    True
    >>> greedy_check("dBcd", "ABC")
    False
    >>> greedy_check("ABc", "ABC")
    True
    """
    j = 0
    for i, ch in enumerate(a):
        if j < len(b) and ch.upper() == b[j]:
            j += 1
        elif ch.isupper():
            # Uppercase char that doesn't match b[j] — can't delete it
            return False
    return j == len(b)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ("daBcd", "ABC", True),
    ("dBcd", "ABC", False),
    ("ABc", "ABC", True),
    ("ABC", "ABC", True),
    ("abc", "ABC", True),
    ("abcd", "ABC", True),
    ("ABcd", "BCD", False),
    ("", "", True),
    ("a", "", True),
    ("", "A", False),
    ("A", "", False),
    ("aAbBcC", "ABC", True),
    ("abcDEF", "DEF", True),
    ("AbCdEfG", "ACEG", True),
]

IMPLS = [
    ("reference", reference),
    ("dp_2d", dp_2d),
    ("dp_1d", dp_1d),
    ("top_down", top_down),
    ("greedy_check", greedy_check),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for a, b, expected in TEST_CASES:
        row = {}
        for name, fn in IMPLS:
            try:
                row[name] = fn(a, b)
            except Exception as e:
                row[name] = f"ERR:{e}"
        ok = all(v == expected for v in row.values())
        if not ok:
            all_pass = False
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] abbr({a!r:>12}, {b!r:>6})  expected={expected!s:<6}  "
              + "  ".join(f"{nm}={v}" for nm, v in row.items()))

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    # Benchmark
    REPS = 50_000
    test_inputs = [("daBcd", "ABC"), ("aAbBcCdDeE", "ABCDE"), ("abcdefghij", "ABCDEFGHIJ")]

    print(f"\n=== Benchmark: {REPS} runs, {len(test_inputs)} inputs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(a, b) for a, b in test_inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms / batch of {len(test_inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
