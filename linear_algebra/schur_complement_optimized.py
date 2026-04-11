#!/usr/bin/env python3
"""
Optimized and alternative implementations of the Schur Complement.

For a block matrix X = [[A, B], [B^T, C]], the Schur complement of A is:
    S = C - B^T A^{-1} B

The reference computes A^{-1} explicitly via np.linalg.inv.

Three variants:
  solve_based       — avoid explicit inverse: solve AX=B then compute C - B^T X
  cholesky_based    — when A is SPD, use Cholesky for efficiency and stability
  woodbury_update   — incremental Schur complement update (rank-1 change to A)

Key interview insight:
    NEVER compute A^{-1} explicitly if you can avoid it.  np.linalg.solve(A, B)
    uses LU factorization and is both faster AND more numerically stable.
    The Schur complement appears in: block matrix inversion, Gaussian elimination
    on block matrices, saddle point systems, and convex optimization (LMIs).

Run:
    python linear_algebra/schur_complement_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from linear_algebra.schur_complement import schur_complement as reference


# ---------------------------------------------------------------------------
# Variant 1 — solve_based: avoid explicit inverse
# ---------------------------------------------------------------------------
def schur_solve_based(
    mat_a: np.ndarray,
    mat_b: np.ndarray,
    mat_c: np.ndarray,
) -> np.ndarray:
    """
    Schur complement via solve (no explicit inverse).
    S = C - B^T A^{-1} B  computed as C - B^T @ solve(A, B)

    >>> import numpy as np
    >>> a = np.array([[1, 2], [2, 1]], dtype=float)
    >>> b = np.array([[0, 3], [3, 0]], dtype=float)
    >>> c = np.array([[2, 1], [6, 3]], dtype=float)
    >>> schur_solve_based(a, b, c)
    array([[ 5., -5.],
           [ 0.,  6.]])
    """
    X = np.linalg.solve(mat_a, mat_b)  # A^{-1} B without forming A^{-1}
    return mat_c - mat_b.T @ X


# ---------------------------------------------------------------------------
# Variant 2 — cholesky_based: when A is SPD
# ---------------------------------------------------------------------------
def schur_cholesky(
    mat_a: np.ndarray,
    mat_b: np.ndarray,
    mat_c: np.ndarray,
) -> np.ndarray:
    """
    Schur complement via Cholesky factorization (A must be SPD).
    S = C - B^T A^{-1} B using L L^T = A.

    >>> import numpy as np
    >>> a = np.array([[4, 2], [2, 3]], dtype=float)  # SPD
    >>> b = np.array([[1, 0], [0, 1]], dtype=float)
    >>> c = np.array([[5, 1], [1, 5]], dtype=float)
    >>> S = schur_cholesky(a, b, c)
    >>> expected = c - b.T @ np.linalg.inv(a) @ b
    >>> np.allclose(S, expected)
    True
    """
    from scipy.linalg import cho_factor, cho_solve

    cho, low = cho_factor(mat_a)
    X = cho_solve((cho, low), mat_b)
    return mat_c - mat_b.T @ X


# ---------------------------------------------------------------------------
# Variant 3 — block_determinant: use Schur to compute block matrix determinant
# ---------------------------------------------------------------------------
def block_determinant(
    mat_a: np.ndarray,
    mat_b: np.ndarray,
    mat_c: np.ndarray,
) -> float:
    """
    Compute determinant of block matrix [[A, B], [B^T, C]] using Schur complement.
    det(X) = det(A) * det(S) where S is the Schur complement.

    >>> import numpy as np
    >>> a = np.array([[1, 2], [2, 1]], dtype=float)
    >>> b = np.array([[0, 3], [3, 0]], dtype=float)
    >>> c = np.array([[2, 1], [6, 3]], dtype=float)
    >>> X = np.block([[a, b], [b.T, c]])
    >>> abs(block_determinant(a, b, c) - np.linalg.det(X)) < 1e-6
    True
    """
    S = schur_solve_based(mat_a, mat_b, mat_c)
    return float(np.linalg.det(mat_a) * np.linalg.det(S))


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    """Compare all variants."""
    rng = np.random.default_rng(42)
    n_a, n_b = 100, 50

    A = rng.normal(size=(n_a, n_a))
    A = A @ A.T + np.eye(n_a)  # SPD
    B = rng.normal(size=(n_a, n_b))
    C = rng.normal(size=(n_b, n_b))
    C = C + C.T

    number = 100

    t_ref = timeit.timeit(lambda: reference(A, B, C), number=number)
    t_solve = timeit.timeit(lambda: schur_solve_based(A, B, C), number=number)
    t_chol = timeit.timeit(lambda: schur_cholesky(A, B, C), number=number)
    t_det = timeit.timeit(lambda: block_determinant(A, B, C), number=number)

    print(f"Schur Complement Benchmark (A:{n_a}x{n_a}, B:{n_a}x{n_b}, {number} runs)")
    print(f"{'Variant':<25} {'Total (s)':>10} {'Speedup':>10}")
    print("-" * 47)
    for name, t in [
        ("reference (explicit inv)", t_ref),
        ("solve_based (no inv)", t_solve),
        ("cholesky_based (SPD)", t_chol),
        ("block_determinant", t_det),
    ]:
        speedup = t_ref / t if t > 0 else float("inf")
        print(f"{name:<25} {t:>10.4f} {speedup:>9.1f}x")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
