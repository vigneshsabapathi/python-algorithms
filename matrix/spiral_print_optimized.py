#!/usr/bin/env python3
"""
Optimized and alternative implementations of Spiral Matrix Traversal.

The reference provides recursive peeling and transpose+reverse approaches.
Both create intermediate lists. Time: O(m*n), Space: O(m*n) for output.

Three alternatives:
  boundary_walk    -- Iterative boundary shrinking (LeetCode 54 standard)
  direction_sim    -- Simulate walking with direction changes
  generate_spiral  -- Build a matrix by filling in spiral order (LeetCode 59)

Run:
    python matrix/spiral_print_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matrix.spiral_print import spiral_traversal as reference


# ---------------------------------------------------------------------------
# Variant 1 -- Boundary walk (LeetCode 54 standard solution)
# ---------------------------------------------------------------------------

def spiral_boundary(matrix: list[list[int]]) -> list[int]:
    """
    Iterative spiral traversal using boundary pointers.
    top, bottom, left, right shrink as we traverse.

    >>> spiral_boundary([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    >>> spiral_boundary([[1, 2], [3, 4]])
    [1, 2, 4, 3]
    >>> spiral_boundary([[1]])
    [1]
    >>> spiral_boundary([[1, 2, 3]])
    [1, 2, 3]
    >>> spiral_boundary([[1], [2], [3]])
    [1, 2, 3]
    """
    if not matrix:
        return []
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        for j in range(left, right + 1):
            result.append(matrix[top][j])
        top += 1

        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1

        if top <= bottom:
            for j in range(right, left - 1, -1):
                result.append(matrix[bottom][j])
            bottom -= 1

        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1

    return result


# ---------------------------------------------------------------------------
# Variant 2 -- Direction simulation with visited tracking
# ---------------------------------------------------------------------------

def spiral_direction(matrix: list[list[int]]) -> list[int]:
    """
    Simulate walking in spiral using direction vector rotation.
    Turn right when hitting boundary or visited cell.

    >>> spiral_direction([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    >>> spiral_direction([[1]])
    [1]
    >>> spiral_direction([[1, 2], [3, 4]])
    [1, 2, 4, 3]
    """
    if not matrix or not matrix[0]:
        return []
    rows, cols = len(matrix), len(matrix[0])
    visited = [[False] * cols for _ in range(rows)]
    # Right, Down, Left, Up
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    direction = 0
    r = c = 0
    result = []

    for _ in range(rows * cols):
        result.append(matrix[r][c])
        visited[r][c] = True
        nr, nc = r + dr[direction], c + dc[direction]
        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
            r, c = nr, nc
        else:
            direction = (direction + 1) % 4
            r, c = r + dr[direction], c + dc[direction]

    return result


# ---------------------------------------------------------------------------
# Variant 3 -- Generate spiral matrix (LeetCode 59)
# ---------------------------------------------------------------------------

def generate_spiral_matrix(n: int) -> list[list[int]]:
    """
    Generate an n x n matrix filled with values 1 to n^2 in spiral order.
    (LeetCode 59: Spiral Matrix II)

    >>> generate_spiral_matrix(1)
    [[1]]
    >>> generate_spiral_matrix(2)
    [[1, 2], [4, 3]]
    >>> generate_spiral_matrix(3)
    [[1, 2, 3], [8, 9, 4], [7, 6, 5]]
    """
    matrix = [[0] * n for _ in range(n)]
    top, bottom, left, right = 0, n - 1, 0, n - 1
    num = 1

    while top <= bottom and left <= right:
        for j in range(left, right + 1):
            matrix[top][j] = num
            num += 1
        top += 1
        for i in range(top, bottom + 1):
            matrix[i][right] = num
            num += 1
        right -= 1
        if top <= bottom:
            for j in range(right, left - 1, -1):
                matrix[bottom][j] = num
                num += 1
            bottom -= 1
        if left <= right:
            for i in range(bottom, top - 1, -1):
                matrix[i][left] = num
                num += 1
            left += 1

    return matrix


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    matrix = [[i * 100 + j for j in range(100)] for i in range(100)]

    number = 5_000
    print(f"Benchmark ({number} spiral traversals of 100x100):\n")

    funcs = [
        ("reference (transpose+reverse)", lambda: reference([row[:] for row in matrix])),
        ("boundary_walk", lambda: spiral_boundary(matrix)),
        ("direction_simulation", lambda: spiral_direction(matrix)),
        ("generate_spiral (n=100)", lambda: generate_spiral_matrix(100)),
    ]

    for name, func in funcs:
        t = timeit.timeit(func, number=number)
        print(f"  {name:40s} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
