#!/usr/bin/env python3
"""
Optimized and alternative implementations of Merge Sort.

The reference is classic top-down merge sort: O(n log n).

Three variants:
  bottom_up       — iterative bottom-up merge sort (no recursion)
  timsort_hybrid  — merge sort + insertion sort for small runs (like Python's sort)
  natural_merge   — detect existing sorted runs, merge them (adaptive)

Run:
    python divide_and_conquer/mergesort_optimized.py
"""

from __future__ import annotations

import os
import random
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from divide_and_conquer.mergesort import merge_sort as reference


# ---------------------------------------------------------------------------
# Variant 1 — Bottom-up merge sort (iterative): O(n log n)
# ---------------------------------------------------------------------------

def bottom_up(arr: list) -> list:
    """
    Iterative bottom-up merge sort. Merges pairs of subarrays of
    increasing size: 1, 2, 4, 8, ...

    >>> bottom_up([38, 27, 43, 3, 9, 82, 10])
    [3, 9, 10, 27, 38, 43, 82]
    >>> bottom_up([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]
    >>> bottom_up([])
    []
    >>> bottom_up([1])
    [1]
    """
    arr = arr[:]
    n = len(arr)
    width = 1

    while width < n:
        for i in range(0, n, 2 * width):
            left = arr[i : i + width]
            right = arr[i + width : i + 2 * width]
            merged = _merge(left, right)
            arr[i : i + len(merged)] = merged
        width *= 2

    return arr


def _merge(left: list, right: list) -> list:
    result: list = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------------------------------------------------------------------------
# Variant 2 — Timsort-style hybrid: merge sort + insertion sort for small runs
# ---------------------------------------------------------------------------

_INSERTION_THRESHOLD = 32


def timsort_hybrid(arr: list) -> list:
    """
    Hybrid merge sort using insertion sort for subarrays <= 32 elements.
    Similar to Python's built-in Timsort strategy.

    >>> timsort_hybrid([38, 27, 43, 3, 9, 82, 10])
    [3, 9, 10, 27, 38, 43, 82]
    >>> timsort_hybrid([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]
    >>> timsort_hybrid([])
    []
    """
    if len(arr) <= _INSERTION_THRESHOLD:
        return _insertion_sort(arr[:])

    mid = len(arr) // 2
    left = timsort_hybrid(arr[:mid])
    right = timsort_hybrid(arr[mid:])
    return _merge(left, right)


def _insertion_sort(arr: list) -> list:
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# ---------------------------------------------------------------------------
# Variant 3 — Natural merge sort (adaptive): O(n) best case
# ---------------------------------------------------------------------------

def natural_merge(arr: list) -> list:
    """
    Natural merge sort — detects existing sorted runs and merges them.
    O(n) for already-sorted input, O(n log n) worst case.

    >>> natural_merge([38, 27, 43, 3, 9, 82, 10])
    [3, 9, 10, 27, 38, 43, 82]
    >>> natural_merge([1, 2, 3, 4, 5])
    [1, 2, 3, 4, 5]
    >>> natural_merge([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]
    >>> natural_merge([])
    []
    """
    if len(arr) <= 1:
        return arr[:]

    # Find natural runs
    runs: list[list] = []
    current_run = [arr[0]]
    for i in range(1, len(arr)):
        if arr[i] >= arr[i - 1]:
            current_run.append(arr[i])
        else:
            runs.append(current_run)
            current_run = [arr[i]]
    runs.append(current_run)

    # Merge runs pairwise until one remains
    while len(runs) > 1:
        new_runs: list[list] = []
        for i in range(0, len(runs), 2):
            if i + 1 < len(runs):
                new_runs.append(_merge(runs[i], runs[i + 1]))
            else:
                new_runs.append(runs[i])
        runs = new_runs

    return runs[0]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    [38, 27, 43, 3, 9, 82, 10],
    [5, 4, 3, 2, 1],
    [1, 2, 3, 4, 5],
    [],
    [1],
    [3, 3, 1, 1, 2, 2],
]

IMPLS = [
    ("reference", reference),
    ("bottom_up", bottom_up),
    ("timsort", timsort_hybrid),
    ("natural", natural_merge),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for arr in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            results[name] = fn(arr)
        ref = results["reference"]
        ok = all(v == ref for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] arr={str(arr):<30} -> {ref}")

    sizes = [1000, 10000, 100000]
    REPS = 20

    for n in sizes:
        arr_random = [random.randint(1, n) for _ in range(n)]
        arr_sorted = list(range(n))
        arr_reverse = list(range(n, 0, -1))

        for label, arr in [("random", arr_random), ("sorted", arr_sorted), ("reverse", arr_reverse)]:
            print(f"\n=== Benchmark n={n} ({label}), {REPS} runs ===")
            for name, fn in IMPLS:
                t = timeit.timeit(lambda fn=fn: fn(arr), number=REPS) * 1000 / REPS
                print(f"  {name:<14} {t:>8.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
