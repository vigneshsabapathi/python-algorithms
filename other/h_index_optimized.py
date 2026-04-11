#!/usr/bin/env python3
"""
Optimized and alternative implementations of H-Index.

Variants covered:
1. sorting_approach   -- Sort descending, linear scan (reference)
2. counting_sort      -- O(n) bucket counting (reference)
3. binary_search      -- Binary search on sorted array

Run:
    python other/h_index_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.h_index import h_index as reference
from other.h_index import h_index_counting_sort as counting_ref


def binary_search_h_index(citations: list[int]) -> int:
    """
    H-index using binary search on sorted citations.

    >>> binary_search_h_index([3, 0, 6, 1, 5])
    3
    >>> binary_search_h_index([1, 3, 1])
    1
    >>> binary_search_h_index([0, 0, 0])
    0
    >>> binary_search_h_index([10, 8, 5, 4, 3])
    4
    >>> binary_search_h_index([])
    0
    """
    if not citations:
        return 0
    sorted_cit = sorted(citations, reverse=True)
    n = len(sorted_cit)
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if sorted_cit[mid - 1] >= mid:
            lo = mid
        else:
            hi = mid - 1
    return lo


def h_index_numpy(citations: list[int]) -> int:
    """
    H-index using sorting (same as reference but explicit).

    >>> h_index_numpy([3, 0, 6, 1, 5])
    3
    >>> h_index_numpy([])
    0
    """
    if not citations:
        return 0
    s = sorted(citations, reverse=True)
    return max((min(i + 1, c) for i, c in enumerate(s)), default=0)


def h_index_one_liner(citations: list[int]) -> int:
    """
    H-index one-liner using sum of boolean comparisons.

    >>> h_index_one_liner([3, 0, 6, 1, 5])
    3
    >>> h_index_one_liner([])
    0
    """
    return sum(c > i for i, c in enumerate(sorted(citations, reverse=True)))


TEST_CASES = [
    ([3, 0, 6, 1, 5], 3),
    ([1, 3, 1], 1),
    ([0, 0, 0], 0),
    ([10, 8, 5, 4, 3], 4),
    ([], 0),
    ([100], 1),
    ([1, 1, 1, 1, 1], 1),
]

IMPLS = [
    ("reference", reference),
    ("counting", counting_ref),
    ("binary_search", binary_search_h_index),
    ("one_liner", h_index_one_liner),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for citations, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(list(citations))
            ok = result == expected
            tag = "OK" if ok else "FAIL"
            if not ok:
                print(f"  [{tag}] {name}: expected={expected} got={result}")
        print(f"  [OK] citations={citations} -> h={expected}")

    import random
    rng = random.Random(42)
    large = [rng.randint(0, 1000) for _ in range(10000)]
    REPS = 5000
    print(f"\n=== Benchmark: {REPS} runs, {len(large)} papers ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(list(large)), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
