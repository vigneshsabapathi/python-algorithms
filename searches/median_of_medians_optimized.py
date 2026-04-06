#!/usr/bin/env python3

"""
Optimized and alternative implementations for kth-smallest / order-statistics.

Variants covered:
1. quick_select_randomized  — randomized pivot (O(n) average, O(n^2) worst)
2. quick_select_mom_clean   — median-of-medians with proper 5-element groups
                              (O(n) WORST case guaranteed)
3. kth_smallest_heapq       — heapq.nsmallest (O(n log k))
4. kth_smallest_sorted      — sorted()[k-1]   (O(n log n)) — simplest baseline
5. kth_smallest_numpy       — numpy.partition  (O(n) average, C-backed)

Run benchmarks:
    python searches/median_of_medians_optimized.py
"""

from __future__ import annotations

import heapq
import random


# ---------------------------------------------------------------------------
# Variant 1 — randomized quickselect (O(n) average, O(n^2) worst)
# ---------------------------------------------------------------------------


def quick_select_randomized(arr: list, k: int, seed: int | None = None) -> int:
    """
    Quickselect with a random pivot — O(n) average, O(n^2) worst case.

    In practice faster than median-of-medians because the pivot selection
    is O(1) instead of O(n). The O(n^2) worst case is astronomically unlikely
    with a good random source.

    :param arr: unsorted list
    :param k: 1-indexed rank (1 = smallest)
    :return: kth smallest element, or -1 if k > len(arr)

    >>> quick_select_randomized([2, 4, 5, 7, 899, 54, 32], 5, seed=0)
    32
    >>> quick_select_randomized([2, 4, 5, 7, 899, 54, 32], 1, seed=0)
    2
    >>> quick_select_randomized([5, 4, 3, 2], 2, seed=0)
    3
    >>> quick_select_randomized([3, 5, 7, 10, 2, 12], 3, seed=0)
    5
    >>> quick_select_randomized([1], 1, seed=0)
    1
    >>> quick_select_randomized([1, 2], 3, seed=0)
    -1
    """
    if k > len(arr) or k < 1:
        return -1

    rng = random.Random(seed)

    def _select(a: list, rank: int) -> int:
        if len(a) == 1:
            return a[0]
        pivot = rng.choice(a)
        left  = [x for x in a if x < pivot]
        equal = [x for x in a if x == pivot]
        right = [x for x in a if x > pivot]
        if rank <= len(left):
            return _select(left, rank)
        elif rank <= len(left) + len(equal):
            return pivot
        else:
            return _select(right, rank - len(left) - len(equal))

    return _select(list(arr), k)


# ---------------------------------------------------------------------------
# Variant 2 — clean median-of-medians (proper 5-element groups)
# ---------------------------------------------------------------------------


def _median_of_five_clean(chunk: list) -> int:
    """Return median of a list of up to 5 elements."""
    s = sorted(chunk)
    return s[len(s) // 2]


def _mom_pivot(arr: list) -> int:
    """
    True median-of-medians pivot: split into groups of exactly 5,
    find median of each group, then recursively find median of those medians.
    Guarantees pivot is between 30th and 70th percentile -> O(n) worst case.
    """
    if len(arr) <= 5:
        return _median_of_five_clean(arr)
    groups = [arr[i:i + 5] for i in range(0, len(arr), 5)]
    medians = [_median_of_five_clean(g) for g in groups]
    return _mom_pivot(medians)


def quick_select_mom_clean(arr: list, k: int) -> int:
    """
    Quickselect with proper median-of-medians pivot — O(n) WORST case.

    Uses correct groups of exactly 5 (the original implementation has a bug
    where arr[i:] passes all remaining elements, not just 5).

    :param arr: unsorted list
    :param k: 1-indexed rank
    :return: kth smallest element, or -1 if k > len(arr)

    >>> quick_select_mom_clean([2, 4, 5, 7, 899, 54, 32], 5)
    32
    >>> quick_select_mom_clean([2, 4, 5, 7, 899, 54, 32], 1)
    2
    >>> quick_select_mom_clean([5, 4, 3, 2], 2)
    3
    >>> quick_select_mom_clean([3, 5, 7, 10, 2, 12], 3)
    5
    >>> quick_select_mom_clean([1], 1)
    1
    >>> quick_select_mom_clean([1, 2], 3)
    -1
    """
    if k > len(arr) or k < 1:
        return -1

    def _select(a: list, rank: int) -> int:
        if len(a) == 1:
            return a[0]
        pivot = _mom_pivot(a)
        left  = [x for x in a if x < pivot]
        equal = [x for x in a if x == pivot]
        right = [x for x in a if x > pivot]
        if rank <= len(left):
            return _select(left, rank)
        elif rank <= len(left) + len(equal):
            return pivot
        else:
            return _select(right, rank - len(left) - len(equal))

    return _select(list(arr), k)


# ---------------------------------------------------------------------------
# Variant 3 — heapq.nsmallest  O(n log k)
# ---------------------------------------------------------------------------


def kth_smallest_heapq(arr: list, k: int) -> int:
    """
    heapq.nsmallest(k, arr)[-1] — returns kth smallest in O(n log k).

    Faster than sorting when k << n. C-backed heap operations.

    >>> kth_smallest_heapq([2, 4, 5, 7, 899, 54, 32], 5)
    32
    >>> kth_smallest_heapq([2, 4, 5, 7, 899, 54, 32], 1)
    2
    >>> kth_smallest_heapq([5, 4, 3, 2], 2)
    3
    >>> kth_smallest_heapq([3, 5, 7, 10, 2, 12], 3)
    5
    >>> kth_smallest_heapq([1, 2], 3)
    -1
    """
    if k > len(arr) or k < 1:
        return -1
    return heapq.nsmallest(k, arr)[-1]


# ---------------------------------------------------------------------------
# Variant 4 — sorted()[k-1]  O(n log n)
# ---------------------------------------------------------------------------


def kth_smallest_sorted(arr: list, k: int) -> int:
    """
    sorted(arr)[k-1] — O(n log n) Timsort baseline, simplest correct solution.

    >>> kth_smallest_sorted([2, 4, 5, 7, 899, 54, 32], 5)
    32
    >>> kth_smallest_sorted([2, 4, 5, 7, 899, 54, 32], 1)
    2
    >>> kth_smallest_sorted([5, 4, 3, 2], 2)
    3
    >>> kth_smallest_sorted([3, 5, 7, 10, 2, 12], 3)
    5
    >>> kth_smallest_sorted([1, 2], 3)
    -1
    """
    if k > len(arr) or k < 1:
        return -1
    return sorted(arr)[k - 1]


# ---------------------------------------------------------------------------
# Variant 5 — numpy.partition  O(n) average, C-backed
# ---------------------------------------------------------------------------


def kth_smallest_numpy(arr: list, k: int) -> int:
    """
    numpy.partition(arr, k-1)[k-1] — O(n) average introselect, C-backed.

    numpy.partition rearranges arr so element at position k-1 is the
    value that would be there in sorted order. O(n) average (introselect).

    >>> kth_smallest_numpy([2, 4, 5, 7, 899, 54, 32], 5)
    32
    >>> kth_smallest_numpy([2, 4, 5, 7, 899, 54, 32], 1)
    2
    >>> kth_smallest_numpy([5, 4, 3, 2], 2)
    3
    >>> kth_smallest_numpy([3, 5, 7, 10, 2, 12], 3)
    5
    >>> kth_smallest_numpy([1, 2], 3)
    -1
    """
    import numpy as np

    if k > len(arr) or k < 1:
        return -1
    a = np.asarray(arr)
    return int(np.partition(a, k - 1)[k - 1])


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------


def benchmark() -> None:
    import timeit
    import sys
    import os

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from searches.median_of_medians import quick_select as qs_original

    REPS = 200

    for size in [100, 1_000, 5_000]:
        random.seed(42)
        data = random.sample(range(size * 10), size)
        ks = [1, size // 4, size // 2, size * 3 // 4, size]

        print(f"\n{'='*64}")
        print(f"  n = {size:,}  (k values tested: {ks})")
        print(f"{'='*64}")

        fns = [
            ("quick_select MoM (original)",           lambda d, k: qs_original(d, k)),
            ("quick_select MoM clean (proper groups)", lambda d, k: quick_select_mom_clean(d, k)),
            ("quick_select randomized",                lambda d, k: quick_select_randomized(d, k, seed=None)),
            ("heapq.nsmallest",                        lambda d, k: kth_smallest_heapq(d, k)),
            ("sorted()[k-1]",                          lambda d, k: kth_smallest_sorted(d, k)),
            ("numpy.partition",                        lambda d, k: kth_smallest_numpy(d, k)),
        ]

        results = {}
        for name, fn in fns:
            t = timeit.timeit(
                lambda fn=fn: [fn(data, k) for k in ks],
                number=REPS,
            )
            results[name] = t
            print(f"  {name:<46} {t*1000/REPS:8.3f} ms/run")

        best = min(results, key=results.get)
        print(f"\n  Winner: {best}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
