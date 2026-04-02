"""
Quick Sort — Optimized & Alternative Implementations
=====================================================

Quick sort is the most widely used sorting algorithm in practice (C stdlib qsort,
Java Arrays.sort for primitives, PDQsort in Rust/C++).  Its average O(n log n)
time with tiny constants and excellent cache behaviour beat merge sort and heap
sort in most real-world scenarios.

Variants compared
-----------------
1.  functional_random  — reference: random pivot, list comprehension, out-of-place
2.  hoare_inplace      — Hoare partition scheme (original), in-place, 2-pointer
3.  lomuto_inplace     — Lomuto partition (right pivot), in-place
4.  three_way_dnf      — 3-way partition (Dutch National Flag), handles duplicates
5.  median_of_three    — median-of-3 pivot + insertion sort for small subarrays
6.  iterative_stack    — replaces recursion with an explicit stack (no stack overflow)
7.  builtin            — sorted() / list.sort() for reference
"""

from __future__ import annotations

import sys
import time
import random

sys.setrecursionlimit(200_000)   # needed for Lomuto on nearly-sorted large input
INSERTION_THRESHOLD = 16         # switch to insertion sort below this size


# ---------------------------------------------------------------------------
# 1. Functional (reference) — random pivot, out-of-place
# ---------------------------------------------------------------------------
def qs_functional(lst: list) -> list:
    """
    Random-pivot functional quicksort.  Not in-place; creates new lists.

    >>> qs_functional([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> qs_functional([])
    []
    >>> qs_functional([-2, 5, 0, -45])
    [-45, -2, 0, 5]
    """
    if len(lst) < 2:
        return lst[:]
    pivot_idx = random.randrange(len(lst))
    pivot = lst[pivot_idx]
    rest = lst[:pivot_idx] + lst[pivot_idx + 1:]
    return qs_functional([x for x in rest if x <= pivot]) + [pivot] + qs_functional([x for x in rest if x > pivot])


# ---------------------------------------------------------------------------
# 2. Hoare partition — original scheme, 2-pointer, fewest swaps in practice
# ---------------------------------------------------------------------------
def _hoare_partition(arr: list, lo: int, hi: int) -> int:
    pivot = arr[(lo + hi) // 2]
    i, j = lo - 1, hi + 1
    while True:
        i += 1
        while arr[i] < pivot:
            i += 1
        j -= 1
        while arr[j] > pivot:
            j -= 1
        if i >= j:
            return j
        arr[i], arr[j] = arr[j], arr[i]


def _qs_hoare(arr: list, lo: int, hi: int) -> None:
    if lo < hi:
        p = _hoare_partition(arr, lo, hi)
        _qs_hoare(arr, lo, p)
        _qs_hoare(arr, p + 1, hi)


def qs_hoare(lst: list) -> list:
    """
    In-place Hoare partition quicksort.  Fewer swaps than Lomuto (~1/3 as many).

    >>> qs_hoare([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> qs_hoare([])
    []
    >>> qs_hoare([-2, 5, 0, -45])
    [-45, -2, 0, 5]
    """
    arr = lst[:]
    if len(arr) > 1:
        _qs_hoare(arr, 0, len(arr) - 1)
    return arr


# ---------------------------------------------------------------------------
# 3. Lomuto partition — simpler code, slightly more swaps
# ---------------------------------------------------------------------------
def _lomuto_partition(arr: list, lo: int, hi: int) -> int:
    pivot = arr[hi]
    i = lo
    for j in range(lo, hi):
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[hi] = arr[hi], arr[i]
    return i


def _qs_lomuto(arr: list, lo: int, hi: int) -> None:
    if lo < hi:
        p = _lomuto_partition(arr, lo, hi)
        _qs_lomuto(arr, lo, p - 1)
        _qs_lomuto(arr, p + 1, hi)


def qs_lomuto(lst: list) -> list:
    """
    In-place Lomuto partition quicksort.

    >>> qs_lomuto([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> qs_lomuto([])
    []
    >>> qs_lomuto([-2, 5, 0, -45])
    [-45, -2, 0, 5]
    """
    arr = lst[:]
    if len(arr) > 1:
        _qs_lomuto(arr, 0, len(arr) - 1)
    return arr


# ---------------------------------------------------------------------------
# 4. 3-way partition (Dutch National Flag) — O(n) on all-duplicates input
# ---------------------------------------------------------------------------
def _qs_3way(arr: list, lo: int, hi: int) -> None:
    if lo >= hi:
        return
    pivot = arr[lo]
    lt, i, gt = lo, lo, hi
    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1; i += 1
        elif arr[i] > pivot:
            arr[gt], arr[i] = arr[i], arr[gt]
            gt -= 1
        else:
            i += 1
    _qs_3way(arr, lo, lt - 1)
    _qs_3way(arr, gt + 1, hi)


def qs_3way(lst: list) -> list:
    """
    3-way partition: partitions into <pivot, ==pivot, >pivot in one pass.
    O(n) time on arrays with many duplicates.

    >>> qs_3way([5, -1, -1, 5, 5, 24, 0])
    [-1, -1, 0, 5, 5, 5, 24]
    >>> qs_3way([1, 1, 1, 1])
    [1, 1, 1, 1]
    >>> qs_3way([])
    []
    >>> qs_3way([-2, 5, 0, -45])
    [-45, -2, 0, 5]
    """
    arr = lst[:]
    if len(arr) > 1:
        _qs_3way(arr, 0, len(arr) - 1)
    return arr


# ---------------------------------------------------------------------------
# 5. Median-of-3 + insertion sort fallback — production-quality hybrid
# ---------------------------------------------------------------------------
def _insertion_sort(arr: list, lo: int, hi: int) -> None:
    for i in range(lo + 1, hi + 1):
        key = arr[i]
        j = i - 1
        while j >= lo and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def _median_of_3_pivot(arr: list, lo: int, hi: int) -> object:
    mid = (lo + hi) // 2
    if arr[lo] > arr[mid]: arr[lo], arr[mid] = arr[mid], arr[lo]
    if arr[lo] > arr[hi]:  arr[lo], arr[hi]  = arr[hi],  arr[lo]
    if arr[mid] > arr[hi]: arr[mid], arr[hi] = arr[hi],  arr[mid]
    arr[mid], arr[hi - 1] = arr[hi - 1], arr[mid]
    return arr[hi - 1]


def _qs_median3(arr: list, lo: int, hi: int) -> None:
    if hi - lo < INSERTION_THRESHOLD:
        _insertion_sort(arr, lo, hi)
        return
    pivot = _median_of_3_pivot(arr, lo, hi)
    i, j = lo, hi - 1
    while True:
        i += 1
        while arr[i] < pivot: i += 1
        j -= 1
        while arr[j] > pivot: j -= 1
        if i >= j: break
        arr[i], arr[j] = arr[j], arr[i]
    arr[i], arr[hi - 1] = arr[hi - 1], arr[i]
    _qs_median3(arr, lo, i - 1)
    _qs_median3(arr, i + 1, hi)


def qs_median3(lst: list) -> list:
    """
    Hybrid: median-of-3 pivot + insertion sort for small subarrays.
    Models the strategy used in most production quicksort implementations.

    >>> qs_median3([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> qs_median3([])
    []
    >>> qs_median3([-2, 5, 0, -45])
    [-45, -2, 0, 5]
    """
    arr = lst[:]
    if len(arr) > INSERTION_THRESHOLD:
        _qs_median3(arr, 0, len(arr) - 1)
    else:
        _insertion_sort(arr, 0, len(arr) - 1)
    return arr


# ---------------------------------------------------------------------------
# 6. Iterative quicksort — explicit stack instead of recursion
# ---------------------------------------------------------------------------
def qs_iterative(lst: list) -> list:
    """
    Iterative quicksort using an explicit stack.  No recursion depth limit.

    >>> qs_iterative([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> qs_iterative([])
    []
    >>> qs_iterative([-2, 5, 0, -45])
    [-45, -2, 0, 5]
    """
    arr = lst[:]
    if len(arr) < 2:
        return arr
    stack = [(0, len(arr) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        pivot = arr[hi]
        i = lo
        for j in range(lo, hi):
            if arr[j] <= pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        arr[i], arr[hi] = arr[hi], arr[i]
        # Push larger subarray last so smaller is processed first (minimises max stack depth)
        if i - lo < hi - i:
            stack.append((i + 1, hi))
            stack.append((lo, i - 1))
        else:
            stack.append((lo, i - 1))
            stack.append((i + 1, hi))
    return arr


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    sizes_random = [1_000, 5_000, 20_000, 100_000]
    # Lomuto/functional degenerate to O(n²) on sorted/reversed/dupes — keep small
    sizes_degenerate = [200, 500, 1_000]
    sizes_dupes = [1_000, 5_000, 20_000]  # functional degenerates at 100k with few unique values
    implementations = [
        ("functional",  qs_functional),
        ("hoare",       qs_hoare),
        ("lomuto",      qs_lomuto),
        ("3way_dnf",    qs_3way),
        ("median3+ins", qs_median3),
        ("iterative",   qs_iterative),
        ("sorted()",    sorted),
    ]

    scenarios = [
        ("random",        lambda n: random.sample(range(n * 2), n), sizes_random),
        ("nearly sorted", lambda n: list(range(n - 5)) + random.sample(range(n), 5), sizes_degenerate),
        ("reversed",      lambda n: list(range(n, 0, -1)), sizes_degenerate),
        ("many dupes",    lambda n: [random.randint(0, 9) for _ in range(n)], sizes_dupes),
    ]

    for label, gen, sizes in scenarios:
        print(f"\n--- {label} ---")
        header = f"{'n':>8}  " + "  ".join(f"{name:>14}" for name, _ in implementations)
        print(header)
        print("-" * len(header))
        for n in sizes:
            data = gen(n)
            row = f"{n:>8}  "
            for _, fn in implementations:
                try:
                    best = float("inf")
                    for _ in range(3):
                        d = data[:]
                        t0 = time.perf_counter()
                        fn(d)
                        best = min(best, time.perf_counter() - t0)
                    row += f"{best:>14.4f}  "
                except RecursionError:
                    row += f"{'OVERFLOW':>14}  "
            print(row)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Benchmark (seconds, best of 3 runs) ===")
    benchmark()
