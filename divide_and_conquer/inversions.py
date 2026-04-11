"""
Count Inversions — Divide and Conquer (Modified Merge Sort)

An inversion is a pair (i, j) where i < j but arr[i] > arr[j].
Brute force: O(n^2). Modified merge sort: O(n log n).

The key insight: during merge, when we pick from the right half,
every remaining element in the left half forms an inversion with it.

Reference: https://github.com/TheAlgorithms/Python/blob/master/divide_and_conquer/inversions.py
"""

from __future__ import annotations


def count_inversions(arr: list[int]) -> tuple[int, list[int]]:
    """
    Count inversions using modified merge sort.
    Returns (inversion_count, sorted_array).

    >>> count_inversions([2, 4, 1, 3, 5])
    (3, [1, 2, 3, 4, 5])
    >>> count_inversions([1, 2, 3, 4, 5])
    (0, [1, 2, 3, 4, 5])
    >>> count_inversions([5, 4, 3, 2, 1])
    (10, [1, 2, 3, 4, 5])
    >>> count_inversions([1, 20, 6, 4, 5])
    (5, [1, 4, 5, 6, 20])
    >>> count_inversions([])
    (0, [])
    >>> count_inversions([1])
    (0, [1])
    """
    if len(arr) <= 1:
        return 0, arr[:]

    mid = len(arr) // 2
    left_inv, left = count_inversions(arr[:mid])
    right_inv, right = count_inversions(arr[mid:])
    merge_inv, merged = _merge_count(left, right)

    return left_inv + right_inv + merge_inv, merged


def _merge_count(left: list[int], right: list[int]) -> tuple[int, list[int]]:
    """
    Merge two sorted lists and count split inversions.

    >>> _merge_count([1, 3, 5], [2, 4, 6])
    (3, [1, 2, 3, 4, 5, 6])
    """
    result: list[int] = []
    inversions = 0
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            inversions += len(left) - i  # all remaining left elements are inversions
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return inversions, result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
