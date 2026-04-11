#!/usr/bin/env python3
"""
Optimized and alternative implementations of the Rayleigh Quotient.

The Rayleigh quotient R(A,v) = (v*Av)/(v*v) gives the "best scalar approximation"
of an eigenvalue for a given vector v.  If v is an eigenvector, R returns exactly
the corresponding eigenvalue.

Three variants:
  rayleigh_shift_iteration — use Rayleigh quotient as shift for cubic convergence
  generalized_rayleigh     — generalized Rayleigh quotient R(A,B,v) = (v*Av)/(v*Bv)
  batch_rayleigh           — compute Rayleigh quotients for multiple vectors at once

Key interview insight:
    Rayleigh quotient iteration achieves CUBIC convergence (doubling correct digits
    every step), versus linear convergence for plain power iteration.  This is because
    the shift adapts each iteration to get closer to the true eigenvalue.

Run:
    python linear_algebra/rayleigh_quotient_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from linear_algebra.rayleigh_quotient import rayleigh_quotient as reference


# ---------------------------------------------------------------------------
# Variant 1 — rayleigh_shift_iteration: cubic convergence eigenvalue finder
# ---------------------------------------------------------------------------
def rayleigh_quotient_iteration(
    A: np.ndarray,
    v: np.ndarray,
    max_iter: int = 50,
    tol: float = 1e-14,
) -> tuple[float, np.ndarray]:
    """
    Rayleigh quotient iteration — cubic convergence to nearest eigenvalue.

    >>> import numpy as np
    >>> A = np.array([[1, 2, 4], [2, 3, -1], [4, -1, 1]], dtype=float)
    >>> v = np.array([[1], [2], [3]], dtype=float)
    >>> eigenvalue, eigenvector = rayleigh_quotient_iteration(A, v)
    >>> eigs = np.linalg.eigvalsh(A)
    >>> min(abs(eigs - eigenvalue)) < 1e-10
    True
    """
    n = A.shape[0]
    v = v.astype(float).flatten()
    v = v / np.linalg.norm(v)

    sigma = float(v.T @ A @ v)

    for _ in range(max_iter):
        try:
            w = np.linalg.solve(A - sigma * np.eye(n), v)
        except np.linalg.LinAlgError:
            break  # sigma is already an eigenvalue
        v = w / np.linalg.norm(w)
        sigma_new = float(v.T @ A @ v)

        if abs(sigma_new - sigma) < tol:
            sigma = sigma_new
            break
        sigma = sigma_new

    return sigma, v.reshape(-1, 1)


# ---------------------------------------------------------------------------
# Variant 2 — generalized_rayleigh: R(A,B,v) = (v*Av)/(v*Bv)
# ---------------------------------------------------------------------------
def generalized_rayleigh_quotient(
    A: np.ndarray, B: np.ndarray, v: np.ndarray
) -> float:
    """
    Generalized Rayleigh quotient for the pencil (A, B).
    R(A,B,v) = (v^H A v) / (v^H B v)

    Used in generalized eigenvalue problems Av = lambda Bv.

    >>> import numpy as np
    >>> A = np.array([[4, 1], [1, 3]], dtype=float)
    >>> B = np.array([[2, 0], [0, 1]], dtype=float)
    >>> v = np.array([[1], [0]], dtype=float)
    >>> generalized_rayleigh_quotient(A, B, v)
    2.0
    """
    vH = v.conjugate().T
    return float((vH @ A @ v) / (vH @ B @ v))


# ---------------------------------------------------------------------------
# Variant 3 — batch_rayleigh: vectorized for multiple vectors
# ---------------------------------------------------------------------------
def batch_rayleigh_quotient(A: np.ndarray, V: np.ndarray) -> np.ndarray:
    """
    Compute Rayleigh quotients for multiple column vectors simultaneously.
    V has shape (n, k) for k vectors.

    >>> import numpy as np
    >>> A = np.array([[2, 0], [0, 3]], dtype=float)
    >>> V = np.array([[1, 0], [0, 1]], dtype=float)
    >>> batch_rayleigh_quotient(A, V)
    array([2., 3.])
    """
    AV = A @ V
    numerator = np.sum(V.conjugate() * AV, axis=0)
    denominator = np.sum(V.conjugate() * V, axis=0)
    return np.real(numerator / denominator)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    """Compare Rayleigh quotient variants."""
    rng = np.random.default_rng(42)
    n = 100
    R = rng.normal(size=(n, n))
    A = R + R.T  # symmetric
    v = rng.normal(size=(n, 1))

    number = 200

    t_ref = timeit.timeit(lambda: reference(A, v), number=number)
    t_rqi = timeit.timeit(lambda: rayleigh_quotient_iteration(A, v), number=number)

    # Batch: 50 vectors
    V = rng.normal(size=(n, 50))
    t_batch = timeit.timeit(lambda: batch_rayleigh_quotient(A, V), number=number)
    t_loop = timeit.timeit(
        lambda: [reference(A, V[:, i:i+1]) for i in range(50)], number=number
    )

    print(f"Rayleigh Quotient Benchmark ({n}x{n} matrix, {number} runs)")
    print(f"{'Variant':<30} {'Total (s)':>10} {'Notes':>20}")
    print("-" * 63)
    print(f"{'reference (single)':<30} {t_ref:>10.4f} {'1 quotient':>20}")
    print(f"{'RQ iteration (cubic conv)':<30} {t_rqi:>10.4f} {'eigenvalue finder':>20}")
    print(f"{'batch (50 vectors)':<30} {t_batch:>10.4f} {'vectorized':>20}")
    print(f"{'loop (50 vectors)':<30} {t_loop:>10.4f} {'sequential':>20}")
    if t_batch > 0:
        print(f"\nBatch speedup over loop: {t_loop/t_batch:.1f}x")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
