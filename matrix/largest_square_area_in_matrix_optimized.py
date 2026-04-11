#!/usr/bin/env python3
"""
Optimized and alternative implementations of Largest Square Area in Matrix.

The reference provides 4 variants: naive recursive, memoized, bottom-up DP,
and space-optimized DP. The bottom-up with O(n) space is already quite good.

Three additional perspectives:
  histograms        -- Use largest rectangle in histogram technique per row
  prefix_sum        -- Precompute prefix sums to check sub-matrices in O(1)
  single_pass_dp    -- Top-down DP scanning forward (standard LeetCode 221 approach)

Run:
    python matrix/largest_square_area_in_matrix_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matrix.largest_square_area_in_matrix import (
    largest_square_area_in_matrix_bottom_up as reference,
)


# ---------------------------------------------------------------------------
# Variant 1 -- Standard forward DP (LeetCode 221 canonical)
# ---------------------------------------------------------------------------

def largest_square_forward_dp(mat: list[list[int]]) -> int:
    """
    Forward-scanning DP. dp[i][j] = side length of largest square with
    bottom-right corner at (i,j).

    >>> largest_square_forward_dp([[1, 1], [1, 1]])
    2
    >>> largest_square_forward_dp([[0, 0], [0, 0]])
    0
    >>> largest_square_forward_dp([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    3
    >>> largest_square_forward_dp([[1, 0], [1, 1]])
    1
    >>> largest_square_forward_dp([[1]])
    1
    >>> largest_square_forward_dp([[0]])
    0
    """
    if not mat:
        return 0
    rows, cols = len(mat), len(mat[0])
    dp = [row[:] for row in mat]
    max_side = max(max(row) for row in dp)

    for i in range(1, rows):
        for j in range(1, cols):
            if mat[i][j] == 1:
                dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
                max_side = max(max_side, dp[i][j])

    return max_side


# ---------------------------------------------------------------------------
# Variant 2 -- Space-optimized forward DP (single row)
# ---------------------------------------------------------------------------

def largest_square_1d_dp(mat: list[list[int]]) -> int:
    """
    Forward DP using only one row of space plus a prev variable.

    >>> largest_square_1d_dp([[1, 1], [1, 1]])
    2
    >>> largest_square_1d_dp([[0, 0], [0, 0]])
    0
    >>> largest_square_1d_dp([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    3
    >>> largest_square_1d_dp([[1, 0, 1, 0], [1, 1, 1, 1], [1, 1, 1, 0]])
    2
    """
    if not mat:
        return 0
    rows, cols = len(mat), len(mat[0])
    dp = mat[0][:]
    max_side = max(dp)

    for i in range(1, rows):
        prev = 0
        for j in range(cols):
            temp = dp[j]
            if mat[i][j] == 1:
                dp[j] = min(dp[j], dp[j-1] if j > 0 else 0, prev) + 1
                max_side = max(max_side, dp[j])
            else:
                dp[j] = 0
            prev = temp

    return max_side


# ---------------------------------------------------------------------------
# Variant 3 -- Histogram-based approach
# ---------------------------------------------------------------------------

def largest_square_histogram(mat: list[list[int]]) -> int:
    """
    Build histogram heights per row, then for each row find the largest
    square that fits. The largest square of side s requires s consecutive
    columns with height >= s.

    >>> largest_square_histogram([[1, 1], [1, 1]])
    2
    >>> largest_square_histogram([[0, 0], [0, 0]])
    0
    >>> largest_square_histogram([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    3
    >>> largest_square_histogram([[1, 0, 1, 0], [1, 1, 1, 1], [1, 1, 1, 0]])
    2
    """
    if not mat:
        return 0
    rows, cols = len(mat), len(mat[0])
    heights = [0] * cols
    max_side = 0

    for i in range(rows):
        for j in range(cols):
            heights[j] = heights[j] + 1 if mat[i][j] == 1 else 0

        # For each possible side length, check if there are enough consecutive columns
        for j in range(cols):
            side = heights[j]
            while side > max_side:
                # Check if we can form a square of this side ending at column j
                ok = True
                for k in range(j - side + 1, j + 1):
                    if k < 0 or heights[k] < side:
                        ok = False
                        break
                if ok:
                    max_side = side
                    break
                side -= 1

    return max_side


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    import random
    random.seed(42)
    size = 100
    mat = [[random.choice([0, 1]) for _ in range(size)] for _ in range(size)]

    number = 1_000
    print(f"Benchmark ({number} runs on {size}x{size} random matrix):\n")

    funcs = [
        ("reference (bottom-up DP)", lambda: reference(size, size, mat)),
        ("forward_dp (LeetCode 221)", lambda: largest_square_forward_dp(mat)),
        ("1d_dp (space optimized)", lambda: largest_square_1d_dp(mat)),
        ("histogram-based", lambda: largest_square_histogram(mat)),
    ]

    for name, func in funcs:
        t = timeit.timeit(func, number=number)
        print(f"  {name:35s} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
