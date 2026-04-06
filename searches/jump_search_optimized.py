#!/usr/bin/env python3

"""
Optimized and alternative implementations of jump search.

Variants covered:
1. jump_search_isqrt       — uses integer square root (math.isqrt) instead of
                             int(math.sqrt(...)) — avoids float rounding on large n
2. jump_search_bisect      — replaces linear back-scan with bisect.bisect_left
                             (O(log step) instead of O(step) for the scan phase)
3. bisect_only             — pure stdlib bisect baseline (O(log n))
4. jump_search_numpy       — numpy.searchsorted baseline for numeric arrays

Run benchmarks:
    python searches/jump_search_optimized.py
"""

from __future__ import annotations

import bisect
import math
from collections.abc import Sequence
from typing import Any, Protocol


class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


# ---------------------------------------------------------------------------
# Variant 1 — integer sqrt (safer for large n)
# ---------------------------------------------------------------------------


def jump_search_isqrt(arr: Sequence, item) -> int:
    """
    Jump search using math.isqrt for the block size.

    math.isqrt(n) is exact for all integers; int(math.sqrt(n)) can round
    incorrectly for perfect squares above ~2^53 due to float precision.

    >>> jump_search_isqrt([0, 1, 2, 3, 4, 5], 3)
    3
    >>> jump_search_isqrt([-5, -2, -1], -1)
    2
    >>> jump_search_isqrt([0, 5, 10, 20], 8)
    -1
    >>> jump_search_isqrt([0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610], 55)
    10
    >>> jump_search_isqrt(["aa", "bb", "cc", "dd", "ee", "ff"], "ee")
    4
    >>> jump_search_isqrt([], 1)
    -1
    >>> jump_search_isqrt([5], 5)
    0
    >>> jump_search_isqrt([5], 6)
    -1
    """
    n = len(arr)
    if n == 0:
        return -1
    block = math.isqrt(n)
    if block == 0:
        block = 1

    prev, step = 0, block
    while arr[min(step, n) - 1] < item:
        prev = step
        step += block
        if prev >= n:
            return -1

    while arr[prev] < item:
        prev += 1
        if prev == min(step, n):
            return -1

    return prev if arr[prev] == item else -1


# ---------------------------------------------------------------------------
# Variant 2 — bisect back-scan (O(log step) vs O(step) for linear scan phase)
# ---------------------------------------------------------------------------


def jump_search_bisect_scan(arr: list, item) -> int:
    """
    Jump search: jump phase identical to original; back-scan uses
    bisect.bisect_left instead of a linear walk — O(log step) instead of O(step).

    For the optimal block_size = sqrt(n), the scan phase is at most sqrt(n)
    elements, so:
      original: O(sqrt n) scan
      this:     O(log(sqrt n)) = O(0.5 log n) scan

    >>> jump_search_bisect_scan([0, 1, 2, 3, 4, 5], 3)
    3
    >>> jump_search_bisect_scan([-5, -2, -1], -1)
    2
    >>> jump_search_bisect_scan([0, 5, 10, 20], 8)
    -1
    >>> jump_search_bisect_scan([0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610], 55)
    10
    >>> jump_search_bisect_scan(["aa", "bb", "cc", "dd", "ee", "ff"], "ee")
    4
    >>> jump_search_bisect_scan([], 1)
    -1
    >>> jump_search_bisect_scan([5], 5)
    0
    >>> jump_search_bisect_scan([5], 6)
    -1
    """
    n = len(arr)
    if n == 0:
        return -1
    block = math.isqrt(n) or 1

    prev, step = 0, block
    while arr[min(step, n) - 1] < item:
        prev = step
        step += block
        if prev >= n:
            return -1

    # Binary scan within [prev, min(step, n))
    right = min(step, n)
    idx = bisect.bisect_left(arr, item, prev, right)
    if idx < right and arr[idx] == item:
        return idx
    return -1


# ---------------------------------------------------------------------------
# Variant 3 — pure bisect baseline
# ---------------------------------------------------------------------------


def bisect_only(arr: list, item) -> int:
    """
    Pure stdlib bisect.bisect_left — O(log n) baseline.

    >>> bisect_only([0, 1, 2, 3, 4, 5], 3)
    3
    >>> bisect_only([-5, -2, -1], -1)
    2
    >>> bisect_only([0, 5, 10, 20], 8)
    -1
    >>> bisect_only([], 1)
    -1
    """
    if not arr:
        return -1
    idx = bisect.bisect_left(arr, item)
    if idx < len(arr) and arr[idx] == item:
        return idx
    return -1


# ---------------------------------------------------------------------------
# Variant 4 — numpy searchsorted baseline
# ---------------------------------------------------------------------------


def jump_search_numpy(arr: list, item) -> int:
    """
    numpy.searchsorted — O(log n) baseline for numeric arrays.

    >>> jump_search_numpy([0, 1, 2, 3, 4, 5], 3)
    3
    >>> jump_search_numpy([-5, -2, -1], -1)
    2
    >>> jump_search_numpy([0, 5, 10, 20], 8)
    -1
    >>> jump_search_numpy([], 1)
    -1
    """
    import numpy as np

    if not arr:
        return -1
    a = np.asarray(arr)
    idx = int(np.searchsorted(a, item))
    if idx < len(a) and a[idx] == item:
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
    from searches.jump_search import jump_search as jump_original

    fns = [
        ("jump_search (original, float sqrt)",     jump_original),
        ("jump_search_isqrt (int sqrt)",            jump_search_isqrt),
        ("jump_search_bisect_scan (isqrt+bisect)",  jump_search_bisect_scan),
        ("bisect_only (stdlib baseline)",            bisect_only),
        ("numpy_searchsorted (baseline)",            jump_search_numpy),
    ]

    REPS = 400

    for size in [1_000, 10_000, 100_000]:
        random.seed(42)
        data = sorted(random.sample(range(size * 10), size))
        targets = [random.choice(data) for _ in range(REPS)]
        targets += [random.randint(0, size * 10) for _ in range(REPS)]

        print(f"\n{'='*64}")
        print(f"  n = {size:,}  ({REPS*2} lookups: {REPS} hits + {REPS} misses)")
        print(f"{'='*64}")

        results = {}
        for name, fn in fns:
            t = timeit.timeit(
                lambda fn=fn: [fn(data, x) for x in targets],
                number=5,
            )
            results[name] = t
            print(f"  {name:<46} {t*1000/5:8.3f} ms/run")

        best = min(results, key=results.get)
        print(f"\n  Winner: {best}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
