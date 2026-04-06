#!/usr/bin/env python3

"""
Optimized and alternative implementations of simple binary search (bool result).

This module focuses on the bool-returning interface (exists or not), contrasting
with binary_search.py which returns the index.

Variants:
1. binary_search_iterative — O(1) space; no slicing copies; same bool result
2. binary_search_bisect    — stdlib bisect, C-backed O(log n), returns bool
3. binary_search_in_op     — `item in sequence` operator (C loop; O(log n) for
                             range/sorted containers; O(n) for plain lists)
4. binary_search_set       — convert to set, O(1) average lookup (unsorted OK)

Run benchmarks:
    python searches/simple_binary_search_optimized.py
"""

from __future__ import annotations

import bisect
from collections.abc import Sequence
from typing import Any


# ---------------------------------------------------------------------------
# Variant 1 — iterative, no slicing (O(log n) time, O(1) space)
# ---------------------------------------------------------------------------


def binary_search_iterative(a_list: Sequence, item: Any) -> bool:
    """
    Iterative binary search returning bool.

    Avoids the O(n) total space cost of the recursive version's list slices.
    Works on any random-access sorted sequence (list, tuple, range).

    >>> binary_search_iterative([0, 1, 2, 8, 13, 17, 19, 32, 42], 13)
    True
    >>> binary_search_iterative([0, 1, 2, 8, 13, 17, 19, 32, 42], 3)
    False
    >>> binary_search_iterative([], 1)
    False
    >>> binary_search_iterative([5], 5)
    True
    >>> binary_search_iterative(['a', 'c', 'd'], 'c')
    True
    >>> binary_search_iterative(['a', 'c', 'd'], 'f')
    False
    >>> binary_search_iterative(range(-5000, 5000, 10), 80)
    True
    >>> binary_search_iterative(range(-5000, 5000, 10), 1255)
    False
    """
    left, right = 0, len(a_list) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if a_list[mid] == item:
            return True
        elif item < a_list[mid]:
            right = mid - 1
        else:
            left = mid + 1
    return False


# ---------------------------------------------------------------------------
# Variant 2 — stdlib bisect (C-backed, O(log n))
# ---------------------------------------------------------------------------


def binary_search_bisect(a_list: list, item: Any) -> bool:
    """
    Uses bisect.bisect_left — C-backed O(log n), fastest for lists.

    >>> binary_search_bisect([0, 1, 2, 8, 13, 17, 19, 32, 42], 13)
    True
    >>> binary_search_bisect([0, 1, 2, 8, 13, 17, 19, 32, 42], 3)
    False
    >>> binary_search_bisect([], 1)
    False
    >>> binary_search_bisect([5], 5)
    True
    >>> binary_search_bisect(['a', 'c', 'd'], 'c')
    True
    >>> binary_search_bisect(['a', 'c', 'd'], 'f')
    False
    """
    if not a_list:
        return False
    idx = bisect.bisect_left(a_list, item)
    return idx < len(a_list) and a_list[idx] == item


# ---------------------------------------------------------------------------
# Variant 3 — `in` operator
# ---------------------------------------------------------------------------


def binary_search_in_op(a_list: Sequence, item: Any) -> bool:
    """
    Uses the `in` operator.

    - For `list` / `tuple`: O(n) linear scan in C — same complexity as linear search.
    - For `range`: O(1) — range.__contains__ uses arithmetic, not iteration.
    - For `set` / `frozenset`: O(1) average hash lookup.

    Shown here as a comparison baseline: simple, Pythonic, sometimes optimal.

    >>> binary_search_in_op([0, 1, 2, 8, 13, 17, 19, 32, 42], 13)
    True
    >>> binary_search_in_op([0, 1, 2, 8, 13, 17, 19, 32, 42], 3)
    False
    >>> binary_search_in_op([], 1)
    False
    >>> binary_search_in_op(range(-5000, 5000, 10), 80)
    True
    >>> binary_search_in_op(range(-5000, 5000, 10), 1255)
    False
    """
    return item in a_list


# ---------------------------------------------------------------------------
# Variant 4 — set lookup (O(1) average, unsorted OK, one-time build cost)
# ---------------------------------------------------------------------------


def binary_search_set(a_list: list, item: Any) -> bool:
    """
    Converts to set for O(1) average lookup — optimal for repeated searches.

    NOT binary search — included to show when sorting/binary search is the
    wrong tool entirely.

    >>> binary_search_set([0, 1, 2, 8, 13, 17, 19, 32, 42], 13)
    True
    >>> binary_search_set([0, 1, 2, 8, 13, 17, 19, 32, 42], 3)
    False
    >>> binary_search_set([], 1)
    False
    >>> binary_search_set([5], 5)
    True
    """
    return item in set(a_list)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------


def benchmark() -> None:
    import random
    import timeit
    import sys
    import os

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from searches.simple_binary_search import binary_search as bs_original

    REPS = 500

    for size in [100, 1_000, 10_000]:
        random.seed(42)
        data = sorted(random.sample(range(size * 10), size))
        prebuilt_set = set(data)

        targets_hit  = random.choices(data, k=REPS)
        targets_miss = [random.randint(size * 10, size * 20) for _ in range(REPS)]
        targets = targets_hit + targets_miss

        print(f"\n{'='*64}")
        print(f"  n = {size:,}  ({REPS*2} lookups: {REPS} hits + {REPS} misses)")
        print(f"{'='*64}")

        fns_clean = [
            ("recursive+slice (original)", lambda t: bs_original(data, t)),
            ("iterative (no slice)",        lambda t: binary_search_iterative(data, t)),
            ("bisect (stdlib C)",           lambda t: binary_search_bisect(data, t)),
            ("in op on list (O(n))",        lambda t: t in data),
            ("set rebuild each call",       lambda t: binary_search_set(data, t)),
            ("prebuilt set (O(1))",         lambda t: t in prebuilt_set),
        ]

        results = {}
        for name, fn in fns_clean:
            t = timeit.timeit(lambda fn=fn: [fn(x) for x in targets], number=5)
            results[name] = t
            print(f"  {name:<38} {t*1000/5:8.3f} ms/run")

        best = min(results, key=results.get)
        print(f"\n  Winner: {best}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
