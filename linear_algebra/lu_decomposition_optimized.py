#!/usr/bin/env python3
"""
Optimized and alternative implementations of LU Decomposition.

LU decomposition factors A = LU where L is lower-triangular (ones on diagonal)
and U is upper-triangular.  The reference uses nested loops with slice-dot products.

Three variants:
  doolittle_pure  — pure Python Doolittle method (no NumPy dependency)
  crout_method    — Crout decomposition (L has the diagonal, U has ones)
  scipy_lu        — delegates to scipy.linalg.lu (LAPACK with partial pivoting)

Key interview insight:
    Plain LU fails when a leading principal minor is zero.  In practice you always
    use PA = LU (with row permutations).  scipy.linalg.lu returns P, L, U and
    handles all edge cases via LAPACK dgetrf.

Run:
    python linear_algebra/lu_decomposition_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from linear_algebra.lu_decomposition import lower_upper_decomposition as reference


# ---------------------------------------------------------------------------
# Variant 1 — doolittle_pure: pure Python, no NumPy
# ---------------------------------------------------------------------------
def doolittle_pure(matrix: list[list[float]]) -> tuple[list[list[float]], list[list[float]]]:
    """
    Pure Python Doolittle LU decomposition.
    L has ones on diagonal, U has the pivots.

    >>> L, U = doolittle_pure([[2, -2, 1], [0, 1, 2], [5, 3, 1]])
    >>> [[round(v, 1) for v in row] for row in L]
    [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [2.5, 8.0, 1.0]]
    >>> [[round(v, 1) for v in row] for row in U]
    [[2.0, -2.0, 1.0], [0.0, 1.0, 2.0], [0.0, 0.0, -17.5]]
    """
    n = len(matrix)
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]

    for i in range(n):
        # Upper triangular
        for k in range(i, n):
            total = sum(L[i][j] * U[j][k] for j in range(i))
            U[i][k] = float(matrix[i][k]) - total

        # Lower triangular
        L[i][i] = 1.0
        for k in range(i + 1, n):
            total = sum(L[k][j] * U[j][i] for j in range(i))
            if U[i][i] == 0:
                raise ArithmeticError("No LU decomposition exists")
            L[k][i] = (matrix[k][i] - total) / U[i][i]

    return L, U


# ---------------------------------------------------------------------------
# Variant 2 — crout_method: L has diagonal values, U has ones on diagonal
# ---------------------------------------------------------------------------
def crout_method(matrix: list[list[float]]) -> tuple[list[list[float]], list[list[float]]]:
    """
    Crout decomposition: L holds the diagonal, U has ones on diagonal.

    >>> L, U = crout_method([[4, 3], [6, 3]])
    >>> [[round(v, 2) for v in row] for row in L]
    [[4.0, 0.0], [6.0, -1.5]]
    >>> [[round(v, 2) for v in row] for row in U]
    [[1.0, 0.75], [0.0, 1.0]]
    """
    n = len(matrix)
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]

    for j in range(n):
        U[j][j] = 1.0  # Crout: U diagonal = 1

        for i in range(j, n):
            total = sum(L[i][k] * U[k][j] for k in range(j))
            L[i][j] = float(matrix[i][j]) - total

        for i in range(j + 1, n):
            total = sum(L[j][k] * U[k][i] for k in range(j))
            if L[j][j] == 0:
                raise ArithmeticError("No Crout decomposition exists")
            U[j][i] = (matrix[j][i] - total) / L[j][j]

    return L, U


# ---------------------------------------------------------------------------
# Variant 3 — scipy_lu: PA = LU via LAPACK dgetrf
# ---------------------------------------------------------------------------
def scipy_lu(matrix: list[list[float]]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    LU decomposition with partial pivoting via scipy.

    >>> import numpy as np
    >>> P, L, U = scipy_lu([[2, -2, 1], [0, 1, 2], [5, 3, 1]])
    >>> np.allclose(P @ L @ U, [[2, -2, 1], [0, 1, 2], [5, 3, 1]])
    True
    """
    from scipy.linalg import lu

    A = np.array(matrix, dtype=float)
    P, L, U = lu(A)
    return P, L, U


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    """Compare all variants on a 100x100 random matrix."""
    rng = np.random.default_rng(42)
    n = 100
    A = rng.normal(size=(n, n))
    A_list = A.tolist()
    A_np = np.array(A)

    number = 50

    t_ref = timeit.timeit(lambda: reference(A_np), number=number)
    t_dp = timeit.timeit(lambda: doolittle_pure(A_list), number=number)
    t_cr = timeit.timeit(lambda: crout_method(A_list), number=number)
    t_sp = timeit.timeit(lambda: scipy_lu(A_list), number=number)

    print(f"LU Decomposition Benchmark ({n}x{n} matrix, {number} runs)")
    print(f"{'Variant':<25} {'Total (s)':>10} {'Speedup':>10}")
    print("-" * 47)
    for name, t in [
        ("reference (numpy loops)", t_ref),
        ("doolittle_pure", t_dp),
        ("crout_method", t_cr),
        ("scipy_lu (LAPACK)", t_sp),
    ]:
        speedup = t_ref / t if t > 0 else float("inf")
        print(f"{name:<25} {t:>10.4f} {speedup:>9.1f}x")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
