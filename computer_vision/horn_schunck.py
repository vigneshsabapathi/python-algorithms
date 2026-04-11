"""
Horn-Schunck Optical Flow — dense motion estimation between frames.

Estimates per-pixel velocity (u, v) between two consecutive grayscale
frames by minimizing:

    E = sum[ (Ix*u + Iy*v + It)^2 + alpha^2 * (|grad(u)|^2 + |grad(v)|^2) ]

where:
- Ix, Iy, It are spatiotemporal image gradients
- alpha controls the smoothness weight
- The first term enforces the brightness constancy constraint
- The second term enforces smoothness of the flow field

Solved iteratively using Gauss-Seidel / Jacobi relaxation.

Reference: TheAlgorithms/Python — computer_vision/horn_schunck.py
Paper: Horn & Schunck, "Determining optical flow" (1981)

>>> import numpy as np
>>> frame1 = np.zeros((8, 8), dtype=np.float64)
>>> frame2 = np.zeros((8, 8), dtype=np.float64)
>>> frame1[3:5, 3:5] = 255.0
>>> frame2[3:5, 4:6] = 255.0
>>> u, v = horn_schunck(frame1, frame2, alpha=1.0, iterations=100)
>>> u.shape
(8, 8)
>>> v.shape
(8, 8)
"""

from __future__ import annotations

import numpy as np


def horn_schunck(
    frame1: np.ndarray,
    frame2: np.ndarray,
    alpha: float = 1.0,
    iterations: int = 100,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute dense optical flow using the Horn-Schunck method.

    Args:
        frame1: first grayscale frame (2D float array).
        frame2: second grayscale frame (2D float array).
        alpha: smoothness weight (larger = smoother flow).
        iterations: number of Jacobi relaxation iterations.

    Returns:
        (u, v) — horizontal and vertical flow fields.

    >>> import numpy as np
    >>> f1 = np.random.seed(42)
    >>> f1 = np.random.rand(10, 10)
    >>> f2 = np.roll(f1, 1, axis=1)  # shift right by 1
    >>> u, v = horn_schunck(f1, f2, alpha=1.0, iterations=200)
    >>> u.shape == (10, 10)
    True
    """
    f1 = frame1.astype(np.float64)
    f2 = frame2.astype(np.float64)
    rows, cols = f1.shape

    # Compute spatiotemporal gradients using central differences
    # Ix: horizontal gradient (average of both frames)
    # Iy: vertical gradient (average of both frames)
    # It: temporal gradient
    ix = np.zeros_like(f1)
    iy = np.zeros_like(f1)
    it = f2 - f1

    # Horizontal gradient (central difference, averaged over frames)
    ix[:, 1:-1] = ((f1[:, 2:] - f1[:, :-2]) + (f2[:, 2:] - f2[:, :-2])) / 4.0
    # Vertical gradient
    iy[1:-1, :] = ((f1[2:, :] - f1[:-2, :]) + (f2[2:, :] - f2[:-2, :])) / 4.0

    # Initialize flow fields
    u = np.zeros_like(f1)
    v = np.zeros_like(f1)

    # Laplacian kernel for neighborhood averaging
    # avg_u = (u[i-1,j] + u[i+1,j] + u[i,j-1] + u[i,j+1]) / 4
    for _ in range(iterations):
        # Compute local averages using neighbors
        u_avg = np.zeros_like(u)
        v_avg = np.zeros_like(v)

        u_avg[1:-1, 1:-1] = (
            u[:-2, 1:-1] + u[2:, 1:-1] + u[1:-1, :-2] + u[1:-1, 2:]
        ) / 4.0
        v_avg[1:-1, 1:-1] = (
            v[:-2, 1:-1] + v[2:, 1:-1] + v[1:-1, :-2] + v[1:-1, 2:]
        ) / 4.0

        # Handle borders with available neighbors
        # Top row
        u_avg[0, 1:-1] = (u[1, 1:-1] + u[0, :-2] + u[0, 2:]) / 3.0
        v_avg[0, 1:-1] = (v[1, 1:-1] + v[0, :-2] + v[0, 2:]) / 3.0
        # Bottom row
        u_avg[-1, 1:-1] = (u[-2, 1:-1] + u[-1, :-2] + u[-1, 2:]) / 3.0
        v_avg[-1, 1:-1] = (v[-2, 1:-1] + v[-1, :-2] + v[-1, 2:]) / 3.0
        # Left col
        u_avg[1:-1, 0] = (u[:-2, 0] + u[2:, 0] + u[1:-1, 1]) / 3.0
        v_avg[1:-1, 0] = (v[:-2, 0] + v[2:, 0] + v[1:-1, 1]) / 3.0
        # Right col
        u_avg[1:-1, -1] = (u[:-2, -1] + u[2:, -1] + u[1:-1, -2]) / 3.0
        v_avg[1:-1, -1] = (v[:-2, -1] + v[2:, -1] + v[1:-1, -2]) / 3.0

        # Update step: u = u_avg - Ix * (Ix*u_avg + Iy*v_avg + It) / (alpha^2 + Ix^2 + Iy^2)
        denom = alpha**2 + ix**2 + iy**2
        p = ix * u_avg + iy * v_avg + it

        u = u_avg - ix * p / denom
        v = v_avg - iy * p / denom

    return u, v


if __name__ == "__main__":
    import doctest

    doctest.testmod()
