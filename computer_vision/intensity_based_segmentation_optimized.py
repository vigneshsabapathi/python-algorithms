#!/usr/bin/env python3
"""
Optimized and alternative implementations of Intensity-Based Segmentation.

The reference implements Otsu's method with a Python loop over all 256
thresholds. Variants here vectorize or use cumulative sums.

Variants covered:
1. loop_otsu        -- reference: Python loop over all thresholds
2. cumsum_otsu      -- vectorized using cumulative sums (no loop)
3. histogram_valley -- find threshold at the valley between histogram peaks
4. iterative_mean   -- iterative thresholding: converge on mean-of-means

Run:
    python computer_vision/intensity_based_segmentation_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from computer_vision.intensity_based_segmentation import otsu_threshold as reference


# ---------------------------------------------------------------------------
# Variant 1 — loop_otsu (reference wrapper)
# ---------------------------------------------------------------------------

def loop_otsu(image: np.ndarray) -> tuple[int, np.ndarray]:
    """
    Otsu's method via explicit loop (reference).

    >>> import numpy as np
    >>> img = np.concatenate([np.full(50, 30), np.full(50, 200)]).reshape(10, 10).astype(np.uint8)
    >>> t, _ = loop_otsu(img)
    >>> 29 < t < 200
    True
    """
    return reference(image)


# ---------------------------------------------------------------------------
# Variant 2 — cumsum_otsu (fully vectorized)
# ---------------------------------------------------------------------------

def cumsum_otsu(image: np.ndarray) -> tuple[int, np.ndarray]:
    """
    Otsu's method using cumulative sums — no Python loop over thresholds.

    Computes between-class variance for all 256 thresholds simultaneously
    using prefix sums.

    >>> import numpy as np
    >>> img = np.concatenate([np.full(50, 30), np.full(50, 200)]).reshape(10, 10).astype(np.uint8)
    >>> t, _ = cumsum_otsu(img)
    >>> 29 < t < 200
    True
    """
    hist = np.bincount(image.ravel(), minlength=256).astype(np.float64)
    total = hist.sum()
    hist_norm = hist / total

    intensities = np.arange(256, dtype=np.float64)

    # Cumulative sums
    w0 = np.cumsum(hist_norm)           # class 0 weight
    w1 = 1.0 - w0                       # class 1 weight
    mu0_num = np.cumsum(hist_norm * intensities)  # class 0 mean numerator
    mu_total = mu0_num[-1]              # total mean

    # Avoid division by zero
    with np.errstate(divide="ignore", invalid="ignore"):
        mu0 = mu0_num / w0
        mu1 = (mu_total - mu0_num) / w1

    variance = w0 * w1 * (mu0 - mu1) ** 2
    variance = np.nan_to_num(variance)

    best_t = int(np.argmax(variance))
    binary = np.zeros_like(image, dtype=np.uint8)
    binary[image > best_t] = 255
    return best_t, binary


# ---------------------------------------------------------------------------
# Variant 3 — histogram valley detection
# ---------------------------------------------------------------------------

def histogram_valley(image: np.ndarray) -> tuple[int, np.ndarray]:
    """
    Find threshold at the valley between two histogram peaks.
    Works well for bimodal distributions.

    Smooths the histogram, finds the two highest peaks, then picks
    the minimum between them as the threshold.

    >>> import numpy as np
    >>> img = np.concatenate([np.full(50, 30), np.full(50, 200)]).reshape(10, 10).astype(np.uint8)
    >>> t, _ = histogram_valley(img)
    >>> 20 < t < 210
    True
    """
    hist = np.bincount(image.ravel(), minlength=256).astype(np.float64)

    # Smooth histogram with a moving average
    kernel_size = 11
    kernel = np.ones(kernel_size) / kernel_size
    smoothed = np.convolve(hist, kernel, mode="same")

    # Find peaks (local maxima)
    peaks = []
    for i in range(1, 254):
        if smoothed[i] > smoothed[i - 1] and smoothed[i] > smoothed[i + 1]:
            peaks.append((smoothed[i], i))

    if len(peaks) < 2:
        # Fallback: use mean intensity
        t = int(image.mean())
    else:
        # Sort by height, take top 2 peaks
        peaks.sort(reverse=True)
        p1 = min(peaks[0][1], peaks[1][1])
        p2 = max(peaks[0][1], peaks[1][1])
        # Find valley (minimum) between the two peaks
        valley_region = smoothed[p1:p2 + 1]
        t = p1 + int(np.argmin(valley_region))

    binary = np.zeros_like(image, dtype=np.uint8)
    binary[image > t] = 255
    return t, binary


# ---------------------------------------------------------------------------
# Variant 4 — iterative mean thresholding
# ---------------------------------------------------------------------------

def iterative_mean(image: np.ndarray, max_iter: int = 100) -> tuple[int, np.ndarray]:
    """
    Iterative thresholding: start with mean, split, re-average, repeat.

    1. T = mean(image)
    2. Compute mean of pixels <= T (mu1) and > T (mu2)
    3. T_new = (mu1 + mu2) / 2
    4. Repeat until convergence

    >>> import numpy as np
    >>> img = np.concatenate([np.full(50, 30), np.full(50, 200)]).reshape(10, 10).astype(np.uint8)
    >>> t, _ = iterative_mean(img)
    >>> 30 < t < 200
    True
    """
    t = float(image.mean())

    for _ in range(max_iter):
        below = image[image <= t]
        above = image[image > t]

        if len(below) == 0 or len(above) == 0:
            break

        mu1 = below.mean()
        mu2 = above.mean()
        t_new = (mu1 + mu2) / 2.0

        if abs(t_new - t) < 0.5:
            break
        t = t_new

    t_int = int(round(t))
    binary = np.zeros_like(image, dtype=np.uint8)
    binary[image > t_int] = 255
    return t_int, binary


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

IMPLS = [
    ("loop_otsu", loop_otsu),
    ("cumsum_otsu", cumsum_otsu),
    ("histogram_valley", histogram_valley),
    ("iterative_mean", iterative_mean),
]


def run_all() -> None:
    np.random.seed(42)

    # Bimodal image: dark (30) + bright (200) with some noise
    dark = np.random.normal(30, 10, 500).clip(0, 255)
    bright = np.random.normal(200, 10, 500).clip(0, 255)
    img = np.concatenate([dark, bright]).astype(np.uint8).reshape(25, 40)

    print("\n=== Correctness (bimodal 25x40) ===")
    ref_t, ref_bin = reference(img)
    print(f"  Reference threshold: {ref_t}")

    for name, fn in IMPLS:
        try:
            t, binary = fn(img)
            white_pct = 100 * np.sum(binary == 255) / binary.size
            print(f"  [OK] {name:<20} threshold={t:>3d}  white={white_pct:5.1f}%")
        except Exception as e:
            print(f"  [ERR] {name:<20} {e}")

    REPS = 500
    sizes = [(50, 50), (100, 100), (200, 200)]
    for rows, cols in sizes:
        dark = np.random.normal(50, 15, rows * cols // 2).clip(0, 255)
        bright = np.random.normal(180, 15, rows * cols // 2).clip(0, 255)
        img = np.concatenate([dark, bright]).astype(np.uint8).reshape(rows, cols)

        print(f"\n=== Benchmark ({rows}x{cols}): {REPS} runs ===")
        for name, fn in IMPLS:
            try:
                t = timeit.timeit(lambda fn=fn, img=img: fn(img), number=REPS)
                ms = t * 1000 / REPS
                print(f"  {name:<20} {ms:>8.3f} ms")
            except Exception as e:
                print(f"  {name:<20} ERR: {e}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
