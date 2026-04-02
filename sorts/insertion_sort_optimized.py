"""
Insertion Sort — optimized variants for interview prep.

Insertion sort: O(n^2) worst/average, O(n) best (sorted input), stable,
adaptive, in-place. The practical O(n^2) sort — used as the base case in
Timsort (Python's sorted()) and introsort (C++ std::sort) for small subarrays.

Key insight: for n < 64, insertion sort beats merge sort and quicksort
because it has very small constants and no recursion overhead.

Variants:
  insertion_sort_binary: bisect.insort — O(n log n) comparisons, O(n^2) shifts
  shell_sort:            Ciura gaps — practical O(n^{1.3}) with tiny constants
  timsort_run:           insertion sort as a Timsort inner loop — sorts a slice
                         of an array in-place for use in merge-based algorithms
"""

from __future__ import annotations

import bisect
from typing import Any


# ---------------------------------------------------------------------------
# Variant 1: Binary insertion sort (bisect.insort)
# ---------------------------------------------------------------------------

def insertion_sort_binary(collection: list) -> list:
    """
    Binary insertion sort: uses bisect.insort to find the insertion position
    in O(log n) comparisons, then shifts via list slice assignment in O(n).

    Total: O(n log n) comparisons (vs O(n^2) for linear), O(n^2) shifts.
    Advantage: when comparisons are expensive (custom __lt__, DB calls).
    For plain int/str, shifts dominate and wall-clock is comparable to linear.

    bisect.insort is implemented in C — slice shifts are also C-level,
    making this the fastest pure-sort for int/str at small n.

    Examples:
    >>> insertion_sort_binary([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> insertion_sort_binary([])
    []
    >>> insertion_sort_binary([-2, -5, -45])
    [-45, -5, -2]
    >>> insertion_sort_binary([4, 3, 2, 1])
    [1, 2, 3, 4]
    >>> insertion_sort_binary(['d', 'a', 'b', 'e', 'c'])
    ['a', 'b', 'c', 'd', 'e']
    """
    result = []
    for item in collection:
        bisect.insort(result, item)
    return result


# ---------------------------------------------------------------------------
# Variant 2: Shell sort (Ciura gap sequence)
# ---------------------------------------------------------------------------

# Ciura's empirically optimal gaps (2001) — best known for n up to ~4500
CIURA_GAPS = [701, 301, 132, 57, 23, 10, 4, 1]


def shell_sort(collection: list) -> list:
    """
    Shell sort with Ciura gap sequence.

    Shell sort generalizes insertion sort: instead of shifting by 1, shift by
    gap h. Reduces O(n^2) inversions to O(n^{1.3}) with Ciura gaps.
    After all gaps, the final pass (gap=1) is a standard insertion sort on a
    nearly-sorted array — nearly O(n).

    With Ciura gaps, empirical complexity is approximately O(n^{1.3}), beating
    O(n log^2 n) for Hibbard/Sedgewick gaps in practice.

    Examples:
    >>> shell_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> shell_sort([])
    []
    >>> shell_sort([-2, -5, -45])
    [-45, -5, -2]
    >>> shell_sort([4, 3, 2, 1])
    [1, 2, 3, 4]
    >>> shell_sort(['d', 'a', 'b', 'e', 'c'])
    ['a', 'b', 'c', 'd', 'e']
    """
    arr = list(collection)
    n = len(arr)
    for gap in CIURA_GAPS:
        if gap >= n:
            continue
        for i in range(gap, n):
            key = arr[i]
            j = i
            while j >= gap and arr[j - gap] > key:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = key
    return arr


# ---------------------------------------------------------------------------
# Variant 3: Timsort-style run insertion sort (in-place on a slice)
# ---------------------------------------------------------------------------

def insertion_sort_inplace(arr: list, lo: int = 0, hi: int | None = None) -> None:
    """
    In-place insertion sort on arr[lo:hi] (hi exclusive).
    Used as the base case in Timsort: sorts small runs of size < MIN_RUN (32-64).

    Operates directly on the array slice — no copies, no return value.

    Examples:
    >>> a = [5, 3, 1, 4, 2]
    >>> insertion_sort_inplace(a)
    >>> a
    [1, 2, 3, 4, 5]

    >>> a = [5, 3, 1, 4, 2]; insertion_sort_inplace(a, 1, 4)
    >>> a
    [5, 1, 3, 4, 2]

    >>> a = []; insertion_sort_inplace(a)
    >>> a
    []
    """
    if hi is None:
        hi = len(arr)
    for i in range(lo + 1, hi):
        key = arr[i]
        j = i
        while j > lo and arr[j - 1] > key:
            arr[j] = arr[j - 1]
            j -= 1
        arr[j] = key


# ---------------------------------------------------------------------------
# Reference: original linear insertion sort
# ---------------------------------------------------------------------------

def _insertion_sort_linear(collection: list) -> list:
    arr = list(collection)
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def benchmark() -> None:
    import copy
    import random
    import timeit

    random.seed(42)
    iters = 3000

    print("=== Small n benchmark (where insertion sort is used in practice) ===\n")

    for n in [10, 32, 64, 128]:
        data_rand = [random.randint(0, 999) for _ in range(n)]
        data_rev  = list(range(n, 0, -1))
        data_sort = list(range(n))

        print(f"n={n}")
        header = f"  {'dataset':<14} {'linear':>8} {'binary':>8} {'shell':>8} {'sorted()':>9}"
        print(header)
        print("  " + "-" * (len(header) - 2))

        for label, data in [("random", data_rand), ("reversed", data_rev), ("sorted", data_sort)]:
            t_l = timeit.timeit(lambda: _insertion_sort_linear(data), number=iters)
            t_b = timeit.timeit(lambda: insertion_sort_binary(data),  number=iters)
            t_s = timeit.timeit(lambda: shell_sort(data),             number=iters)
            t_p = timeit.timeit(lambda: sorted(data),                 number=iters)
            print(f"  {label:<14} {t_l:>8.3f} {t_b:>8.3f} {t_s:>8.3f} {t_p:>9.3f}")
        print()

    # --- Large n: shell sort vs insertion ---
    print("=== Large n: shell sort vs insertion sort ===\n")
    header2 = f"{'n':<8} {'linear':>8} {'shell':>8} {'sorted()':>9}"
    print(header2)
    print("-" * len(header2))
    for n in [500, 1000, 5000]:
        data = [random.randint(0, 9999) for _ in range(n)]
        reps = max(1, 500_000 // (n * n))  # scale down for large n
        t_l = timeit.timeit(lambda: _insertion_sort_linear(data), number=reps)
        t_s = timeit.timeit(lambda: shell_sort(data),             number=reps)
        t_p = timeit.timeit(lambda: sorted(data),                 number=reps)
        print(f"{n:<8} {t_l:>8.3f} {t_s:>8.3f} {t_p:>9.3f}")

    # --- Stability check ---
    print("\n=== Stability check ===")
    data = [(2, 'a'), (1, 'b'), (2, 'c'), (1, 'd')]
    expected = sorted(data, key=lambda x: x[0])
    r_lin = _insertion_sort_linear(copy.copy(data))
    r_bin = insertion_sort_binary(data)
    r_sh  = shell_sort(data)
    print(f"Input:    {data}")
    print(f"Expected: {expected}")
    print(f"linear:   {r_lin}  stable={r_lin == expected}")
    print(f"binary:   {r_bin}  stable={r_bin == expected}")
    print(f"shell:    {r_sh}   stable={r_sh == expected}")

    # --- Write count: insertion vs gnome ---
    print("\n=== Write counts on reversed n=20 ===")
    rev = list(range(20, 0, -1))

    def ins_writes(data):
        arr, count = list(data), 0
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]; count += 1; j -= 1
            arr[j + 1] = key; count += 1
        return count

    def gnome_writes(data):
        arr, count = list(data), 0
        i = 1
        while i < len(arr):
            if arr[i - 1] <= arr[i]:
                i += 1
            else:
                arr[i - 1], arr[i] = arr[i], arr[i - 1]
                count += 2; i -= 1
                if i == 0: i = 1
        return count

    iw = ins_writes(rev)
    gw = gnome_writes(rev)
    print(f"  insertion sort: {iw} writes (shifts + placement)")
    print(f"  gnome sort:     {gw} writes (swap = 2 per step)")
    print(f"  gnome / insertion ratio: {gw / iw:.1f}x")


if __name__ == "__main__":
    benchmark()
