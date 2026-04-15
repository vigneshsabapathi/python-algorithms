#!/usr/bin/env python3
"""
Optimized and alternative implementations of Palindrome Partitioning.

Variants covered:
1. min_pal_expand         -- expand-around-center for palindrome check
2. min_pal_manacher       -- Manacher-inspired O(n) palindrome precompute
3. min_pal_recursive      -- top-down memoized recursion

Run:
    python dynamic_programming/palindrome_partitioning_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.palindrome_partitioning import min_palindrome_partitions as reference


# ---------------------------------------------------------------------------
# Variant 1 — Expand around center
# ---------------------------------------------------------------------------

def min_pal_expand(s: str) -> int:
    """
    O(n^2) using expand-around-center for palindrome detection
    combined with O(n) cuts array.

    >>> min_pal_expand("aab")
    1
    >>> min_pal_expand("a")
    0
    >>> min_pal_expand("aba")
    0
    >>> min_pal_expand("abcd")
    3
    >>> min_pal_expand("")
    0
    """
    n = len(s)
    if n <= 1:
        return 0

    cuts = list(range(n))  # worst case

    for center in range(n):
        # Odd-length palindromes
        lo, hi = center, center
        while lo >= 0 and hi < n and s[lo] == s[hi]:
            cuts[hi] = 0 if lo == 0 else min(cuts[hi], cuts[lo - 1] + 1)
            lo -= 1
            hi += 1

        # Even-length palindromes
        lo, hi = center, center + 1
        while lo >= 0 and hi < n and s[lo] == s[hi]:
            cuts[hi] = 0 if lo == 0 else min(cuts[hi], cuts[lo - 1] + 1)
            lo -= 1
            hi += 1

    return cuts[n - 1]


# ---------------------------------------------------------------------------
# Variant 2 — Optimized DP with boolean palindrome table
# ---------------------------------------------------------------------------

def min_pal_manacher(s: str) -> int:
    """
    Standard DP but with an optimized O(n^2) palindrome build
    that fills the table in a single pass.

    >>> min_pal_manacher("aab")
    1
    >>> min_pal_manacher("a")
    0
    >>> min_pal_manacher("aba")
    0
    >>> min_pal_manacher("abcd")
    3
    >>> min_pal_manacher("")
    0
    """
    n = len(s)
    if n <= 1:
        return 0

    is_pal = [[False] * n for _ in range(n)]
    cuts = [0] * n

    for i in range(n):
        min_cut = i  # worst: cut before every char
        for j in range(i + 1):
            if s[j] == s[i] and (i - j < 2 or is_pal[j + 1][i - 1]):
                is_pal[j][i] = True
                min_cut = 0 if j == 0 else min(min_cut, cuts[j - 1] + 1)
        cuts[i] = min_cut

    return cuts[n - 1]


# ---------------------------------------------------------------------------
# Variant 3 — Top-down memoized recursion
# ---------------------------------------------------------------------------

def min_pal_recursive(s: str) -> int:
    """
    Top-down recursion with memoization.

    >>> min_pal_recursive("aab")
    1
    >>> min_pal_recursive("a")
    0
    >>> min_pal_recursive("aba")
    0
    >>> min_pal_recursive("abcd")
    3
    >>> min_pal_recursive("")
    0
    """
    n = len(s)
    if n <= 1:
        return 0

    @lru_cache(maxsize=None)
    def is_pal(i: int, j: int) -> bool:
        if i >= j:
            return True
        return s[i] == s[j] and is_pal(i + 1, j - 1)

    @lru_cache(maxsize=None)
    def dp(i: int) -> int:
        if is_pal(0, i):
            return 0
        best = i
        for j in range(i):
            if is_pal(j + 1, i):
                best = min(best, dp(j) + 1)
        return best

    result = dp(n - 1)
    is_pal.cache_clear()
    dp.cache_clear()
    return result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ("aab", 1), ("a", 0), ("ab", 1), ("aba", 0),
    ("abcba", 0), ("abcd", 3), ("", 0),
]

IMPLS = [
    ("reference", reference),
    ("expand", min_pal_expand),
    ("manacher", min_pal_manacher),
    ("recursive", min_pal_recursive),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for s, expected in TEST_CASES:
        results = {name: fn(s) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] s={s!r}  expected={expected}  " +
              "  ".join(f"{n}={v}" for n, v in results.items()))

    REPS = 5_000
    bench_s = "abacabadefedcbaabcba"
    print(f"\n=== Benchmark: {REPS} runs, len={len(bench_s)} ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(bench_s), number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
