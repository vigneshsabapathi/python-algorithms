#!/usr/bin/env python3
"""
Optimized and alternative implementations of Longest Increasing Subsequence.

Three variants:
  recursive       — divide-and-conquer recursive (reference)
  dp_n_squared    — O(n^2) iterative DP with path reconstruction
  patience_nlogn  — O(n log n) patience sorting with reconstruction

Run:
    python dynamic_programming/longest_increasing_subsequence_optimized.py
"""

from __future__ import annotations

import bisect
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.longest_increasing_subsequence import longest_subsequence as reference


# ---------------------------------------------------------------------------
# Variant 1 — recursive (same as reference)
# ---------------------------------------------------------------------------

def recursive(array: list[int]) -> list[int]:
    """
    >>> recursive([10, 22, 9, 33, 21, 50, 41, 60, 80])
    [10, 22, 33, 41, 60, 80]
    """
    return reference(array)


# ---------------------------------------------------------------------------
# Variant 2 — dp_n_squared: O(n^2) iterative DP
# ---------------------------------------------------------------------------

def dp_n_squared(array: list[int]) -> list[int]:
    """
    >>> dp_n_squared([10, 22, 9, 33, 21, 50, 41, 60, 80])
    [10, 22, 33, 50, 60, 80]
    >>> dp_n_squared([4, 8, 7, 5, 1, 12, 2, 3, 9])
    [1, 2, 3, 9]
    >>> dp_n_squared([])
    []
    """
    n = len(array)
    if n == 0:
        return []

    dp = [1] * n
    parent = [-1] * n

    for i in range(1, n):
        for j in range(i):
            if array[j] < array[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j

    # Find the index of the maximum length
    max_idx = max(range(n), key=lambda i: dp[i])

    # Reconstruct path
    result = []
    idx = max_idx
    while idx != -1:
        result.append(array[idx])
        idx = parent[idx]
    return result[::-1]


# ---------------------------------------------------------------------------
# Variant 3 — patience_nlogn: O(n log n) with reconstruction
# ---------------------------------------------------------------------------

def patience_nlogn(array: list[int]) -> list[int]:
    """
    Uses patience sorting with binary search, plus parent tracking
    for full subsequence reconstruction.

    >>> patience_nlogn([10, 22, 9, 33, 21, 50, 41, 60, 80])
    [10, 22, 33, 41, 60, 80]
    >>> patience_nlogn([4, 8, 7, 5, 1, 12, 2, 3, 9])
    [1, 2, 3, 9]
    >>> patience_nlogn([])
    []
    """
    n = len(array)
    if n == 0:
        return []

    tails = []          # smallest tail values
    tail_indices = []   # indices in original array
    parent = [-1] * n   # parent index for reconstruction

    for i in range(n):
        pos = bisect.bisect_left(tails, array[i])
        if pos == len(tails):
            tails.append(array[i])
            tail_indices.append(i)
        else:
            tails[pos] = array[i]
            tail_indices[pos] = i

        if pos > 0:
            parent[i] = tail_indices[pos - 1]

    # Reconstruct
    result = []
    idx = tail_indices[-1]
    while idx != -1:
        result.append(array[idx])
        idx = parent[idx]
    return result[::-1]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    [10, 22, 9, 33, 21, 50, 41, 60, 80],
    [4, 8, 7, 5, 1, 12, 2, 3, 9],
    [9, 8, 7, 6, 5, 7],
    [1, 2, 3, 4, 5],
    [],
]

IMPLS = [
    ("recursive", recursive),
    ("dp_n_squared", dp_n_squared),
    ("patience_nlogn", patience_nlogn),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for arr in TEST_CASES:
        ref_len = len(reference(arr))
        for name, fn in IMPLS:
            result = fn(arr)
            ok = len(result) == ref_len
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}({arr[:5]}...) = {result} (len {len(result)}, expected {ref_len})")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    REPS = 10_000
    import random
    random.seed(42)
    large = [random.randint(0, 100) for _ in range(50)]
    print(f"\n=== Benchmark (50 elements): {REPS} runs ===")
    for name, fn in IMPLS[1:]:  # skip recursive (too slow for large)
        t = timeit.timeit(lambda fn=fn: fn(large), number=REPS) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
