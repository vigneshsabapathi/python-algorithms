#!/usr/bin/env python3

"""
Optimized and alternative implementations of linear search.

Variants covered:
1. linear_search_index     — list.index() (C-backed O(n), raises on miss)
2. linear_search_index_safe — list.index() wrapped to return -1 on miss
3. linear_search_next      — next() + enumerate generator (short-circuits, lazy)
4. linear_search_in_index  — `in` check then .index() (two C passes but clean)
5. linear_search_numpy     — numpy.where for numeric arrays (vectorised)
6. bisect_search           — bisect.bisect_left for SORTED arrays (O(log n))

Run benchmarks:
    python searches/linear_search_optimized.py
"""

from __future__ import annotations

import bisect


# ---------------------------------------------------------------------------
# Variant 1 — list.index() (C-backed, raises ValueError on miss)
# ---------------------------------------------------------------------------


def linear_search_index(sequence: list, target) -> int:
    """
    Uses list.index() — C-backed linear scan; raises ValueError if not found.
    Wrap with try/except to match the -1 interface.

    This is the fastest pure-Python linear search because the loop runs in C.

    >>> linear_search_index([0, 5, 7, 10, 15], 0)
    0
    >>> linear_search_index([0, 5, 7, 10, 15], 15)
    4
    >>> linear_search_index([0, 5, 7, 10, 15], 5)
    1
    >>> linear_search_index([0, 5, 7, 10, 15], 6)
    -1
    >>> linear_search_index([], 5)
    -1
    """
    try:
        return sequence.index(target)
    except ValueError:
        return -1


# ---------------------------------------------------------------------------
# Variant 2 — next() + enumerate generator (lazy, Pythonic)
# ---------------------------------------------------------------------------


def linear_search_next(sequence: list, target) -> int:
    """
    Uses next() over an enumerate generator — short-circuits on first match,
    returns -1 via the default argument if exhausted.

    Slightly slower than list.index() but works on any iterable (not just lists).

    >>> linear_search_next([0, 5, 7, 10, 15], 0)
    0
    >>> linear_search_next([0, 5, 7, 10, 15], 15)
    4
    >>> linear_search_next([0, 5, 7, 10, 15], 5)
    1
    >>> linear_search_next([0, 5, 7, 10, 15], 6)
    -1
    >>> linear_search_next([], 5)
    -1
    >>> linear_search_next((x for x in range(5)), 3)
    3
    """
    return next((i for i, v in enumerate(sequence) if v == target), -1)


# ---------------------------------------------------------------------------
# Variant 3 — numpy.where (vectorised, numeric arrays only)
# ---------------------------------------------------------------------------


def linear_search_numpy(sequence: list, target) -> int:
    """
    numpy.where — vectorised element-wise comparison; returns first match index.

    Best when sequence is already a numpy array and many lookups are done.
    Overhead of np.asarray() makes it slower for single lookups on small lists.

    >>> linear_search_numpy([0, 5, 7, 10, 15], 0)
    0
    >>> linear_search_numpy([0, 5, 7, 10, 15], 15)
    4
    >>> linear_search_numpy([0, 5, 7, 10, 15], 5)
    1
    >>> linear_search_numpy([0, 5, 7, 10, 15], 6)
    -1
    >>> linear_search_numpy([], 5)
    -1
    """
    import numpy as np

    if not sequence:
        return -1
    arr = np.asarray(sequence)
    indices = np.where(arr == target)[0]
    return int(indices[0]) if indices.size > 0 else -1


# ---------------------------------------------------------------------------
# Variant 4 — bisect (SORTED arrays only, O(log n))
# ---------------------------------------------------------------------------


def bisect_search(sequence: list, target) -> int:
    """
    bisect.bisect_left — O(log n) search for SORTED sequences only.

    This is NOT linear search — included as the performance baseline showing
    what you get when sorting is possible.

    >>> bisect_search([0, 5, 7, 10, 15], 0)
    0
    >>> bisect_search([0, 5, 7, 10, 15], 15)
    4
    >>> bisect_search([0, 5, 7, 10, 15], 5)
    1
    >>> bisect_search([0, 5, 7, 10, 15], 6)
    -1
    >>> bisect_search([], 5)
    -1
    """
    if not sequence:
        return -1
    idx = bisect.bisect_left(sequence, target)
    if idx < len(sequence) and sequence[idx] == target:
        return idx
    return -1


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------


def benchmark() -> None:
    import random
    import timeit
    import sys
    import os

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from searches.linear_search import linear_search, rec_linear_search

    fns_linear = [
        ("linear_search (enumerate loop)",     linear_search),
        ("linear_search_index (list.index)",   linear_search_index),
        ("linear_search_next (next+generator)", linear_search_next),
        ("linear_search_numpy (np.where)",     linear_search_numpy),
        ("bisect_search (sorted only, O(logn))", bisect_search),
    ]

    REPS = 500

    for size in [100, 1_000, 10_000]:
        random.seed(42)
        # Unsorted for linear search variants
        data_unsorted = random.choices(range(size * 5), k=size)
        # Sorted for bisect
        data_sorted = sorted(data_unsorted)

        # Mix of hits and misses
        targets = random.choices(data_unsorted, k=REPS) + \
                  [random.randint(size * 5, size * 10) for _ in range(REPS)]

        print(f"\n{'='*62}")
        print(f"  n = {size:,}  ({REPS*2} lookups: {REPS} hits + {REPS} misses)")
        print(f"{'='*62}")

        results = {}
        for name, fn in fns_linear:
            # Use sorted data for bisect, unsorted for the rest
            seq = data_sorted if "bisect" in name else data_unsorted
            t = timeit.timeit(
                lambda fn=fn, seq=seq: [fn(seq, x) for x in targets],
                number=5,
            )
            results[name] = t
            print(f"  {name:<44}  {t*1000/5:8.3f} ms/run")

        best = min(results, key=results.get)
        print(f"\n  Winner: {best}")

    # Recursion depth note
    print("\n=== rec_linear_search: recursion depth limit ===")
    limit = 1
    seq = list(range(1000))
    try:
        for limit in range(1, 1000, 50):
            rec_linear_search(seq, 0, limit * 2, seq[limit])
        print(f"  Reached depth ~{limit} without RecursionError")
    except RecursionError:
        print(f"  RecursionError at n/2 depth ~ {limit} (Python default limit: 1000)")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
