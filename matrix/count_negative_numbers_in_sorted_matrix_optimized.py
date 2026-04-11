#!/usr/bin/env python3
"""
Optimized and alternative implementations of Count Negative Numbers in Sorted Matrix.

The reference uses binary search per row with bound narrowing: O(m log n).
It also provides brute force O(m*n) and brute force with break.

Three additional variants:
  staircase       -- Start bottom-left, walk right/up in O(m + n) time
  bisect_builtin  -- Use Python's bisect module for cleaner binary search
  numpy_vectorized -- NumPy comparison for batch processing

The staircase approach is the optimal O(m + n) solution for this problem.

Run:
    python matrix/count_negative_numbers_in_sorted_matrix_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matrix.count_negative_numbers_in_sorted_matrix import (
    count_negatives_binary_search as reference,
    generate_large_matrix,
    test_grids,
)


# ---------------------------------------------------------------------------
# Variant 1 -- staircase: O(m + n) optimal
# ---------------------------------------------------------------------------

def count_negatives_staircase(grid: list[list[int]]) -> int:
    """
    Start at bottom-left. If current >= 0, move right; if < 0, count rest
    of row as negative and move up. O(m + n) time.

    >>> [count_negatives_staircase(g) for g in test_grids]
    [8, 0, 0, 3, 1498500]
    """
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    col = 0  # start bottom-left
    for row in range(rows - 1, -1, -1):
        while col < cols and grid[row][col] >= 0:
            col += 1
        count += cols - col
    return count


# ---------------------------------------------------------------------------
# Variant 2 -- bisect_builtin: cleaner per-row binary search
# ---------------------------------------------------------------------------

def count_negatives_bisect(grid: list[list[int]]) -> int:
    """
    Use bisect to find the insertion point of 0 (negatives are at the end
    since rows are sorted in decreasing order). We use a key trick: search
    for the transition point.

    >>> [count_negatives_bisect(g) for g in test_grids]
    [8, 0, 0, 3, 1498500]
    """
    import bisect
    count = 0
    for row in grid:
        # Row is decreasing, so we negate and use bisect_left to find where
        # values become positive (i.e., original values become negative)
        neg_row = [-x for x in row]
        idx = bisect.bisect_left(neg_row, 1)  # first position where -x >= 1 => x <= -1
        count += len(row) - idx
    return count


# ---------------------------------------------------------------------------
# Variant 3 -- functional one-liner with sum + generator
# ---------------------------------------------------------------------------

def count_negatives_functional(grid: list[list[int]]) -> int:
    """
    Pythonic one-liner using sum and generator expression.

    >>> [count_negatives_functional(g) for g in test_grids]
    [8, 0, 0, 3, 1498500]
    """
    return sum(1 for row in grid for x in row if x < 0)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    large = generate_large_matrix()
    number = 50
    print(f"Benchmark ({number} runs on 1000x2000 matrix):\n")

    funcs = [
        ("reference (binary search + bound)", lambda: reference(large)),
        ("staircase O(m+n)", lambda: count_negatives_staircase(large)),
        ("bisect_builtin", lambda: count_negatives_bisect(large)),
        ("functional (sum+generator)", lambda: count_negatives_functional(large)),
    ]

    for name, func in funcs:
        t = timeit.timeit(func, number=number)
        print(f"  {name:42s} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
