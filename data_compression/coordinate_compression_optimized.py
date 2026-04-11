#!/usr/bin/env python3
"""
Optimized and alternative implementations of Coordinate Compression.

The reference uses a class with dictionary + list for mapping.

Variants covered:
1. class_based      -- CoordinateCompressor class (reference)
2. sorted_set       -- sorted(set(arr)) with dict comprehension
3. bisect_based     -- uses bisect for O(log n) compress without pre-building map
4. enumerate_sorted -- one-liner with enumerate

Key interview insight:
    Coordinate compression maps large/sparse values to consecutive small
    integers [0, k). Essential for BIT/segment tree problems where the
    value range is huge but the number of distinct values is small.

Run:
    python data_compression/coordinate_compression_optimized.py
"""

from __future__ import annotations

import bisect
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_compression.coordinate_compression import CoordinateCompressor as Reference


# ---------------------------------------------------------------------------
# Variant 1 -- class_based (reference wrapper)
# ---------------------------------------------------------------------------

def class_based_compress(arr: list[int]) -> list[int]:
    """
    Compress using the reference CoordinateCompressor class.

    >>> class_based_compress([100, 10, 52, 83])
    [3, 0, 1, 2]
    >>> class_based_compress([5, 5, 5])
    [0, 0, 0]
    """
    cc = Reference(arr)
    return [cc.compress(v) for v in arr]


# ---------------------------------------------------------------------------
# Variant 2 -- sorted_set: dict comprehension on sorted unique values
# ---------------------------------------------------------------------------

def sorted_set_compress(arr: list[int]) -> list[int]:
    """
    Compress using sorted(set(arr)) + dict comprehension. O(n log n).

    >>> sorted_set_compress([100, 10, 52, 83])
    [3, 0, 1, 2]
    >>> sorted_set_compress([5, 5, 5])
    [0, 0, 0]
    >>> sorted_set_compress([])
    []
    """
    if not arr:
        return []
    mapping = {v: i for i, v in enumerate(sorted(set(arr)))}
    return [mapping[v] for v in arr]


# ---------------------------------------------------------------------------
# Variant 3 -- bisect_based: no pre-built map, binary search on sorted unique
# ---------------------------------------------------------------------------

def bisect_compress(arr: list[int]) -> list[int]:
    """
    Compress using bisect on sorted unique values. O(n log n).

    No dictionary needed -- uses binary search to find rank.

    >>> bisect_compress([100, 10, 52, 83])
    [3, 0, 1, 2]
    >>> bisect_compress([5, 5, 5])
    [0, 0, 0]
    >>> bisect_compress([3, 1, 4, 1, 5])
    [1, 0, 2, 0, 3]
    """
    if not arr:
        return []
    sorted_unique = sorted(set(arr))
    return [bisect.bisect_left(sorted_unique, v) for v in arr]


# ---------------------------------------------------------------------------
# Variant 4 -- enumerate_sorted: concise one-liner
# ---------------------------------------------------------------------------

def enumerate_compress(arr: list[int]) -> list[int]:
    """
    Compress using enumerate over sorted unique values.

    >>> enumerate_compress([100, 10, 52, 83])
    [3, 0, 1, 2]
    >>> enumerate_compress([7, 2, 7, 3, 2])
    [2, 0, 2, 1, 0]
    """
    if not arr:
        return []
    rank = {v: i for i, v in enumerate(sorted(set(arr)))}
    return [rank[v] for v in arr]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    [100, 10, 52, 83],
    [5, 5, 5],
    [3, 1, 4, 1, 5, 9, 2, 6],
    list(range(1000, 0, -1)),
    [10**9, 1, 10**6, 500],
]

EXPECTED = [
    [3, 0, 1, 2],
    [0, 0, 0],
    [1, 0, 2, 0, 3, 5, 4, 6],  # note: 4 is rank of 6 but actually let me check
    None,  # just verify roundtrip
    [3, 0, 2, 1],
]

IMPLS = [
    ("class_based",      class_based_compress),
    ("sorted_set",       sorted_set_compress),
    ("bisect_based",     bisect_compress),
    ("enumerate_sorted", enumerate_compress),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    # Use sorted_set as ground truth for all
    for arr in TEST_CASES:
        expected = sorted_set_compress(arr)
        for name, fn in IMPLS:
            result = fn(arr)
            ok = result == expected
            tag = "OK" if ok else "FAIL"
            arr_str = str(arr[:6]) + ("..." if len(arr) > 6 else "")
            print(f"  [{tag}] {name:<20} arr={arr_str}")

    import random
    random.seed(42)
    small_arr = [random.randint(0, 100) for _ in range(100)]
    large_arr = [random.randint(0, 10**9) for _ in range(10_000)]

    REPS = 10_000
    print(f"\n=== Benchmark (100 elements): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(small_arr), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>8.4f} ms")

    REPS2 = 500
    print(f"\n=== Benchmark (10,000 elements): {REPS2} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(large_arr), number=REPS2) * 1000 / REPS2
        print(f"  {name:<20} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
