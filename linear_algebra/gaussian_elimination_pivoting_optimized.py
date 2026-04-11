#!/usr/bin/env python3
"""
Optimized and alternative implementations of Gaussian Elimination with Pivoting.

The reference implements partial pivoting with back-substitution.

Three variants:
  complete_pivoting — pivots on both rows and columns (maximum stability)
  lu_factored_solve — factorize once, solve for multiple right-hand sides
  numpy_lstsq       — least-squares solver (works even for non-square systems)

Key interview insight:
    Complete pivoting swaps both rows AND columns to find the globally largest
    element.  It's O(n^3) but with higher constant — used only when partial
    pivoting isn't stable enough (rare in practice).

Run:
    python linear_algebra/gaussian_elimination_pivoting_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from linear_algebra.gaussian_elimination_pivoting import solve_linear_system as reference


# ---------------------------------------------------------------------------
# Variant 1 — complete_pivoting: pivot on rows AND columns
# ---------------------------------------------------------------------------
def complete_pivoting_solve(matrix: np.ndarray) -> np.ndarray:
    """
    Gaussian elimination with complete pivoting.

    >>> import numpy as np
    >>> A = np.array([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], dtype=float)
    >>> B = np.array([8, -11, -3], dtype=float)
    >>> solution = complete_pivoting_solve(np.column_stack((A, B)))
    >>> np.allclose(solution, [2., 3., -1.])
    True
    """
    ab = np.copy(matrix).astype(float)
    n = ab.shape[0]
    col_order = list(range(n))  # track column swaps

    # Forward elimination
    for k in range(n):
        # Find maximum element in submatrix
        sub = np.abs(ab[k:, k:n])
        max_idx = np.unravel_index(np.argmax(sub), sub.shape)
        pivot_row, pivot_col = max_idx[0] + k, max_idx[1] + k

        if abs(ab[pivot_row, pivot_col]) < 1e-12:
            raise ValueError("Matrix is singular")

        # Swap rows and columns
        if pivot_row != k:
            ab[[k, pivot_row]] = ab[[pivot_row, k]]
        if pivot_col != k:
            ab[:, [k, pivot_col]] = ab[:, [pivot_col, k]]
            col_order[k], col_order[pivot_col] = col_order[pivot_col], col_order[k]

        # Eliminate
        for i in range(k + 1, n):
            factor = ab[i, k] / ab[k, k]
            ab[i, k:] -= factor * ab[k, k:]

    # Back substitution
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (ab[i, -1] - np.dot(ab[i, i + 1:n], x[i + 1:])) / ab[i, i]

    # Undo column permutation
    result = np.zeros(n)
    for i in range(n):
        result[col_order[i]] = x[i]

    return result


# ---------------------------------------------------------------------------
# Variant 2 — lu_factored_solve: factor once, solve many
# ---------------------------------------------------------------------------
def lu_factored_solve(matrix: np.ndarray) -> np.ndarray:
    """
    Factor A = PLU once, then solve via forward/back substitution.

    >>> import numpy as np
    >>> A = np.array([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], dtype=float)
    >>> B = np.array([8, -11, -3], dtype=float)
    >>> solution = lu_factored_solve(np.column_stack((A, B)))
    >>> np.allclose(solution, [2., 3., -1.])
    True
    """
    from scipy.linalg import lu_factor, lu_solve

    ab = np.copy(matrix).astype(float)
    n = ab.shape[0]
    A = ab[:, :n]
    b = ab[:, -1]

    lu, piv = lu_factor(A)
    return lu_solve((lu, piv), b)


# ---------------------------------------------------------------------------
# Variant 3 — numpy_lstsq: least-squares (robust, handles rank deficiency)
# ---------------------------------------------------------------------------
def numpy_lstsq_solve(matrix: np.ndarray) -> np.ndarray:
    """
    Solve using numpy least-squares (works for over/underdetermined too).

    >>> import numpy as np
    >>> A = np.array([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], dtype=float)
    >>> B = np.array([8, -11, -3], dtype=float)
    >>> solution = numpy_lstsq_solve(np.column_stack((A, B)))
    >>> np.allclose(solution, [2., 3., -1.])
    True
    """
    ab = np.copy(matrix).astype(float)
    n = ab.shape[0]
    A = ab[:, :n]
    b = ab[:, -1]
    x, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    return x


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    """Compare all variants on a 100x100 system."""
    rng = np.random.default_rng(42)
    n = 100
    A = rng.normal(size=(n, n))
    b = rng.normal(size=n)
    matrix = np.column_stack((A, b))

    number = 50

    t_ref = timeit.timeit(lambda: reference(matrix.copy()), number=number)
    t_cp = timeit.timeit(lambda: complete_pivoting_solve(matrix.copy()), number=number)
    t_lu = timeit.timeit(lambda: lu_factored_solve(matrix.copy()), number=number)
    t_ls = timeit.timeit(lambda: numpy_lstsq_solve(matrix.copy()), number=number)

    print(f"Gaussian Elimination Pivoting Benchmark ({n}x{n}, {number} runs)")
    print(f"{'Variant':<25} {'Total (s)':>10} {'Speedup':>10}")
    print("-" * 47)
    for name, t in [
        ("reference (partial)", t_ref),
        ("complete_pivoting", t_cp),
        ("lu_factored_solve", t_lu),
        ("numpy_lstsq", t_ls),
    ]:
        speedup = t_ref / t if t > 0 else float("inf")
        print(f"{name:<25} {t:>10.4f} {speedup:>9.1f}x")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
