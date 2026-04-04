#!/usr/bin/env python3

"""
Pure Python implementations of binary search algorithms.

Includes:
  - bisect_left / bisect_right  — lower/upper bound (mirrors stdlib bisect)
  - insort_left / insort_right  — sorted insertion (mirrors stdlib bisect)
  - binary_search               — iterative, returns index or -1
  - binary_search_std_lib       — wrapper around stdlib bisect
  - binary_search_with_duplicates — returns list of all matching indices
  - binary_search_by_recursion  — recursive variant
  - exponential_search          — doubling probe + binary search (good for
                                  unbounded / infinite sorted sequences)

For doctests run:
    python3 -m doctest -v binary_search.py

For manual testing run:
    python3 binary_search.py
"""

import bisect
from itertools import pairwise


def bisect_left(
    sorted_collection: list[int], item: int, lo: int = 0, hi: int = -1
) -> int:
    """
    Locates the first position where item can be inserted to keep sorted order.
    Equivalent to stdlib bisect.bisect_left.

    Returns index i such that all values in sorted_collection[lo:i] are < item
    and all values in sorted_collection[i:hi] are >= item.

    Examples:
    >>> bisect_left([0, 5, 7, 10, 15], 0)
    0
    >>> bisect_left([0, 5, 7, 10, 15], 6)
    2
    >>> bisect_left([0, 5, 7, 10, 15], 20)
    5
    >>> bisect_left([0, 5, 7, 10, 15], 15, 1, 3)
    3
    >>> bisect_left([0, 5, 7, 10, 15], 6, 2)
    2
    """
    if hi < 0:
        hi = len(sorted_collection)

    while lo < hi:
        mid = lo + (hi - lo) // 2
        if sorted_collection[mid] < item:
            lo = mid + 1
        else:
            hi = mid

    return lo


def bisect_right(
    sorted_collection: list[int], item: int, lo: int = 0, hi: int = -1
) -> int:
    """
    Locates the first position after all occurrences of item in sorted order.
    Equivalent to stdlib bisect.bisect_right.

    Returns index i such that all values in sorted_collection[lo:i] are <= item
    and all values in sorted_collection[i:hi] are > item.

    Examples:
    >>> bisect_right([0, 5, 7, 10, 15], 0)
    1
    >>> bisect_right([0, 5, 7, 10, 15], 15)
    5
    >>> bisect_right([0, 5, 7, 10, 15], 6)
    2
    >>> bisect_right([0, 5, 7, 10, 15], 15, 1, 3)
    3
    >>> bisect_right([0, 5, 7, 10, 15], 6, 2)
    2
    """
    if hi < 0:
        hi = len(sorted_collection)

    while lo < hi:
        mid = lo + (hi - lo) // 2
        if sorted_collection[mid] <= item:
            lo = mid + 1
        else:
            hi = mid

    return lo


def insort_left(
    sorted_collection: list[int], item: int, lo: int = 0, hi: int = -1
) -> None:
    """
    Insert item into sorted_collection, before any existing equal values.
    Equivalent to stdlib bisect.insort_left.

    Examples:
    >>> sorted_collection = [0, 5, 7, 10, 15]
    >>> insort_left(sorted_collection, 6)
    >>> sorted_collection
    [0, 5, 6, 7, 10, 15]
    >>> sorted_collection = [(0, 0), (5, 5), (7, 7), (10, 10), (15, 15)]
    >>> item = (5, 5)
    >>> insort_left(sorted_collection, item)
    >>> sorted_collection
    [(0, 0), (5, 5), (5, 5), (7, 7), (10, 10), (15, 15)]
    >>> item is sorted_collection[1]
    True
    >>> item is sorted_collection[2]
    False
    >>> sorted_collection = [0, 5, 7, 10, 15]
    >>> insort_left(sorted_collection, 20)
    >>> sorted_collection
    [0, 5, 7, 10, 15, 20]
    >>> sorted_collection = [0, 5, 7, 10, 15]
    >>> insort_left(sorted_collection, 15, 1, 3)
    >>> sorted_collection
    [0, 5, 7, 15, 10, 15]
    """
    sorted_collection.insert(bisect_left(sorted_collection, item, lo, hi), item)


def insort_right(
    sorted_collection: list[int], item: int, lo: int = 0, hi: int = -1
) -> None:
    """
    Insert item into sorted_collection, after any existing equal values.
    Equivalent to stdlib bisect.insort_right.

    Examples:
    >>> sorted_collection = [0, 5, 7, 10, 15]
    >>> insort_right(sorted_collection, 6)
    >>> sorted_collection
    [0, 5, 6, 7, 10, 15]
    >>> sorted_collection = [(0, 0), (5, 5), (7, 7), (10, 10), (15, 15)]
    >>> item = (5, 5)
    >>> insort_right(sorted_collection, item)
    >>> sorted_collection
    [(0, 0), (5, 5), (5, 5), (7, 7), (10, 10), (15, 15)]
    >>> item is sorted_collection[1]
    False
    >>> item is sorted_collection[2]
    True
    >>> sorted_collection = [0, 5, 7, 10, 15]
    >>> insort_right(sorted_collection, 20)
    >>> sorted_collection
    [0, 5, 7, 10, 15, 20]
    >>> sorted_collection = [0, 5, 7, 10, 15]
    >>> insort_right(sorted_collection, 15, 1, 3)
    >>> sorted_collection
    [0, 5, 7, 15, 10, 15]
    """
    sorted_collection.insert(bisect_right(sorted_collection, item, lo, hi), item)


def binary_search(sorted_collection: list[int], item: int) -> int:
    """Iterative binary search — returns index of item or -1 if not found.

    The collection must be ascending-sorted; otherwise the result is unpredictable.
    Validates sort order at call time using pairwise comparison (O(n) overhead).

    Examples:
    >>> binary_search([0, 5, 7, 10, 15], 0)
    0
    >>> binary_search([0, 5, 7, 10, 15], 15)
    4
    >>> binary_search([0, 5, 7, 10, 15], 5)
    1
    >>> binary_search([0, 5, 7, 10, 15], 6)
    -1
    """
    if any(a > b for a, b in pairwise(sorted_collection)):
        raise ValueError("sorted_collection must be sorted in ascending order")
    left = 0
    right = len(sorted_collection) - 1

    while left <= right:
        midpoint = left + (right - left) // 2
        current_item = sorted_collection[midpoint]
        if current_item == item:
            return midpoint
        elif item < current_item:
            right = midpoint - 1
        else:
            left = midpoint + 1
    return -1


def binary_search_std_lib(sorted_collection: list[int], item: int) -> int:
    """Binary search using Python's stdlib bisect module.

    Returns index of item or -1 if not found.

    Examples:
    >>> binary_search_std_lib([0, 5, 7, 10, 15], 0)
    0
    >>> binary_search_std_lib([0, 5, 7, 10, 15], 15)
    4
    >>> binary_search_std_lib([0, 5, 7, 10, 15], 5)
    1
    >>> binary_search_std_lib([0, 5, 7, 10, 15], 6)
    -1
    """
    if list(sorted_collection) != sorted(sorted_collection):
        raise ValueError("sorted_collection must be sorted in ascending order")
    index = bisect.bisect_left(sorted_collection, item)
    if index != len(sorted_collection) and sorted_collection[index] == item:
        return index
    return -1


def binary_search_with_duplicates(
    sorted_collection: list[int], item: int
) -> list[int]:
    """Binary search that returns all indices where item occurs.

    Uses lower_bound and upper_bound (equivalent to bisect_left / bisect_right)
    to locate the full contiguous range of matching elements in O(log n).

    Returns an empty list if item is not found.

    Examples:
    >>> binary_search_with_duplicates([0, 5, 7, 10, 15], 0)
    [0]
    >>> binary_search_with_duplicates([0, 5, 7, 10, 15], 15)
    [4]
    >>> binary_search_with_duplicates([1, 2, 2, 2, 3], 2)
    [1, 2, 3]
    >>> binary_search_with_duplicates([1, 2, 2, 2, 3], 4)
    []
    """
    if list(sorted_collection) != sorted(sorted_collection):
        raise ValueError("sorted_collection must be sorted in ascending order")

    def lower_bound(arr: list[int], val: int) -> int:
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if arr[mid] < val:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def upper_bound(arr: list[int], val: int) -> int:
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if arr[mid] <= val:
                lo = mid + 1
            else:
                hi = mid
        return lo

    lo = lower_bound(sorted_collection, item)
    hi = upper_bound(sorted_collection, item)

    if lo == len(sorted_collection) or sorted_collection[lo] != item:
        return []
    return list(range(lo, hi))


def binary_search_by_recursion(
    sorted_collection: list[int], item: int, left: int = 0, right: int = -1
) -> int:
    """Recursive binary search — returns index of item or -1 if not found.

    First call should use left=0 and right=len(sorted_collection)-1.
    Right defaults to -1 which triggers automatic initialisation.

    Examples:
    >>> binary_search_by_recursion([0, 5, 7, 10, 15], 0, 0, 4)
    0
    >>> binary_search_by_recursion([0, 5, 7, 10, 15], 15, 0, 4)
    4
    >>> binary_search_by_recursion([0, 5, 7, 10, 15], 5, 0, 4)
    1
    >>> binary_search_by_recursion([0, 5, 7, 10, 15], 6, 0, 4)
    -1
    """
    if right < 0:
        right = len(sorted_collection) - 1
    if list(sorted_collection) != sorted(sorted_collection):
        raise ValueError("sorted_collection must be sorted in ascending order")
    if right < left:
        return -1

    midpoint = left + (right - left) // 2

    if sorted_collection[midpoint] == item:
        return midpoint
    elif sorted_collection[midpoint] > item:
        return binary_search_by_recursion(sorted_collection, item, left, midpoint - 1)
    else:
        return binary_search_by_recursion(sorted_collection, item, midpoint + 1, right)


def exponential_search(sorted_collection: list[int], item: int) -> int:
    """Exponential search — doubles probe bound until item is bracketed, then
    applies binary search in that window.

    Useful for unbounded or very large sorted sequences where the item is likely
    near the beginning: best case O(log i) where i is the item's index.
    Worst case O(log n) — same as binary search.

    Examples:
    >>> exponential_search([0, 5, 7, 10, 15], 0)
    0
    >>> exponential_search([0, 5, 7, 10, 15], 15)
    4
    >>> exponential_search([0, 5, 7, 10, 15], 5)
    1
    >>> exponential_search([0, 5, 7, 10, 15], 6)
    -1
    """
    if list(sorted_collection) != sorted(sorted_collection):
        raise ValueError("sorted_collection must be sorted in ascending order")
    bound = 1
    while bound < len(sorted_collection) and sorted_collection[bound] < item:
        bound *= 2
    left = bound // 2
    right = min(bound, len(sorted_collection) - 1)
    return binary_search_by_recursion(
        sorted_collection=sorted_collection, item=item, left=left, right=right
    )


# Ordered fastest → slowest (approximate, depends on input)
searches = (
    binary_search_std_lib,
    binary_search,
    exponential_search,
    binary_search_by_recursion,
)


if __name__ == "__main__":
    import doctest
    import timeit

    doctest.testmod(verbose=True)

    collection = [0, 5, 7, 10, 15]
    for search in searches:
        name = f"{search.__name__:>26}"
        print(f"{name}: {search(collection, 10) = }")  # type: ignore[operator]

    print("\nBenchmarks...")
    setup = "collection = list(range(1000))"
    for search in searches:
        name = search.__name__
        t = timeit.timeit(
            f"{name}(collection, 500)",
            setup=setup,
            number=5_000,
            globals=globals(),
        )
        print(f"{name:>26}: {t:.4f}s")
