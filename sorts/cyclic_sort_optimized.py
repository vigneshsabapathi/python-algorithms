"""
Cyclic Sort pattern — interview extensions for interview prep.

Cyclic sort exploits a key invariant: if nums contains integers 1..n,
then value v belongs at index v-1. One pass swaps each element into its
correct index — O(n) time, O(1) space, no extra data structures.

The same idea powers a family of interview problems about arrays containing
values in a bounded range:
  LeetCode 268  — Missing Number
  LeetCode 448  — Find All Numbers Disappeared in an Array
  LeetCode 442  — Find All Duplicates in an Array
  LeetCode 41   — First Missing Positive
  LeetCode 287  — Find the Duplicate Number

All variants: O(n) time, O(1) space (output list excluded).
"""

from __future__ import annotations


def cyclic_sort_zero_indexed(nums: list[int]) -> list[int]:
    """
    Cyclic sort for arrays containing 0..n-1 (value v belongs at index v).

    >>> cyclic_sort_zero_indexed([2, 0, 1])
    [0, 1, 2]
    >>> cyclic_sort_zero_indexed([])
    []
    >>> cyclic_sort_zero_indexed([0])
    [0]
    >>> cyclic_sort_zero_indexed([4, 0, 3, 1, 2])
    [0, 1, 2, 3, 4]
    >>> cyclic_sort_zero_indexed([0, 1, 2, 3])
    [0, 1, 2, 3]
    """
    arr = list(nums)
    i = 0
    while i < len(arr):
        correct = arr[i]  # value v belongs at index v
        if correct < len(arr) and arr[i] != arr[correct]:
            arr[i], arr[correct] = arr[correct], arr[i]
        else:
            i += 1
    return arr


def find_missing_number(nums: list[int]) -> int:
    """
    Find the one missing integer from an array containing n-1 distinct
    integers from 1..n. O(n) time, O(1) space.
    LeetCode 268 variant.

    >>> find_missing_number([3, 1, 2])   # n=3, all of 1..3 present -> missing 4
    4
    >>> find_missing_number([3, 1, 4])   # n=3 elements, values 1..4 -> missing 2
    2
    >>> find_missing_number([2, 3, 4, 5])  # missing 1
    1
    >>> find_missing_number([1, 2, 3, 5])  # missing 4
    4
    >>> find_missing_number([1])           # n=1, only 1 present -> missing 2
    2
    """
    arr = list(nums)
    n = len(arr)

    # Place each number at its correct index (1-indexed: value v at index v-1)
    # Values outside 1..n are left in place; they mark the missing-number slot.
    i = 0
    while i < n:
        correct = arr[i] - 1
        if 0 <= correct < n and arr[i] != arr[correct]:
            arr[i], arr[correct] = arr[correct], arr[i]
        else:
            i += 1

    # First index where arr[i] != i+1 holds the missing number
    for i in range(n):
        if arr[i] != i + 1:
            return i + 1

    # All positions 1..n are filled -> missing number is n+1
    return n + 1


def find_all_missing_numbers(nums: list[int]) -> list[int]:
    """
    Find all integers missing from 1..n in an n-element array where each
    value is in [1, n] but some values appear twice and others are missing.
    O(n) time, O(1) extra space (output list excluded).
    LeetCode 448.

    >>> find_all_missing_numbers([4, 3, 2, 7, 8, 2, 3, 1])
    [5, 6]
    >>> find_all_missing_numbers([1, 1])
    [2]
    >>> find_all_missing_numbers([1, 2, 3])
    []
    >>> find_all_missing_numbers([2, 2])
    [1]
    """
    arr = list(nums)
    n = len(arr)
    i = 0
    while i < n:
        correct = arr[i] - 1
        if arr[i] != arr[correct]:  # avoid infinite loop on duplicates
            arr[i], arr[correct] = arr[correct], arr[i]
        else:
            i += 1
    return [i + 1 for i in range(n) if arr[i] != i + 1]


def find_all_duplicates(nums: list[int]) -> list[int]:
    """
    Find all integers that appear twice in an n-element array where each
    value is in [1, n]. O(n) time, O(1) extra space.
    LeetCode 442.

    >>> find_all_duplicates([4, 3, 2, 7, 8, 2, 3, 1])
    [3, 2]
    >>> find_all_duplicates([1, 1, 2])
    [1]
    >>> find_all_duplicates([1, 2, 3])
    []
    """
    arr = list(nums)
    n = len(arr)
    i = 0
    while i < n:
        correct = arr[i] - 1
        if arr[i] != arr[correct]:
            arr[i], arr[correct] = arr[correct], arr[i]
        else:
            i += 1
    return [arr[i] for i in range(n) if arr[i] != i + 1]


def first_missing_positive(nums: list[int]) -> int:
    """
    Find the smallest missing positive integer in an unsorted array that may
    contain any integers (negatives, zeros, duplicates, out-of-range values).
    O(n) time, O(1) space. LeetCode 41.

    Strategy: ignore values outside [1, n]; place valid values at index v-1.
    Then scan for the first index where arr[i] != i+1.

    >>> first_missing_positive([1, 2, 0])
    3
    >>> first_missing_positive([3, 4, -1, 1])
    2
    >>> first_missing_positive([7, 8, 9, 11, 12])
    1
    >>> first_missing_positive([1, 2, 3])
    4
    >>> first_missing_positive([])
    1
    """
    arr = list(nums)
    n = len(arr)
    i = 0
    while i < n:
        correct = arr[i] - 1
        # Only place values in range [1, n]; skip negatives/zeros/out-of-range
        if 0 <= correct < n and arr[i] != arr[correct]:
            arr[i], arr[correct] = arr[correct], arr[i]
        else:
            i += 1
    for i in range(n):
        if arr[i] != i + 1:
            return i + 1
    return n + 1


def benchmark() -> None:
    import random
    import timeit

    from sorts.cyclic_sort import cyclic_sort as orig

    random.seed(42)
    n_runs = 5_000

    print("Correctness checks:")
    tests = [
        ([3, 5, 2, 1, 4], [1, 2, 3, 4, 5]),
        ([1], [1]),
        ([], []),
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
    ]
    for inp, expected in tests:
        result = orig(list(inp))
        print(f"  cyclic_sort({inp}) = {result}  correct={result == expected}")

    print()
    print("Pattern extensions:")
    print(f"  find_missing_number([2,3,4,5])           = {find_missing_number([2,3,4,5])}")
    print(f"  find_all_missing([4,3,2,7,8,2,3,1])     = {find_all_missing_numbers([4,3,2,7,8,2,3,1])}")
    print(f"  find_all_duplicates([4,3,2,7,8,2,3,1])  = {find_all_duplicates([4,3,2,7,8,2,3,1])}")
    print(f"  first_missing_positive([3,4,-1,1])       = {first_missing_positive([3,4,-1,1])}")
    print(f"  first_missing_positive([7,8,9,11,12])    = {first_missing_positive([7,8,9,11,12])}")

    print()
    datasets = {
        "random 1..n n=200":  random.sample(range(1, 201), 200),
        "random 1..n n=1000": random.sample(range(1, 1001), 1000),
        "reversed    n=200":  list(range(200, 0, -1)),
    }
    hdr = f"{'Dataset':<26} {'cyclic O(n)':>13} {'sorted() O(nlogn)':>18}"
    print(hdr)
    print("-" * len(hdr))
    for label, data in datasets.items():
        tc = timeit.timeit(lambda d=data: orig(list(d)), number=n_runs)
        tq = timeit.timeit(lambda d=data: sorted(d), number=n_runs)
        print(f"{label:<26} {tc:>13.3f} {tq:>18.3f}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
