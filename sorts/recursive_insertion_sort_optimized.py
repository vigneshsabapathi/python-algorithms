"""
Recursive Insertion Sort — Optimized & Alternative Implementations
==================================================================

Recursive insertion sort restructures the classic iterative insertion sort
as two mutually recursive functions:
  rec_insertion_sort(arr, n): sort first n elements
    → insert_next(arr, n-1): bubble arr[n-1] rightward to its correct position
    → rec_insertion_sort(arr, n-1): sort first n-1 elements

This is primarily a teaching / interview algorithm. Both recursive and iterative
insertion sort are O(n²) average/worst, O(n) best (already sorted).

Recursion depth: O(n) for rec_insertion_sort + O(n) for insert_next =
O(n) total stack depth — Python's default limit of 1000 is hit at n≈500.

Variants compared
-----------------
1. recursive_swap    — reference: swap-based bubble step (rec_insertion_sort)
2. iterative_shift   — classic iterative insertion sort with key+shift (faster)
3. iterative_bisect  — bisect_left for O(log n) position find + slice insert
4. builtin           — sorted() / list.sort() for reference
"""

from __future__ import annotations

import sys
import time
import random
from bisect import bisect_left, insort

sys.setrecursionlimit(20_000)


# ---------------------------------------------------------------------------
# 1. Recursive swap-based (reference)
# ---------------------------------------------------------------------------
def _insert_next(arr: list, index: int) -> None:
    if index >= len(arr) or arr[index - 1] <= arr[index]:
        return
    arr[index - 1], arr[index] = arr[index], arr[index - 1]
    _insert_next(arr, index + 1)


def insertion_sort_recursive(lst: list) -> list:
    """
    Recursive insertion sort: sort first n elements by inserting the nth
    element into its correct position via recursive bubble-right.

    >>> insertion_sort_recursive([1, 2, 1])
    [1, 1, 2]
    >>> insertion_sort_recursive([2, 1, 0, -1, -2])
    [-2, -1, 0, 1, 2]
    >>> insertion_sort_recursive([])
    []
    """
    def _sort(arr: list, n: int) -> None:
        if n <= 1:
            return
        _insert_next(arr, n - 1)
        _sort(arr, n - 1)

    arr = lst[:]
    _sort(arr, len(arr))
    return arr


# ---------------------------------------------------------------------------
# 2. Iterative shift-based (classic) — same O(n²) but no recursion overhead
# ---------------------------------------------------------------------------
def insertion_sort_iterative(lst: list) -> list:
    """
    Classic iterative insertion sort: pick key, shift larger elements right,
    insert. No recursion, no swap overhead.

    >>> insertion_sort_iterative([1, 2, 1])
    [1, 1, 2]
    >>> insertion_sort_iterative([2, 1, 0, -1, -2])
    [-2, -1, 0, 1, 2]
    >>> insertion_sort_iterative([])
    []
    >>> insertion_sort_iterative([5, 5, 5])
    [5, 5, 5]
    """
    arr = lst[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# ---------------------------------------------------------------------------
# 3. Bisect insertion sort — O(log n) search + O(n) shift per element
#    Still O(n²) overall but fewer comparisons (good for expensive comparisons)
# ---------------------------------------------------------------------------
def insertion_sort_bisect(lst: list) -> list:
    """
    Uses bisect_left for O(log n) position search, then slice-insert.
    Minimises comparisons but O(n) shifts remain.

    >>> insertion_sort_bisect([1, 2, 1])
    [1, 1, 2]
    >>> insertion_sort_bisect([2, 1, 0, -1, -2])
    [-2, -1, 0, 1, 2]
    >>> insertion_sort_bisect([])
    []
    """
    arr = lst[:]
    sorted_part: list = []
    for x in arr:
        insort(sorted_part, x)
    return sorted_part


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    # Keep small — O(n²) sorts are slow beyond n~5000 in Python
    sizes = [100, 500, 1_000, 3_000]
    implementations = [
        ("recursive",  insertion_sort_recursive),
        ("iterative",  insertion_sort_iterative),
        ("bisect",     insertion_sort_bisect),
        ("sorted()",   sorted),
    ]

    for label, gen in [
        ("random",        lambda n: random.sample(range(n * 2), n)),
        ("nearly sorted", lambda n: list(range(n - 3)) + random.sample(range(n), 3)),
        ("reversed",      lambda n: list(range(n, 0, -1))),
    ]:
        print(f"\n--- {label} ---")
        header = f"{'n':>6}  " + "  ".join(f"{name:>12}" for name, _ in implementations)
        print(header)
        print("-" * len(header))
        for n in sizes:
            data = gen(n)
            row = f"{n:>6}  "
            for _, fn in implementations:
                best = float("inf")
                for _ in range(3):
                    d = data[:]
                    t0 = time.perf_counter()
                    fn(d)
                    best = min(best, time.perf_counter() - t0)
                row += f"{best:>12.4f}  "
            print(row)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Benchmark (seconds, best of 3 runs) ===")
    benchmark()
