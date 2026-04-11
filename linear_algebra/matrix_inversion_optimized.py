#!/usr/bin/env python3
"""
Optimized and alternative implementations of Matrix Inversion.

The reference delegates to np.linalg.inv which uses LAPACK dgetri (LU-based).
Here we implement from-scratch alternatives for interview practice.

Three variants:
  gauss_jordan     — augment [A|I], row-reduce to [I|A^{-1}] (classic interview)
  adjugate_method  — A^{-1} = adj(A)/det(A) using cofactors (O(n!), educational)
  scipy_inv        — scipy.linalg.inv with LAPACK (handles edge cases, check=True)

Key interview insight:
    Gauss-Jordan is O(n^3) and the expected "from scratch" answer.
    The adjugate/cofactor method is O(n!) via Laplace expansion — never use in
    practice but shows deep understanding.  np.linalg.inv is O(n^3) via LU.

Run:
    python linear_algebra/matrix_inversion_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from linear_algebra.matrix_inversion import invert_matrix as reference


# ---------------------------------------------------------------------------
# Variant 1 — gauss_jordan: augment [A|I] and row-reduce
# ---------------------------------------------------------------------------
def gauss_jordan_inverse(matrix: list[list[float]]) -> list[list[float]]:
    """
    Matrix inversion via Gauss-Jordan elimination.
    Augments [A|I] and reduces to [I|A^{-1}].

    >>> result = gauss_jordan_inverse([[4.0, 7.0], [2.0, 6.0]])
    >>> [[round(v, 4) for v in row] for row in result]
    [[0.6, -0.7], [-0.2, 0.4]]
    >>> gauss_jordan_inverse([[1.0, 2.0], [2.0, 4.0]])
    Traceback (most recent call last):
        ...
    ValueError: Matrix is singular and cannot be inverted
    """
    n = len(matrix)
    # Build augmented matrix [A | I]
    aug = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(matrix)]

    for col in range(n):
        # Find pivot
        max_row = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[max_row][col]) < 1e-12:
            raise ValueError("Matrix is singular and cannot be inverted")
        aug[col], aug[max_row] = aug[max_row], aug[col]

        # Scale pivot row
        pivot = aug[col][col]
        aug[col] = [v / pivot for v in aug[col]]

        # Eliminate column
        for row in range(n):
            if row != col:
                factor = aug[row][col]
                aug[row] = [aug[row][j] - factor * aug[col][j] for j in range(2 * n)]

    # Extract right half
    return [row[n:] for row in aug]


# ---------------------------------------------------------------------------
# Variant 2 — adjugate_method: A^{-1} = adj(A) / det(A)
# ---------------------------------------------------------------------------
def _minor(matrix: list[list[float]], i: int, j: int) -> list[list[float]]:
    """Return the minor matrix with row i and column j removed."""
    return [row[:j] + row[j + 1:] for k, row in enumerate(matrix) if k != i]


def _determinant(matrix: list[list[float]]) -> float:
    """Recursive determinant via Laplace expansion."""
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    det = 0.0
    for j in range(n):
        det += ((-1) ** j) * matrix[0][j] * _determinant(_minor(matrix, 0, j))
    return det


def adjugate_inverse(matrix: list[list[float]]) -> list[list[float]]:
    """
    Matrix inversion via adjugate: A^{-1} = adj(A) / det(A).
    O(n!) due to recursive determinant — educational only.

    >>> result = adjugate_inverse([[4.0, 7.0], [2.0, 6.0]])
    >>> [[round(v, 4) for v in row] for row in result]
    [[0.6, -0.7], [-0.2, 0.4]]
    >>> adjugate_inverse([[1.0, 2.0], [2.0, 4.0]])
    Traceback (most recent call last):
        ...
    ValueError: Matrix is singular (det=0)
    """
    n = len(matrix)
    det = _determinant(matrix)
    if abs(det) < 1e-12:
        raise ValueError("Matrix is singular (det=0)")

    # Cofactor matrix
    cofactors = [
        [((-1) ** (i + j)) * _determinant(_minor(matrix, i, j)) for j in range(n)]
        for i in range(n)
    ]

    # Adjugate = transpose of cofactor matrix
    adjugate = [[cofactors[j][i] / det for j in range(n)] for i in range(n)]
    return adjugate


# ---------------------------------------------------------------------------
# Variant 3 — scipy_inv: LAPACK with error checking
# ---------------------------------------------------------------------------
def scipy_inverse(matrix: list[list[float]]) -> list[list[float]]:
    """
    Matrix inversion via scipy.linalg.inv (LAPACK dgetri).

    >>> result = scipy_inverse([[4.0, 7.0], [2.0, 6.0]])
    >>> [[round(v, 4) for v in row] for row in result]
    [[0.6, -0.7], [-0.2, 0.4]]
    """
    from scipy.linalg import inv

    A = np.array(matrix, dtype=float)
    return inv(A).tolist()


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    """Compare all variants on various matrix sizes."""
    rng = np.random.default_rng(42)

    # Use small n for adjugate (it's O(n!))
    print("Matrix Inversion Benchmark")
    print(f"{'Variant':<25} {'Size':>5} {'Total (s)':>10} {'Speedup':>10}")
    print("-" * 55)

    # Large matrix benchmark (skip adjugate)
    n = 50
    A = rng.normal(size=(n, n))
    A = A + np.eye(n) * n  # ensure invertibility
    A_list = A.tolist()
    number = 100

    t_ref = timeit.timeit(lambda: reference(A_list), number=number)
    t_gj = timeit.timeit(lambda: gauss_jordan_inverse(A_list), number=number)
    t_sp = timeit.timeit(lambda: scipy_inverse(A_list), number=number)

    for name, t in [
        ("reference (np.linalg)", t_ref),
        ("gauss_jordan", t_gj),
        ("scipy_inv (LAPACK)", t_sp),
    ]:
        speedup = t_ref / t if t > 0 else float("inf")
        print(f"{name:<25} {n:>5} {t:>10.4f} {speedup:>9.1f}x")

    # Small matrix for adjugate comparison
    n_small = 8
    A_small = rng.normal(size=(n_small, n_small))
    A_small = A_small + np.eye(n_small) * n_small
    A_small_list = A_small.tolist()
    number_small = 50

    t_ref_s = timeit.timeit(lambda: reference(A_small_list), number=number_small)
    t_adj = timeit.timeit(lambda: adjugate_inverse(A_small_list), number=number_small)

    print(f"{'adjugate (O(n!))':<25} {n_small:>5} {t_adj:>10.4f} {t_ref_s / t_adj if t_adj > 0 else 0:>9.1f}x")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
