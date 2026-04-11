#!/usr/bin/env python3
"""
Optimized and alternative implementations of Matrix Operations.

The reference provides functional matrix operations (add, subtract, multiply,
determinant, inverse, transpose). Determinant is O(n!) via cofactor expansion.

Three alternatives:
  gauss_det       -- O(n^3) determinant via Gaussian elimination
  transpose_inplace -- In-place transpose for square matrices
  multiply_transposed -- Multiply using pre-transposed B for cache efficiency

Run:
    python matrix/matrix_operation_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matrix.matrix_operation import determinant as reference_det, multiply as reference_mul


# ---------------------------------------------------------------------------
# Variant 1 -- Gaussian elimination determinant O(n^3)
# ---------------------------------------------------------------------------

def determinant_gauss(matrix: list[list[float]]) -> float:
    """
    Compute determinant using Gaussian elimination with partial pivoting.

    >>> determinant_gauss([[1, 2], [3, 4]])
    -2.0
    >>> determinant_gauss([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    1.0
    >>> abs(determinant_gauss([[1, 2, 3], [4, 5, 6], [7, 8, 9]])) < 1e-10
    True
    >>> determinant_gauss([[5]])
    5.0
    """
    n = len(matrix)
    mat = [row[:] for row in matrix]
    sign = 1

    for col in range(n):
        max_row = max(range(col, n), key=lambda r: abs(mat[r][col]))
        if abs(mat[max_row][col]) < 1e-12:
            return 0.0
        if max_row != col:
            mat[col], mat[max_row] = mat[max_row], mat[col]
            sign *= -1
        for row in range(col + 1, n):
            factor = mat[row][col] / mat[col][col]
            for j in range(col, n):
                mat[row][j] -= factor * mat[col][j]

    result = float(sign)
    for i in range(n):
        result *= mat[i][i]
    return result


# ---------------------------------------------------------------------------
# Variant 2 -- In-place transpose for square matrices
# ---------------------------------------------------------------------------

def transpose_inplace(matrix: list[list[int]]) -> list[list[int]]:
    """
    Transpose a square matrix in-place by swapping elements across diagonal.

    >>> transpose_inplace([[1, 2], [3, 4]])
    [[1, 3], [2, 4]]
    >>> transpose_inplace([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    """
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    return matrix


# ---------------------------------------------------------------------------
# Variant 3 -- Multiply with pre-transposed B for cache efficiency
# ---------------------------------------------------------------------------

def multiply_transposed(matrix_a: list[list[int]], matrix_b: list[list[int]]) -> list[list[int]]:
    """
    Multiply A * B by first transposing B, then doing row-row dot products.
    Better cache locality since we access B by rows instead of columns.

    >>> multiply_transposed([[1,2],[3,4]], [[5,5],[7,5]])
    [[19, 15], [43, 35]]
    >>> multiply_transposed([[1, 2, 3]], [[2], [3], [4]])
    [[20]]
    """
    bt = [list(col) for col in zip(*matrix_b)]
    return [
        [sum(a * b for a, b in zip(row_a, row_bt)) for row_bt in bt]
        for row_a in matrix_a
    ]


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    m4 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    m4b = [[5, 8, 1, 2], [6, 7, 3, 0], [4, 5, 9, 1], [2, 6, 10, 14]]

    number = 50_000
    print(f"Benchmark ({number} runs on 4x4):\n")

    print("Determinant:")
    funcs_det = [
        ("reference (cofactor O(n!))", lambda: reference_det(m4)),
        ("gauss (O(n^3))", lambda: determinant_gauss(m4)),
    ]
    for name, func in funcs_det:
        t = timeit.timeit(func, number=number)
        print(f"  {name:35s} {t:.4f}s")

    print("\nMultiplication:")
    funcs_mul = [
        ("reference (zip columns)", lambda: reference_mul(m4, m4b)),
        ("transposed B (row-row)", lambda: multiply_transposed(m4, m4b)),
    ]
    for name, func in funcs_mul:
        t = timeit.timeit(func, number=number)
        print(f"  {name:35s} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
