#!/usr/bin/env python3
"""
Optimized and alternative implementations of 2D Transformations.

The reference computes 2D transformation matrices (scaling, rotation,
projection, reflection) using math.cos/sin and list comprehensions.

Three variants:
  numpy_transforms    — numpy-backed with matrix multiplication support
  homogeneous_coords  — 3x3 affine matrices (support translation too)
  compose_transforms  — chain multiple transforms into one matrix

Key interview insight:
    In computer graphics, 2D transforms are represented as 3x3 homogeneous
    matrices so that translation (which is NOT linear) can be expressed as
    matrix multiplication.  This lets you compose any sequence of transforms
    into a single matrix multiply.

Run:
    python linear_algebra/transformations_2d_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from linear_algebra.transformations_2d import (
    projection as ref_projection,
    reflection as ref_reflection,
    rotation as ref_rotation,
    scaling as ref_scaling,
)


# ---------------------------------------------------------------------------
# Variant 1 — numpy_transforms: numpy arrays with apply method
# ---------------------------------------------------------------------------
def np_scaling(factor: float) -> np.ndarray:
    """
    >>> np_scaling(5.0)
    array([[5., 0.],
           [0., 5.]])
    """
    return np.array([[factor, 0.0], [0.0, factor]])


def np_rotation(angle: float) -> np.ndarray:
    """
    >>> R = np_rotation(np.pi / 4)
    >>> np.allclose(R @ R.T, np.eye(2))
    True
    """
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s], [s, c]])


def np_projection(angle: float) -> np.ndarray:
    """
    >>> P = np_projection(np.pi / 4)
    >>> np.allclose(P @ P, P)  # idempotent
    True
    """
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c * c, c * s], [c * s, s * s]])


def np_reflection(angle: float) -> np.ndarray:
    """
    >>> R = np_reflection(np.pi / 4)
    >>> np.allclose(R @ R, np.eye(2))  # involution
    True
    """
    c, s = np.cos(2 * angle), np.sin(2 * angle)
    return np.array([[c, s], [s, -c]])


# ---------------------------------------------------------------------------
# Variant 2 — homogeneous_coords: 3x3 affine transforms
# ---------------------------------------------------------------------------
def homogeneous_scaling(sx: float, sy: float | None = None) -> np.ndarray:
    """
    3x3 homogeneous scaling matrix (supports non-uniform scaling).

    >>> homogeneous_scaling(2.0, 3.0)
    array([[2., 0., 0.],
           [0., 3., 0.],
           [0., 0., 1.]])
    """
    if sy is None:
        sy = sx
    return np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]], dtype=float)


def homogeneous_rotation(angle: float) -> np.ndarray:
    """
    3x3 homogeneous rotation matrix.

    >>> R = homogeneous_rotation(np.pi / 2)
    >>> np.allclose(R[:2, :2] @ R[:2, :2].T, np.eye(2))
    True
    """
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=float)


def homogeneous_translation(tx: float, ty: float) -> np.ndarray:
    """
    3x3 translation matrix (only possible in homogeneous coordinates).

    >>> homogeneous_translation(5.0, 3.0)
    array([[1., 0., 5.],
           [0., 1., 3.],
           [0., 0., 1.]])
    """
    return np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]], dtype=float)


# ---------------------------------------------------------------------------
# Variant 3 — compose_transforms: chain transforms
# ---------------------------------------------------------------------------
def compose_transforms(*transforms: np.ndarray) -> np.ndarray:
    """
    Compose multiple transformation matrices (applied right to left).

    >>> T = homogeneous_translation(1, 0)
    >>> R = homogeneous_rotation(np.pi / 2)
    >>> M = compose_transforms(T, R)  # first rotate, then translate
    >>> point = np.array([1, 0, 1])  # homogeneous coords
    >>> result = M @ point
    >>> np.allclose(result[:2], [1, 1])
    True
    """
    result = transforms[0]
    for t in transforms[1:]:
        result = result @ t
    return result


def apply_transform(matrix: np.ndarray, points: np.ndarray) -> np.ndarray:
    """
    Apply a 2x2 or 3x3 transform to an array of points.
    Points shape: (N, 2) for 2D, automatically handles homogeneous conversion.

    >>> pts = np.array([[1, 0], [0, 1]], dtype=float)
    >>> scaled = apply_transform(np_scaling(2.0), pts)
    >>> np.allclose(scaled, [[2, 0], [0, 2]])
    True
    """
    if matrix.shape == (3, 3) and points.shape[1] == 2:
        # Convert to homogeneous
        ones = np.ones((points.shape[0], 1))
        pts_h = np.hstack([points, ones])
        result = (matrix @ pts_h.T).T
        return result[:, :2]
    return (matrix @ points.T).T


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    """Compare reference vs numpy transforms."""
    angle = 0.7854  # ~45 degrees
    n_points = 10000
    rng = np.random.default_rng(42)
    points = rng.normal(size=(n_points, 2))

    number = 1000

    # Single matrix creation
    t_ref_rot = timeit.timeit(lambda: ref_rotation(angle), number=number)
    t_np_rot = timeit.timeit(lambda: np_rotation(angle), number=number)

    # Transform application (ref requires manual conversion)
    np_R = np_rotation(angle)
    t_apply = timeit.timeit(lambda: apply_transform(np_R, points), number=number)

    # List-based apply for reference
    ref_R = ref_rotation(angle)

    def ref_apply():
        return [[ref_R[0][0] * p[0] + ref_R[0][1] * p[1],
                 ref_R[1][0] * p[0] + ref_R[1][1] * p[1]] for p in points]

    t_ref_apply = timeit.timeit(ref_apply, number=20)

    print(f"2D Transformations Benchmark ({number} matrix creations, {n_points} points)")
    print(f"{'Operation':<30} {'Time (s)':>10} {'Speedup':>10}")
    print("-" * 53)
    print(f"{'rotation (reference list)':<30} {t_ref_rot:>10.4f}")
    print(f"{'rotation (numpy array)':<30} {t_np_rot:>10.4f} {t_ref_rot/t_np_rot:>9.1f}x")
    print(f"{'apply {n_points}pts (numpy)':<30} {t_apply:>10.4f}")
    print(f"{'apply {n_points}pts (list, 20x)':<30} {t_ref_apply:>10.4f} {t_ref_apply*number/20/t_apply:>9.1f}x slower")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
