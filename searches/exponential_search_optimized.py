#!/usr/bin/env python3

"""
Optimized and alternative implementations of exponential search.

Variants covered:
1. exponential_search_iterative_bisect  — replaces recursive binary search with
   stdlib bisect (iterative, no recursion limit, fastest in practice)
2. exponential_search_iterative         — fully iterative fallback (no stdlib)
3. exponential_search_numpy             — vectorised bisect via numpy.searchsorted
4. bisect_only                          — pure stdlib bisect (baseline comparison)

Run benchmarks:
    python searches/exponential_search_optimized.py
"""

from __future__ import annotations

import bisect
import timeit
from typing import Sequence

# ---------------------------------------------------------------------------
# Variant 1 — stdlib bisect replaces the recursive helper (recommended)
# ---------------------------------------------------------------------------


def exponential_search_iterative_bisect(
    sorted_collection: list[int], item: int
) -> int:
    """
    Exponential search using stdlib bisect.bisect_left for the binary phase.

    Avoids recursion depth limits; bisect is implemented in C so it's fast.

    :param sorted_collection: ascending-sorted list
    :param item: value to find
    :return: index of item, or -1 if not found

    >>> exponential_search_iterative_bisect([0, 5, 7, 10, 15], 0)
    0
    >>> exponential_search_iterative_bisect([0, 5, 7, 10, 15], 15)
    4
    >>> exponential_search_iterative_bisect([0, 5, 7, 10, 15], 5)
    1
    >>> exponential_search_iterative_bisect([0, 5, 7, 10, 15], 6)
    -1
    """
    if not sorted_collection:
        return -1
    if sorted_collection[0] == item:
        return 0

    n = len(sorted_collection)
    bound = 1
    while bound < n and sorted_collection[bound] < item:
        bound *= 2

    left = bound // 2
    right = min(bound, n - 1)

    idx = bisect.bisect_left(sorted_collection, item, left, right + 1)
    if idx <= right and sorted_collection[idx] == item:
        return idx
    return -1


# ---------------------------------------------------------------------------
# Variant 2 — fully iterative (no stdlib, no recursion)
# ---------------------------------------------------------------------------


def _binary_search_iterative(
    col: list[int], item: int, left: int, right: int
) -> int:
    """Iterative binary search within [left, right]."""
    while left <= right:
        mid = left + (right - left) // 2
        if col[mid] == item:
            return mid
        elif col[mid] < item:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def exponential_search_iterative(sorted_collection: list[int], item: int) -> int:
    """
    Fully iterative exponential search (no recursion, no stdlib).

    >>> exponential_search_iterative([0, 5, 7, 10, 15], 0)
    0
    >>> exponential_search_iterative([0, 5, 7, 10, 15], 15)
    4
    >>> exponential_search_iterative([0, 5, 7, 10, 15], 5)
    1
    >>> exponential_search_iterative([0, 5, 7, 10, 15], 6)
    -1
    """
    if not sorted_collection:
        return -1
    if sorted_collection[0] == item:
        return 0

    n = len(sorted_collection)
    bound = 1
    while bound < n and sorted_collection[bound] < item:
        bound *= 2

    left = bound // 2
    right = min(bound, n - 1)
    return _binary_search_iterative(sorted_collection, item, left, right)


# ---------------------------------------------------------------------------
# Variant 3 — numpy vectorised (best for bulk / repeated lookups)
# ---------------------------------------------------------------------------


def exponential_search_numpy(sorted_collection: list[int], item: int) -> int:
    """
    Exponential search using numpy.searchsorted for the binary phase.

    numpy.searchsorted is O(log n) and heavily optimised for numeric arrays.
    Overhead of np.asarray makes this slower for single lookups on small lists,
    but dominant for large arrays or repeated queries on the same array.

    >>> exponential_search_numpy([0, 5, 7, 10, 15], 0)
    0
    >>> exponential_search_numpy([0, 5, 7, 10, 15], 15)
    4
    >>> exponential_search_numpy([0, 5, 7, 10, 15], 5)
    1
    >>> exponential_search_numpy([0, 5, 7, 10, 15], 6)
    -1
    """
    import numpy as np

    arr = np.asarray(sorted_collection)
    if arr.size == 0:
        return -1
    if arr[0] == item:
        return 0

    n = len(arr)
    bound = 1
    while bound < n and arr[bound] < item:
        bound *= 2

    left = bound // 2
    right = min(bound, n - 1)

    idx = int(np.searchsorted(arr, item, side="left", sorter=None))
    # searchsorted searches full array; verify result is within our window and correct
    if left <= idx <= right and arr[idx] == item:
        return idx
    return -1


# ---------------------------------------------------------------------------
# Baseline — pure bisect (no exponential phase)
# ---------------------------------------------------------------------------


def bisect_only(sorted_collection: list[int], item: int) -> int:
    """
    Pure stdlib bisect on the full list — O(log n) baseline.

    >>> bisect_only([0, 5, 7, 10, 15], 0)
    0
    >>> bisect_only([0, 5, 7, 10, 15], 15)
    4
    >>> bisect_only([0, 5, 7, 10, 15], 5)
    1
    >>> bisect_only([0, 5, 7, 10, 15], 6)
    -1
    """
    idx = bisect.bisect_left(sorted_collection, item)
    if idx < len(sorted_collection) and sorted_collection[idx] == item:
        return idx
    return -1


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------


def benchmark() -> None:
    import random

    sizes = [1_000, 100_000, 1_000_000]
    REPS = 500

    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from searches.exponential_search import exponential_search as exp_recursive

    fns = [
        ("exponential (recursive bisect — original)", exp_recursive),
        ("exponential (iterative bisect — stdlib)",   exponential_search_iterative_bisect),
        ("exponential (fully iterative)",              exponential_search_iterative),
        ("exponential (numpy)",                        exponential_search_numpy),
        ("bisect only (baseline)",                     bisect_only),
    ]

    for size in sizes:
        data = sorted(random.sample(range(size * 10), size))
        targets = [random.choice(data) for _ in range(REPS)]   # hits
        targets += [random.randint(0, size * 10) for _ in range(REPS)]  # misses

        print(f"\n{'='*60}")
        print(f"  n = {size:,}  ({REPS*2} lookups: {REPS} hits + {REPS} misses)")
        print(f"{'='*60}")

        results = {}
        for name, fn in fns:
            try:
                t = timeit.timeit(
                    lambda fn=fn, targets=targets, data=data: [fn(data, t) for t in targets],
                    number=5,
                )
                results[name] = t
                print(f"  {name:<48}  {t*1000/5:7.2f} ms/run")
            except Exception as e:
                print(f"  {name:<48}  ERROR: {e}")

        best = min(results, key=results.get)
        print(f"\n  Winner: {best}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
