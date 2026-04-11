#!/usr/bin/env python3
"""
Optimized and alternative implementations of Matrix Inverse.

The reference handles only 2x2 and 3x3 matrices using cofactor expansion
with Decimal precision. Time complexity is O(1) for fixed sizes.

Three alternatives:
  gauss_jordan     -- Gauss-Jordan elimination for any NxN matrix, O(n^3)
  adjugate_nxn     -- Cofactor expansion generalized to NxN (recursive det)
  analytic_2x2     -- Simplified direct formula without Decimal overhead

Run:
    python matrix/inverse_of_matrix_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matrix.inverse_of_matrix import inverse_of_matrix as reference


# ---------------------------------------------------------------------------
# Variant 1 -- Gauss-Jordan elimination: works for any NxN
# ---------------------------------------------------------------------------

def inverse_gauss_jordan(matrix: list[list[float]]) -> list[list[float]]:
    """
    Compute the inverse using Gauss-Jordan elimination (row reduction).
    Augment [A | I], reduce A to I, yielding [I | A^(-1)].

    >>> inverse_gauss_jordan([[2, 5], [2, 0]])
    [[0.0, 0.5], [0.2, -0.2]]
    >>> inverse_gauss_jordan([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    >>> inverse_gauss_jordan([[2, 5, 7], [2, 0, 1], [1, 2, 3]])
    [[2.0, 1.0, -5.0], [5.0, 1.0, -12.0], [-4.0, -1.0, 10.0]]
    >>> inverse_gauss_jordan([[1, 2], [2, 4]])
    Traceback (most recent call last):
        ...
    ValueError: Matrix is singular and cannot be inverted.
    """
    n = len(matrix)
    # Create augmented matrix [A | I]
    aug = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(matrix)]

    for col in range(n):
        # Find pivot
        max_row = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[max_row][col]) < 1e-12:
            raise ValueError("Matrix is singular and cannot be inverted.")
        aug[col], aug[max_row] = aug[max_row], aug[col]

        # Scale pivot row
        pivot = aug[col][col]
        for j in range(2 * n):
            aug[col][j] /= pivot

        # Eliminate column
        for i in range(n):
            if i != col:
                factor = aug[i][col]
                for j in range(2 * n):
                    aug[i][j] -= factor * aug[col][j]

    result = [row[n:] for row in aug]
    return [[round(x, 10) if abs(x) > 1e-12 else 0.0 for x in row] for row in result]


# ---------------------------------------------------------------------------
# Variant 2 -- Recursive cofactor expansion (any NxN)
# ---------------------------------------------------------------------------

def inverse_cofactor_nxn(matrix: list[list[float]]) -> list[list[float]]:
    """
    Generalized cofactor expansion inverse for any NxN matrix.
    O(n! * n) time -- only practical for small matrices.

    >>> inverse_cofactor_nxn([[2, 5], [2, 0]])
    [[0.0, 0.5], [0.2, -0.2]]
    >>> inverse_cofactor_nxn([[1, 0], [0, 1]])
    [[1.0, 0.0], [0.0, 1.0]]
    """
    n = len(matrix)

    def det(m: list[list[float]]) -> float:
        if len(m) == 1:
            return m[0][0]
        if len(m) == 2:
            return m[0][0] * m[1][1] - m[0][1] * m[1][0]
        return sum(
            ((-1) ** j) * m[0][j] * det([row[:j] + row[j+1:] for row in m[1:]])
            for j in range(len(m))
        )

    d = det(matrix)
    if abs(d) < 1e-12:
        raise ValueError("Matrix is singular.")

    # Cofactor matrix
    cofactors = []
    for i in range(n):
        row = []
        for j in range(n):
            minor = [r[:j] + r[j+1:] for r in (matrix[:i] + matrix[i+1:])]
            row.append(((-1) ** (i + j)) * det(minor))
        cofactors.append(row)

    # Transpose (adjugate) and divide by determinant
    return [
        [round(cofactors[j][i] / d, 10) if abs(cofactors[j][i] / d) > 1e-12 else 0.0
         for j in range(n)]
        for i in range(n)
    ]


# ---------------------------------------------------------------------------
# Variant 3 -- Direct 2x2 formula (no Decimal overhead)
# ---------------------------------------------------------------------------

def inverse_2x2_direct(matrix: list[list[float]]) -> list[list[float]]:
    """
    Direct 2x2 inverse without Decimal: A^(-1) = (1/det) * [[d, -b], [-c, a]].
    Fastest for 2x2 matrices.

    >>> inverse_2x2_direct([[2, 5], [2, 0]])
    [[0.0, 0.5], [0.2, -0.2]]
    >>> inverse_2x2_direct([[1, 0], [0, 1]])
    [[1.0, 0.0], [0.0, 1.0]]
    >>> result = inverse_2x2_direct([[10, 5], [3, 2.5]])
    >>> [[round(x, 10) for x in row] for row in result]
    [[0.25, -0.5], [-0.3, 1.0]]
    """
    a, b = matrix[0]
    c, d = matrix[1]
    det = a * d - b * c
    if det == 0:
        raise ValueError("Matrix is singular.")
    inv_det = 1.0 / det
    return [
        [d * inv_det or 0.0, -b * inv_det or 0.0],
        [-c * inv_det or 0.0, a * inv_det or 0.0],
    ]


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    m2 = [[2, 5], [2, 0]]
    m3 = [[2, 5, 7], [2, 0, 1], [1, 2, 3]]
    number = 100_000
    print(f"Benchmark ({number} inversions):\n")

    print("2x2 matrix:")
    funcs_2x2 = [
        ("reference (Decimal)", lambda: reference(m2)),
        ("gauss_jordan", lambda: inverse_gauss_jordan(m2)),
        ("cofactor_nxn", lambda: inverse_cofactor_nxn(m2)),
        ("direct_2x2 (no Decimal)", lambda: inverse_2x2_direct(m2)),
    ]
    for name, func in funcs_2x2:
        t = timeit.timeit(func, number=number)
        print(f"  {name:35s} {t:.4f}s")

    print("\n3x3 matrix:")
    funcs_3x3 = [
        ("reference (Decimal)", lambda: reference(m3)),
        ("gauss_jordan", lambda: inverse_gauss_jordan(m3)),
        ("cofactor_nxn", lambda: inverse_cofactor_nxn(m3)),
    ]
    for name, func in funcs_3x3:
        t = timeit.timeit(func, number=number)
        print(f"  {name:35s} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
