"""
Merge Sort — Classic Divide and Conquer Sorting

Split array in half, recursively sort each half, merge sorted halves.

Time: O(n log n) always   Space: O(n) for merge buffer
Stable sort — equal elements preserve relative order.

Reference: https://github.com/TheAlgorithms/Python/blob/master/divide_and_conquer/mergesort.py
"""

from __future__ import annotations


def merge_sort(arr: list) -> list:
    """
    Sort array using merge sort.

    >>> merge_sort([38, 27, 43, 3, 9, 82, 10])
    [3, 9, 10, 27, 38, 43, 82]
    >>> merge_sort([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]
    >>> merge_sort([1, 2, 3, 4, 5])
    [1, 2, 3, 4, 5]
    >>> merge_sort([])
    []
    >>> merge_sort([1])
    [1]
    >>> merge_sort([3, 3, 1, 1, 2, 2])
    [1, 1, 2, 2, 3, 3]
    """
    if len(arr) <= 1:
        return arr[:]

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left: list, right: list) -> list:
    """
    Merge two sorted lists into one sorted list.

    >>> _merge([1, 3, 5], [2, 4, 6])
    [1, 2, 3, 4, 5, 6]
    """
    result: list = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
