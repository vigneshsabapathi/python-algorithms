#!/usr/bin/env python3
"""
Optimized and alternative implementations of the Jacobi Iteration Method.

The Jacobi method iteratively solves Ax = b for diagonally dominant A by
splitting A = D + R, then iterating x^{k+1} = D^{-1}(b - Rx^k).
The reference uses vectorised NumPy with boolean masks.

Three variants:
  pure_python    — no NumPy, explicit loops (interview-style implementation)
  gauss_seidel   — uses newest values immediately (faster convergence, same cost)
  numpy_vectorized — fully vectorized with matrix ops (no Python loops in iteration)

Key interview insight:
    Gauss-Seidel converges ~2x faster than Jacobi for the same matrix because it
    uses updated values within the same iteration. Both require diagonal dominance
    (or SPD for Gauss-Seidel) for guaranteed convergence.

Run:
    python linear_algebra/jacobi_iteration_method_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

import numpy as np
from numpy import float64
from numpy.typing import NDArray

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from linear_algebra.jacobi_iteration_method import jacobi_iteration_method as reference


# ---------------------------------------------------------------------------
# Variant 1 — pure_python: no NumPy, explicit loops
# ---------------------------------------------------------------------------
def jacobi_pure_python(
    coefficients: list[list[float]],
    constants: list[float],
    init_val: list[float],
    iterations: int,
) -> list[float]:
    """
    Pure Python Jacobi iteration — no external libraries.

    >>> jacobi_pure_python(
    ...     [[4, 1, 1], [1, 5, 2], [1, 2, 4]],
    ...     [2, -6, -4],
    ...     [0.5, -0.5, -0.5],
    ...     3
    ... )
    [0.909375, -1.14375, -0.7484375]
    """
    n = len(constants)
    x = list(init_val)
    for _ in range(iterations):
        x_new = [0.0] * n
        for i in range(n):
            sigma = sum(coefficients[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (constants[i] - sigma) / coefficients[i][i]
        x = x_new
    return x


# ---------------------------------------------------------------------------
# Variant 2 — gauss_seidel: use newest values immediately
# ---------------------------------------------------------------------------
def gauss_seidel(
    coefficients: list[list[float]],
    constants: list[float],
    init_val: list[float],
    iterations: int,
) -> list[float]:
    """
    Gauss-Seidel method — uses updated values within the same iteration.
    Converges faster than Jacobi for diagonally dominant systems.

    >>> gauss_seidel(
    ...     [[4, 1, 1], [1, 5, 2], [1, 2, 4]],
    ...     [2, -6, -4],
    ...     [0.5, -0.5, -0.5],
    ...     3
    ... )
    [0.9516796875, -1.1248984375, -0.675470703125]
    """
    n = len(constants)
    x = list(init_val)
    for _ in range(iterations):
        for i in range(n):
            sigma = sum(coefficients[i][j] * x[j] for j in range(n) if j != i)
            x[i] = (constants[i] - sigma) / coefficients[i][i]
    return x


# ---------------------------------------------------------------------------
# Variant 3 — numpy_vectorized: matrix-form iteration
# ---------------------------------------------------------------------------
def jacobi_numpy_vectorized(
    coefficient_matrix: NDArray[float64],
    constant_matrix: NDArray[float64],
    init_val: list[float],
    iterations: int,
) -> list[float]:
    """
    Fully vectorized Jacobi using D^{-1}(b - Rx) matrix form.

    >>> import numpy as np
    >>> jacobi_numpy_vectorized(
    ...     np.array([[4, 1, 1], [1, 5, 2], [1, 2, 4]]),
    ...     np.array([[2], [-6], [-4]]),
    ...     [0.5, -0.5, -0.5],
    ...     3
    ... )
    [0.909375, -1.14375, -0.7484375]
    """
    A = np.array(coefficient_matrix, dtype=float)
    b = np.array(constant_matrix, dtype=float).flatten()
    x = np.array(init_val, dtype=float)
    n = len(b)

    D_inv = np.diag(1.0 / np.diag(A))
    R = A - np.diag(np.diag(A))

    for _ in range(iterations):
        x = D_inv @ (b - R @ x)

    return x.tolist()


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    """Compare all variants on a 50x50 diagonally dominant system."""
    rng = np.random.default_rng(42)
    n = 50
    iters = 100

    # Create diagonally dominant matrix
    A = rng.normal(size=(n, n))
    A = A + A.T  # symmetric
    np.fill_diagonal(A, np.sum(np.abs(A), axis=1) + 1)
    b = rng.normal(size=(n, 1))

    A_list = A.tolist()
    b_flat = b.flatten().tolist()
    init = [0.0] * n

    number = 20

    t_ref = timeit.timeit(
        lambda: reference(A, b, init[:], iters), number=number
    )
    t_pp = timeit.timeit(
        lambda: jacobi_pure_python(A_list, b_flat, init[:], iters), number=number
    )
    t_gs = timeit.timeit(
        lambda: gauss_seidel(A_list, b_flat, init[:], iters), number=number
    )
    t_nv = timeit.timeit(
        lambda: jacobi_numpy_vectorized(A, b, init[:], iters), number=number
    )

    print(f"Jacobi Iteration Benchmark ({n}x{n} system, {iters} iterations, {number} runs)")
    print(f"{'Variant':<25} {'Total (s)':>10} {'Speedup':>10}")
    print("-" * 47)
    for name, t in [
        ("reference (numpy masks)", t_ref),
        ("pure_python", t_pp),
        ("gauss_seidel", t_gs),
        ("numpy_vectorized (D^-1)", t_nv),
    ]:
        speedup = t_ref / t if t > 0 else float("inf")
        print(f"{name:<25} {t:>10.4f} {speedup:>9.1f}x")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
