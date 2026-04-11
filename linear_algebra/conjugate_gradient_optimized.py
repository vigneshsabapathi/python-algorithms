#!/usr/bin/env python3
"""
Optimized and alternative implementations of the Conjugate Gradient method.

The reference implements the standard CG algorithm for SPD matrices.
CG finds x such that Ax = b in at most n iterations (exact arithmetic),
with O(n^2) per iteration (one matrix-vector product).

Three variants:
  preconditioned_cg — uses Jacobi (diagonal) preconditioner for faster convergence
  steepest_descent  — gradient descent baseline (CG without conjugate directions)
  numpy_solve       — np.linalg.solve (direct LU solver for comparison)

Key interview insight:
    CG is the go-to iterative solver for large sparse SPD systems.  Preconditioning
    (M^{-1}A x = M^{-1}b) reduces the condition number and cuts iterations dramatically.
    Jacobi preconditioner M = diag(A) is simplest; incomplete Cholesky is stronger.

Run:
    python linear_algebra/conjugate_gradient_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from linear_algebra.conjugate_gradient import conjugate_gradient as reference


# ---------------------------------------------------------------------------
# Variant 1 — preconditioned_cg: Jacobi (diagonal) preconditioner
# ---------------------------------------------------------------------------
def preconditioned_cg(
    A: np.ndarray,
    b: np.ndarray,
    max_iterations: int = 1000,
    tol: float = 1e-8,
) -> np.ndarray:
    """
    Preconditioned Conjugate Gradient with Jacobi preconditioner M = diag(A).

    >>> import numpy as np
    >>> A = np.array([
    ...     [8.73256573, -5.02034289, -2.68709226],
    ...     [-5.02034289,  3.78188322,  0.91980451],
    ...     [-2.68709226,  0.91980451,  1.94746467]])
    >>> b = np.array([[-5.80872761], [ 3.23807431], [ 1.95381422]])
    >>> x = preconditioned_cg(A, b)
    >>> np.allclose(x, [[-0.63114139], [-0.01561498], [0.13979294]], atol=1e-6)
    True
    """
    n = A.shape[0]
    M_inv = np.diag(1.0 / np.diag(A))  # Jacobi preconditioner

    x = np.zeros((n, 1))
    r = b - A @ x
    z = M_inv @ r
    p = z.copy()

    for _ in range(max_iterations):
        Ap = A @ p
        rz = float(r.T @ z)
        alpha = rz / float(p.T @ Ap)
        x = x + alpha * p
        r_new = r - alpha * Ap

        if np.linalg.norm(r_new) < tol:
            break

        z_new = M_inv @ r_new
        beta = float(r_new.T @ z_new) / rz
        p = z_new + beta * p
        r = r_new
        z = z_new

    return x


# ---------------------------------------------------------------------------
# Variant 2 — steepest_descent: gradient descent (CG without conjugation)
# ---------------------------------------------------------------------------
def steepest_descent(
    A: np.ndarray,
    b: np.ndarray,
    max_iterations: int = 1000,
    tol: float = 1e-8,
) -> np.ndarray:
    """
    Steepest descent for Ax = b (SPD matrix).
    Uses the negative gradient as search direction each step.

    >>> import numpy as np
    >>> A = np.array([
    ...     [8.73256573, -5.02034289, -2.68709226],
    ...     [-5.02034289,  3.78188322,  0.91980451],
    ...     [-2.68709226,  0.91980451,  1.94746467]])
    >>> b = np.array([[-5.80872761], [ 3.23807431], [ 1.95381422]])
    >>> x = steepest_descent(A, b)
    >>> np.allclose(x, [[-0.63114139], [-0.01561498], [0.13979294]], atol=1e-4)
    True
    """
    n = A.shape[0]
    x = np.zeros((n, 1))
    r = b - A @ x

    for _ in range(max_iterations):
        Ar = A @ r
        alpha = float(r.T @ r) / float(r.T @ Ar)
        x = x + alpha * r
        r = b - A @ x

        if np.linalg.norm(r) < tol:
            break

    return x


# ---------------------------------------------------------------------------
# Variant 3 — numpy_solve: direct solver for comparison
# ---------------------------------------------------------------------------
def numpy_direct_solve(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Direct solve via np.linalg.solve (LAPACK).

    >>> import numpy as np
    >>> A = np.array([
    ...     [8.73256573, -5.02034289, -2.68709226],
    ...     [-5.02034289,  3.78188322,  0.91980451],
    ...     [-2.68709226,  0.91980451,  1.94746467]])
    >>> b = np.array([[-5.80872761], [ 3.23807431], [ 1.95381422]])
    >>> x = numpy_direct_solve(A, b)
    >>> np.allclose(x, [[-0.63114139], [-0.01561498], [0.13979294]], atol=1e-6)
    True
    """
    return np.linalg.solve(A, b)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    """Compare all variants on a 200x200 SPD system."""
    rng = np.random.default_rng(42)
    n = 200
    R = rng.normal(size=(n, n))
    A = R.T @ R + np.eye(n) * 0.1  # SPD
    x_true = rng.normal(size=(n, 1))
    b = A @ x_true

    number = 20

    t_ref = timeit.timeit(lambda: reference(A, b), number=number)
    t_pcg = timeit.timeit(lambda: preconditioned_cg(A, b), number=number)
    t_sd = timeit.timeit(lambda: steepest_descent(A, b), number=number)
    t_np = timeit.timeit(lambda: numpy_direct_solve(A, b), number=number)

    print(f"Conjugate Gradient Benchmark ({n}x{n} SPD system, {number} runs)")
    print(f"{'Variant':<25} {'Total (s)':>10} {'Speedup':>10}")
    print("-" * 47)
    for name, t in [
        ("reference CG", t_ref),
        ("preconditioned CG", t_pcg),
        ("steepest_descent", t_sd),
        ("numpy_solve (direct)", t_np),
    ]:
        speedup = t_ref / t if t > 0 else float("inf")
        print(f"{name:<25} {t:>10.4f} {speedup:>9.1f}x")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
