"""
Maximum Subsequence (Kadane's Algorithm) — Find the contiguous subarray with the largest sum.

Returns the maximum sum achievable from any contiguous subarray.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/maximum_subsequence.py
"""

from __future__ import annotations


def max_subsequence(arr: list[int]) -> int:
    """
    Find maximum sum contiguous subarray (Kadane's algorithm).

    >>> max_subsequence([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    6
    >>> max_subsequence([1, 2, 3, 4])
    10
    >>> max_subsequence([-1, -2, -3])
    -1
    >>> max_subsequence([5])
    5
    >>> max_subsequence([])
    0
    >>> max_subsequence([-2, -3, 4, -1, -2, 1, 5, -3])
    7
    """
    if not arr:
        return 0

    max_ending_here = arr[0]
    max_so_far = arr[0]

    for num in arr[1:]:
        max_ending_here = max(num, max_ending_here + num)
        max_so_far = max(max_so_far, max_ending_here)

    return max_so_far


def max_subsequence_with_indices(arr: list[int]) -> tuple[int, int, int]:
    """
    Return (max_sum, start_index, end_index) of the maximum subarray.

    >>> max_subsequence_with_indices([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    (6, 3, 6)
    >>> max_subsequence_with_indices([1, 2, 3])
    (6, 0, 2)
    >>> max_subsequence_with_indices([-5, -2, -1])
    (-1, 2, 2)
    """
    if not arr:
        return (0, 0, 0)

    max_ending_here = arr[0]
    max_so_far = arr[0]
    start = end = temp_start = 0

    for i in range(1, len(arr)):
        if arr[i] > max_ending_here + arr[i]:
            max_ending_here = arr[i]
            temp_start = i
        else:
            max_ending_here += arr[i]

        if max_ending_here > max_so_far:
            max_so_far = max_ending_here
            start = temp_start
            end = i

    return max_so_far, start, end


if __name__ == "__main__":
    import doctest

    doctest.testmod()
