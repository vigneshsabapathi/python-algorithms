#!/usr/bin/env python3
"""
Optimized and alternative implementations of Horn-Schunck Optical Flow.

The reference uses Jacobi relaxation with numpy vectorized updates.
Variants here explore convergence criteria, SOR acceleration, and
alternative gradient computation.

Variants covered:
1. jacobi_basic     -- reference: basic Jacobi iteration
2. sor_accelerated  -- successive over-relaxation for faster convergence
3. multi_scale      -- coarse-to-fine pyramid for large displacements
4. convergence_check-- early stopping when flow change < epsilon

Run:
    python computer_vision/horn_schunck_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from computer_vision.horn_schunck import horn_schunck as reference


# ---------------------------------------------------------------------------
# Variant 1 — jacobi_basic (reference wrapper)
# ---------------------------------------------------------------------------

def jacobi_basic(
    frame1: np.ndarray, frame2: np.ndarray, alpha: float = 1.0, iterations: int = 100
) -> tuple[np.ndarray, np.ndarray]:
    """
    Horn-Schunck via basic Jacobi iteration (reference).

    >>> import numpy as np
    >>> f1 = np.zeros((8, 8), dtype=np.float64)
    >>> f2 = np.zeros((8, 8), dtype=np.float64)
    >>> u, v = jacobi_basic(f1, f2)
    >>> u.shape
    (8, 8)
    """
    return reference(frame1, frame2, alpha, iterations)


# ---------------------------------------------------------------------------
# Variant 2 — SOR (Successive Over-Relaxation)
# ---------------------------------------------------------------------------

def sor_accelerated(
    frame1: np.ndarray,
    frame2: np.ndarray,
    alpha: float = 1.0,
    iterations: int = 100,
    omega: float = 1.05,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Horn-Schunck with SOR acceleration.

    Uses omega > 1 to over-correct each update, converging faster.
    Optimal omega is typically 1.2-1.9 for this problem.

    >>> import numpy as np
    >>> f1 = np.zeros((8, 8), dtype=np.float64)
    >>> f2 = np.zeros((8, 8), dtype=np.float64)
    >>> u, v = sor_accelerated(f1, f2)
    >>> u.shape
    (8, 8)
    """
    f1 = frame1.astype(np.float64)
    f2 = frame2.astype(np.float64)

    ix = np.zeros_like(f1)
    iy = np.zeros_like(f1)
    it = f2 - f1

    ix[:, 1:-1] = ((f1[:, 2:] - f1[:, :-2]) + (f2[:, 2:] - f2[:, :-2])) / 4.0
    iy[1:-1, :] = ((f1[2:, :] - f1[:-2, :]) + (f2[2:, :] - f2[:-2, :])) / 4.0

    u = np.zeros_like(f1)
    v = np.zeros_like(f1)

    denom = alpha**2 + ix**2 + iy**2

    for _ in range(iterations):
        u_avg = np.zeros_like(u)
        v_avg = np.zeros_like(v)
        u_avg[1:-1, 1:-1] = (u[:-2, 1:-1] + u[2:, 1:-1] + u[1:-1, :-2] + u[1:-1, 2:]) / 4.0
        v_avg[1:-1, 1:-1] = (v[:-2, 1:-1] + v[2:, 1:-1] + v[1:-1, :-2] + v[1:-1, 2:]) / 4.0

        p = ix * u_avg + iy * v_avg + it
        u_new = u_avg - ix * p / denom
        v_new = v_avg - iy * p / denom

        # SOR: blend old value with Jacobi update
        u = (1 - omega) * u + omega * u_new
        v = (1 - omega) * v + omega * v_new

    return u, v


# ---------------------------------------------------------------------------
# Variant 3 — multi-scale (coarse-to-fine)
# ---------------------------------------------------------------------------

def _downsample(img: np.ndarray) -> np.ndarray:
    """Downsample by 2x using averaging."""
    rows, cols = img.shape
    r = rows - rows % 2
    c = cols - cols % 2
    return img[:r, :c].reshape(r // 2, 2, c // 2, 2).mean(axis=(1, 3))


def _upsample(flow: np.ndarray, target_shape: tuple[int, int]) -> np.ndarray:
    """Upsample flow field to target_shape using nearest-neighbor * 2."""
    result = np.zeros(target_shape, dtype=np.float64)
    rows, cols = flow.shape
    tr, tc = target_shape
    for i in range(tr):
        for j in range(tc):
            si = min(i // 2, rows - 1)
            sj = min(j // 2, cols - 1)
            result[i, j] = flow[si, sj] * 2.0  # scale flow with resolution
    return result


def multi_scale(
    frame1: np.ndarray,
    frame2: np.ndarray,
    alpha: float = 1.0,
    iterations: int = 50,
    levels: int = 3,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Coarse-to-fine Horn-Schunck for handling larger displacements.

    Builds an image pyramid, estimates flow at the coarsest level,
    then refines at each finer level.

    >>> import numpy as np
    >>> f1 = np.zeros((16, 16), dtype=np.float64)
    >>> f2 = np.zeros((16, 16), dtype=np.float64)
    >>> u, v = multi_scale(f1, f2, levels=2)
    >>> u.shape
    (16, 16)
    """
    f1 = frame1.astype(np.float64)
    f2 = frame2.astype(np.float64)

    # Build pyramid
    pyr1 = [f1]
    pyr2 = [f2]
    for _ in range(levels - 1):
        pyr1.append(_downsample(pyr1[-1]))
        pyr2.append(_downsample(pyr2[-1]))

    # Start from coarsest level
    u, v = reference(pyr1[-1], pyr2[-1], alpha, iterations)

    # Refine at each finer level
    for level in range(levels - 2, -1, -1):
        target = pyr1[level].shape
        u = _upsample(u, target)
        v = _upsample(v, target)

        # Compute residual flow at this level
        du, dv = reference(pyr1[level], pyr2[level], alpha, iterations // 2)
        u += du
        v += dv

    return u, v


# ---------------------------------------------------------------------------
# Variant 4 — early stopping with convergence check
# ---------------------------------------------------------------------------

def convergence_check(
    frame1: np.ndarray,
    frame2: np.ndarray,
    alpha: float = 1.0,
    max_iter: int = 500,
    epsilon: float = 1e-4,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Horn-Schunck with early stopping when flow changes < epsilon.

    >>> import numpy as np
    >>> f1 = np.zeros((8, 8), dtype=np.float64)
    >>> f2 = np.zeros((8, 8), dtype=np.float64)
    >>> u, v = convergence_check(f1, f2)
    >>> u.shape
    (8, 8)
    """
    f1 = frame1.astype(np.float64)
    f2 = frame2.astype(np.float64)

    ix = np.zeros_like(f1)
    iy = np.zeros_like(f1)
    it = f2 - f1

    ix[:, 1:-1] = ((f1[:, 2:] - f1[:, :-2]) + (f2[:, 2:] - f2[:, :-2])) / 4.0
    iy[1:-1, :] = ((f1[2:, :] - f1[:-2, :]) + (f2[2:, :] - f2[:-2, :])) / 4.0

    u = np.zeros_like(f1)
    v = np.zeros_like(f1)
    denom = alpha**2 + ix**2 + iy**2
    actual_iter = max_iter

    for iteration in range(max_iter):
        u_old = u.copy()

        u_avg = np.zeros_like(u)
        v_avg = np.zeros_like(v)
        u_avg[1:-1, 1:-1] = (u[:-2, 1:-1] + u[2:, 1:-1] + u[1:-1, :-2] + u[1:-1, 2:]) / 4.0
        v_avg[1:-1, 1:-1] = (v[:-2, 1:-1] + v[2:, 1:-1] + v[1:-1, :-2] + v[1:-1, 2:]) / 4.0

        p = ix * u_avg + iy * v_avg + it
        u = u_avg - ix * p / denom
        v = v_avg - iy * p / denom

        change = np.max(np.abs(u - u_old))
        if change < epsilon:
            actual_iter = iteration + 1
            break

    return u, v


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

def run_all() -> None:
    np.random.seed(42)

    # Create test frames: a bright square that shifts right by 1 pixel
    f1 = np.zeros((16, 16), dtype=np.float64)
    f2 = np.zeros((16, 16), dtype=np.float64)
    f1[5:11, 5:11] = 255.0
    f2[5:11, 6:12] = 255.0

    print("\n=== Correctness (16x16, square shifts right by 1) ===")
    impls = [
        ("jacobi_basic", lambda: jacobi_basic(f1, f2, alpha=1.0, iterations=200)),
        ("sor_accelerated", lambda: sor_accelerated(f1, f2, alpha=1.0, iterations=200, omega=1.05)),
        ("multi_scale", lambda: multi_scale(f1, f2, alpha=1.0, iterations=100, levels=2)),
        ("convergence_check", lambda: convergence_check(f1, f2, alpha=1.0, max_iter=500)),
    ]

    for name, fn in impls:
        try:
            u, v = fn()
            mean_u = np.mean(u[6:10, 6:10])  # interior of square
            mean_v = np.mean(v[6:10, 6:10])
            mag = np.sqrt(u**2 + v**2).mean()
            print(f"  [OK] {name:<22} mean_u={mean_u:+.4f}  mean_v={mean_v:+.4f}  avg_mag={mag:.4f}")
        except Exception as e:
            print(f"  [ERR] {name:<22} {e}")

    REPS = 50
    sizes = [16, 32]
    for sz in sizes:
        f1 = np.random.rand(sz, sz) * 255
        f2 = np.roll(f1, 1, axis=1)  # shift right by 1

        print(f"\n=== Benchmark ({sz}x{sz}): {REPS} runs, 100 iterations ===")
        bench_impls = [
            ("jacobi_basic", lambda f1=f1, f2=f2: jacobi_basic(f1, f2, iterations=100)),
            ("sor_accelerated", lambda f1=f1, f2=f2: sor_accelerated(f1, f2, iterations=100)),
            ("convergence_check", lambda f1=f1, f2=f2: convergence_check(f1, f2, max_iter=100)),
        ]

        for name, fn in bench_impls:
            try:
                t = timeit.timeit(fn, number=REPS)
                ms = t * 1000 / REPS
                print(f"  {name:<22} {ms:>8.3f} ms")
            except Exception as e:
                print(f"  {name:<22} ERR: {e}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
