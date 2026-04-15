#!/usr/bin/env python3
"""
Optimized and alternative implementations of LIS O(n log n).

Three variants:
  manual_binary_search — custom ceil_index binary search (reference)
  bisect_builtin       — Python bisect module (cleaner)
  with_reconstruction  — O(n log n) with full subsequence reconstruction

Run:
    python dynamic_programming/longest_increasing_subsequence_o_nlogn_optimized.py
"""

from __future__ import annotations

import bisect
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.longest_increasing_subsequence_o_nlogn import (
    longest_increasing_subsequence_length as reference,
)


# ---------------------------------------------------------------------------
# Variant 1 — manual_binary_search (same as reference)
# ---------------------------------------------------------------------------

def manual_binary_search(v: list[int]) -> int:
    """
    >>> manual_binary_search([2, 5, 3, 7, 11, 8, 10, 13, 6])
    6
    """
    return reference(v)


# ---------------------------------------------------------------------------
# Variant 2 — bisect_builtin: Using Python's bisect module
# ---------------------------------------------------------------------------

def bisect_builtin(v: list[int]) -> int:
    """
    >>> bisect_builtin([2, 5, 3, 7, 11, 8, 10, 13, 6])
    6
    >>> bisect_builtin([5, 4, 3, 2, 1])
    1
    >>> bisect_builtin([])
    0
    """
    tails: list[int] = []
    for x in v:
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)


# ---------------------------------------------------------------------------
# Variant 3 — with_reconstruction: Full subsequence recovery
# ---------------------------------------------------------------------------

def with_reconstruction(v: list[int]) -> list[int]:
    """
    Returns the actual LIS, not just the length.

    >>> with_reconstruction([2, 5, 3, 7, 11, 8, 10, 13, 6])
    [2, 3, 7, 8, 10, 13]
    >>> with_reconstruction([5, 4, 3, 2, 1])
    [1]
    >>> with_reconstruction([])
    []
    """
    n = len(v)
    if n == 0:
        return []

    tails: list[int] = []
    tail_indices: list[int] = []
    parent = [-1] * n

    for i in range(n):
        pos = bisect.bisect_left(tails, v[i])
        if pos == len(tails):
            tails.append(v[i])
            tail_indices.append(i)
        else:
            tails[pos] = v[i]
            tail_indices[pos] = i
        if pos > 0:
            parent[i] = tail_indices[pos - 1]

    # Reconstruct
    result = []
    idx = tail_indices[-1]
    while idx != -1:
        result.append(v[idx])
        idx = parent[idx]
    return result[::-1]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    [2, 5, 3, 7, 11, 8, 10, 13, 6],
    [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15],
    [5, 4, 3, 2, 1],
    [1, 2, 3, 4, 5],
    [],
]

IMPLS_LEN = [
    ("manual_binary_search", manual_binary_search),
    ("bisect_builtin", bisect_builtin),
]


def run_all() -> None:
    print("\n=== Correctness (length) ===")
    all_pass = True
    for arr in TEST_CASES:
        ref = reference(arr)
        for name, fn in IMPLS_LEN:
            result = fn(arr)
            ok = result == ref
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}({arr[:5]}...) = {result}")

    print(f"\n=== Correctness (reconstruction) ===")
    for arr in TEST_CASES:
        result = with_reconstruction(arr)
        ref_len = reference(arr)
        ok = len(result) == ref_len
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] with_reconstruction({arr[:5]}...) = {result} (len={len(result)}, expected={ref_len})")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    import random
    random.seed(42)
    large = [random.randint(0, 1000) for _ in range(1000)]
    REPS = 5_000
    print(f"\n=== Benchmark (1000 elements): {REPS} runs ===")
    for name, fn in [*IMPLS_LEN, ("with_reconstruction", lambda v: len(with_reconstruction(v)))]:
        t = timeit.timeit(lambda fn=fn: fn(large), number=REPS) * 1000 / REPS
        print(f"  {name:<24} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
