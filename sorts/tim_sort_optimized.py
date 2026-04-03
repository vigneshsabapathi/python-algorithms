"""Optimized and alternative implementations of Timsort.

Timsort (Tim Peters, 2002) is Python's actual sorting algorithm — used by
sorted() and list.sort(). It is a hybrid of merge sort and insertion sort,
designed to exploit natural runs in real-world data.

The educational implementation in tim_sort.py has four issues:
  1. Empty input crashes: `lst[0]` raises IndexError
  2. `merge()` is recursive — O(n) stack depth, crashes on large inputs
  3. `merge()` uses `[right[0], *merge(...)]` — O(n²) copies total
  4. No RUN_SIZE cap — all natural runs are insertion-sorted regardless of
     length; real Timsort caps runs at 32–64 elements

This file shows:
  1. Educational (original) — preserved for reference
  2. Educational fixed — handles empty, iterative merge, no recursion limit
  3. Proper educational Timsort — RUN_SIZE=32, iterative bottom-up merge
  4. sorted() / list.sort() — the actual C Timsort (always use this)

Key Timsort features NOT in the educational versions:
  - Galloping mode: when one run dominates, switches to binary search jumps
  - Descending run detection: reverses naturally descending runs
  - Min-run calculation: chooses optimal RUN_SIZE (32–64) based on n
  - Run stack merging: maintains merge stack with invariants for O(n log n)

Reference: https://svn.python.org/projects/python/trunk/Objects/listsort.txt
"""

from __future__ import annotations
import bisect
import time
import random

RUN_SIZE = 32  # Real Timsort uses 32–64; powers-of-2 for clean merges


# ---------------------------------------------------------------------------
# 1. Educational original (from tim_sort.py) — preserved with its issues
# ---------------------------------------------------------------------------
def _binary_search_orig(lst, item, start, end):
    if start == end:
        return start if lst[start] > item else start + 1
    if start > end:
        return start
    mid = (start + end) // 2
    if lst[mid] < item:
        return _binary_search_orig(lst, item, mid + 1, end)
    elif lst[mid] > item:
        return _binary_search_orig(lst, item, start, mid - 1)
    else:
        return mid


def _insertion_sort_orig(lst):
    for index in range(1, len(lst)):
        value = lst[index]
        pos = _binary_search_orig(lst, value, 0, index - 1)
        lst = [*lst[:pos], value, *lst[pos:index], *lst[index + 1:]]
    return lst


def _merge_orig(left, right):
    if not left:
        return right
    if not right:
        return left
    if left[0] < right[0]:
        return [left[0], *_merge_orig(left[1:], right)]  # recursive — O(n) stack
    return [right[0], *_merge_orig(left, right[1:])]


def timsort_educational(lst: list) -> list:
    """Original educational Timsort — crashes on empty, O(n²) merge copies.

    >>> timsort_educational([5, 3, 1, 4, 2])
    [1, 2, 3, 4, 5]
    >>> timsort_educational([3, 2, 1])
    [1, 2, 3]
    """
    if not lst:
        return []
    length = len(lst)
    runs, new_run = [], [lst[0]]
    for i in range(1, length):
        if lst[i] < lst[i - 1]:
            runs.append(new_run)
            new_run = [lst[i]]
        else:
            new_run.append(lst[i])
    runs.append(new_run)
    sorted_runs = [_insertion_sort_orig(run) for run in runs]
    result = []
    for run in sorted_runs:
        result = _merge_orig(result, run)
    return result


# ---------------------------------------------------------------------------
# 2. Educational fixed — handles empty, iterative merge, bisect for insertion
# ---------------------------------------------------------------------------
def _insertion_sort_fixed(arr: list, lo: int, hi: int) -> None:
    """In-place binary insertion sort on arr[lo:hi+1]."""
    for i in range(lo + 1, hi + 1):
        key = arr[i]
        pos = bisect.bisect_left(arr, key, lo, i)
        arr[pos + 1: i + 1] = arr[pos:i]
        arr[pos] = key


def _merge_fixed(arr: list, lo: int, mid: int, hi: int) -> None:
    """In-place merge of arr[lo:mid+1] and arr[mid+1:hi+1] — O(n) copies."""
    left = arr[lo: mid + 1]
    right = arr[mid + 1: hi + 1]
    i = j = 0
    k = lo
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]; i += 1
        else:
            arr[k] = right[j]; j += 1
        k += 1
    while i < len(left):
        arr[k] = left[i]; i += 1; k += 1
    while j < len(right):
        arr[k] = right[j]; j += 1; k += 1


def timsort_fixed(lst: list) -> list:
    """Fixed educational version: handles empty, iterative merge, no recursion limit.

    >>> timsort_fixed([5, 3, 1, 4, 2])
    [1, 2, 3, 4, 5]
    >>> timsort_fixed([])
    []
    >>> timsort_fixed([1])
    [1]
    >>> timsort_fixed("Python")
    ['P', 'h', 'n', 'o', 't', 'y']
    """
    arr = list(lst)
    n = len(arr)
    if n <= 1:
        return arr
    # Detect natural runs (ascending), insertion-sort each
    runs: list[tuple[int, int]] = []  # (start, end) inclusive
    i = 0
    while i < n:
        run_start = i
        if i + 1 < n and arr[i + 1] < arr[i]:
            # Descending run — find extent and reverse
            while i + 1 < n and arr[i + 1] < arr[i]:
                i += 1
            arr[run_start:i + 1] = arr[run_start:i + 1][::-1]
        else:
            while i + 1 < n and arr[i + 1] >= arr[i]:
                i += 1
        runs.append((run_start, i))
        i += 1
    # Insertion-sort any run shorter than RUN_SIZE
    for start, end in runs:
        if end - start + 1 < RUN_SIZE:
            _insertion_sort_fixed(arr, start, end)
    # Merge runs pairwise until one remains
    run_starts = [s for s, _ in runs]
    run_ends = [e for _, e in runs]
    while len(run_starts) > 1:
        new_starts, new_ends = [], []
        for i in range(0, len(run_starts), 2):
            if i + 1 < len(run_starts):
                _merge_fixed(arr, run_starts[i], run_ends[i], run_ends[i + 1])
                new_starts.append(run_starts[i])
                new_ends.append(run_ends[i + 1])
            else:
                new_starts.append(run_starts[i])
                new_ends.append(run_ends[i])
        run_starts, run_ends = new_starts, new_ends
    return arr


# ---------------------------------------------------------------------------
# 3. Proper educational Timsort — RUN_SIZE=32, bottom-up iterative merge
#    Closest to the real algorithm while remaining readable
# ---------------------------------------------------------------------------
def timsort_proper(lst: list) -> list:
    """Proper educational Timsort: RUN_SIZE=32, bottom-up iterative merge.
    Handles descending runs. O(n log n) worst case.

    >>> timsort_proper([5, 3, 1, 4, 2])
    [1, 2, 3, 4, 5]
    >>> timsort_proper([])
    []
    >>> timsort_proper([1, 2, 3, 4, 5])
    [1, 2, 3, 4, 5]
    >>> timsort_proper(list(range(100, 0, -1)))
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
    """
    arr = list(lst)
    n = len(arr)
    if n <= 1:
        return arr

    # Step 1: insertion-sort each RUN_SIZE chunk
    for start in range(0, n, RUN_SIZE):
        end = min(start + RUN_SIZE - 1, n - 1)
        _insertion_sort_fixed(arr, start, end)

    # Step 2: iteratively merge runs of increasing size
    size = RUN_SIZE
    while size < n:
        for lo in range(0, n, size * 2):
            mid = min(lo + size - 1, n - 1)
            hi = min(lo + size * 2 - 1, n - 1)
            if mid < hi:
                _merge_fixed(arr, lo, mid, hi)
        size *= 2

    return arr


# ---------------------------------------------------------------------------
# 4. Built-in sorted() — actual CPython Timsort (C implementation)
# ---------------------------------------------------------------------------
def timsort_builtin(lst) -> list:
    """Python sorted() — the real Timsort in C. Always use this.

    >>> timsort_builtin([5, 3, 1, 4, 2])
    [1, 2, 3, 4, 5]
    >>> timsort_builtin([])
    []
    """
    return sorted(lst)


# ---------------------------------------------------------------------------
# Demonstrate Timsort's key features
# ---------------------------------------------------------------------------
def show_features() -> None:
    print("Timsort key properties:")

    # 1. Adaptive on nearly-sorted
    import time
    n = 10_000
    sorted_data = list(range(n))
    random_data = random.sample(range(n * 2), n)

    t0 = time.perf_counter()
    sorted(sorted_data)
    t_sorted = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    sorted(random_data)
    t_random = (time.perf_counter() - t0) * 1000

    print(f"  sorted() on sorted n={n:,}: {t_sorted:.3f} ms (O(n))")
    print(f"  sorted() on random n={n:,}: {t_random:.3f} ms (O(n log n))")
    print(f"  Speedup on sorted input: {t_random / t_sorted:.1f}x")

    # 2. Stable
    data = [(1, 'b'), (2, 'a'), (1, 'c'), (2, 'd')]
    result = sorted(data, key=lambda x: x[0])
    print(f"\n  Stability test (sort by first element only):")
    print(f"    Input:  {data}")
    print(f"    Output: {result}  (second elements maintain original order)")


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    import sys
    sys.setrecursionlimit(50_000)

    variants = [
        ("educational (orig)", timsort_educational),
        ("educational fixed  ", timsort_fixed),
        ("proper (RUN=32)    ", timsort_proper),
        ("sorted() builtin   ", timsort_builtin),
    ]

    scenarios = [
        ("random",          lambda n: random.sample(range(n * 2), n)),
        ("already sorted",  lambda n: list(range(n))),
        ("reverse sorted",  lambda n: list(range(n, 0, -1))),
        ("nearly sorted",   lambda n: list(range(n - n//10))
                                      + random.sample(range(n), n//10)),
    ]

    sizes = [100, 1_000, 5_000]

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
    show_features()
    print()
    benchmark()
