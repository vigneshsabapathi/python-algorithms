"""
Iterative Merge Sort — optimized variants for interview prep.

The original iter_merge_sort has one performance bug:
  merge() uses list.pop(0) — O(n) per call (shifts the whole list)
  → merge becomes O(n^2) instead of O(n)
  → overall sort is O(n^2 * log n) instead of O(n log n)

This file provides three fixed/optimized variants:
  iter_merge_sort_deque  : replace pop(0) with deque.popleft() → O(1) pop
  iter_merge_sort_index  : index-pointer merge, no temporary deque
  merge_sort_recursive   : classic recursive merge sort (reference baseline)
  sorted()               : Python Timsort — always the production answer
"""

from __future__ import annotations

from collections import deque


# ---------------------------------------------------------------------------
# Bug demo — pop(0) is O(n)
# ---------------------------------------------------------------------------
#
# Original merge():
#   while left and right:
#       result.append((left if left[0] <= right[0] else right).pop(0))
#
# list.pop(0) removes the first element by shifting ALL remaining elements
# left by one position → O(n) per call.
# For a merge of two halves of size k each → O(k^2) instead of O(k).
# Total across all merges: O(n^2 * log n) instead of O(n log n).
#
# Fix: use collections.deque (popleft is O(1)) or index pointers.


# ---------------------------------------------------------------------------
# Variant 1: deque-based merge (fix pop(0) → popleft())
# ---------------------------------------------------------------------------

def _merge_deque(arr: list, lo: int, mid: int, hi: int) -> None:
    """Merge arr[lo:mid+1] and arr[mid+1:hi+1] in-place using deques (O(n) merge).
    mid and hi are inclusive indices."""
    left  = deque(arr[lo:mid + 1])
    right = deque(arr[mid + 1:hi + 1])
    i = lo
    while left and right:
        if left[0] <= right[0]:
            arr[i] = left.popleft()
        else:
            arr[i] = right.popleft()
        i += 1
    while left:
        arr[i] = left.popleft(); i += 1
    while right:
        arr[i] = right.popleft(); i += 1


def iter_merge_sort_deque(input_list: list) -> list:
    """
    Bottom-up iterative merge sort using deque for O(1) front-pop.

    Fixes the O(n^2) pop(0) bug in the original. Total complexity: O(n log n).

    Examples:
    >>> iter_merge_sort_deque([5, 9, 8, 7, 1, 2, 7])
    [1, 2, 5, 7, 7, 8, 9]
    >>> iter_merge_sort_deque([])
    []
    >>> iter_merge_sort_deque([1])
    [1]
    >>> iter_merge_sort_deque([4, 3, 2, 1])
    [1, 2, 3, 4]
    >>> iter_merge_sort_deque(['c', 'b', 'a'])
    ['a', 'b', 'c']
    >>> iter_merge_sort_deque([2, 1, 3])
    [1, 2, 3]
    """
    arr = list(input_list)
    n = len(arr)
    if n <= 1:
        return arr
    width = 1
    while width < n:
        for lo in range(0, n, 2 * width):
            mid = min(lo + width, n) - 1        # inclusive mid
            hi  = min(lo + 2 * width, n) - 1   # inclusive hi
            if mid < hi:
                _merge_deque(arr, lo, mid, hi)
        width *= 2
    return arr


# ---------------------------------------------------------------------------
# Variant 2: index-pointer merge (no auxiliary deque object)
# ---------------------------------------------------------------------------

def _merge_index(arr: list, buf: list, lo: int, mid: int, hi: int) -> None:
    """
    Merge arr[lo:mid+1] and arr[mid+1:hi+1] using a pre-allocated buffer.
    Index pointers instead of popping — pure O(n) with minimal allocations.
    """
    buf[lo:hi + 1] = arr[lo:hi + 1]
    i, j, k = lo, mid + 1, lo
    while i <= mid and j <= hi:
        if buf[i] <= buf[j]:
            arr[k] = buf[i]; i += 1
        else:
            arr[k] = buf[j]; j += 1
        k += 1
    while i <= mid:
        arr[k] = buf[i]; i += 1; k += 1
    while j <= hi:
        arr[k] = buf[j]; j += 1; k += 1


def iter_merge_sort_index(input_list: list) -> list:
    """
    Bottom-up iterative merge sort with index-pointer merge and a shared buffer.

    Single buffer allocation for the whole sort (reused across all merges).
    Typically the fastest pure-Python merge sort variant.

    Examples:
    >>> iter_merge_sort_index([5, 9, 8, 7, 1, 2, 7])
    [1, 2, 5, 7, 7, 8, 9]
    >>> iter_merge_sort_index([])
    []
    >>> iter_merge_sort_index([1])
    [1]
    >>> iter_merge_sort_index([4, 3, 2, 1])
    [1, 2, 3, 4]
    >>> iter_merge_sort_index(['c', 'b', 'a'])
    ['a', 'b', 'c']
    >>> iter_merge_sort_index([2, 1, 3])
    [1, 2, 3]
    """
    arr = list(input_list)
    n = len(arr)
    if n <= 1:
        return arr
    buf = arr[:]   # single buffer allocation, reused for every merge
    width = 1
    while width < n:
        for lo in range(0, n, 2 * width):
            mid = min(lo + width, n) - 1
            hi  = min(lo + 2 * width, n) - 1
            if mid < hi:
                _merge_index(arr, buf, lo, mid, hi)
        width *= 2
    return arr


# ---------------------------------------------------------------------------
# Reference: classic recursive merge sort
# ---------------------------------------------------------------------------

def merge_sort_recursive(arr: list) -> list:
    """
    Classic top-down recursive merge sort. O(n log n) time, O(n log n) stack.

    Examples:
    >>> merge_sort_recursive([5, 9, 8, 7, 1, 2, 7])
    [1, 2, 5, 7, 7, 8, 9]
    >>> merge_sort_recursive([])
    []
    >>> merge_sort_recursive([4, 3, 2, 1])
    [1, 2, 3, 4]
    """
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left  = merge_sort_recursive(arr[:mid])
    right = merge_sort_recursive(arr[mid:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]


def benchmark() -> None:
    import copy
    import random
    import timeit

    random.seed(42)

    import sys
    sys.path.insert(0, 'sorts')
    from iterative_merge_sort import iter_merge_sort as original

    print("Performance bug: pop(0) is O(n) — merge becomes O(n^2)")
    print("Scaling test (200 iterations):\n")
    header = f"{'n':<7} {'original(pop0)':>16} {'deque':>8} {'index':>8} {'recursive':>11} {'sorted()':>9}"
    print(header)
    print("-" * len(header))

    for n in [100, 500, 1000, 2000, 5000]:
        data = [random.randint(0, 9999) for _ in range(n)]
        iters = max(10, 2000 // n)
        t_o = timeit.timeit(lambda: original(list(data)),               number=iters)
        t_d = timeit.timeit(lambda: iter_merge_sort_deque(list(data)),  number=iters)
        t_i = timeit.timeit(lambda: iter_merge_sort_index(list(data)),  number=iters)
        t_r = timeit.timeit(lambda: merge_sort_recursive(list(data)),   number=iters)
        t_s = timeit.timeit(lambda: sorted(data),                       number=iters)
        print(f"{n:<7} {t_o:>16.3f} {t_d:>8.3f} {t_i:>8.3f} {t_r:>11.3f} {t_s:>9.3f}")

    # --- Stability check ---
    print("\nStability check:")
    data = [(2, 'a'), (1, 'b'), (2, 'c'), (1, 'd')]
    expected = sorted(data, key=lambda x: x[0])
    r_orig  = original(copy.copy(data))
    r_deque = iter_merge_sort_deque(copy.copy(data))
    r_idx   = iter_merge_sort_index(copy.copy(data))
    r_rec   = merge_sort_recursive(copy.copy(data))
    print(f"  Input:     {data}")
    print(f"  Expected:  {expected}")
    print(f"  original:  {r_orig}  stable={r_orig == expected}")
    print(f"  deque:     {r_deque}  stable={r_deque == expected}")
    print(f"  index:     {r_idx}  stable={r_idx == expected}")
    print(f"  recursive: {r_rec}  stable={r_rec == expected}")

    # --- Dataset variety ---
    print("\nDataset comparison (n=2000, 100 iters, seconds):")
    n = 2000
    iters = 100
    datasets = {
        "random":        [random.randint(0, 9999) for _ in range(n)],
        "reversed":      list(range(n, 0, -1)),
        "sorted":        list(range(n)),
        "nearly sorted": list(range(n - 20)) + [random.randint(0, n) for _ in range(20)],
    }
    header2 = f"{'Dataset':<16} {'index':>7} {'recursive':>11} {'sorted()':>9}"
    print(header2)
    print("-" * len(header2))
    for label, data in datasets.items():
        t_i = timeit.timeit(lambda: iter_merge_sort_index(list(data)),  number=iters)
        t_r = timeit.timeit(lambda: merge_sort_recursive(list(data)),   number=iters)
        t_s = timeit.timeit(lambda: sorted(data),                       number=iters)
        print(f"{label:<16} {t_i:>7.3f} {t_r:>11.3f} {t_s:>9.3f}")


if __name__ == "__main__":
    benchmark()
