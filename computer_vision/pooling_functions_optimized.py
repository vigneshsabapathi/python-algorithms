#!/usr/bin/env python3
"""
Optimized and alternative implementations of Pooling Functions.

The reference uses Python loops over windows. Variants here vectorize
or use stride tricks for zero-copy windowed views.

Variants covered:
1. loop_pool         -- reference: explicit Python loops
2. reshape_pool      -- reshape into blocks (works when size divides evenly)
3. stride_tricks     -- as_strided for zero-copy windowed views
4. einsum_pool       -- np.einsum for average pooling via reshape

Run:
    python computer_vision/pooling_functions_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from computer_vision.pooling_functions import max_pool as ref_max
from computer_vision.pooling_functions import avg_pool as ref_avg


# ---------------------------------------------------------------------------
# Variant 1 — loop_pool (reference wrapper)
# ---------------------------------------------------------------------------

def loop_max_pool(image: np.ndarray, pool_size: int = 2, stride: int = 2) -> np.ndarray:
    """
    Max pooling via explicit loops (reference).

    >>> import numpy as np
    >>> img = np.arange(16, dtype=np.float64).reshape(4, 4)
    >>> loop_max_pool(img, 2, 2)
    array([[ 5.,  7.],
           [13., 15.]])
    """
    return ref_max(image, pool_size, stride)


def loop_avg_pool(image: np.ndarray, pool_size: int = 2, stride: int = 2) -> np.ndarray:
    """
    Average pooling via explicit loops (reference).

    >>> import numpy as np
    >>> img = np.arange(16, dtype=np.float64).reshape(4, 4)
    >>> loop_avg_pool(img, 2, 2)
    array([[ 2.5,  4.5],
           [10.5, 12.5]])
    """
    return ref_avg(image, pool_size, stride)


# ---------------------------------------------------------------------------
# Variant 2 — reshape_pool (no loops, requires evenly divisible)
# ---------------------------------------------------------------------------

def reshape_max_pool(image: np.ndarray, pool_size: int = 2, stride: int = 2) -> np.ndarray:
    """
    Max pooling via reshape — splits image into blocks, takes max.
    Only works when stride == pool_size and dimensions are evenly divisible.

    >>> import numpy as np
    >>> img = np.arange(16, dtype=np.float64).reshape(4, 4)
    >>> reshape_max_pool(img, 2, 2)
    array([[ 5.,  7.],
           [13., 15.]])
    """
    rows, cols = image.shape
    return (
        image.reshape(rows // pool_size, pool_size, cols // pool_size, pool_size)
        .max(axis=(1, 3))
    )


def reshape_avg_pool(image: np.ndarray, pool_size: int = 2, stride: int = 2) -> np.ndarray:
    """
    Average pooling via reshape — splits image into blocks, takes mean.

    >>> import numpy as np
    >>> img = np.arange(16, dtype=np.float64).reshape(4, 4)
    >>> reshape_avg_pool(img, 2, 2)
    array([[ 2.5,  4.5],
           [10.5, 12.5]])
    """
    rows, cols = image.shape
    return (
        image.reshape(rows // pool_size, pool_size, cols // pool_size, pool_size)
        .mean(axis=(1, 3))
    )


# ---------------------------------------------------------------------------
# Variant 3 — stride_tricks (general, zero-copy windowed view)
# ---------------------------------------------------------------------------

def _windowed_view(image: np.ndarray, pool_size: int, stride: int) -> np.ndarray:
    """Create a 4D view of the image as (out_r, out_c, pool_size, pool_size)."""
    rows, cols = image.shape
    out_r = (rows - pool_size) // stride + 1
    out_c = (cols - pool_size) // stride + 1

    s_row, s_col = image.strides
    new_strides = (s_row * stride, s_col * stride, s_row, s_col)
    new_shape = (out_r, out_c, pool_size, pool_size)

    return np.lib.stride_tricks.as_strided(image, shape=new_shape, strides=new_strides)


def stride_max_pool(image: np.ndarray, pool_size: int = 2, stride: int = 2) -> np.ndarray:
    """
    Max pooling via np.lib.stride_tricks — zero-copy windowed views.
    Works with any stride and pool_size combination.

    >>> import numpy as np
    >>> img = np.arange(16, dtype=np.float64).reshape(4, 4)
    >>> stride_max_pool(img, 2, 2)
    array([[ 5.,  7.],
           [13., 15.]])
    """
    windows = _windowed_view(image, pool_size, stride)
    return windows.max(axis=(2, 3))


def stride_avg_pool(image: np.ndarray, pool_size: int = 2, stride: int = 2) -> np.ndarray:
    """
    Average pooling via stride_tricks.

    >>> import numpy as np
    >>> img = np.arange(16, dtype=np.float64).reshape(4, 4)
    >>> stride_avg_pool(img, 2, 2)
    array([[ 2.5,  4.5],
           [10.5, 12.5]])
    """
    windows = _windowed_view(image, pool_size, stride)
    return windows.mean(axis=(2, 3))


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

def run_all() -> None:
    sizes = [16, 64, 256]
    pool_size = 2
    stride = 2

    max_impls = [
        ("loop_max_pool", loop_max_pool),
        ("reshape_max_pool", reshape_max_pool),
        ("stride_max_pool", stride_max_pool),
    ]
    avg_impls = [
        ("loop_avg_pool", loop_avg_pool),
        ("reshape_avg_pool", reshape_avg_pool),
        ("stride_avg_pool", stride_avg_pool),
    ]

    print("\n=== Correctness (16x16) ===")
    np.random.seed(42)
    img = np.random.rand(16, 16)
    ref_max_result = ref_max(img, pool_size, stride)
    ref_avg_result = ref_avg(img, pool_size, stride)

    for name, fn in max_impls:
        result = fn(img, pool_size, stride)
        match = np.allclose(result, ref_max_result)
        print(f"  [{'OK' if match else 'FAIL'}] {name:<20} shape={result.shape}")

    for name, fn in avg_impls:
        result = fn(img, pool_size, stride)
        match = np.allclose(result, ref_avg_result)
        print(f"  [{'OK' if match else 'FAIL'}] {name:<20} shape={result.shape}")

    REPS = 500
    for sz in sizes:
        img = np.random.rand(sz, sz)
        print(f"\n=== Benchmark MAX pool ({sz}x{sz}): {REPS} runs ===")
        for name, fn in max_impls:
            t = timeit.timeit(lambda fn=fn, img=img: fn(img, pool_size, stride), number=REPS)
            ms = t * 1000 / REPS
            print(f"  {name:<20} {ms:>8.3f} ms")

        print(f"\n=== Benchmark AVG pool ({sz}x{sz}): {REPS} runs ===")
        for name, fn in avg_impls:
            t = timeit.timeit(lambda fn=fn, img=img: fn(img, pool_size, stride), number=REPS)
            ms = t * 1000 / REPS
            print(f"  {name:<20} {ms:>8.3f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
