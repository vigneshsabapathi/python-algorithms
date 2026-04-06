#!/usr/bin/env python3

"""
Optimized and alternative implementations of fibonacci search.

Variants covered:
1. fibonacci_search_iterative_fib  — replaces lru_cache recursion with an
   iterative Fibonacci number generator (no function-call overhead, no cache)
2. fibonacci_search_bisect         — pure stdlib bisect baseline (O(log n))
3. fibonacci_search_numpy          — numpy.searchsorted baseline for numeric arrays

Run benchmarks:
    python searches/fibonacci_search_optimized.py
"""

from __future__ import annotations

import bisect
import timeit


# ---------------------------------------------------------------------------
# Variant 1 — iterative Fibonacci generation (no lru_cache, no recursion)
# ---------------------------------------------------------------------------


def fibonacci_search_iterative_fib(arr: list, val: int) -> int:
    """
    Fibonacci search with an iterative Fibonacci sequence precomputed upfront.

    Builds the Fibonacci sequence as a list (O(log n) entries), then uses
    index arithmetic identical to the original — no lru_cache, no recursion.

    :param arr: ascending-sorted list of comparable items
    :param val: value to search for
    :return: index of val, or -1 if not found

    >>> fibonacci_search_iterative_fib([4, 5, 6, 7], 4)
    0
    >>> fibonacci_search_iterative_fib([4, 5, 6, 7], -10)
    -1
    >>> fibonacci_search_iterative_fib([-18, 2], -18)
    0
    >>> fibonacci_search_iterative_fib([5], 5)
    0
    >>> fibonacci_search_iterative_fib(['a', 'c', 'd'], 'c')
    1
    >>> fibonacci_search_iterative_fib(['a', 'c', 'd'], 'f')
    -1
    >>> fibonacci_search_iterative_fib([], 1)
    -1
    >>> fibonacci_search_iterative_fib([.1, .4, 7], .4)
    1
    >>> fibonacci_search_iterative_fib(list(range(100)), 63)
    63
    >>> fibonacci_search_iterative_fib(list(range(100)), 99)
    99
    """
    n = len(arr)
    if n == 0:
        return -1

    # Build Fibonacci sequence until fibs[-1] >= n
    # fibs = [F(0), F(1), F(2), ...] = [0, 1, 1, 2, 3, 5, 8, ...]
    fibs = [0, 1]
    while fibs[-1] < n:
        fibs.append(fibs[-1] + fibs[-2])
    k = len(fibs) - 1  # fibs[k] >= n; probe uses fibs[k-1]

    offset = 0
    while k > 0:
        idx = min(offset + fibs[k - 1], n - 1)
        if arr[idx] == val:
            return idx
        elif val < arr[idx]:
            k -= 1
        else:
            offset += fibs[k - 1]
            k -= 2
    return -1


# ---------------------------------------------------------------------------
# Variant 2 — stdlib bisect (O(log n) baseline, simplest correct solution)
# ---------------------------------------------------------------------------


def fibonacci_search_bisect(arr: list, val: int) -> int:
    """
    Pure stdlib bisect — O(log n) baseline.

    Not fibonacci search but provided as a performance baseline.

    >>> fibonacci_search_bisect([4, 5, 6, 7], 4)
    0
    >>> fibonacci_search_bisect([4, 5, 6, 7], -10)
    -1
    >>> fibonacci_search_bisect([-18, 2], -18)
    0
    >>> fibonacci_search_bisect([5], 5)
    0
    >>> fibonacci_search_bisect([], 1)
    -1
    >>> fibonacci_search_bisect(list(range(100)), 63)
    63
    >>> fibonacci_search_bisect(list(range(100)), 99)
    99
    """
    if not arr:
        return -1
    idx = bisect.bisect_left(arr, val)
    if idx < len(arr) and arr[idx] == val:
        return idx
    return -1


# ---------------------------------------------------------------------------
# Variant 3 — numpy searchsorted (numeric arrays only)
# ---------------------------------------------------------------------------


def fibonacci_search_numpy(arr: list, val: int) -> int:
    """
    numpy.searchsorted — O(log n) baseline for numeric arrays.

    >>> fibonacci_search_numpy([4, 5, 6, 7], 4)
    0
    >>> fibonacci_search_numpy([4, 5, 6, 7], -10)
    -1
    >>> fibonacci_search_numpy(list(range(100)), 63)
    63
    >>> fibonacci_search_numpy(list(range(100)), 99)
    99
    >>> fibonacci_search_numpy([], 1)
    -1
    """
    import numpy as np

    if not arr:
        return -1
    a = np.asarray(arr)
    idx = int(np.searchsorted(a, val))
    if idx < len(a) and a[idx] == val:
        return idx
    return -1


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------


def benchmark() -> None:
    import random
    import sys
    import os

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from searches.fibonacci_search import fibonacci_search as fib_original

    fns = [
        ("fibonacci_search (original, lru_cache)", fib_original),
        ("fibonacci_search (iterative fib)",        fibonacci_search_iterative_fib),
        ("bisect_only (stdlib baseline)",            fibonacci_search_bisect),
        ("numpy.searchsorted (baseline)",            fibonacci_search_numpy),
    ]

    sizes = [1_000, 10_000, 100_000]
    REPS = 500

    for size in sizes:
        data = sorted(random.sample(range(size * 10), size))
        targets = [random.choice(data) for _ in range(REPS)]
        targets += [random.randint(0, size * 10) for _ in range(REPS)]

        print(f"\n{'='*62}")
        print(f"  n = {size:,}  ({REPS*2} lookups: {REPS} hits + {REPS} misses)")
        print(f"{'='*62}")

        results = {}
        for name, fn in fns:
            try:
                t = timeit.timeit(
                    lambda fn=fn, targets=targets, data=data: [fn(data, t) for t in targets],
                    number=5,
                )
                results[name] = t
                print(f"  {name:<44}  {t*1000/5:8.3f} ms/run")
            except Exception as e:
                print(f"  {name:<44}  ERROR: {e}")

        best = min(results, key=results.get)
        print(f"\n  Winner: {best}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
