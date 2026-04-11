#!/usr/bin/env python3
"""
Optimized and alternative implementations of Power Iteration.

Power iteration finds the dominant (largest magnitude) eigenvalue and its
eigenvector by repeatedly multiplying: v_{k+1} = Av_k / ||Av_k||.
Converges at rate |lambda_2/lambda_1|.

Three variants:
  inverse_iteration — finds the SMALLEST eigenvalue (solve Ax=v instead of Av)
  shifted_inverse   — finds eigenvalue closest to a given shift sigma
  qr_algorithm      — finds ALL eigenvalues simultaneously via QR iteration

Key interview insight:
    Power iteration gives you ONE eigenvalue.  Inverse iteration targets the
    smallest (useful for conditioning).  Shifted inverse targets ANY specific
    eigenvalue near sigma.  QR algorithm computes the full eigendecomposition
    in O(n^3) — it's what numpy.linalg.eig uses under the hood.

Run:
    python linear_algebra/power_iteration_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from linear_algebra.power_iteration import power_iteration as reference


# ---------------------------------------------------------------------------
# Variant 1 — inverse_iteration: find smallest eigenvalue
# ---------------------------------------------------------------------------
def inverse_iteration(
    A: np.ndarray,
    v: np.ndarray,
    tol: float = 1e-12,
    max_iter: int = 100,
) -> tuple[float, np.ndarray]:
    """
    Inverse iteration — finds the smallest eigenvalue of A.

    >>> import numpy as np
    >>> A = np.array([[41, 4, 20], [4, 26, 30], [20, 30, 50]])
    >>> v = np.array([1.0, 1.0, 1.0])
    >>> eigenvalue, eigenvector = inverse_iteration(A, v)
    >>> np.allclose(eigenvalue, np.min(np.abs(np.linalg.eigvalsh(A))), atol=1e-6)
    True
    """
    v = v.astype(float)
    lambda_prev = 0.0

    for _ in range(max_iter):
        w = np.linalg.solve(A, v)
        v = w / np.linalg.norm(w)
        lambda_ = float(v.T @ A @ v)

        if abs(lambda_ - lambda_prev) / max(abs(lambda_), 1e-15) < tol:
            break
        lambda_prev = lambda_

    return lambda_, v


# ---------------------------------------------------------------------------
# Variant 2 — shifted_inverse: find eigenvalue closest to sigma
# ---------------------------------------------------------------------------
def shifted_inverse_iteration(
    A: np.ndarray,
    v: np.ndarray,
    sigma: float,
    tol: float = 1e-12,
    max_iter: int = 100,
) -> tuple[float, np.ndarray]:
    """
    Shifted inverse iteration — finds eigenvalue closest to sigma.

    >>> import numpy as np
    >>> A = np.array([[41, 4, 20], [4, 26, 30], [20, 30, 50]])
    >>> v = np.array([1.0, 1.0, 1.0])
    >>> eigenvalue, _ = shifted_inverse_iteration(A, v, sigma=30.0)
    >>> eigs = np.linalg.eigvalsh(A)
    >>> closest = eigs[np.argmin(np.abs(eigs - 30.0))]
    >>> np.allclose(eigenvalue, closest, atol=1e-6)
    True
    """
    n = A.shape[0]
    v = v.astype(float)
    shifted = A - sigma * np.eye(n)
    lambda_prev = 0.0

    for _ in range(max_iter):
        w = np.linalg.solve(shifted, v)
        v = w / np.linalg.norm(w)
        lambda_ = float(v.T @ A @ v)

        if abs(lambda_ - lambda_prev) / max(abs(lambda_), 1e-15) < tol:
            break
        lambda_prev = lambda_

    return lambda_, v


# ---------------------------------------------------------------------------
# Variant 3 — qr_algorithm: find ALL eigenvalues
# ---------------------------------------------------------------------------
def qr_eigenvalues(
    A: np.ndarray,
    max_iter: int = 200,
    tol: float = 1e-10,
) -> np.ndarray:
    """
    Basic QR algorithm to find all eigenvalues.

    >>> import numpy as np
    >>> A = np.array([[41, 4, 20], [4, 26, 30], [20, 30, 50]])
    >>> eigs = qr_eigenvalues(A)
    >>> expected = np.sort(np.linalg.eigvalsh(A))
    >>> np.allclose(np.sort(eigs), expected, atol=1e-6)
    True
    """
    A_k = A.astype(float).copy()
    n = A_k.shape[0]

    for _ in range(max_iter):
        Q, R = np.linalg.qr(A_k)
        A_k = R @ Q

        # Check convergence (off-diagonal elements small)
        off_diag = np.sum(np.abs(A_k) - np.abs(np.diag(np.diag(A_k))))
        if off_diag < tol:
            break

    return np.diag(A_k)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    """Compare all variants."""
    rng = np.random.default_rng(42)
    n = 50
    R = rng.normal(size=(n, n))
    A = R + R.T  # symmetric
    v = rng.normal(size=n)

    number = 50

    t_ref = timeit.timeit(lambda: reference(A, v), number=number)
    t_inv = timeit.timeit(lambda: inverse_iteration(A, v), number=number)
    t_shi = timeit.timeit(lambda: shifted_inverse_iteration(A, v, sigma=0.0), number=number)
    t_qr = timeit.timeit(lambda: qr_eigenvalues(A), number=number)
    t_np = timeit.timeit(lambda: np.linalg.eigvalsh(A), number=number)

    print(f"Power Iteration Benchmark ({n}x{n} symmetric matrix, {number} runs)")
    print(f"{'Variant':<28} {'Total (s)':>10} {'Eigenvalues':>12}")
    print("-" * 53)
    for name, t, count in [
        ("reference (power iter)", t_ref, "1 (max)"),
        ("inverse_iteration", t_inv, "1 (min)"),
        ("shifted_inverse (s=0)", t_shi, "1 (nearest)"),
        ("qr_algorithm", t_qr, "all"),
        ("numpy eigvalsh", t_np, "all"),
    ]:
        print(f"{name:<28} {t:>10.4f} {count:>12}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
