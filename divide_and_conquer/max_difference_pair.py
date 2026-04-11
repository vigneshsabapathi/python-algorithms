"""
Maximum Difference Pair — Divide and Conquer

Given an array, find the maximum difference arr[j] - arr[i] where j > i.
(Like the "best time to buy and sell stock" problem.)

Brute force: O(n^2). D&C: O(n log n). Linear scan: O(n).

D&C approach: split array, the max difference is either:
  (a) entirely in the left half,
  (b) entirely in the right half, or
  (c) min of left half subtracted from max of right half (cross-boundary).

Reference: https://github.com/TheAlgorithms/Python/blob/master/divide_and_conquer/max_difference_pair.py
"""

from __future__ import annotations


def max_difference_pair(arr: list[int | float]) -> tuple[int | float, int, int]:
    """
    Find maximum arr[j] - arr[i] where j > i using divide and conquer.
    Returns (max_diff, buy_index, sell_index).

    >>> max_difference_pair([2, 3, 10, 6, 4, 8, 1])
    (8, 0, 2)
    >>> max_difference_pair([7, 9, 5, 6, 3, 2])
    (2, 0, 1)
    >>> max_difference_pair([1, 2, 3, 4, 5])
    (4, 0, 4)
    >>> max_difference_pair([5, 4, 3, 2, 1])
    (-1, 0, 1)
    >>> max_difference_pair([1])
    Traceback (most recent call last):
        ...
    ValueError: Need at least 2 elements
    """
    if len(arr) < 2:
        raise ValueError("Need at least 2 elements")
    diff, i, j = _max_diff_rec(arr, 0, len(arr) - 1)
    return diff, i, j


def _max_diff_rec(
    arr: list[int | float], lo: int, hi: int
) -> tuple[int | float, int, int]:
    """Recursive helper returning (max_diff, min_index, max_index)."""
    if hi - lo == 1:
        return arr[hi] - arr[lo], lo, hi
    if lo == hi:
        return float("-inf"), lo, lo

    mid = (lo + hi) // 2

    left_diff, left_min_i, left_max_j = _max_diff_rec(arr, lo, mid)
    right_diff, right_min_i, right_max_j = _max_diff_rec(arr, mid + 1, hi)

    # Find min in left half, max in right half
    min_left_val = float("inf")
    min_left_idx = lo
    for k in range(lo, mid + 1):
        if arr[k] < min_left_val:
            min_left_val = arr[k]
            min_left_idx = k

    max_right_val = float("-inf")
    max_right_idx = mid + 1
    for k in range(mid + 1, hi + 1):
        if arr[k] > max_right_val:
            max_right_val = arr[k]
            max_right_idx = k

    cross_diff = max_right_val - min_left_val

    if left_diff >= right_diff and left_diff >= cross_diff:
        return left_diff, left_min_i, left_max_j
    elif right_diff >= left_diff and right_diff >= cross_diff:
        return right_diff, right_min_i, right_max_j
    else:
        return cross_diff, min_left_idx, max_right_idx


if __name__ == "__main__":
    import doctest

    doctest.testmod()
