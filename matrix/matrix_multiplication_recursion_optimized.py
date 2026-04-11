#!/usr/bin/env python3
"""
Optimized and alternative implementations of Matrix Multiplication.

The reference provides iterative O(n^3) and recursive O(n^3) multiplication.
The recursive version has massive overhead from function calls.

Three alternatives:
  strassen           -- Strassen's algorithm O(n^2.807) for large matrices
  list_comprehension -- Pythonic one-liner using zip
  blocked            -- Cache-friendly blocked multiplication

Run:
    python matrix/matrix_multiplication_recursion_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matrix.matrix_multiplication_recursion import (
    matrix_multiply as reference,
    matrix_multiply_recursive as reference_recursive,
)

Matrix = list[list[int]]


# ---------------------------------------------------------------------------
# Variant 1 -- Strassen's algorithm O(n^2.807)
# ---------------------------------------------------------------------------

def strassen(a: Matrix, b: Matrix) -> Matrix:
    """
    Strassen's matrix multiplication. Only works on 2^k x 2^k matrices.
    Falls back to naive for small matrices.

    >>> strassen([[1, 2], [3, 4]], [[5, 6], [7, 8]])
    [[19, 22], [43, 50]]
    >>> strassen([[1]], [[2]])
    [[2]]
    """
    n = len(a)
    if n == 1:
        return [[a[0][0] * b[0][0]]]

    mid = n // 2

    def sub(x: Matrix, y: Matrix) -> Matrix:
        return [[x[i][j] - y[i][j] for j in range(len(x[0]))] for i in range(len(x))]

    def add(x: Matrix, y: Matrix) -> Matrix:
        return [[x[i][j] + y[i][j] for j in range(len(x[0]))] for i in range(len(x))]

    def quarter(m: Matrix, r: int, c: int) -> Matrix:
        return [row[c:c+mid] for row in m[r:r+mid]]

    a11, a12 = quarter(a, 0, 0), quarter(a, 0, mid)
    a21, a22 = quarter(a, mid, 0), quarter(a, mid, mid)
    b11, b12 = quarter(b, 0, 0), quarter(b, 0, mid)
    b21, b22 = quarter(b, mid, 0), quarter(b, mid, mid)

    m1 = strassen(add(a11, a22), add(b11, b22))
    m2 = strassen(add(a21, a22), b11)
    m3 = strassen(a11, sub(b12, b22))
    m4 = strassen(a22, sub(b21, b11))
    m5 = strassen(add(a11, a12), b22)
    m6 = strassen(sub(a21, a11), add(b11, b12))
    m7 = strassen(sub(a12, a22), add(b21, b22))

    c11 = add(sub(add(m1, m4), m5), m7)
    c12 = add(m3, m5)
    c21 = add(m2, m4)
    c22 = add(sub(add(m1, m3), m2), m6)

    result = [[0] * n for _ in range(n)]
    for i in range(mid):
        for j in range(mid):
            result[i][j] = c11[i][j]
            result[i][j + mid] = c12[i][j]
            result[i + mid][j] = c21[i][j]
            result[i + mid][j + mid] = c22[i][j]

    return result


# ---------------------------------------------------------------------------
# Variant 2 -- Pythonic zip-based multiplication
# ---------------------------------------------------------------------------

def multiply_zip(a: Matrix, b: Matrix) -> Matrix:
    """
    Clean Pythonic matrix multiplication using zip for transposition.

    >>> multiply_zip([[1, 2], [3, 4]], [[5, 6], [7, 8]])
    [[19, 22], [43, 50]]
    >>> multiply_zip([[1, 2, 3]], [[1], [2], [3]])
    [[14]]
    """
    return [
        [sum(x * y for x, y in zip(row_a, col_b)) for col_b in zip(*b)]
        for row_a in a
    ]


# ---------------------------------------------------------------------------
# Variant 3 -- Blocked (tiled) multiplication for cache efficiency
# ---------------------------------------------------------------------------

def multiply_blocked(a: Matrix, b: Matrix, block_size: int = 16) -> Matrix:
    """
    Cache-friendly blocked matrix multiplication. Processes sub-blocks
    to improve locality of reference.

    >>> multiply_blocked([[1, 2], [3, 4]], [[5, 6], [7, 8]])
    [[19, 22], [43, 50]]
    >>> multiply_blocked([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]],
    ...                  [[5,8,1,2],[6,7,3,0],[4,5,9,1],[2,6,10,14]])
    [[37, 61, 74, 61], [105, 165, 166, 129], [173, 269, 258, 197], [241, 373, 350, 265]]
    """
    n = len(a)
    m = len(b[0])
    p = len(b)
    result = [[0] * m for _ in range(n)]

    for ii in range(0, n, block_size):
        for jj in range(0, m, block_size):
            for kk in range(0, p, block_size):
                for i in range(ii, min(ii + block_size, n)):
                    for k in range(kk, min(kk + block_size, p)):
                        a_ik = a[i][k]
                        for j in range(jj, min(jj + block_size, m)):
                            result[i][j] += a_ik * b[k][j]

    return result


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    a = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    b = [[5, 8, 1, 2], [6, 7, 3, 0], [4, 5, 9, 1], [2, 6, 10, 14]]

    number = 50_000
    print(f"Benchmark ({number} multiplications of 4x4 matrices):\n")

    funcs = [
        ("reference (iterative)", lambda: reference(a, b)),
        ("reference (recursive)", lambda: reference_recursive(a, b)),
        ("zip-based", lambda: multiply_zip(a, b)),
        ("blocked (tile=2)", lambda: multiply_blocked(a, b, 2)),
        ("strassen", lambda: strassen(a, b)),
    ]

    for name, func in funcs:
        t = timeit.timeit(func, number=number)
        print(f"  {name:30s} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
