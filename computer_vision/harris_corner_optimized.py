#!/usr/bin/env python3
"""
Optimized and alternative implementations of Harris Corner Detection.

The reference uses Python loops for convolution. Variants here vectorize
the gradient and structure tensor computation.

Variants covered:
1. loop_harris      -- reference: explicit Python loops
2. vectorized       -- fully vectorized with numpy correlate2d-style
3. scipy_harris     -- scipy.ndimage for gradient + Gaussian smoothing
4. shi_tomasi       -- Shi-Tomasi variant: R = min(eigenvalue) instead of det-k*trace^2

Run:
    python computer_vision/harris_corner_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from computer_vision.harris_corner import harris_corner as reference


# ---------------------------------------------------------------------------
# Variant 1 — loop_harris (reference wrapper)
# ---------------------------------------------------------------------------

def loop_harris(image: np.ndarray, k: float = 0.04) -> np.ndarray:
    """
    Harris corner response via explicit loops (reference).

    >>> import numpy as np
    >>> img = np.zeros((8, 8), dtype=np.float64)
    >>> img[2:6, 2:6] = 1.0
    >>> R = loop_harris(img)
    >>> R.shape
    (8, 8)
    """
    return reference(image, k=k)


# ---------------------------------------------------------------------------
# Variant 2 — vectorized numpy
# ---------------------------------------------------------------------------

def _convolve2d(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """2D convolution via vectorized sliding window."""
    kh, kw = kernel.shape
    ph, pw = kh // 2, kw // 2
    padded = np.pad(image, ((ph, ph), (pw, pw)), mode="reflect")
    rows, cols = image.shape
    result = np.zeros_like(image)
    for di in range(kh):
        for dj in range(kw):
            result += padded[di:di + rows, dj:dj + cols] * kernel[di, dj]
    return result


def vectorized_harris(image: np.ndarray, k: float = 0.04, sigma: float = 1.0) -> np.ndarray:
    """
    Harris corner detection with vectorized convolution.

    >>> import numpy as np
    >>> img = np.zeros((8, 8), dtype=np.float64)
    >>> img[2:6, 2:6] = 1.0
    >>> R = vectorized_harris(img)
    >>> R.shape
    (8, 8)
    """
    if image.ndim == 3:
        image = np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])
    img = image.astype(np.float64)

    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float64)
    ky = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float64)

    ix = _convolve2d(img, kx)
    iy = _convolve2d(img, ky)

    ixx = ix * ix
    iyy = iy * iy
    ixy = ix * iy

    # Gaussian smoothing kernel
    size = 3
    half = size // 2
    ax = np.arange(-half, half + 1)
    xx, yy = np.meshgrid(ax, ax)
    gauss = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    gauss /= gauss.sum()

    sxx = _convolve2d(ixx, gauss)
    syy = _convolve2d(iyy, gauss)
    sxy = _convolve2d(ixy, gauss)

    det_m = sxx * syy - sxy**2
    trace_m = sxx + syy
    return det_m - k * trace_m**2


# ---------------------------------------------------------------------------
# Variant 3 — scipy-based
# ---------------------------------------------------------------------------

def scipy_harris(image: np.ndarray, k: float = 0.04, sigma: float = 1.0) -> np.ndarray:
    """
    Harris corner detection using scipy for gradients and Gaussian smoothing.

    >>> import numpy as np
    >>> img = np.zeros((8, 8), dtype=np.float64)
    >>> img[2:6, 2:6] = 1.0
    >>> R = scipy_harris(img)
    >>> R.shape
    (8, 8)
    """
    from scipy.ndimage import gaussian_filter, sobel

    if image.ndim == 3:
        image = np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])
    img = image.astype(np.float64)

    ix = sobel(img, axis=1)  # horizontal gradient
    iy = sobel(img, axis=0)  # vertical gradient

    sxx = gaussian_filter(ix * ix, sigma=sigma)
    syy = gaussian_filter(iy * iy, sigma=sigma)
    sxy = gaussian_filter(ix * iy, sigma=sigma)

    det_m = sxx * syy - sxy**2
    trace_m = sxx + syy
    return det_m - k * trace_m**2


# ---------------------------------------------------------------------------
# Variant 4 — Shi-Tomasi: min(eigenvalue) criterion
# ---------------------------------------------------------------------------

def shi_tomasi(image: np.ndarray, sigma: float = 1.0) -> np.ndarray:
    """
    Shi-Tomasi corner response: R = min(lambda1, lambda2).

    More stable than Harris — directly uses the smaller eigenvalue.
    Good features to track (KLT tracker uses this).

    >>> import numpy as np
    >>> img = np.zeros((8, 8), dtype=np.float64)
    >>> img[2:6, 2:6] = 1.0
    >>> R = shi_tomasi(img)
    >>> R.shape
    (8, 8)
    """
    from scipy.ndimage import gaussian_filter, sobel

    if image.ndim == 3:
        image = np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])
    img = image.astype(np.float64)

    ix = sobel(img, axis=1)
    iy = sobel(img, axis=0)

    sxx = gaussian_filter(ix * ix, sigma=sigma)
    syy = gaussian_filter(iy * iy, sigma=sigma)
    sxy = gaussian_filter(ix * iy, sigma=sigma)

    # Eigenvalues of 2x2 symmetric matrix: lambda = (a+d)/2 +/- sqrt(((a-d)/2)^2 + b^2)
    trace = sxx + syy
    det = sxx * syy - sxy**2
    discriminant = np.sqrt(np.maximum((trace / 2) ** 2 - det, 0))

    lambda1 = trace / 2 + discriminant
    lambda2 = trace / 2 - discriminant

    return np.minimum(lambda1, lambda2)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

def run_all() -> None:
    np.random.seed(42)

    # Create test image: checkerboard with corners
    img = np.zeros((32, 32), dtype=np.float64)
    img[8:24, 8:24] = 255.0
    img[4:12, 20:28] = 128.0

    print("\n=== Correctness (32x32 with squares) ===")
    ref_result = reference(img, k=0.04)

    impls = [
        ("loop_harris", lambda img: loop_harris(img, k=0.04)),
        ("vectorized", lambda img: vectorized_harris(img, k=0.04)),
        ("scipy_harris", lambda img: scipy_harris(img, k=0.04)),
        ("shi_tomasi", lambda img: shi_tomasi(img)),
    ]

    for name, fn in impls:
        try:
            result = fn(img)
            corners = np.sum(result > 0.01 * result.max())
            print(f"  [OK] {name:<18} shape={result.shape}  corners(R>1%max)={corners}")
        except Exception as e:
            print(f"  [ERR] {name:<18} {e}")

    REPS = 100
    sizes = [16, 32, 64]
    bench_impls = [
        ("loop_harris", lambda img: loop_harris(img, k=0.04)),
        ("vectorized", lambda img: vectorized_harris(img, k=0.04)),
        ("scipy_harris", lambda img: scipy_harris(img, k=0.04)),
        ("shi_tomasi", lambda img: shi_tomasi(img)),
    ]

    for sz in sizes:
        img = np.random.rand(sz, sz) * 255
        print(f"\n=== Benchmark ({sz}x{sz}): {REPS} runs ===")
        for name, fn in bench_impls:
            try:
                t = timeit.timeit(lambda fn=fn, img=img: fn(img), number=REPS)
                ms = t * 1000 / REPS
                print(f"  {name:<18} {ms:>8.3f} ms")
            except Exception as e:
                print(f"  {name:<18} ERR: {e}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
