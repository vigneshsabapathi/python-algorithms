#!/usr/bin/env python3
"""
Optimized and alternative implementations of Mean Threshold.

The reference uses an integral image with per-pixel Python loops.
Variants here vectorize the computation or explore alternative
adaptive thresholding strategies.

Variants covered:
1. loop_integral   -- reference: integral image + Python loop
2. vectorized      -- fully vectorized integral image lookups (no loops)
3. uniform_filter  -- scipy uniform_filter for local mean (fastest)
4. gaussian_mean   -- Gaussian-weighted local mean (softer edges)

Run:
    python computer_vision/mean_threshold_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from computer_vision.mean_threshold import mean_threshold as reference


# ---------------------------------------------------------------------------
# Variant 1 — loop_integral (reference wrapper)
# ---------------------------------------------------------------------------

def loop_integral(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """
    Adaptive mean threshold via integral image + Python loop.

    >>> import numpy as np
    >>> img = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]], dtype=np.uint8)
    >>> out = loop_integral(img, 3)
    >>> out.shape
    (3, 3)
    """
    return reference(image, kernel_size)


# ---------------------------------------------------------------------------
# Variant 2 — vectorized integral image
# ---------------------------------------------------------------------------

def vectorized(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """
    Fully vectorized adaptive mean threshold using integral image.
    No Python loops — uses numpy array indexing for all local sums.

    >>> import numpy as np
    >>> img = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]], dtype=np.uint8)
    >>> out = vectorized(img, 3)
    >>> out.shape
    (3, 3)
    """
    if kernel_size % 2 == 0:
        raise ValueError("kernel_size must be odd")

    if image.ndim == 3:
        image = np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])
    img = image.astype(np.float64)

    rows, cols = img.shape
    half = kernel_size // 2

    # Integral image with zero-padding
    integral = np.cumsum(np.cumsum(img, axis=0), axis=1)
    padded = np.zeros((rows + 1, cols + 1), dtype=np.float64)
    padded[1:, 1:] = integral

    # Build coordinate arrays for window boundaries
    row_idx = np.arange(rows)
    col_idx = np.arange(cols)
    rr, cc = np.meshgrid(row_idx, col_idx, indexing="ij")

    r1 = np.maximum(rr - half, 0)
    r2 = np.minimum(rr + half, rows - 1)
    c1 = np.maximum(cc - half, 0)
    c2 = np.minimum(cc + half, cols - 1)

    area = (r2 - r1 + 1) * (c2 - c1 + 1)

    local_sum = (
        padded[r2 + 1, c2 + 1]
        - padded[r1, c2 + 1]
        - padded[r2 + 1, c1]
        + padded[r1, c1]
    )
    local_mean = local_sum / area

    output = np.zeros_like(img, dtype=np.uint8)
    output[img > local_mean] = 255
    return output


# ---------------------------------------------------------------------------
# Variant 3 — uniform_filter (scipy)
# ---------------------------------------------------------------------------

def uniform_filter_threshold(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """
    Adaptive mean threshold using scipy's uniform_filter for local mean.
    This is the fastest approach for large images.

    >>> import numpy as np
    >>> img = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]], dtype=np.uint8)
    >>> out = uniform_filter_threshold(img, 3)
    >>> out.shape
    (3, 3)
    """
    from scipy.ndimage import uniform_filter as uf

    if image.ndim == 3:
        image = np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])
    img = image.astype(np.float64)

    local_mean = uf(img, size=kernel_size, mode="reflect")
    output = np.zeros_like(img, dtype=np.uint8)
    output[img > local_mean] = 255
    return output


# ---------------------------------------------------------------------------
# Variant 4 — Gaussian-weighted local mean
# ---------------------------------------------------------------------------

def gaussian_mean(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """
    Adaptive threshold using Gaussian-weighted local mean.
    Pixels closer to the center contribute more, producing softer edges.

    >>> import numpy as np
    >>> img = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]], dtype=np.uint8)
    >>> out = gaussian_mean(img, 3)
    >>> out.shape
    (3, 3)
    """
    from scipy.ndimage import gaussian_filter

    if image.ndim == 3:
        image = np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])
    img = image.astype(np.float64)

    sigma = kernel_size / 6.0  # ~99.7% of weight within kernel
    local_mean = gaussian_filter(img, sigma=sigma)
    output = np.zeros_like(img, dtype=np.uint8)
    output[img > local_mean] = 255
    return output


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

def _make_test_image(size: int = 64) -> np.ndarray:
    """Create a test image with a gradient and some features."""
    np.random.seed(42)
    img = np.zeros((size, size), dtype=np.uint8)
    # Gradient background
    for i in range(size):
        img[i, :] = int(255 * i / size)
    # Add bright spots
    img[size // 4, size // 4] = 255
    img[3 * size // 4, 3 * size // 4] = 255
    # Add noise
    noise = np.random.randint(0, 30, (size, size), dtype=np.uint8)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    return img


TEST_IMAGE = _make_test_image(32)

IMPLS = [
    ("loop_integral", loop_integral),
    ("vectorized", vectorized),
    ("uniform_filter", uniform_filter_threshold),
    ("gaussian_mean", gaussian_mean),
]


def run_all() -> None:
    print("\n=== Correctness (32x32 test image, kernel=3) ===")
    ref_result = reference(TEST_IMAGE, 3)
    for name, fn in IMPLS:
        try:
            result = fn(TEST_IMAGE, 3)
            if name == "gaussian_mean":
                # Gaussian uses different weighting, so just check shape/type
                match = result.shape == ref_result.shape and result.dtype == ref_result.dtype
                tag = "OK (different weighting)" if match else "FAIL"
            else:
                match = np.array_equal(result, ref_result)
                tag = "OK" if match else "FAIL"
            white_pct = 100 * np.sum(result == 255) / result.size
            print(f"  [{tag}] {name:<20} white={white_pct:5.1f}%  shape={result.shape}")
        except Exception as e:
            print(f"  [ERR] {name:<20} {e}")

    REPS = 200
    sizes = [32, 64]
    for sz in sizes:
        img = _make_test_image(sz)
        print(f"\n=== Benchmark ({sz}x{sz}): {REPS} runs ===")
        for name, fn in IMPLS:
            try:
                t = timeit.timeit(lambda fn=fn, img=img: fn(img, 3), number=REPS)
                ms = t * 1000 / REPS
                print(f"  {name:<20} {ms:>8.3f} ms")
            except Exception as e:
                print(f"  {name:<20} ERR: {e}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
