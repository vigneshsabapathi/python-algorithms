"""
Optimized Dutch National Flag variants for interview prep.

The DNF algorithm (Dijkstra, 1976) partitions an array around a pivot into
three regions: < pivot | == pivot | > pivot — in a single O(n) pass with O(1)
space using three pointers (low, mid, high).

This is the foundation of:
  LeetCode 75  — Sort Colors (exact DNF on {0,1,2})
  3-way quicksort — use DNF as the partition step to handle duplicates in O(n)
  Generic 3-region partition — any pivot value, any comparable type

Variants:
1. sort_colors      — clean LeetCode 75 solution (same algorithm, no hardcoded colors)
2. three_way_partition — generalised: partition any list around an arbitrary pivot
3. three_way_quicksort — full sort using DNF partition recursively; O(n log n) avg,
                         O(n) for arrays of few distinct values
"""

from __future__ import annotations


def sort_colors(nums: list[int]) -> list[int]:
    """
    LeetCode 75: Sort Colors.
    Sort an array containing only 0, 1, 2 in-place in one pass, O(1) space.
    Same three-pointer DNF algorithm; no hardcoded color constants.

    Invariant at all times:
      nums[0..low-1]  = 0  (red region)
      nums[low..mid-1] = 1  (white region)
      nums[mid..high]  = unprocessed
      nums[high+1..n-1] = 2  (blue region)

    >>> sort_colors([2, 0, 2, 1, 1, 0])
    [0, 0, 1, 1, 2, 2]
    >>> sort_colors([2, 0, 1])
    [0, 1, 2]
    >>> sort_colors([0])
    [0]
    >>> sort_colors([])
    []
    >>> sort_colors([1, 1, 1])
    [1, 1, 1]
    >>> sort_colors([2, 2, 0, 0])
    [0, 0, 2, 2]
    """
    arr = list(nums)
    low = mid = 0
    high = len(arr) - 1

    while mid <= high:
        if arr[mid] == 0:
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] == 1:
            mid += 1
        else:  # arr[mid] == 2
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1
            # do NOT increment mid: swapped-in element not yet examined

    return arr


def three_way_partition(arr: list, pivot) -> list:
    """
    Generalised DNF partition: rearrange arr into [< pivot | == pivot | > pivot].
    Works on any list with comparable elements and any pivot value.
    O(n) time, O(1) space, single pass.

    >>> three_way_partition([3, 1, 4, 1, 5, 9, 2, 6, 5, 3], 3)
    [1, 1, 2, 3, 3, 9, 6, 5, 5, 4]
    >>> three_way_partition([1, 1, 1, 1], 1)
    [1, 1, 1, 1]
    >>> three_way_partition([], 5)
    []
    >>> three_way_partition([2, 1, 3], 2)
    [1, 2, 3]
    >>> three_way_partition(['b', 'a', 'c', 'a'], 'b')
    ['a', 'a', 'b', 'c']
    """
    a = list(arr)
    low = mid = 0
    high = len(a) - 1

    while mid <= high:
        if a[mid] < pivot:
            a[low], a[mid] = a[mid], a[low]
            low += 1
            mid += 1
        elif a[mid] == pivot:
            mid += 1
        else:
            a[mid], a[high] = a[high], a[mid]
            high -= 1

    return a


def three_way_quicksort(arr: list) -> list:
    """
    Full in-place sort using DNF as the partition step.
    Picks the median of first/mid/last as pivot to avoid O(n^2) on sorted input.
    O(n log n) average; O(n) for arrays with few distinct values (all-equal = O(n)).

    >>> three_way_quicksort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
    [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
    >>> three_way_quicksort([])
    []
    >>> three_way_quicksort([1])
    [1]
    >>> three_way_quicksort([2, 1, 0, 0, 1, 2])
    [0, 0, 1, 1, 2, 2]
    >>> three_way_quicksort([4, 3, 2, 1])
    [1, 2, 3, 4]
    >>> three_way_quicksort([3, 3, 3, 3])
    [3, 3, 3, 3]
    """

    def _median3(a: list, lo: int, hi: int) -> object:
        mid = (lo + hi) // 2
        if a[lo] > a[mid]:
            a[lo], a[mid] = a[mid], a[lo]
        if a[lo] > a[hi]:
            a[lo], a[hi] = a[hi], a[lo]
        if a[mid] > a[hi]:
            a[mid], a[hi] = a[hi], a[mid]
        return a[mid]

    def _sort(a: list, lo: int, hi: int) -> None:
        if lo >= hi:
            return
        pivot = _median3(a, lo, hi)
        low = mid = lo
        high = hi
        while mid <= high:
            if a[mid] < pivot:
                a[low], a[mid] = a[mid], a[low]
                low += 1
                mid += 1
            elif a[mid] == pivot:
                mid += 1
            else:
                a[mid], a[high] = a[high], a[mid]
                high -= 1
        # a[lo..low-1] < pivot, a[low..mid-1] == pivot, a[mid..hi] > pivot
        _sort(a, lo, low - 1)
        _sort(a, mid, hi)

    result = list(arr)
    _sort(result, 0, len(result) - 1)
    return result


def benchmark() -> None:
    import random
    import timeit

    from sorts.dutch_national_flag_sort import dutch_national_flag_sort as orig

    random.seed(42)
    n_runs = 5_000

    # ── DNF on {0,1,2} arrays ───────────────────────────────────────────
    print("DNF {0,1,2} arrays (time in seconds):")
    dnf_datasets = {
        "random {0,1,2} n=200":  random.choices([0, 1, 2], k=200),
        "random {0,1,2} n=1000": random.choices([0, 1, 2], k=1000),
        "all same value  n=200":  [1] * 200,
    }
    hdr = f"{'Dataset':<28} {'original':>10} {'sort_colors':>12} {'sorted()':>10}"
    print(hdr)
    print("-" * len(hdr))
    for label, data in dnf_datasets.items():
        to = timeit.timeit(lambda d=data: orig(list(d)), number=n_runs)
        ts = timeit.timeit(lambda d=data: sort_colors(d), number=n_runs)
        tq = timeit.timeit(lambda d=data: sorted(d), number=n_runs)
        print(f"{label:<28} {to:>10.3f} {ts:>12.3f} {tq:>10.3f}")

    # ── 3-way quicksort vs sorted() on general arrays ───────────────────
    print()
    print("3-way quicksort vs sorted() (general arrays):")
    gen_datasets = {
        "random n=200":          random.sample(range(-500, 500), 200),
        "few distinct n=200":    random.choices(range(5), k=200),
        "all equal n=200":       [7] * 200,
        "reversed n=200":        list(range(200, 0, -1)),
    }
    hdr2 = f"{'Dataset':<26} {'3-way QS':>10} {'sorted()':>10}"
    print(hdr2)
    print("-" * len(hdr2))
    for label, data in gen_datasets.items():
        tq3 = timeit.timeit(lambda d=data: three_way_quicksort(d), number=n_runs)
        ts  = timeit.timeit(lambda d=data: sorted(d), number=n_runs)
        print(f"{label:<26} {tq3:>10.3f} {ts:>10.3f}")

    print()
    print("Correctness checks:")

    sc_in = [2, 0, 1]
    sc_out = sort_colors(sc_in)
    print(f"  sort_colors:            {sc_out}  correct={sc_out == sorted(sc_in)}")

    # three_way_partition: verify partition property (< pivot | == pivot | > pivot)
    p_in, pivot = [3, 1, 4, 1, 5, 9, 2], 3
    p_out = three_way_partition(list(p_in), pivot)
    lt = [x for x in p_out if x < pivot]
    eq = [x for x in p_out if x == pivot]
    gt = [x for x in p_out if x > pivot]
    partition_ok = (
        sorted(p_out) == sorted(p_in)   # same elements
        and p_out == lt + eq + gt        # correct region order
    )
    print(f"  three_way_partition:    {p_out}  partition_correct={partition_ok}")

    qs_in = [3, 1, 4, 1, 5, 9, 2]
    qs_out = three_way_quicksort(list(qs_in))
    print(f"  three_way_quicksort:    {qs_out}  correct={qs_out == sorted(qs_in)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
