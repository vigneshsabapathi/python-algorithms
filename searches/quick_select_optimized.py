#!/usr/bin/env python3

"""
Optimized and alternative implementations for quick_select / median.

This module focuses on:
1. quick_select_iterative   — iterative instead of recursive (no stack overflow)
2. quick_select_inplace     — Lomuto in-place partition (O(1) extra space)
3. median_statistics        — statistics.median from stdlib (production baseline)
4. median_numpy             — numpy.median (C-backed, numeric arrays)
5. median_sorted            — sorted()[mid] (Timsort baseline)

NOTE: Benchmarks for kth-element variants are covered in median_of_medians_optimized.py.
This module focuses on the median use case and the space/recursion tradeoffs.

Run benchmarks:
    python searches/quick_select_optimized.py
"""

from __future__ import annotations

import random
import statistics


# ---------------------------------------------------------------------------
# Variant 1 — iterative quickselect (no recursion limit, O(n) avg, O(1) extra)
# ---------------------------------------------------------------------------


def quick_select_iterative(items: list, index: int):
    """
    Iterative quickselect with random pivot — avoids RecursionError on large n.

    Converts the tail recursion of the original into a while loop by narrowing
    the working list in place each iteration. O(n) average, O(1) extra space
    (beyond the copy of items).

    >>> quick_select_iterative([2, 4, 5, 7, 899, 54, 32], 5)
    54
    >>> quick_select_iterative([2, 4, 5, 7, 899, 54, 32], 1)
    4
    >>> quick_select_iterative([5, 4, 3, 2], 2)
    4
    >>> quick_select_iterative([3, 5, 7, 10, 2, 12], 3)
    7
    >>> quick_select_iterative([1], 0)
    1
    >>> quick_select_iterative([3, 1, 2], 0)
    1
    >>> quick_select_iterative([2, 4, 5, 7, 899, 54, 32], -1) is None
    True
    >>> quick_select_iterative([2, 4, 5, 7, 899, 54, 32], 7) is None
    True
    """
    if index < 0 or index >= len(items):
        return None

    arr = list(items)
    target = index

    while True:
        if len(arr) == 1:
            return arr[0]

        pivot = arr[random.randint(0, len(arr) - 1)]
        less    = [x for x in arr if x < pivot]
        equal   = [x for x in arr if x == pivot]
        greater = [x for x in arr if x > pivot]

        m = len(less)
        c = len(equal)

        if m <= target < m + c:
            return pivot
        elif target < m:
            arr = less
        else:
            arr = greater
            target -= m + c


# ---------------------------------------------------------------------------
# Variant 2 — in-place Lomuto partition (O(1) extra space, mutates input)
# ---------------------------------------------------------------------------


def _lomuto_partition(arr: list, lo: int, hi: int, pivot_idx: int) -> int:
    """Lomuto-style partition around arr[pivot_idx]; returns final pivot index."""
    arr[pivot_idx], arr[hi] = arr[hi], arr[pivot_idx]
    pivot = arr[hi]
    i = lo
    for j in range(lo, hi):
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[hi] = arr[hi], arr[i]
    return i


def quick_select_inplace(items: list, index: int):
    """
    In-place quickselect: O(1) extra space (excluding the input copy).

    Uses Lomuto partition on a copy of the list — never allocates three
    sub-lists, just swaps elements. Still O(n) average.

    >>> quick_select_inplace([2, 4, 5, 7, 899, 54, 32], 5)
    54
    >>> quick_select_inplace([2, 4, 5, 7, 899, 54, 32], 1)
    4
    >>> quick_select_inplace([5, 4, 3, 2], 2)
    4
    >>> quick_select_inplace([3, 5, 7, 10, 2, 12], 3)
    7
    >>> quick_select_inplace([1], 0)
    1
    >>> quick_select_inplace([2, 4, 5, 7, 899, 54, 32], -1) is None
    True
    >>> quick_select_inplace([2, 4, 5, 7, 899, 54, 32], 7) is None
    True
    """
    if index < 0 or index >= len(items):
        return None

    arr = list(items)
    lo, hi = 0, len(arr) - 1

    while lo < hi:
        pivot_idx = random.randint(lo, hi)
        pivot_idx = _lomuto_partition(arr, lo, hi, pivot_idx)
        if pivot_idx == index:
            return arr[index]
        elif pivot_idx < index:
            lo = pivot_idx + 1
        else:
            hi = pivot_idx - 1

    return arr[index]


# ---------------------------------------------------------------------------
# Variant 3 — statistics.median (stdlib, exact, works on any numeric type)
# ---------------------------------------------------------------------------


def median_statistics(items: list):
    """
    statistics.median — stdlib, O(n log n), exact result, handles int/float/Decimal.

    >>> median_statistics([3, 2, 2, 9, 9])
    3
    >>> median_statistics([2, 2, 9, 9, 9, 3])
    6.0
    >>> median_statistics([1])
    1
    >>> median_statistics([1, 2])
    1.5
    """
    return statistics.median(items)


# ---------------------------------------------------------------------------
# Variant 4 — numpy.median (C-backed, numeric arrays only)
# ---------------------------------------------------------------------------


def median_numpy(items: list):
    """
    numpy.median — C-backed, O(n log n) sort + O(1) index.
    Returns float always; exact for integer inputs.

    >>> median_numpy([3, 2, 2, 9, 9])
    3.0
    >>> median_numpy([2, 2, 9, 9, 9, 3])
    6.0
    >>> median_numpy([1])
    1.0
    >>> median_numpy([1, 2])
    1.5
    """
    import numpy as np

    return float(np.median(items))


# ---------------------------------------------------------------------------
# Variant 5 — sorted()[mid] (Timsort baseline)
# ---------------------------------------------------------------------------


def median_sorted(items: list):
    """
    sorted()[mid] — O(n log n) Timsort baseline; simplest correct solution.

    >>> median_sorted([3, 2, 2, 9, 9])
    3
    >>> median_sorted([2, 2, 9, 9, 9, 3])
    6.0
    >>> median_sorted([1])
    1
    >>> median_sorted([1, 2])
    1.5
    """
    s = sorted(items)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------


def benchmark() -> None:
    import timeit
    import sys
    import os

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from searches.quick_select import quick_select as qs_original, median as median_original

    print("\n=== Benchmark: quick_select (index-based) ===")
    for size in [1_000, 10_000]:
        random.seed(42)
        data = random.sample(range(size * 10), size)
        indices = [0, size // 4, size // 2, size * 3 // 4, size - 1]

        fns_qs = [
            ("quick_select original (recursive)",  lambda d, i: qs_original(d, i)),
            ("quick_select_iterative",              lambda d, i: quick_select_iterative(d, i)),
            ("quick_select_inplace (Lomuto)",       lambda d, i: quick_select_inplace(d, i)),
        ]

        print(f"\n  n={size}, indices={indices}")
        results = {}
        for name, fn in fns_qs:
            t = timeit.timeit(
                lambda fn=fn: [fn(data, i) for i in indices],
                number=200,
            )
            results[name] = t
            print(f"    {name:<42} {t*1000/200:8.3f} ms/run")
        print(f"    Winner: {min(results, key=results.get)}")

    print("\n=== Benchmark: median ===")
    for size in [100, 1_000, 10_000]:
        random.seed(42)
        data = random.sample(range(size * 10), size)

        fns_med = [
            ("median original (quickselect)",   lambda d: median_original(d)),
            ("median_statistics (stdlib)",       lambda d: median_statistics(d)),
            ("median_numpy",                     lambda d: median_numpy(d)),
            ("median_sorted (Timsort)",          lambda d: median_sorted(d)),
        ]

        print(f"\n  n={size}")
        results = {}
        for name, fn in fns_med:
            t = timeit.timeit(lambda fn=fn: fn(data), number=500)
            results[name] = t
            print(f"    {name:<42} {t*1000/500:8.3f} ms/run")
        print(f"    Winner: {min(results, key=results.get)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
