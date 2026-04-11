"""
Peak Finding — Divide and Conquer

A peak element is one that is greater than or equal to its neighbours.

1D peak: Binary search approach — O(log n).
2D peak: Column-max + binary search on rows — O(n log n) or O(n log m).

Reference: https://github.com/TheAlgorithms/Python/blob/master/divide_and_conquer/peak.py
"""

from __future__ import annotations


def peak_1d(arr: list[int | float]) -> int:
    """
    Find a peak element index in a 1D array using binary search.
    A peak is >= its neighbours.

    >>> arr = [1, 3, 20, 4, 1, 0]
    >>> i = peak_1d(arr)
    >>> arr[i] >= (arr[i-1] if i > 0 else float('-inf'))
    True
    >>> arr[i] >= (arr[i+1] if i < len(arr)-1 else float('-inf'))
    True
    >>> peak_1d([5, 4, 3, 2, 1])
    0
    >>> peak_1d([1, 2, 3, 4, 5])
    4
    >>> peak_1d([1])
    0
    """
    if not arr:
        raise ValueError("Array must not be empty")
    return _peak_1d_rec(arr, 0, len(arr) - 1)


def _peak_1d_rec(arr: list[int | float], lo: int, hi: int) -> int:
    mid = (lo + hi) // 2

    if (mid == 0 or arr[mid] >= arr[mid - 1]) and (
        mid == len(arr) - 1 or arr[mid] >= arr[mid + 1]
    ):
        return mid

    if mid > 0 and arr[mid - 1] > arr[mid]:
        return _peak_1d_rec(arr, lo, mid - 1)
    return _peak_1d_rec(arr, mid + 1, hi)


def peak_2d(matrix: list[list[int | float]]) -> tuple[int, int]:
    """
    Find a peak element position in a 2D matrix.
    A peak is >= all four neighbours.

    >>> m = [[10, 8, 10, 10], [14, 13, 12, 11], [15, 9, 11, 21], [16, 17, 19, 20]]
    >>> r, c = peak_2d(m)
    >>> val = m[r][c]
    >>> val >= (m[r-1][c] if r > 0 else float('-inf'))
    True
    >>> val >= (m[r+1][c] if r < len(m)-1 else float('-inf'))
    True
    >>> val >= (m[r][c-1] if c > 0 else float('-inf'))
    True
    >>> val >= (m[r][c+1] if c < len(m[0])-1 else float('-inf'))
    True
    """
    if not matrix or not matrix[0]:
        raise ValueError("Matrix must not be empty")
    rows = len(matrix)
    cols = len(matrix[0])
    return _peak_2d_rec(matrix, 0, cols - 1, rows)


def _peak_2d_rec(
    matrix: list[list[int | float]], lo_col: int, hi_col: int, rows: int
) -> tuple[int, int]:
    mid_col = (lo_col + hi_col) // 2

    # Find max in the mid column
    max_row = 0
    for r in range(rows):
        if matrix[r][mid_col] > matrix[max_row][mid_col]:
            max_row = r

    # Check if it's a peak
    val = matrix[max_row][mid_col]
    left = matrix[max_row][mid_col - 1] if mid_col > 0 else float("-inf")
    right = (
        matrix[max_row][mid_col + 1] if mid_col < len(matrix[0]) - 1 else float("-inf")
    )

    if val >= left and val >= right:
        return max_row, mid_col
    elif left > val:
        return _peak_2d_rec(matrix, lo_col, mid_col - 1, rows)
    else:
        return _peak_2d_rec(matrix, mid_col + 1, hi_col, rows)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
