#!/usr/bin/env python3
"""
Optimized and alternative implementations of Flip Augmentation.

The reference uses numpy slicing with .copy(). Variants explore
in-place operations, np.flip, and transpose-based approaches.

Variants covered:
1. slice_copy       -- reference: numpy slice + copy
2. np_flip          -- np.flip / np.flipud / np.fliplr (standard API)
3. index_array      -- explicit index array construction
4. inplace_swap     -- in-place row/column swapping (no allocation)

Run:
    python computer_vision/flip_augmentation_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from computer_vision.flip_augmentation import flip_horizontal as ref_h
from computer_vision.flip_augmentation import flip_vertical as ref_v
from computer_vision.flip_augmentation import flip_both as ref_b


# ---------------------------------------------------------------------------
# Variant 1 — slice_copy (reference wrapper)
# ---------------------------------------------------------------------------

def slice_h(image: np.ndarray) -> np.ndarray:
    """
    Horizontal flip via numpy slice + copy.

    >>> import numpy as np
    >>> slice_h(np.array([[1, 2], [3, 4]]))
    array([[2, 1],
           [4, 3]])
    """
    return ref_h(image)


def slice_v(image: np.ndarray) -> np.ndarray:
    """
    Vertical flip via numpy slice + copy.

    >>> import numpy as np
    >>> slice_v(np.array([[1, 2], [3, 4]]))
    array([[3, 4],
           [1, 2]])
    """
    return ref_v(image)


# ---------------------------------------------------------------------------
# Variant 2 — np.flip / np.flipud / np.fliplr
# ---------------------------------------------------------------------------

def npflip_h(image: np.ndarray) -> np.ndarray:
    """
    Horizontal flip via np.fliplr.

    >>> import numpy as np
    >>> npflip_h(np.array([[1, 2], [3, 4]]))
    array([[2, 1],
           [4, 3]])
    """
    return np.fliplr(image).copy()


def npflip_v(image: np.ndarray) -> np.ndarray:
    """
    Vertical flip via np.flipud.

    >>> import numpy as np
    >>> npflip_v(np.array([[1, 2], [3, 4]]))
    array([[3, 4],
           [1, 2]])
    """
    return np.flipud(image).copy()


# ---------------------------------------------------------------------------
# Variant 3 — index array construction
# ---------------------------------------------------------------------------

def index_h(image: np.ndarray) -> np.ndarray:
    """
    Horizontal flip via explicit index array.

    >>> import numpy as np
    >>> index_h(np.array([[1, 2], [3, 4]]))
    array([[2, 1],
           [4, 3]])
    """
    cols = image.shape[1]
    idx = np.arange(cols - 1, -1, -1)
    return image[:, idx]


def index_v(image: np.ndarray) -> np.ndarray:
    """
    Vertical flip via explicit index array.

    >>> import numpy as np
    >>> index_v(np.array([[1, 2], [3, 4]]))
    array([[3, 4],
           [1, 2]])
    """
    rows = image.shape[0]
    idx = np.arange(rows - 1, -1, -1)
    return image[idx, :]


# ---------------------------------------------------------------------------
# Variant 4 — in-place swap (no extra allocation)
# ---------------------------------------------------------------------------

def inplace_h(image: np.ndarray) -> np.ndarray:
    """
    Horizontal flip via in-place column swapping.

    >>> import numpy as np
    >>> img = np.array([[1, 2, 3], [4, 5, 6]])
    >>> inplace_h(img)
    array([[3, 2, 1],
           [6, 5, 4]])
    """
    result = image.copy()
    cols = result.shape[1]
    for j in range(cols // 2):
        result[:, j], result[:, cols - 1 - j] = (
            result[:, cols - 1 - j].copy(),
            result[:, j].copy(),
        )
    return result


def inplace_v(image: np.ndarray) -> np.ndarray:
    """
    Vertical flip via in-place row swapping.

    >>> import numpy as np
    >>> img = np.array([[1, 2], [3, 4], [5, 6]])
    >>> inplace_v(img)
    array([[5, 6],
           [3, 4],
           [1, 2]])
    """
    result = image.copy()
    rows = result.shape[0]
    for i in range(rows // 2):
        result[i, :], result[rows - 1 - i, :] = (
            result[rows - 1 - i, :].copy(),
            result[i, :].copy(),
        )
    return result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

H_IMPLS = [
    ("slice_h", slice_h),
    ("npflip_h", npflip_h),
    ("index_h", index_h),
    ("inplace_h", inplace_h),
]

V_IMPLS = [
    ("slice_v", slice_v),
    ("npflip_v", npflip_v),
    ("index_v", index_v),
    ("inplace_v", inplace_v),
]


def run_all() -> None:
    np.random.seed(42)
    img = np.random.randint(0, 256, (64, 64), dtype=np.uint8)

    print("\n=== Correctness (64x64) ===")
    ref_hr = ref_h(img)
    ref_vr = ref_v(img)

    for name, fn in H_IMPLS:
        result = fn(img)
        match = np.array_equal(result, ref_hr)
        print(f"  [{'OK' if match else 'FAIL'}] {name}")

    for name, fn in V_IMPLS:
        result = fn(img)
        match = np.array_equal(result, ref_vr)
        print(f"  [{'OK' if match else 'FAIL'}] {name}")

    REPS = 5000
    sizes = [64, 256, 1024]
    for sz in sizes:
        img = np.random.randint(0, 256, (sz, sz), dtype=np.uint8)
        print(f"\n=== Benchmark horizontal flip ({sz}x{sz}): {REPS} runs ===")
        for name, fn in H_IMPLS:
            t = timeit.timeit(lambda fn=fn, img=img: fn(img), number=REPS)
            ms = t * 1000 / REPS
            print(f"  {name:<12} {ms:>8.4f} ms")

        print(f"\n=== Benchmark vertical flip ({sz}x{sz}): {REPS} runs ===")
        for name, fn in V_IMPLS:
            t = timeit.timeit(lambda fn=fn, img=img: fn(img), number=REPS)
            ms = t * 1000 / REPS
            print(f"  {name:<12} {ms:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
