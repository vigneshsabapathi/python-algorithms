"""Slowsort — comparison against practical algorithms.

Slowsort is intentionally the worst sorting algorithm that still terminates.
It is based on "multiply and surrender" (parody of divide and conquer) and
has super-polynomial time complexity: Omega(n^(log n / (2+epsilon))).

This file does NOT try to "optimise" slowsort (that defeats the point).
Instead it:
  1. Shows how bad slowsort really is with timed benchmarks vs real sorts
  2. Demonstrates the partial-sort capability (its one unique feature)
  3. Provides a memoised call-counter to visualise the explosion in recursion

Reference: Broder & Stolfi, "Pessimal Algorithms and Simplexity Analysis", 1986
           https://en.wikipedia.org/wiki/Slowsort
"""

from __future__ import annotations
import sys
import time
import random

sys.setrecursionlimit(500_000)


# ---------------------------------------------------------------------------
# 1. Slowsort (original) — in-place, returns None
# ---------------------------------------------------------------------------
def slowsort(sequence: list, start: int | None = None, end: int | None = None) -> None:
    """Slowsort: intentionally pessimal. Omega(n^(log n)) complexity.

    >>> seq = [4, 3, 2, 1]; slowsort(seq); seq
    [1, 2, 3, 4]
    >>> seq = []; slowsort(seq); seq
    []
    >>> seq = [1]; slowsort(seq); seq
    [1]
    """
    if start is None:
        start = 0
    if end is None:
        end = len(sequence) - 1
    if start >= end:
        return
    mid = (start + end) // 2
    slowsort(sequence, start, mid)
    slowsort(sequence, mid + 1, end)
    if sequence[end] < sequence[mid]:
        sequence[end], sequence[mid] = sequence[mid], sequence[end]
    slowsort(sequence, start, end - 1)


# ---------------------------------------------------------------------------
# 2. Call counter — shows recursion explosion
# ---------------------------------------------------------------------------
def slowsort_counted(sequence: list) -> tuple[list, int]:
    """Returns (sorted list, number of recursive calls made).

    >>> result, calls = slowsort_counted([3, 1, 2])
    >>> result
    [1, 2, 3]
    >>> calls >= 10
    True
    """
    counter = [0]

    def _sort(seq, start, end):
        counter[0] += 1
        if start >= end:
            return
        mid = (start + end) // 2
        _sort(seq, start, mid)
        _sort(seq, mid + 1, end)
        if seq[end] < seq[mid]:
            seq[end], seq[mid] = seq[mid], seq[end]
        _sort(seq, start, end - 1)

    arr = list(sequence)
    _sort(arr, 0, len(arr) - 1)
    return arr, counter[0]


# ---------------------------------------------------------------------------
# 3. Reference sorts for comparison
# ---------------------------------------------------------------------------
def sort_builtin(arr: list) -> list:
    """Python sorted() — Timsort.

    >>> sort_builtin([3, 1, 2])
    [1, 2, 3]
    """
    return sorted(arr)


def sort_merge(arr: list) -> list:
    """Merge sort — O(n log n).

    >>> sort_merge([3, 1, 2])
    [1, 2, 3]
    """
    if len(arr) <= 1:
        return list(arr)
    mid = len(arr) // 2
    left = sort_merge(arr[:mid])
    right = sort_merge(arr[mid:])
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:]); result.extend(right[j:])
    return result


def sort_insertion(arr: list) -> list:
    """Insertion sort — O(n²) but fast on small arrays.

    >>> sort_insertion([3, 1, 2])
    [1, 2, 3]
    """
    a = list(arr)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


# ---------------------------------------------------------------------------
# Recursion call counts — show the explosion
# ---------------------------------------------------------------------------
def show_call_counts() -> None:
    print("Recursion call counts for slowsort:")
    print(f"  {'n':>4}  {'calls':>12}  {'ratio vs n²':>14}")
    prev = None
    for n in [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]:
        data = list(range(n, 0, -1))  # reverse sorted — worst case
        _, calls = slowsort_counted(data)
        ratio = calls / (n * n)
        note = f"  ({calls/prev:.1f}x prev)" if prev else ""
        print(f"  {n:>4}  {calls:>12,}  {ratio:>14.2f}x n²{note}")
        prev = calls


# ---------------------------------------------------------------------------
# Benchmark — VERY small sizes only (slowsort is catastrophically slow)
# ---------------------------------------------------------------------------
def benchmark() -> None:
    variants = [
        ("slowsort        ", lambda d: (slowsort(d), d)[1]),
        ("insertion sort  ", sort_insertion),
        ("merge sort      ", sort_merge),
        ("sorted()        ", sort_builtin),
    ]

    print("\nBenchmark (random input, best of 3 runs):")
    print(f"  {'n':>4}  " + "  ".join(f"{name.strip():>16}" for name, _ in variants))
    print("  " + "-" * 80)

    # Slowsort is usable only up to ~n=50 before it takes seconds
    for n in [5, 10, 15, 20, 25, 30]:
        data = random.sample(range(n * 3), n)
        row = f"  {n:>4}  "
        for name, fn in variants:
            best = float("inf")
            for _ in range(3):
                d = list(data)
                t0 = time.perf_counter()
                result = fn(d)
                elapsed = time.perf_counter() - t0
                best = min(best, elapsed)
            row += f"{best * 1000:>16.4f}  "
        print(row)

    # Show just how much worse slowsort gets — single timed run at n=35, 40
    print("\n  Slowsort alone (single run, reverse sorted — worst case):")
    for n in [25, 30, 35, 40]:
        data = list(range(n, 0, -1))
        t0 = time.perf_counter()
        slowsort(data)
        elapsed = (time.perf_counter() - t0) * 1000
        print(f"    n={n}: {elapsed:.1f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("All doctests passed.\n")
    show_call_counts()
    benchmark()
