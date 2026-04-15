#!/usr/bin/env python3
"""
Optimized and alternative implementations of Wildcard Matching.

Variants covered:
1. wildcard_greedy       -- two-pointer greedy with backtracking
2. wildcard_space_opt    -- O(n) space DP
3. wildcard_recursive    -- memoized recursion

Run:
    python dynamic_programming/wildcard_matching_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.wildcard_matching import wildcard_match as reference


# ---------------------------------------------------------------------------
# Variant 1 — Two-pointer greedy with backtracking
# ---------------------------------------------------------------------------

def wildcard_greedy(text: str, pattern: str) -> bool:
    """
    Wildcard matching using greedy two-pointer approach.

    O(m*n) worst case but typically O(m+n) for practical inputs.

    >>> wildcard_greedy("aa", "a")
    False
    >>> wildcard_greedy("aa", "*")
    True
    >>> wildcard_greedy("cb", "?a")
    False
    >>> wildcard_greedy("adceb", "*a*b")
    True
    >>> wildcard_greedy("acdcb", "a*c?b")
    False
    >>> wildcard_greedy("", "")
    True
    >>> wildcard_greedy("", "*")
    True
    """
    m, n = len(text), len(pattern)
    ti = pi = 0
    star_idx = -1
    match_idx = 0

    while ti < m:
        if pi < n and (pattern[pi] == "?" or pattern[pi] == text[ti]):
            ti += 1
            pi += 1
        elif pi < n and pattern[pi] == "*":
            star_idx = pi
            match_idx = ti
            pi += 1
        elif star_idx != -1:
            pi = star_idx + 1
            match_idx += 1
            ti = match_idx
        else:
            return False

    while pi < n and pattern[pi] == "*":
        pi += 1

    return pi == n


# ---------------------------------------------------------------------------
# Variant 2 — Space-optimized DP
# ---------------------------------------------------------------------------

def wildcard_space_opt(text: str, pattern: str) -> bool:
    """
    Wildcard matching with O(n) space.

    >>> wildcard_space_opt("aa", "a")
    False
    >>> wildcard_space_opt("aa", "*")
    True
    >>> wildcard_space_opt("cb", "?a")
    False
    >>> wildcard_space_opt("adceb", "*a*b")
    True
    >>> wildcard_space_opt("acdcb", "a*c?b")
    False
    >>> wildcard_space_opt("", "")
    True
    """
    m, n = len(text), len(pattern)
    prev = [False] * (n + 1)
    prev[0] = True
    for j in range(1, n + 1):
        if pattern[j - 1] == "*":
            prev[j] = prev[j - 1]

    for i in range(1, m + 1):
        curr = [False] * (n + 1)
        for j in range(1, n + 1):
            if pattern[j - 1] == "*":
                curr[j] = prev[j] or curr[j - 1]
            elif pattern[j - 1] == "?" or pattern[j - 1] == text[i - 1]:
                curr[j] = prev[j - 1]
        prev = curr

    return prev[n]


# ---------------------------------------------------------------------------
# Variant 3 — Memoized recursion
# ---------------------------------------------------------------------------

def wildcard_recursive(text: str, pattern: str) -> bool:
    """
    Wildcard matching using memoized recursion.

    >>> wildcard_recursive("aa", "a")
    False
    >>> wildcard_recursive("aa", "*")
    True
    >>> wildcard_recursive("cb", "?a")
    False
    >>> wildcard_recursive("adceb", "*a*b")
    True
    >>> wildcard_recursive("acdcb", "a*c?b")
    False
    >>> wildcard_recursive("", "")
    True
    """
    @lru_cache(maxsize=None)
    def dp(i: int, j: int) -> bool:
        if j == len(pattern):
            return i == len(text)
        if pattern[j] == "*":
            return dp(i, j + 1) or (i < len(text) and dp(i + 1, j))
        if i < len(text) and (pattern[j] == "?" or pattern[j] == text[i]):
            return dp(i + 1, j + 1)
        return False

    result = dp(0, 0)
    dp.cache_clear()
    return result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ("aa", "a", False),
    ("aa", "*", True),
    ("cb", "?a", False),
    ("adceb", "*a*b", True),
    ("acdcb", "a*c?b", False),
    ("", "", True),
    ("", "*", True),
    ("abc", "abc", True),
]

IMPLS = [
    ("reference", reference),
    ("greedy", wildcard_greedy),
    ("space_opt", wildcard_space_opt),
    ("recursive", wildcard_recursive),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for text, pattern, expected in TEST_CASES:
        results = {name: fn(text, pattern) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] ({text!r}, {pattern!r})  expected={expected}  " +
              "  ".join(f"{n}={v}" for n, v in results.items()))

    REPS = 20_000
    t_text, t_pat = "abcdefghijklmnop", "*d*h*p"
    print(f"\n=== Benchmark: {REPS} runs, ({t_text!r}, {t_pat!r}) ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(t_text, t_pat), number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
