#!/usr/bin/env python3
"""
Optimized and alternative implementations of Matrix Rank computation.

The reference computes rank via Gaussian elimination with row reduction.
Rank = number of linearly independent rows (or columns).

Three variants:
  svd_rank         — rank via Singular Value Decomposition (most robust)
  rref_rank        — rank via Reduced Row Echelon Form (RREF)
  numpy_matrix_rank — delegates to np.linalg.matrix_rank (SVD-based)

Key interview insight:
    Gaussian elimination can fail on matrices where rounding errors accumulate
    (e.g., nearly singular matrices).  SVD-based rank is numerically the most
    robust: count singular values above a tolerance.  np.linalg.matrix_rank
    uses this approach internally.

Run:
    python linear_algebra/rank_of_matrix_optimized.py
"""

from __future__ import annotations

import copy
import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from linear_algebra.rank_of_matrix import rank_of_matrix as reference


# ---------------------------------------------------------------------------
# Variant 1 — svd_rank: rank via singular value decomposition
# ---------------------------------------------------------------------------
def svd_rank(matrix: list[list[float]], tol: float = 1e-10) -> int:
    """
    Compute matrix rank using SVD. Count singular values above tolerance.

    >>> svd_rank([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    2
    >>> svd_rank([[1, 0, 0], [0, 1, 0], [0, 0, 0]])
    2
    >>> svd_rank([[1]])
    1
    >>> svd_rank([[]])
    0
    """
    A = np.array(matrix, dtype=float)
    if A.size == 0:
        return 0
    singular_values = np.linalg.svd(A, compute_uv=False)
    return int(np.sum(singular_values > tol))


# ---------------------------------------------------------------------------
# Variant 2 — rref_rank: rank via reduced row echelon form
# ---------------------------------------------------------------------------
def rref_rank(matrix: list[list[float]], tol: float = 1e-10) -> int:
    """
    Compute rank via RREF (full row reduction, not just upper triangular).

    >>> rref_rank([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    2
    >>> rref_rank([[2, 3, -1, -1], [1, -1, -2, 4], [3, 1, 3, -2], [6, 3, 0, -7]])
    4
    >>> rref_rank([[3, 2, 1], [-6, -4, -2]])
    1
    >>> rref_rank([[]])
    0
    """
    A = [row[:] for row in matrix]  # deep copy
    rows = len(A)
    cols = len(A[0]) if rows > 0 else 0
    if cols == 0:
        return 0

    pivot_row = 0
    for col in range(cols):
        if pivot_row >= rows:
            break

        # Find pivot
        max_row = max(range(pivot_row, rows), key=lambda r: abs(A[r][col]))
        if abs(A[max_row][col]) < tol:
            continue

        # Swap
        A[pivot_row], A[max_row] = A[max_row], A[pivot_row]

        # Scale
        scale = A[pivot_row][col]
        A[pivot_row] = [v / scale for v in A[pivot_row]]

        # Eliminate all other rows (full RREF)
        for r in range(rows):
            if r != pivot_row and abs(A[r][col]) > tol:
                factor = A[r][col]
                A[r] = [A[r][j] - factor * A[pivot_row][j] for j in range(cols)]

        pivot_row += 1

    return pivot_row


# ---------------------------------------------------------------------------
# Variant 3 — numpy_matrix_rank: direct delegation
# ---------------------------------------------------------------------------
def numpy_matrix_rank(matrix: list[list[float]]) -> int:
    """
    Compute rank via numpy.linalg.matrix_rank (SVD-based).

    >>> numpy_matrix_rank([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    2
    >>> numpy_matrix_rank([[1, 0, 0], [0, 1, 0], [0, 0, 0]])
    2
    >>> numpy_matrix_rank([[1]])
    1
    """
    A = np.array(matrix, dtype=float)
    if A.size == 0:
        return 0
    return int(np.linalg.matrix_rank(A))


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    """Compare all variants on various matrices."""
    rng = np.random.default_rng(42)
    n = 100

    # Full rank matrix
    A_full = rng.normal(size=(n, n)).tolist()
    # Rank-deficient matrix (rank ~50)
    R = rng.normal(size=(n, 50))
    A_low = (R @ R.T).tolist()

    number = 50

    print(f"Rank of Matrix Benchmark ({n}x{n}, {number} runs)")
    print(f"{'Variant':<25} {'Total (s)':>10} {'Speedup':>10}")
    print("-" * 47)

    for label, mat in [("full rank", A_full), ("rank ~50", A_low)]:
        print(f"\n--- {label} ---")
        t_ref = timeit.timeit(lambda: reference(copy.deepcopy(mat)), number=number)
        t_svd = timeit.timeit(lambda: svd_rank(mat), number=number)
        t_rref = timeit.timeit(lambda: rref_rank(mat), number=number)
        t_np = timeit.timeit(lambda: numpy_matrix_rank(mat), number=number)

        for name, t in [
            ("reference (gauss elim)", t_ref),
            ("svd_rank", t_svd),
            ("rref_rank", t_rref),
            ("numpy_matrix_rank", t_np),
        ]:
            speedup = t_ref / t if t > 0 else float("inf")
            print(f"{name:<25} {t:>10.4f} {speedup:>9.1f}x")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
