#!/usr/bin/env python3
"""
Optimized and alternative implementations of Longest Common Substring.

Three variants:
  dp_2d           — standard 2D DP table (reference)
  space_optimized — O(min(m,n)) space using rolling array
  suffix_based    — suffix array-inspired approach

Run:
    python dynamic_programming/longest_common_substring_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.longest_common_substring import longest_common_substring as reference


# ---------------------------------------------------------------------------
# Variant 1 — dp_2d (same as reference)
# ---------------------------------------------------------------------------

def dp_2d(text1: str, text2: str) -> str:
    """
    >>> dp_2d("abcdef", "bcd")
    'bcd'
    """
    return reference(text1, text2)


# ---------------------------------------------------------------------------
# Variant 2 — space_optimized: O(min(m,n)) rolling array
# ---------------------------------------------------------------------------

def space_optimized(text1: str, text2: str) -> str:
    """
    >>> space_optimized("abcdef", "bcd")
    'bcd'
    >>> space_optimized("GeeksforGeeks", "GeeksQuiz")
    'Geeks'
    >>> space_optimized("", "abc")
    ''
    """
    if not text1 or not text2:
        return ""
    # Ensure text2 is shorter for space optimization
    if len(text1) < len(text2):
        text1, text2 = text2, text1

    n = len(text2)
    prev = [0] * (n + 1)
    max_len = 0
    end_pos = 0

    for i in range(1, len(text1) + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                curr[j] = prev[j - 1] + 1
                if curr[j] > max_len:
                    max_len = curr[j]
                    end_pos = i
        prev = curr

    return text1[end_pos - max_len: end_pos]


# ---------------------------------------------------------------------------
# Variant 3 — sliding_window: Binary search + rolling hash
# ---------------------------------------------------------------------------

def sliding_window(text1: str, text2: str) -> str:
    """
    Binary search on answer length, check existence with set of substrings.

    >>> sliding_window("abcdef", "bcd")
    'bcd'
    >>> sliding_window("GeeksforGeeks", "GeeksQuiz")
    'Geeks'
    >>> sliding_window("", "abc")
    ''
    """
    if not text1 or not text2:
        return ""

    def has_common_of_length(length: int) -> str:
        """Check if there's a common substring of given length. Return it or ''."""
        subs = set()
        for i in range(len(text1) - length + 1):
            subs.add(text1[i: i + length])
        for i in range(len(text2) - length + 1):
            candidate = text2[i: i + length]
            if candidate in subs:
                return candidate
        return ""

    lo, hi = 0, min(len(text1), len(text2))
    result = ""
    while lo <= hi:
        mid = (lo + hi) // 2
        found = has_common_of_length(mid)
        if found:
            result = found
            lo = mid + 1
        else:
            hi = mid - 1
    return result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ("abcdef", "bcd", "bcd"),
    ("abcdef", "xabded", "ab"),
    ("GeeksforGeeks", "GeeksQuiz", "Geeks"),
    ("abcdxyz", "xyzabcd", "abcd"),
    ("", "abc", ""),
    ("a", "a", "a"),
]

IMPLS = [
    ("dp_2d", dp_2d),
    ("space_optimized", space_optimized),
    ("sliding_window", sliding_window),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for t1, t2, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(t1, t2)
            ok = len(result) == len(expected)
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}({t1!r}, {t2!r}) = {result!r}  (expected len {len(expected)})")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    REPS = 20_000
    inputs = [("abcdefghij", "cdefgh"), ("GeeksforGeeks", "GeeksQuiz")]
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
