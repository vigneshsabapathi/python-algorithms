"""
Introsort — optimized variants and analysis for interview prep.

Introsort is the hybrid algorithm behind C++ std::sort and many production
sort implementations. It combines:
  - Quicksort  : fast average case, cache-friendly, in-place
  - Heap sort  : O(n log n) worst-case guarantee (fallback)
  - Insertion sort : fast for small subarrays (base case)

The depth limit (2 * floor(log2(n))) is the key: if quicksort's recursion
exceeds this depth, pivot selection has been unlucky (degenerate partitions)
and we switch to heap sort to restore the O(n log n) guarantee.

Variants:
  IntroSortInstrumented : tracks which branch (quick/heap/insertion) is used
  IntroSortThreeWay     : 3-way (Dutch National Flag) partition for arrays
                          with many duplicates — O(n) on all-equal input
  sort_stdlib           : Python sorted() — always the baseline
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Variant 1: Instrumented introsort — shows which branch fires
# ---------------------------------------------------------------------------

@dataclass
class SortStats:
    insertion_calls: int = 0
    quicksort_steps: int = 0
    heapsort_calls: int = 0
    comparisons: int = 0

    def __str__(self) -> str:
        return (f"insertion_calls={self.insertion_calls}, "
                f"quicksort_steps={self.quicksort_steps}, "
                f"heapsort_calls={self.heapsort_calls}, "
                f"comparisons={self.comparisons}")


def _sift_down(arr: list, i: int, n: int) -> None:
    """Iterative max-heap sift-down."""
    while True:
        largest = i
        left, right = 2 * i + 1, 2 * i + 2
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest == i:
            break
        arr[i], arr[largest] = arr[largest], arr[i]
        i = largest


def _heap_sort_inplace(arr: list, lo: int, hi: int) -> None:
    """Heap sort arr[lo:hi] in place."""
    n = hi - lo
    # Build max-heap in the slice (offset all indices by lo)
    for i in range(lo + n // 2 - 1, lo - 1, -1):
        # Sift down within the slice
        idx = i - lo
        while True:
            largest = idx
            left, right = 2 * idx + 1, 2 * idx + 2
            if left < n and arr[lo + left] > arr[lo + largest]:
                largest = left
            if right < n and arr[lo + right] > arr[lo + largest]:
                largest = right
            if largest == idx:
                break
            arr[lo + idx], arr[lo + largest] = arr[lo + largest], arr[lo + idx]
            idx = largest
    # Extract
    for end in range(n - 1, 0, -1):
        arr[lo], arr[lo + end] = arr[lo + end], arr[lo]
        idx = 0
        while True:
            largest = idx
            left, right = 2 * idx + 1, 2 * idx + 2
            if left < end and arr[lo + left] > arr[lo + largest]:
                largest = left
            if right < end and arr[lo + right] > arr[lo + largest]:
                largest = right
            if largest == idx:
                break
            arr[lo + idx], arr[lo + largest] = arr[lo + largest], arr[lo + idx]
            idx = largest


def _insertion_sort_slice(arr: list, lo: int, hi: int) -> None:
    """Insertion sort arr[lo:hi] in place."""
    for i in range(lo + 1, hi):
        key = arr[i]
        j = i
        while j > lo and arr[j - 1] > key:
            arr[j] = arr[j - 1]
            j -= 1
        arr[j] = key


def _median_of_3(arr: list, a: int, b: int, c: int) -> int:
    """Return index of the median of arr[a], arr[b], arr[c]."""
    if arr[a] < arr[b]:
        if arr[b] < arr[c]:
            return b
        elif arr[a] < arr[c]:
            return c
        else:
            return a
    else:
        if arr[a] < arr[c]:
            return a
        elif arr[b] < arr[c]:
            return c
        else:
            return b


def _partition(arr: list, lo: int, hi: int, pivot_val) -> int:
    """Lomuto-style two-pointer partition around pivot_val."""
    i, j = lo, hi
    while True:
        while arr[i] < pivot_val:
            i += 1
        j -= 1
        while pivot_val < arr[j]:
            j -= 1
        if i >= j:
            return i
        arr[i], arr[j] = arr[j], arr[i]
        i += 1


def intro_sort_instrumented(arr: list, stats: SortStats | None = None) -> tuple[list, SortStats]:
    """
    Introsort with instrumentation: tracks insertion/quicksort/heapsort branches.

    Examples:
    >>> result, stats = intro_sort_instrumented([4, 2, 6, 8, 1, 7, 3])
    >>> result
    [1, 2, 3, 4, 6, 7, 8]
    >>> result, stats = intro_sort_instrumented([])
    >>> result
    []
    >>> result, stats = intro_sort_instrumented([3, 1, 2])
    >>> result
    [1, 2, 3]
    """
    arr = list(arr)
    if not arr:
        return arr, SortStats()
    if stats is None:
        stats = SortStats()

    max_depth = 2 * math.floor(math.log2(len(arr)))
    SIZE_THRESHOLD = 16

    def _introsort(lo: int, hi: int, depth: int) -> None:
        if hi - lo <= SIZE_THRESHOLD:
            stats.insertion_calls += 1
            _insertion_sort_slice(arr, lo, hi)
            return
        if depth == 0:
            stats.heapsort_calls += 1
            _heap_sort_inplace(arr, lo, hi)
            return
        stats.quicksort_steps += 1
        mid = lo + (hi - lo) // 2
        pivot_idx = _median_of_3(arr, lo, mid, hi - 1)
        pivot_val = arr[pivot_idx]
        p = _partition(arr, lo, hi, pivot_val)
        _introsort(lo, p, depth - 1)
        _introsort(p, hi, depth - 1)

    _introsort(0, len(arr), max_depth)
    return arr, stats


# ---------------------------------------------------------------------------
# Variant 2: 3-way partition introsort (fast for many duplicates)
# ---------------------------------------------------------------------------

def _partition_3way(arr: list, lo: int, hi: int) -> tuple[int, int]:
    """
    Dutch National Flag 3-way partition around median-of-3 pivot.
    Returns (lt, gt): arr[lo:lt] < pivot, arr[lt:gt] == pivot, arr[gt:hi] > pivot.
    O(n) on all-equal input (unlike 2-way which is O(n^2)).
    """
    mid = lo + (hi - lo) // 2
    pivot_idx = _median_of_3(arr, lo, mid, hi - 1)
    pivot = arr[pivot_idx]

    lt, i, gt = lo, lo, hi
    while i < gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1; i += 1
        elif arr[i] > pivot:
            gt -= 1
            arr[i], arr[gt] = arr[gt], arr[i]
        else:
            i += 1
    return lt, gt


def intro_sort_3way(arr: list) -> list:
    """
    Introsort with 3-way (DNF) partition. Handles duplicates in O(n log n)
    instead of O(n^2), and runs in O(n) on all-equal arrays.

    Examples:
    >>> intro_sort_3way([4, 2, 6, 8, 1, 7, 8, 22, 14, 56, 27, 79, 23, 45, 14, 12])
    [1, 2, 4, 6, 7, 8, 8, 12, 14, 14, 22, 23, 27, 45, 56, 79]
    >>> intro_sort_3way([])
    []
    >>> intro_sort_3way([3, 3, 3, 3, 3])
    [3, 3, 3, 3, 3]
    >>> intro_sort_3way([-1, -5, -3, -13, -44])
    [-44, -13, -5, -3, -1]
    >>> intro_sort_3way([1])
    [1]
    """
    arr = list(arr)
    if not arr:
        return arr
    max_depth = 2 * math.floor(math.log2(len(arr)))
    SIZE_THRESHOLD = 16

    def _sort(lo: int, hi: int, depth: int) -> None:
        if hi - lo <= SIZE_THRESHOLD:
            _insertion_sort_slice(arr, lo, hi)
            return
        if depth == 0:
            _heap_sort_inplace(arr, lo, hi)
            return
        lt, gt = _partition_3way(arr, lo, hi)
        _sort(lo, lt, depth - 1)
        _sort(gt, hi, depth - 1)   # middle (== pivot) already sorted

    _sort(0, len(arr), max_depth)
    return arr


def benchmark() -> None:
    import random
    import timeit

    random.seed(42)
    n = 2000
    iters = 500

    # Reference original sort()
    import sys
    sys.path.insert(0, 'sorts')
    from intro_sort import sort as intro_sort_original

    datasets = {
        "random":        [random.randint(0, 9999) for _ in range(n)],
        "reversed":      list(range(n, 0, -1)),
        "sorted":        list(range(n)),
        "nearly sorted": list(range(n - 20)) + [random.randint(0, n) for _ in range(20)],
        "many dupes":    [random.randint(0, 9) for _ in range(n)],   # only 10 distinct
        "all equal":     [42] * n,
    }

    print(f"Benchmark: n={n}, {iters} iterations\n")
    header = f"{'Dataset':<16} {'original':>9} {'3way':>7} {'sorted()':>9}"
    print(header)
    print("-" * len(header))

    for label, data in datasets.items():
        t_o = timeit.timeit(lambda: intro_sort_original(list(data)),  number=iters)
        t_3 = timeit.timeit(lambda: intro_sort_3way(list(data)),      number=iters)
        t_s = timeit.timeit(lambda: sorted(data),                     number=iters)
        print(f"{label:<16} {t_o:>9.3f} {t_3:>7.3f} {t_s:>9.3f}")

    # --- Instrumented: which branch fires? ---
    print("\nBranch breakdown (n=200 random):")
    data200 = [random.randint(0, 999) for _ in range(200)]
    _, stats = intro_sort_instrumented(data200)
    print(f"  {stats}")

    print("\nBranch breakdown (n=200 sorted — quicksort still fires):")
    _, stats2 = intro_sort_instrumented(list(range(200)))
    print(f"  {stats2}")

    print("\nBranch breakdown (n=200 all equal):")
    _, stats3 = intro_sort_instrumented([5] * 200)
    print(f"  {stats3}")

    # --- Depth limit demo: force heap sort fallback ---
    print("\nDepth limit demo — force heapsort fallback (max_depth=1, n=200):")
    arr_force = [random.randint(0, 999) for _ in range(200)]
    arr_copy = list(arr_force)
    stats_forced = SortStats()
    SIZE_THRESHOLD = 16
    max_depth = 1  # very shallow — will hit heap sort quickly

    def _force(lo: int, hi: int, depth: int) -> None:
        if hi - lo <= SIZE_THRESHOLD:
            stats_forced.insertion_calls += 1
            _insertion_sort_slice(arr_copy, lo, hi)
            return
        if depth == 0:
            stats_forced.heapsort_calls += 1
            _heap_sort_inplace(arr_copy, lo, hi)
            return
        stats_forced.quicksort_steps += 1
        mid = lo + (hi - lo) // 2
        pivot_idx = _median_of_3(arr_copy, lo, mid, hi - 1)
        pivot_val = arr_copy[pivot_idx]
        p = _partition(arr_copy, lo, hi, pivot_val)
        _force(lo, p, depth - 1)
        _force(p, hi, depth - 1)

    _force(0, len(arr_copy), max_depth)
    correct = arr_copy == sorted(arr_force)
    print(f"  {stats_forced}  correct={correct}")


if __name__ == "__main__":
    benchmark()
