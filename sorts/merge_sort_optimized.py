"""
Merge Sort — optimized variants for interview prep.

The original merge_sort has one performance bug:
  merge() uses left.pop(0) — O(n) per call (shifts the whole list)
  → merge becomes O(n^2) instead of O(n)
  → overall sort is O(n^2 log n) instead of O(n log n)

Variants:
  merge_sort_index   : fix pop(0) with index pointers + O(n) slices
  merge_sort_inplace : bottom-up iterative, single shared buffer
  merge_sort_timsort : Timsort-inspired — detect natural runs, use
                       insertion sort for small runs, merge adaptively
"""

from __future__ import annotations

MIN_RUN = 32   # Timsort uses 32-64; elements below this use insertion sort


# ---------------------------------------------------------------------------
# Variant 1: Index-pointer merge (fix pop(0))
# ---------------------------------------------------------------------------

def merge_sort_index(arr: list) -> list:
    """
    Recursive merge sort with index-pointer merge — O(n log n) correct.

    Fixes pop(0) by using index i,j pointers and slice extension.
    Each merge step: O(n) time, O(n) auxiliary space.

    Examples:
    >>> merge_sort_index([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> merge_sort_index([])
    []
    >>> merge_sort_index([-2, -5, -45])
    [-45, -5, -2]
    >>> merge_sort_index([4, 3, 2, 1])
    [1, 2, 3, 4]
    >>> merge_sort_index(['d', 'a', 'b', 'e', 'c'])
    ['a', 'b', 'c', 'd', 'e']
    """
    if len(arr) <= 1:
        return list(arr)
    mid = len(arr) // 2
    left  = merge_sort_index(arr[:mid])
    right = merge_sort_index(arr[mid:])
    return _merge(left, right)


def _merge(left: list, right: list) -> list:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------------------------------------------------------------------------
# Variant 2: Bottom-up iterative merge sort (shared buffer)
# ---------------------------------------------------------------------------

def merge_sort_inplace(arr: list) -> list:
    """
    Bottom-up (iterative) merge sort using a shared auxiliary buffer.
    Avoids recursion stack; single buffer allocation for whole sort.

    Examples:
    >>> merge_sort_inplace([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> merge_sort_inplace([])
    []
    >>> merge_sort_inplace([-2, -5, -45])
    [-45, -5, -2]
    >>> merge_sort_inplace([4, 3, 2, 1])
    [1, 2, 3, 4]
    >>> merge_sort_inplace(['d', 'a', 'b', 'e', 'c'])
    ['a', 'b', 'c', 'd', 'e']
    """
    arr = list(arr)
    n = len(arr)
    if n <= 1:
        return arr
    buf = arr[:]
    width = 1
    while width < n:
        for lo in range(0, n, 2 * width):
            mid = min(lo + width, n)
            hi  = min(lo + 2 * width, n)
            buf[lo:hi] = arr[lo:hi]
            i, j, k = lo, mid, lo
            while i < mid and j < hi:
                if buf[i] <= buf[j]:
                    arr[k] = buf[i]; i += 1
                else:
                    arr[k] = buf[j]; j += 1
                k += 1
            while i < mid:
                arr[k] = buf[i]; i += 1; k += 1
            while j < hi:
                arr[k] = buf[j]; j += 1; k += 1
        width *= 2
    return arr


# ---------------------------------------------------------------------------
# Variant 3: Timsort-inspired — natural run detection + insertion sort base
# ---------------------------------------------------------------------------

def _insertion_sort_slice(arr: list, lo: int, hi: int) -> None:
    """In-place insertion sort on arr[lo:hi]."""
    for i in range(lo + 1, hi):
        key = arr[i]
        j = i
        while j > lo and arr[j - 1] > key:
            arr[j] = arr[j - 1]; j -= 1
        arr[j] = key


def _find_run(arr: list, lo: int, hi: int) -> int:
    """
    Find a natural run starting at lo, return its end index (exclusive).
    Reverses descending runs in-place to make them ascending.
    """
    if lo + 1 >= hi:
        return hi
    if arr[lo] <= arr[lo + 1]:
        # Ascending run
        end = lo + 2
        while end < hi and arr[end - 1] <= arr[end]:
            end += 1
    else:
        # Descending run — reverse it
        end = lo + 2
        while end < hi and arr[end - 1] > arr[end]:
            end += 1
        arr[lo:end] = arr[lo:end][::-1]
    return end


def merge_sort_timsort(arr: list) -> list:
    """
    Timsort-inspired: detect natural runs, sort small runs with insertion sort,
    merge runs bottom-up. Adaptive: O(n) on sorted/nearly-sorted input.

    Not the full CPython Timsort (no galloping, no run-length stack with
    merge-collapse rules) — this shows the core ideas.

    Examples:
    >>> merge_sort_timsort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> merge_sort_timsort([])
    []
    >>> merge_sort_timsort([-2, -5, -45])
    [-45, -5, -2]
    >>> merge_sort_timsort([4, 3, 2, 1])
    [1, 2, 3, 4]
    >>> merge_sort_timsort([1, 2, 3, 4])
    [1, 2, 3, 4]
    """
    arr = list(arr)
    n = len(arr)
    if n <= 1:
        return arr

    # Step 1: find/extend runs to MIN_RUN using insertion sort
    runs = []
    lo = 0
    while lo < n:
        run_end = _find_run(arr, lo, n)
        # Extend short runs to MIN_RUN with insertion sort
        run_end = max(run_end, min(lo + MIN_RUN, n))
        _insertion_sort_slice(arr, lo, run_end)
        runs.append((lo, run_end))
        lo = run_end

    # Step 2: merge runs pairwise until one run remains
    while len(runs) > 1:
        new_runs = []
        for i in range(0, len(runs), 2):
            if i + 1 < len(runs):
                lo1, hi1 = runs[i]
                lo2, hi2 = runs[i + 1]
                # Merge arr[lo1:hi1] and arr[lo2:hi2] (contiguous)
                merged = _merge(arr[lo1:hi1], arr[lo2:hi2])
                arr[lo1:hi2] = merged
                new_runs.append((lo1, hi2))
            else:
                new_runs.append(runs[i])
        runs = new_runs

    return arr


# ---------------------------------------------------------------------------
# Reference: original with pop(0) bug
# ---------------------------------------------------------------------------

def _merge_sort_original(arr: list) -> list:
    def merge(left, right):
        result = []
        while left and right:
            result.append(left.pop(0) if left[0] <= right[0] else right.pop(0))
        result.extend(left)
        result.extend(right)
        return result
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    return merge(_merge_sort_original(arr[:mid]), _merge_sort_original(arr[mid:]))


def benchmark() -> None:
    import copy
    import random
    import timeit

    random.seed(42)

    print("pop(0) bug: list.pop(0) is O(n) — merge becomes O(n^2)\n")

    datasets = {
        "random":        lambda n: [random.randint(0, 9999) for _ in range(n)],
        "reversed":      lambda n: list(range(n, 0, -1)),
        "sorted":        lambda n: list(range(n)),
        "nearly sorted": lambda n: list(range(n - 5)) + [random.randint(0, n) for _ in range(5)],
    }

    # --- Scaling: show pop(0) divergence ---
    print("Scaling (random, seconds per run):")
    header = f"{'n':<7} {'pop0 (bug)':>11} {'index':>7} {'inplace':>8} {'timsort*':>9} {'sorted()':>9}"
    print(header)
    print("-" * len(header))
    for n in [200, 500, 1000, 3000, 5000]:
        data = [random.randint(0, 9999) for _ in range(n)]
        iters = max(3, 300 // n)
        t_o = timeit.timeit(lambda: _merge_sort_original(list(data)), number=iters)
        t_i = timeit.timeit(lambda: merge_sort_index(list(data)),     number=iters)
        t_b = timeit.timeit(lambda: merge_sort_inplace(list(data)),   number=iters)
        t_t = timeit.timeit(lambda: merge_sort_timsort(list(data)),   number=iters)
        t_s = timeit.timeit(lambda: sorted(data),                     number=iters)
        print(f"{n:<7} {t_o/iters:>11.4f} {t_i/iters:>7.4f} {t_b/iters:>8.4f} "
              f"{t_t/iters:>9.4f} {t_s/iters:>9.4f}")
    print("  * timsort here = simplified (no galloping/merge-collapse)")

    # --- Dataset variety (n=2000) ---
    print("\nDataset comparison (n=2000, time per run, seconds):")
    n = 2000
    header2 = f"{'Dataset':<16} {'index':>7} {'inplace':>8} {'timsort*':>9} {'sorted()':>9}"
    print(header2)
    print("-" * len(header2))
    for label, make_data in datasets.items():
        data = make_data(n)
        iters = 50
        t_i = timeit.timeit(lambda: merge_sort_index(list(data)),   number=iters)
        t_b = timeit.timeit(lambda: merge_sort_inplace(list(data)), number=iters)
        t_t = timeit.timeit(lambda: merge_sort_timsort(list(data)), number=iters)
        t_s = timeit.timeit(lambda: sorted(data),                   number=iters)
        print(f"{label:<16} {t_i/iters:>7.4f} {t_b/iters:>8.4f} {t_t/iters:>9.4f} {t_s/iters:>9.4f}")

    # --- Stability ---
    print("\nStability check:")
    data = [(2,'a'), (1,'b'), (2,'c'), (1,'d')]
    expected = sorted(data, key=lambda x: x[0])
    for name, fn in [("index", merge_sort_index), ("inplace", merge_sort_inplace),
                     ("timsort", merge_sort_timsort)]:
        r = fn(copy.copy(data))
        print(f"  {name:<9}: {r}  stable={r == expected}")


if __name__ == "__main__":
    benchmark()
