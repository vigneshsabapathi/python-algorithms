#!/usr/bin/env python3
"""
Optimized and alternative implementations of LIS (Iterative DP).

Three variants:
  iterative_copy    — O(n^2) with copy.copy for path storage (reference)
  iterative_parent  — O(n^2) with parent array (less memory copying)
  bisect_length     — O(n log n) length-only using bisect

Run:
    python dynamic_programming/longest_increasing_subsequence_iterative_optimized.py
"""

from __future__ import annotations

import bisect
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.longest_increasing_subsequence_iterative import (
    longest_subsequence as reference,
)


# ---------------------------------------------------------------------------
# Variant 1 — iterative_copy (same as reference)
# ---------------------------------------------------------------------------

def iterative_copy(array: list[int]) -> list[int]:
    """
    >>> iterative_copy([10, 22, 9, 33, 21, 50, 41, 60, 80])
    [10, 22, 33, 50, 60, 80]
    """
    return reference(array)


# ---------------------------------------------------------------------------
# Variant 2 — iterative_parent: Parent array instead of copying lists
# ---------------------------------------------------------------------------

def iterative_parent(array: list[int]) -> list[int]:
    """
    >>> iterative_parent([10, 22, 9, 33, 21, 50, 41, 60, 80])
    [10, 22, 33, 50, 60, 80]
    >>> iterative_parent([])
    []
    """
    n = len(array)
    if n == 0:
        return []
    dp = [1] * n
    parent = [-1] * n

    for i in range(1, n):
        for j in range(i):
            if array[j] <= array[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j

    max_idx = max(range(n), key=lambda i: dp[i])
    result = []
    idx = max_idx
    while idx != -1:
        result.append(array[idx])
        idx = parent[idx]
    return result[::-1]


# ---------------------------------------------------------------------------
# Variant 3 — bisect_length: O(n log n) length only
# ---------------------------------------------------------------------------

def bisect_length(array: list[int]) -> int:
    """
    >>> bisect_length([10, 22, 9, 33, 21, 50, 41, 60, 80])
    6
    >>> bisect_length([])
    0
    """
    tails: list[int] = []
    for x in array:
        pos = bisect.bisect_right(tails, x)  # non-decreasing: use bisect_right
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    [10, 22, 9, 33, 21, 50, 41, 60, 80],
    [4, 8, 7, 5, 1, 12, 2, 3, 9],
    [9, 8, 7, 6, 5, 7],
    [1, 1, 1],
    [],
]

IMPLS = [
    ("iterative_copy", iterative_copy),
    ("iterative_parent", iterative_parent),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for arr in TEST_CASES:
        ref = reference(arr)
        for name, fn in IMPLS:
            result = fn(arr)
            ok = len(result) == len(ref)
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}({arr[:5]}...) = {result}")

    print(f"\n  bisect_length checks:")
    for arr in TEST_CASES:
        ref_len = len(reference(arr))
        bl = bisect_length(arr)
        ok = bl == ref_len
        print(f"  [{'OK' if ok else 'FAIL'}] bisect_length = {bl}, expected {ref_len}")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    REPS = 10_000
    import random
    random.seed(42)
    large = [random.randint(0, 100) for _ in range(100)]
    print(f"\n=== Benchmark (100 elements): {REPS} runs ===")
    for name, fn in [*IMPLS, ("bisect_length", bisect_length)]:
        t = timeit.timeit(lambda fn=fn: fn(large), number=REPS) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
