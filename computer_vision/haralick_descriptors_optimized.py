#!/usr/bin/env python3
"""
Optimized and alternative implementations of Haralick Descriptors.

The reference builds the GLCM with Python loops. Variants here
vectorize GLCM construction and explore symmetric GLCM.

Variants covered:
1. loop_glcm        -- reference: Python loop for GLCM construction
2. vectorized_glcm  -- numpy advanced indexing (no loops)
3. symmetric_glcm   -- symmetric GLCM (average of P and P^T)
4. multi_distance   -- descriptors at multiple distances for richer features

Run:
    python computer_vision/haralick_descriptors_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from computer_vision.haralick_descriptors import (
    compute_glcm as ref_glcm,
    compute_all_descriptors as reference,
    haralick_contrast,
    haralick_correlation,
    haralick_energy,
    haralick_homogeneity,
    haralick_entropy,
)


# ---------------------------------------------------------------------------
# Variant 1 — loop_glcm (reference wrapper)
# ---------------------------------------------------------------------------

def loop_glcm(image: np.ndarray, distance: int = 1, angle: float = 0, levels: int = 256) -> np.ndarray:
    """
    GLCM via Python loop (reference).

    >>> import numpy as np
    >>> img = np.array([[0, 1], [1, 0]], dtype=np.uint8)
    >>> glcm = loop_glcm(img, levels=2)
    >>> glcm.shape
    (2, 2)
    """
    return ref_glcm(image, distance, angle, levels)


# ---------------------------------------------------------------------------
# Variant 2 — vectorized GLCM (no Python loop)
# ---------------------------------------------------------------------------

def vectorized_glcm(
    image: np.ndarray, distance: int = 1, angle: float = 0, levels: int = 256
) -> np.ndarray:
    """
    GLCM via numpy advanced indexing — no explicit Python loops.

    Uses array slicing to extract all valid pixel pairs at once,
    then np.add.at for histogram accumulation.

    >>> import numpy as np
    >>> img = np.array([[0, 1, 2], [1, 2, 0], [2, 0, 1]], dtype=np.uint8)
    >>> glcm = vectorized_glcm(img, levels=3)
    >>> glcm.shape
    (3, 3)
    >>> abs(glcm.sum() - 1.0) < 1e-10
    True
    """
    dx = int(round(distance * np.cos(angle)))
    dy = int(round(distance * np.sin(angle)))

    rows, cols = image.shape

    # Determine valid source and target ranges
    r_start = max(0, -dy)
    r_end = min(rows, rows - dy)
    c_start = max(0, -dx)
    c_end = min(cols, cols - dx)

    source = image[r_start:r_end, c_start:c_end]
    target = image[r_start + dy:r_end + dy, c_start + dx:c_end + dx]

    glcm = np.zeros((levels, levels), dtype=np.float64)
    np.add.at(glcm, (source.ravel(), target.ravel()), 1)

    total = glcm.sum()
    if total > 0:
        glcm /= total

    return glcm


# ---------------------------------------------------------------------------
# Variant 3 — symmetric GLCM
# ---------------------------------------------------------------------------

def symmetric_glcm(
    image: np.ndarray, distance: int = 1, angle: float = 0, levels: int = 256
) -> np.ndarray:
    """
    Symmetric GLCM: average of P(i,j) and P(j,i).

    This is the standard approach in practice — makes the GLCM
    invariant to the direction of traversal.

    >>> import numpy as np
    >>> img = np.array([[0, 1], [1, 0]], dtype=np.uint8)
    >>> glcm = symmetric_glcm(img, levels=2)
    >>> np.allclose(glcm, glcm.T)
    True
    """
    glcm = vectorized_glcm(image, distance, angle, levels)
    glcm_sym = (glcm + glcm.T) / 2.0
    return glcm_sym


# ---------------------------------------------------------------------------
# Variant 4 — multi-distance descriptors
# ---------------------------------------------------------------------------

def multi_distance_descriptors(
    image: np.ndarray, distances: list[int] | None = None, levels: int = 256
) -> dict[str, list[float]]:
    """
    Compute Haralick descriptors at multiple distances.
    Returns a dict where each key maps to a list of values (one per distance).

    >>> import numpy as np
    >>> img = np.array([[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]], dtype=np.uint8)
    >>> desc = multi_distance_descriptors(img, distances=[1, 2], levels=4)
    >>> len(desc['contrast'])
    2
    """
    if distances is None:
        distances = [1, 2, 3]

    angles = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
    result: dict[str, list[float]] = {
        "contrast": [],
        "correlation": [],
        "energy": [],
        "homogeneity": [],
        "entropy": [],
    }

    for d in distances:
        desc_per_angle = []
        for angle in angles:
            glcm = vectorized_glcm(image, distance=d, angle=angle, levels=levels)
            desc_per_angle.append({
                "contrast": haralick_contrast(glcm),
                "correlation": haralick_correlation(glcm),
                "energy": haralick_energy(glcm),
                "homogeneity": haralick_homogeneity(glcm),
                "entropy": haralick_entropy(glcm),
            })

        for key in result:
            avg = sum(d_[key] for d_ in desc_per_angle) / len(desc_per_angle)
            result[key].append(avg)

    return result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

def run_all() -> None:
    np.random.seed(42)

    # Test image with known texture
    img = np.array([
        [0, 1, 2, 3, 0, 1],
        [1, 2, 3, 0, 1, 2],
        [2, 3, 0, 1, 2, 3],
        [3, 0, 1, 2, 3, 0],
        [0, 1, 2, 3, 0, 1],
        [1, 2, 3, 0, 1, 2],
    ], dtype=np.uint8)

    print("\n=== Correctness (6x6, 4 gray levels) ===")
    ref_result = reference(img, distance=1, levels=4)
    print(f"  Reference descriptors: { {k: round(v, 4) for k, v in ref_result.items()} }")

    # Compare vectorized GLCM vs loop GLCM
    for angle_name, angle in [("0", 0), ("45", np.pi / 4), ("90", np.pi / 2)]:
        g_loop = ref_glcm(img, distance=1, angle=angle, levels=4)
        g_vec = vectorized_glcm(img, distance=1, angle=angle, levels=4)
        g_sym = symmetric_glcm(img, distance=1, angle=angle, levels=4)
        match = np.allclose(g_loop, g_vec)
        print(f"  [{'OK' if match else 'FAIL'}] angle={angle_name:>3}  loop==vectorized  sym_check={np.allclose(g_sym, g_sym.T)}")

    # Multi-distance
    md = multi_distance_descriptors(img, distances=[1, 2], levels=4)
    print(f"  Multi-distance contrast: {[round(v, 4) for v in md['contrast']]}")

    # Benchmark GLCM construction
    REPS = 200
    sizes = [16, 32, 64]
    for sz in sizes:
        test_img = np.random.randint(0, 8, (sz, sz), dtype=np.uint8)
        print(f"\n=== Benchmark GLCM ({sz}x{sz}, 8 levels): {REPS} runs ===")
        for name, fn in [
            ("loop_glcm", lambda img=test_img: ref_glcm(img, levels=8)),
            ("vectorized_glcm", lambda img=test_img: vectorized_glcm(img, levels=8)),
            ("symmetric_glcm", lambda img=test_img: symmetric_glcm(img, levels=8)),
        ]:
            t = timeit.timeit(fn, number=REPS)
            ms = t * 1000 / REPS
            print(f"  {name:<20} {ms:>8.3f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
