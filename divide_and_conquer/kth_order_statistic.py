"""
Kth Order Statistic — Quickselect (Divide and Conquer)

Find the kth smallest element in an unsorted array without fully sorting.

Average case: O(n) using randomised pivot.
Worst case: O(n^2) with bad pivots, O(n) guaranteed with median-of-medians.

Reference: https://github.com/TheAlgorithms/Python/blob/master/divide_and_conquer/kth_order_statistic.py
"""

from __future__ import annotations

import random


def kth_order_statistic(arr: list[int], k: int) -> int:
    """
    Find the kth smallest element (1-indexed) using randomised quickselect.

    >>> kth_order_statistic([3, 2, 1, 5, 4], 1)
    1
    >>> kth_order_statistic([3, 2, 1, 5, 4], 3)
    3
    >>> kth_order_statistic([3, 2, 1, 5, 4], 5)
    5
    >>> kth_order_statistic([7, 10, 4, 3, 20, 15], 3)
    7
    >>> kth_order_statistic([7, 10, 4, 3, 20, 15], 4)
    10
    >>> kth_order_statistic([1], 1)
    1
    """
    if k < 1 or k > len(arr):
        raise ValueError(f"k={k} out of range for array of length {len(arr)}")
    return _quickselect(arr[:], k - 1)  # convert to 0-indexed


def _quickselect(arr: list[int], k: int) -> int:
    """0-indexed quickselect."""
    if len(arr) == 1:
        return arr[0]

    pivot = arr[random.randint(0, len(arr) - 1)]
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]

    if k < len(less):
        return _quickselect(less, k)
    elif k < len(less) + len(equal):
        return pivot
    else:
        return _quickselect(greater, k - len(less) - len(equal))


def median_of_medians(arr: list[int], k: int) -> int:
    """
    Find the kth smallest element (1-indexed) with O(n) worst-case guarantee.
    Uses median-of-medians pivot selection.

    >>> median_of_medians([3, 2, 1, 5, 4], 1)
    1
    >>> median_of_medians([3, 2, 1, 5, 4], 3)
    3
    >>> median_of_medians([3, 2, 1, 5, 4], 5)
    5
    >>> median_of_medians([7, 10, 4, 3, 20, 15], 3)
    7
    """
    if k < 1 or k > len(arr):
        raise ValueError(f"k={k} out of range for array of length {len(arr)}")
    return _mom_select(arr[:], k - 1)


def _mom_select(arr: list[int], k: int) -> int:
    """0-indexed median-of-medians select."""
    if len(arr) <= 5:
        return sorted(arr)[k]

    # Split into groups of 5, find median of each
    medians = []
    for i in range(0, len(arr), 5):
        group = sorted(arr[i : i + 5])
        medians.append(group[len(group) // 2])

    # Recursively find median of medians
    pivot = _mom_select(medians, len(medians) // 2)

    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]

    if k < len(less):
        return _mom_select(less, k)
    elif k < len(less) + len(equal):
        return pivot
    else:
        return _mom_select(greater, k - len(less) - len(equal))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
