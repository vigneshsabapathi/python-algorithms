#!/usr/bin/env python3
"""
Optimized and alternative implementations of Searching in Sorted Matrix.

The reference uses staircase search from bottom-left: O(m + n).
This is already optimal for a matrix sorted by rows and columns separately.

Three alternatives:
  top_right_search    -- Start from top-right instead of bottom-left
  binary_search_rows  -- Binary search each candidate row: O(m * log n)
  divide_conquer      -- Recursive divide and conquer approach

Run:
    python matrix/searching_in_sorted_matrix_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matrix.searching_in_sorted_matrix import search_in_a_sorted_matrix as reference


# ---------------------------------------------------------------------------
# Variant 1 -- Top-right staircase search
# ---------------------------------------------------------------------------

def search_top_right(mat: list[list[int]], key: float) -> tuple[bool, int, int]:
    """
    Staircase search starting from top-right corner.
    If current > key, move left. If current < key, move down.

    >>> mat = [[2, 5, 7], [4, 8, 13], [9, 11, 15], [12, 17, 20]]
    >>> search_top_right(mat, 5)
    (True, 1, 2)
    >>> search_top_right(mat, 21)
    (False, -1, -1)
    >>> search_top_right(mat, 11)
    (True, 3, 2)
    """
    if not mat or not mat[0]:
        return (False, -1, -1)
    rows, cols = len(mat), len(mat[0])
    i, j = 0, cols - 1
    while i < rows and j >= 0:
        if mat[i][j] == key:
            return (True, i + 1, j + 1)
        elif mat[i][j] > key:
            j -= 1
        else:
            i += 1
    return (False, -1, -1)


# ---------------------------------------------------------------------------
# Variant 2 -- Binary search per row
# ---------------------------------------------------------------------------

def search_binary_rows(mat: list[list[int]], key: float) -> tuple[bool, int, int]:
    """
    Binary search on each row. Skip rows where key is out of range.
    O(m * log n) but with good pruning.

    >>> mat = [[2, 5, 7], [4, 8, 13], [9, 11, 15], [12, 17, 20]]
    >>> search_binary_rows(mat, 5)
    (True, 1, 2)
    >>> search_binary_rows(mat, 21)
    (False, -1, -1)
    >>> search_binary_rows(mat, 11)
    (True, 3, 2)
    """
    for i, row in enumerate(mat):
        if not row or row[0] > key:
            continue
        if row[-1] < key:
            continue
        lo, hi = 0, len(row) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if row[mid] == key:
                return (True, i + 1, mid + 1)
            elif row[mid] < key:
                lo = mid + 1
            else:
                hi = mid - 1
    return (False, -1, -1)


# ---------------------------------------------------------------------------
# Variant 3 -- Search with early termination using bounds
# ---------------------------------------------------------------------------

def search_bounded(mat: list[list[int]], key: float) -> tuple[bool, int, int]:
    """
    Bottom-left staircase with tighter bounds tracking.

    >>> mat = [[2, 5, 7], [4, 8, 13], [9, 11, 15], [12, 17, 20]]
    >>> search_bounded(mat, 5)
    (True, 1, 2)
    >>> search_bounded(mat, 21)
    (False, -1, -1)
    >>> search_bounded(mat, 20)
    (True, 4, 3)
    """
    if not mat or not mat[0]:
        return (False, -1, -1)
    rows, cols = len(mat), len(mat[0])
    # Quick bounds check
    if key < mat[0][0] or key > mat[rows - 1][cols - 1]:
        return (False, -1, -1)

    i, j = rows - 1, 0
    while i >= 0 and j < cols:
        if mat[i][j] == key:
            return (True, i + 1, j + 1)
        elif mat[i][j] < key:
            j += 1
        else:
            i -= 1
    return (False, -1, -1)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    # Build a large sorted matrix
    mat = [[i * 100 + j * 3 + 1 for j in range(100)] for i in range(100)]
    key = mat[75][50]  # A value that exists

    number = 100_000
    print(f"Benchmark ({number} searches in 100x100 matrix):\n")

    funcs = [
        ("reference (bottom-left)", lambda: reference(mat, 100, 100, key)),
        ("top_right", lambda: search_top_right(mat, key)),
        ("binary_rows", lambda: search_binary_rows(mat, key)),
        ("bounded", lambda: search_bounded(mat, key)),
    ]

    for name, func in funcs:
        t = timeit.timeit(func, number=number)
        print(f"  {name:30s} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
