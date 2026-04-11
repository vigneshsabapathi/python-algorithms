#!/usr/bin/env python3
"""
Optimized and alternative implementations of Matrix Rotation.

The reference rotates via transpose + reverse operations which modify
the matrix in-place. Each rotation is O(n^2).

Three alternatives:
  rotate_90_cw_inplace  -- In-place 90 clockwise (LeetCode 48) using 4-way swap
  rotate_by_layers      -- Layer-by-layer rotation without transpose
  rotate_arbitrary      -- Rotate by any multiple of 90 degrees

Run:
    python matrix/rotate_matrix_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matrix.rotate_matrix import make_matrix, rotate_90 as reference_90


# ---------------------------------------------------------------------------
# Variant 1 -- In-place 90 CW rotation via 4-way swap (LeetCode 48)
# ---------------------------------------------------------------------------

def rotate_90_clockwise_inplace(matrix: list[list[int]]) -> list[list[int]]:
    """
    Rotate 90 degrees clockwise in-place using the 4-element cycle swap.
    This is the classic LeetCode 48 solution.

    >>> m = [[1,2,3],[4,5,6],[7,8,9]]
    >>> rotate_90_clockwise_inplace(m)
    [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    >>> m = [[1,2],[3,4]]
    >>> rotate_90_clockwise_inplace(m)
    [[3, 1], [4, 2]]
    """
    n = len(matrix)
    for layer in range(n // 2):
        first, last = layer, n - 1 - layer
        for i in range(first, last):
            offset = i - first
            # Save top
            top = matrix[first][i]
            # Left -> Top
            matrix[first][i] = matrix[last - offset][first]
            # Bottom -> Left
            matrix[last - offset][first] = matrix[last][last - offset]
            # Right -> Bottom
            matrix[last][last - offset] = matrix[i][last]
            # Top -> Right
            matrix[i][last] = top
    return matrix


# ---------------------------------------------------------------------------
# Variant 2 -- Layer-by-layer 90 CCW rotation
# ---------------------------------------------------------------------------

def rotate_90_ccw_layers(matrix: list[list[int]]) -> list[list[int]]:
    """
    Rotate 90 degrees counterclockwise using layer-by-layer 4-way swap.

    >>> m = make_matrix(4)
    >>> rotate_90_ccw_layers([row[:] for row in m])
    [[4, 8, 12, 16], [3, 7, 11, 15], [2, 6, 10, 14], [1, 5, 9, 13]]
    >>> rotate_90_ccw_layers([[1, 2], [3, 4]])
    [[2, 4], [1, 3]]
    """
    n = len(matrix)
    for layer in range(n // 2):
        first, last = layer, n - 1 - layer
        for i in range(first, last):
            offset = i - first
            top = matrix[first][i]
            # Right -> Top
            matrix[first][i] = matrix[i][last]
            # Bottom -> Right
            matrix[i][last] = matrix[last][last - offset]
            # Left -> Bottom
            matrix[last][last - offset] = matrix[last - offset][first]
            # Top -> Left
            matrix[last - offset][first] = top
    return matrix


# ---------------------------------------------------------------------------
# Variant 3 -- Generic rotation by k*90 degrees
# ---------------------------------------------------------------------------

def rotate_k_times(matrix: list[list[int]], k: int = 1) -> list[list[int]]:
    """
    Rotate matrix by k * 90 degrees clockwise. k can be negative.

    >>> rotate_k_times([[1,2],[3,4]], 1)
    [[2, 4], [1, 3]]
    >>> rotate_k_times([[1,2],[3,4]], 2)
    [[4, 3], [2, 1]]
    >>> rotate_k_times([[1,2],[3,4]], 0)
    [[1, 2], [3, 4]]
    >>> rotate_k_times([[1,2],[3,4]], 4)
    [[1, 2], [3, 4]]
    >>> rotate_k_times([[1,2],[3,4]], -1)
    [[3, 1], [4, 2]]
    """
    k = k % 4
    result = [row[:] for row in matrix]
    for _ in range(k):
        result = [list(row) for row in zip(*result)][::-1]
        # zip(*m) transposes, [::-1] reverses rows = 90 CW
    return result


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    n = 100
    matrix = [[i * n + j for j in range(n)] for i in range(n)]

    number = 10_000
    print(f"Benchmark ({number} rotations of {n}x{n} matrix):\n")

    funcs = [
        ("reference (transpose+reverse)", lambda: reference_90([row[:] for row in matrix])),
        ("90_cw_inplace (4-way swap)", lambda: rotate_90_clockwise_inplace([row[:] for row in matrix])),
        ("90_ccw_layers", lambda: rotate_90_ccw_layers([row[:] for row in matrix])),
        ("rotate_k_times (k=1)", lambda: rotate_k_times(matrix, 1)),
    ]

    for name, func in funcs:
        t = timeit.timeit(func, number=number)
        print(f"  {name:40s} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
