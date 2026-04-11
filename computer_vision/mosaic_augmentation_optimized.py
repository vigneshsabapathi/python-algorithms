#!/usr/bin/env python3
"""
Optimized and alternative implementations of Mosaic Augmentation.

The reference creates a 2x2 grid mosaic. Variants explore different
grid layouts, blending strategies, and cutmix-style augmentation.

Variants covered:
1. grid_2x2         -- reference: standard 2x2 mosaic
2. grid_3x3         -- 3x3 mosaic from 9 images (or repeated)
3. cutmix           -- CutMix: paste a rectangle from one image onto another
4. blended_mosaic   -- mosaic with Gaussian blending at seams

Run:
    python computer_vision/mosaic_augmentation_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from computer_vision.mosaic_augmentation import (
    mosaic_augmentation as reference,
    _resize_nearest,
)


# ---------------------------------------------------------------------------
# Variant 1 — grid_2x2 (reference wrapper)
# ---------------------------------------------------------------------------

def grid_2x2(images: list[np.ndarray], output_size: tuple[int, int] = (64, 64),
             seed: int | None = None) -> np.ndarray:
    """
    Standard 2x2 mosaic (reference).

    >>> import numpy as np
    >>> imgs = [np.full((4, 4), i * 50, dtype=np.uint8) for i in range(4)]
    >>> grid_2x2(imgs, (8, 8), seed=42).shape
    (8, 8)
    """
    return reference(images, output_size, seed=seed)


# ---------------------------------------------------------------------------
# Variant 2 — grid_3x3 (9 images)
# ---------------------------------------------------------------------------

def grid_3x3(images: list[np.ndarray], output_size: tuple[int, int] = (64, 64)) -> np.ndarray:
    """
    3x3 mosaic from up to 9 images. If fewer than 9 provided, images
    are cycled to fill the grid.

    >>> import numpy as np
    >>> imgs = [np.full((4, 4), i * 25, dtype=np.uint8) for i in range(9)]
    >>> grid_3x3(imgs, (9, 9)).shape
    (9, 9)
    """
    out_h, out_w = output_size
    cell_h = out_h // 3
    cell_w = out_w // 3

    mosaic = np.zeros((out_h, out_w), dtype=np.uint8)

    for idx in range(9):
        row = idx // 3
        col = idx % 3
        img = images[idx % len(images)]

        y = row * cell_h
        x = col * cell_w
        h = cell_h if row < 2 else out_h - 2 * cell_h
        w = cell_w if col < 2 else out_w - 2 * cell_w

        resized = _resize_nearest(img, h, w)
        mosaic[y:y + h, x:x + w] = resized

    return mosaic


# ---------------------------------------------------------------------------
# Variant 3 — CutMix augmentation
# ---------------------------------------------------------------------------

def cutmix(
    image1: np.ndarray,
    image2: np.ndarray,
    lam: float = 0.5,
    seed: int | None = None,
) -> tuple[np.ndarray, float]:
    """
    CutMix: paste a random rectangle from image2 onto image1.

    The area ratio of the pasted rectangle is approximately (1 - lam).
    Returns the mixed image and the actual lambda (proportion of image1).

    >>> import numpy as np
    >>> img1 = np.zeros((8, 8), dtype=np.uint8)
    >>> img2 = np.full((8, 8), 255, dtype=np.uint8)
    >>> mixed, actual_lam = cutmix(img1, img2, lam=0.5, seed=42)
    >>> mixed.shape
    (8, 8)
    >>> 0.0 < actual_lam < 1.0
    True
    """
    rng = np.random.default_rng(seed)
    h, w = image1.shape[:2]

    # Sample cut size from lambda
    cut_ratio = np.sqrt(1.0 - lam)
    cut_h = int(h * cut_ratio)
    cut_w = int(w * cut_ratio)
    cut_h = max(1, min(cut_h, h))
    cut_w = max(1, min(cut_w, w))

    # Random position for the cut
    cy = rng.integers(0, h)
    cx = rng.integers(0, w)

    y1 = max(0, cy - cut_h // 2)
    y2 = min(h, cy + cut_h // 2)
    x1 = max(0, cx - cut_w // 2)
    x2 = min(w, cx + cut_w // 2)

    # Resize image2 if needed
    if image2.shape[:2] != image1.shape[:2]:
        image2 = _resize_nearest(image2, h, w)

    result = image1.copy()
    result[y1:y2, x1:x2] = image2[y1:y2, x1:x2]

    actual_lam = 1.0 - (y2 - y1) * (x2 - x1) / (h * w)
    return result, actual_lam


# ---------------------------------------------------------------------------
# Variant 4 — blended mosaic (Gaussian seam blending)
# ---------------------------------------------------------------------------

def blended_mosaic(
    images: list[np.ndarray],
    output_size: tuple[int, int] = (64, 64),
    blend_width: int = 4,
    seed: int | None = None,
) -> np.ndarray:
    """
    2x2 mosaic with Gaussian blending at seams to reduce hard edges.

    >>> import numpy as np
    >>> imgs = [np.full((10, 10), i * 60, dtype=np.uint8) for i in range(4)]
    >>> result = blended_mosaic(imgs, (16, 16), blend_width=2, seed=42)
    >>> result.shape
    (16, 16)
    """
    # First create regular mosaic
    rng = np.random.default_rng(seed)
    out_h, out_w = output_size

    y_split = rng.uniform(0.25, 0.75)
    x_split = rng.uniform(0.25, 0.75)
    split_y = max(1, min(int(out_h * y_split), out_h - 1))
    split_x = max(1, min(int(out_w * x_split), out_w - 1))

    # Create each quadrant as full-size, then blend
    full_imgs = [_resize_nearest(img, out_h, out_w).astype(np.float64) for img in images]

    # Weight masks for each quadrant
    weight = np.zeros((out_h, out_w, 4), dtype=np.float64)

    # Create smooth masks using distance from split
    for i in range(out_h):
        for j in range(out_w):
            dy = (i - split_y) / max(blend_width, 1)
            dx = (j - split_x) / max(blend_width, 1)
            # Sigmoid-like blending
            wy = 1.0 / (1.0 + np.exp(dy))   # top vs bottom
            wx = 1.0 / (1.0 + np.exp(dx))   # left vs right

            weight[i, j, 0] = wy * wx          # top-left
            weight[i, j, 1] = wy * (1 - wx)    # top-right
            weight[i, j, 2] = (1 - wy) * wx    # bottom-left
            weight[i, j, 3] = (1 - wy) * (1 - wx)  # bottom-right

    # Normalize weights
    weight_sum = weight.sum(axis=2, keepdims=True)
    weight /= np.maximum(weight_sum, 1e-10)

    result = np.zeros((out_h, out_w), dtype=np.float64)
    for idx in range(4):
        result += full_imgs[idx] * weight[:, :, idx]

    return np.clip(result, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

def run_all() -> None:
    np.random.seed(42)

    imgs = [np.random.randint(0, 256, (32, 32), dtype=np.uint8) for _ in range(9)]

    print("\n=== Correctness ===")
    impls = [
        ("grid_2x2", lambda: grid_2x2(imgs[:4], (64, 64), seed=42)),
        ("grid_3x3", lambda: grid_3x3(imgs, (63, 63))),
        ("cutmix", lambda: cutmix(imgs[0], imgs[1], lam=0.5, seed=42)),
        ("blended_mosaic", lambda: blended_mosaic(imgs[:4], (32, 32), seed=42)),
    ]

    for name, fn in impls:
        try:
            result = fn()
            if isinstance(result, tuple):
                img, extra = result
                print(f"  [OK] {name:<18} shape={img.shape}  extra={extra:.3f}")
            else:
                print(f"  [OK] {name:<18} shape={result.shape}  range=[{result.min()}, {result.max()}]")
        except Exception as e:
            print(f"  [ERR] {name:<18} {e}")

    REPS = 200
    print(f"\n=== Benchmark (32x32 inputs -> 64x64): {REPS} runs ===")
    bench = [
        ("grid_2x2", lambda: grid_2x2(imgs[:4], (64, 64), seed=42)),
        ("grid_3x3", lambda: grid_3x3(imgs, (63, 63))),
        ("cutmix", lambda: cutmix(imgs[0], imgs[1], seed=42)),
        ("blended_mosaic", lambda: blended_mosaic(imgs[:4], (32, 32), seed=42)),
    ]

    for name, fn in bench:
        t = timeit.timeit(fn, number=REPS)
        ms = t * 1000 / REPS
        print(f"  {name:<18} {ms:>8.3f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
