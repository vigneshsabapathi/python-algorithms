#!/usr/bin/env python3
"""
Optimized and alternative implementations of Gaussian Elimination.

Gaussian elimination reduces a system Ax = b to upper-triangular form,
then solves via back-substitution.  The reference implementation builds
an augmented matrix and eliminates row by row — O(n^3) time, O(n^2) space.

Three variants:
  partial_pivoting — swaps rows to pick the largest pivot (numerically stable)
  scaled_pivoting  — normalizes by row max before selecting pivot (best stability)
  numpy_solve      — delegates to np.linalg.solve (LAPACK dgesv — production-grade)

Key interview insight:
    Naive Gaussian elimination fails on zero pivots and amplifies rounding errors.
    Partial pivoting is the minimal fix interviewers expect you to mention.
    Scaled partial pivoting is the gold standard for hand-coded solvers.

Run:
    python linear_algebra/gaussian_elimination_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

import numpy as np
from numpy import float64
from numpy.typing import NDArray

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from linear_algebra.gaussian_elimination import gaussian_elimination as reference


# ---------------------------------------------------------------------------
# Variant 1 — partial_pivoting: swap rows to maximize |pivot|
# ---------------------------------------------------------------------------
def gaussian_partial_pivoting(
    coefficients: list[list[float]], vector: list[list[float]]
) -> NDArray[float64]:
    """
    Gaussian elimination with partial pivoting.

    >>> gaussian_partial_pivoting([[1, -4, -2], [5, 2, -2], [1, -1, 0]], [[-2], [-3], [4]])
    array([ 2.3 , -1.7 ,  5.55])
    >>> gaussian_partial_pivoting([[1, 2], [5, 2]], [[5], [5]])
    array([0. , 2.5])
    """
    A = np.array(coefficients, dtype=float)
    b = np.array(vector, dtype=float).flatten()
    n = len(b)

    # Forward elimination with partial pivoting
    for col in range(n):
        # Find pivot row
        max_row = col + np.argmax(np.abs(A[col:, col]))
        if max_row != col:
            A[[col, max_row]] = A[[max_row, col]]
            b[[col, max_row]] = b[[max_row, col]]

        for row in range(col + 1, n):
            factor = A[row, col] / A[col, col]
            A[row, col:] -= factor * A[col, col:]
            b[row] -= factor * b[col]

    # Back substitution
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i, i]

    return x


# ---------------------------------------------------------------------------
# Variant 2 — scaled_pivoting: normalize by row max before pivot selection
# ---------------------------------------------------------------------------
def gaussian_scaled_pivoting(
    coefficients: list[list[float]], vector: list[list[float]]
) -> NDArray[float64]:
    """
    Gaussian elimination with scaled partial pivoting.

    >>> gaussian_scaled_pivoting([[1, -4, -2], [5, 2, -2], [1, -1, 0]], [[-2], [-3], [4]])
    array([ 2.3 , -1.7 ,  5.55])
    >>> gaussian_scaled_pivoting([[1, 2], [5, 2]], [[5], [5]])
    array([0. , 2.5])
    """
    A = np.array(coefficients, dtype=float)
    b = np.array(vector, dtype=float).flatten()
    n = len(b)

    # Scale factors: max absolute value in each row
    scales = np.max(np.abs(A), axis=1)

    for col in range(n):
        # Find pivot row using scaled ratios
        ratios = np.abs(A[col:, col]) / scales[col:]
        max_row = col + np.argmax(ratios)
        if max_row != col:
            A[[col, max_row]] = A[[max_row, col]]
            b[[col, max_row]] = b[[max_row, col]]
            scales[[col, max_row]] = scales[[max_row, col]]

        for row in range(col + 1, n):
            factor = A[row, col] / A[col, col]
            A[row, col:] -= factor * A[col, col:]
            b[row] -= factor * b[col]

    # Back substitution
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i, i]

    return x


# ---------------------------------------------------------------------------
# Variant 3 — numpy_solve: delegates to LAPACK dgesv
# ---------------------------------------------------------------------------
def gaussian_numpy_solve(
    coefficients: list[list[float]], vector: list[list[float]]
) -> NDArray[float64]:
    """
    Solve using numpy.linalg.solve (LAPACK under the hood).

    >>> gaussian_numpy_solve([[1, -4, -2], [5, 2, -2], [1, -1, 0]], [[-2], [-3], [4]])
    array([ 2.3 , -1.7 ,  5.55])
    >>> gaussian_numpy_solve([[1, 2], [5, 2]], [[5], [5]])
    array([0. , 2.5])
    """
    A = np.array(coefficients, dtype=float)
    b = np.array(vector, dtype=float).flatten()
    return np.linalg.solve(A, b)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    """Compare all variants on a 100x100 random system."""
    rng = np.random.default_rng(42)
    n = 100
    A = rng.normal(size=(n, n))
    b = rng.normal(size=(n, 1))
    A_list = A.tolist()
    b_list = b.tolist()

    number = 50

    t_ref = timeit.timeit(lambda: reference(A_list, b_list), number=number)
    t_pp = timeit.timeit(lambda: gaussian_partial_pivoting(A_list, b_list), number=number)
    t_sp = timeit.timeit(lambda: gaussian_scaled_pivoting(A_list, b_list), number=number)
    t_np = timeit.timeit(lambda: gaussian_numpy_solve(A_list, b_list), number=number)

    print(f"Gaussian Elimination Benchmark ({n}x{n} system, {number} runs)")
    print(f"{'Variant':<25} {'Total (s)':>10} {'Speedup':>10}")
    print("-" * 47)
    for name, t in [
        ("reference (naive)", t_ref),
        ("partial_pivoting", t_pp),
        ("scaled_pivoting", t_sp),
        ("numpy_solve (LAPACK)", t_np),
    ]:
        speedup = t_ref / t if t > 0 else float("inf")
        print(f"{name:<25} {t:>10.4f} {speedup:>9.1f}x")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
