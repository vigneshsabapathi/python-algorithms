"""
Maximum Subarray — Divide and Conquer (Kadane comparison)

Find the contiguous subarray with the largest sum.

D&C approach: split array, max subarray is either:
  (a) entirely in left half,
  (b) entirely in right half, or
  (c) crosses the midpoint.

Time: O(n log n) for D&C, O(n) for Kadane's.

Reference: https://github.com/TheAlgorithms/Python/blob/master/divide_and_conquer/max_subarray.py
"""

from __future__ import annotations


def max_subarray(arr: list[int | float]) -> tuple[int, int, int | float]:
    """
    Find the maximum subarray using divide and conquer.
    Returns (left_index, right_index, max_sum).

    >>> max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    (3, 6, 6)
    >>> max_subarray([1, 2, 3, 4, 5])
    (0, 4, 15)
    >>> max_subarray([-1, -2, -3])
    (0, 0, -1)
    >>> max_subarray([5])
    (0, 0, 5)
    >>> max_subarray([])
    Traceback (most recent call last):
        ...
    ValueError: Array must not be empty
    """
    if not arr:
        raise ValueError("Array must not be empty")
    return _max_subarray_rec(arr, 0, len(arr) - 1)


def _max_crossing_subarray(
    arr: list[int | float], lo: int, mid: int, hi: int
) -> tuple[int, int, int | float]:
    """
    Find max subarray crossing the midpoint.

    >>> _max_crossing_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4], 0, 4, 8)
    (3, 6, 6)
    """
    # Extend left from mid
    left_sum = float("-inf")
    total = 0
    max_left = mid
    for i in range(mid, lo - 1, -1):
        total += arr[i]
        if total > left_sum:
            left_sum = total
            max_left = i

    # Extend right from mid+1
    right_sum = float("-inf")
    total = 0
    max_right = mid + 1
    for j in range(mid + 1, hi + 1):
        total += arr[j]
        if total > right_sum:
            right_sum = total
            max_right = j

    return max_left, max_right, left_sum + right_sum


def _max_subarray_rec(
    arr: list[int | float], lo: int, hi: int
) -> tuple[int, int, int | float]:
    if lo == hi:
        return lo, hi, arr[lo]

    mid = (lo + hi) // 2
    left_lo, left_hi, left_sum = _max_subarray_rec(arr, lo, mid)
    right_lo, right_hi, right_sum = _max_subarray_rec(arr, mid + 1, hi)
    cross_lo, cross_hi, cross_sum = _max_crossing_subarray(arr, lo, mid, hi)

    if left_sum >= right_sum and left_sum >= cross_sum:
        return left_lo, left_hi, left_sum
    elif right_sum >= left_sum and right_sum >= cross_sum:
        return right_lo, right_hi, right_sum
    else:
        return cross_lo, cross_hi, cross_sum


if __name__ == "__main__":
    import doctest

    doctest.testmod()
