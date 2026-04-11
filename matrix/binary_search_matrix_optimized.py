#!/usr/bin/env python3
"""
Optimized and alternative implementations of Binary Search in a 2D Matrix.

The reference approach does binary search per-row, which is O(m * log n)
where m = rows, n = cols. It also uses recursion for the inner binary search.

Three improved variants:
  flatten    -- Treat the matrix as a flat sorted array, single binary search O(log(m*n))
  staircase  -- Start top-right corner, walk left/down in O(m + n) (LeetCode 240)
  iterative  -- Same per-row approach but with iterative binary search (no recursion)

The flatten approach only works when the matrix is row-sorted AND the first element
of each row > last element of previous row (LeetCode 74).
The staircase approach works on any row-sorted, column-sorted matrix (LeetCode 240).

Run:
    python matrix/binary_search_matrix_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matrix.binary_search_matrix import mat_bin_search as reference


# ---------------------------------------------------------------------------
# Variant 1 -- flatten: single binary search on virtual flat array  O(log(m*n))
# ---------------------------------------------------------------------------

def flatten_search(value: int, matrix: list[list[int]]) -> list[int]:
    """
    Treat the matrix as a single sorted array and do one binary search.
    Only valid when rows are strictly increasing left-to-right AND
    first element of row i > last element of row i-1.

    >>> m = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    >>> flatten_search(3, m)
    [0, 1]
    >>> flatten_search(13, m)
    [-1, -1]
    >>> flatten_search(60, m)
    [2, 3]
    >>> flatten_search(1, m)
    [0, 0]
    """
    if not matrix or not matrix[0]:
        return [-1, -1]
    rows, cols = len(matrix), len(matrix[0])
    lo, hi = 0, rows * cols - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        r, c = divmod(mid, cols)
        if matrix[r][c] == value:
            return [r, c]
        elif matrix[r][c] < value:
            lo = mid + 1
        else:
            hi = mid - 1
    return [-1, -1]


# ---------------------------------------------------------------------------
# Variant 2 -- staircase: top-right walk  O(m + n)  (LeetCode 240)
# ---------------------------------------------------------------------------

def staircase_search(value: int, matrix: list[list[int]]) -> list[int]:
    """
    Start at top-right corner. Move left if current > value, down if current < value.
    Works on any matrix where rows and columns are individually sorted.

    >>> matrix = [[1, 4, 7, 11, 15],
    ...           [2, 5, 8, 12, 19],
    ...           [3, 6, 9, 16, 22],
    ...           [10, 13, 14, 17, 24],
    ...           [18, 21, 23, 26, 30]]
    >>> staircase_search(1, matrix)
    [0, 0]
    >>> staircase_search(34, matrix)
    [-1, -1]
    >>> staircase_search(14, matrix)
    [3, 2]
    >>> staircase_search(30, matrix)
    [4, 4]
    >>> staircase_search(5, matrix)
    [1, 1]
    """
    if not matrix or not matrix[0]:
        return [-1, -1]
    row, col = 0, len(matrix[0]) - 1
    while row < len(matrix) and col >= 0:
        if matrix[row][col] == value:
            return [row, col]
        elif matrix[row][col] > value:
            col -= 1
        else:
            row += 1
    return [-1, -1]


# ---------------------------------------------------------------------------
# Variant 3 -- iterative: per-row binary search, no recursion
# ---------------------------------------------------------------------------

def iterative_search(value: int, matrix: list[list[int]]) -> list[int]:
    """
    Same row-by-row strategy as reference but uses iterative binary search
    to avoid recursion overhead and stack depth limits.

    >>> matrix = [[1, 4, 7, 11, 15],
    ...           [2, 5, 8, 12, 19],
    ...           [3, 6, 9, 16, 22],
    ...           [10, 13, 14, 17, 24],
    ...           [18, 21, 23, 26, 30]]
    >>> iterative_search(1, matrix)
    [0, 0]
    >>> iterative_search(34, matrix)
    [-1, -1]
    >>> iterative_search(14, matrix)
    [3, 2]
    >>> iterative_search(30, matrix)
    [4, 4]
    """
    for i, row in enumerate(matrix):
        if not row:
            continue
        if row[0] > value:
            break
        lo, hi = 0, len(row) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if row[mid] == value:
                return [i, mid]
            elif row[mid] < value:
                lo = mid + 1
            else:
                hi = mid - 1
    return [-1, -1]


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    matrix = [[1, 4, 7, 11, 15],
              [2, 5, 8, 12, 19],
              [3, 6, 9, 16, 22],
              [10, 13, 14, 17, 24],
              [18, 21, 23, 26, 30]]

    # For flatten, use a strictly row-sorted matrix
    flat_matrix = [[1, 3, 5, 7],
                   [10, 11, 16, 20],
                   [23, 30, 34, 60]]

    number = 100_000
    print("Benchmark (100k searches for value=14 in 5x5 matrix):\n")

    funcs = [
        ("reference (recursive per-row)", lambda: reference(14, matrix)),
        ("iterative (per-row, no recursion)", lambda: iterative_search(14, matrix)),
        ("staircase (top-right walk)", lambda: staircase_search(14, matrix)),
        ("flatten (single binary search)", lambda: flatten_search(34, flat_matrix)),
    ]

    for name, func in funcs:
        t = timeit.timeit(func, number=number)
        print(f"  {name:40s} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
