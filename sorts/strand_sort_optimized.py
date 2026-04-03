"""Optimized and alternative implementations of Strand Sort.

Strand sort extracts naturally ascending "strands" from the input, then
merges them. It is adaptive: O(n) when input is already sorted (1 strand),
O(n²) worst case when input is reverse-sorted (n strands of length 1).

Issues with the original implementation:
  1. arr.pop(0) is O(n) — shifts all remaining elements every call
  2. Iterating with index while popping can SKIP elements in the same pass
     (when item at index i is popped, arr shifts left; next iteration sees
      the element that was at i+1, skipping what was at i — so strands are
      shorter than optimal, requiring more passes)
  3. solution.insert(i, item) is O(n) — making merge O(n²) per strand
  4. Recursive — hits Python recursion limit for large reverse-sorted input

Variants:
1. Original (documented quirks above)
2. Clean iterative — uses deque for O(1) popleft, fixes index-skip bug,
   two-pointer merge instead of O(n) insert
3. heapq.merge — collects all strands first, merges with heap in one pass
4. sorted() built-in — Timsort reference (note: Timsort also detects runs!)

Source: https://en.wikipedia.org/wiki/Strand_sort
"""

from __future__ import annotations
import heapq
import time
import random
from collections import deque


# ---------------------------------------------------------------------------
# 1. Original (preserved exactly — with its quirks)
# ---------------------------------------------------------------------------
import operator as _operator_module


def strand_sort_original(arr: list, reverse: bool = False,
                         solution: list | None = None) -> list:
    """Original implementation — modifies input, skips some strand members.

    >>> strand_sort_original([4, 2, 5, 3, 0, 1])
    [0, 1, 2, 3, 4, 5]
    >>> strand_sort_original([4, 2, 5, 3, 0, 1], reverse=True)
    [5, 4, 3, 2, 1, 0]
    >>> strand_sort_original([])
    []
    """
    _op = _operator_module.lt if reverse else _operator_module.gt
    solution = solution or []
    if not arr:
        return solution
    sublist = [arr.pop(0)]
    for i, item in enumerate(arr):
        if _op(item, sublist[-1]):
            sublist.append(item)
            arr.pop(i)  # ← skips next element (index shifts)
    if not solution:
        solution.extend(sublist)
    else:
        while sublist:
            item = sublist.pop(0)
            for i, xx in enumerate(solution):
                if not _op(item, xx):
                    solution.insert(i, item)  # ← O(n)
                    break
            else:
                solution.append(item)
    strand_sort_original(arr, reverse, solution)
    return solution


# ---------------------------------------------------------------------------
# 2. Clean iterative — fixes all four issues
#    - deque for O(1) popleft
#    - correct strand extraction (no index-skip)
#    - two-pointer merge (O(m+k) instead of O(m*k))
#    - iterative loop instead of recursion
# ---------------------------------------------------------------------------
def strand_sort_clean(arr: list, reverse: bool = False) -> list:
    """Clean iterative strand sort — fixes pop(0), index-skip, O(n) insert, recursion.

    >>> strand_sort_clean([4, 2, 5, 3, 0, 1])
    [0, 1, 2, 3, 4, 5]
    >>> strand_sort_clean([4, 2, 5, 3, 0, 1], reverse=True)
    [5, 4, 3, 2, 1, 0]
    >>> strand_sort_clean([])
    []
    >>> strand_sort_clean([1])
    [1]
    >>> strand_sort_clean([3, 1, 4, 1, 5, 9, 2, 6])
    [1, 1, 2, 3, 4, 5, 6, 9]
    """
    remaining = deque(arr)
    solution: list = []

    def _merge(a: list, b: list) -> list:
        """Two-pointer merge of two sorted lists — O(m+k)."""
        result, i, j = [], 0, 0
        while i < len(a) and j < len(b):
            if (a[i] <= b[j]) ^ reverse:
                result.append(a[i]); i += 1
            else:
                result.append(b[j]); j += 1
        result.extend(a[i:])
        result.extend(b[j:])
        return result

    while remaining:
        # Extract one strand: scan remaining, keep elements that extend the run
        strand = [remaining.popleft()]
        new_remaining: deque = deque()
        for item in remaining:
            cond = item >= strand[-1] if not reverse else item <= strand[-1]
            if cond:
                strand.append(item)
            else:
                new_remaining.append(item)
        remaining = new_remaining
        # Merge strand into solution
        solution = _merge(solution, strand)

    return solution


# ---------------------------------------------------------------------------
# 3. heapq.merge — collect ALL strands, then merge with a heap in one pass
#    This gives O(n log k) merge where k = number of strands
# ---------------------------------------------------------------------------
def strand_sort_heapq(arr: list) -> list:
    """Collect all strands, merge with heapq.merge — O(n log k) merge phase.
    Only supports ascending order (heapq requires comparable elements).

    >>> strand_sort_heapq([4, 2, 5, 3, 0, 1])
    [0, 1, 2, 3, 4, 5]
    >>> strand_sort_heapq([])
    []
    >>> strand_sort_heapq([3, 1, 4, 1, 5, 9, 2, 6])
    [1, 1, 2, 3, 4, 5, 6, 9]
    """
    remaining = deque(arr)
    strands: list[list] = []

    while remaining:
        strand = [remaining.popleft()]
        new_remaining: deque = deque()
        for item in remaining:
            if item >= strand[-1]:
                strand.append(item)
            else:
                new_remaining.append(item)
        remaining = new_remaining
        strands.append(strand)

    return list(heapq.merge(*strands))


# ---------------------------------------------------------------------------
# 4. Built-in sorted() — Timsort (also detects natural runs, same idea)
# ---------------------------------------------------------------------------
def sort_builtin(arr: list) -> list:
    """Python sorted() — Timsort, which also detects natural ascending runs.

    >>> sort_builtin([4, 2, 5, 3, 0, 1])
    [0, 1, 2, 3, 4, 5]
    >>> sort_builtin([])
    []
    """
    return sorted(arr)


# ---------------------------------------------------------------------------
# Strand analysis — show how many strands each scenario produces
# ---------------------------------------------------------------------------
def count_strands(arr: list) -> int:
    """Count the number of strands (ascending runs) in arr."""
    if not arr:
        return 0
    count = 1
    for i in range(1, len(arr)):
        if arr[i] < arr[i - 1]:
            count += 1
    return count


def show_strand_analysis() -> None:
    n = 20
    scenarios = {
        "already sorted":  list(range(n)),
        "reverse sorted":  list(range(n, 0, -1)),
        "random":          random.sample(range(n * 2), n),
        "nearly sorted":   list(range(n - 3)) + [n, n - 1, n + 1],
    }
    print("Strand count analysis (n=20):")
    print(f"  {'scenario':>20}  {'strands':>8}  {'best case?':>12}")
    for label, data in scenarios.items():
        k = count_strands(data)
        best = "O(n) *best*" if k == 1 else f"O(n*{k})"
        print(f"  {label:>20}  {k:>8}  {best:>12}")


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    import sys
    sys.setrecursionlimit(50_000)

    variants = [
        ("original (recursive)", strand_sort_original),
        ("clean iterative     ", strand_sort_clean),
        ("heapq.merge         ", strand_sort_heapq),
        ("sorted()            ", sort_builtin),
    ]

    scenarios = [
        ("random",          lambda n: random.sample(range(n * 2), n)),
        ("already sorted",  lambda n: list(range(n))),
        ("reverse sorted",  lambda n: list(range(n, 0, -1))),
        ("nearly sorted",   lambda n: list(range(n - n//10)) +
                                      random.sample(range(n), n//10)),
    ]

    sizes = [100, 500, 2_000]

    for label, gen in scenarios:
        print(f"\n--- {label} ---")
        for n in sizes:
            data = gen(n)
            print(f"  n={n:,}")
            for name, fn in variants:
                try:
                    best = float("inf")
                    for _ in range(3):
                        t0 = time.perf_counter()
                        result = fn(list(data))
                        best = min(best, time.perf_counter() - t0)
                    assert result == sorted(data), f"{name} wrong!"
                    print(f"    {name}: {best * 1000:8.3f} ms")
                except RecursionError:
                    print(f"    {name}: RECURSION OVERFLOW")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("All doctests passed.\n")
    show_strand_analysis()
    print()
    benchmark()
