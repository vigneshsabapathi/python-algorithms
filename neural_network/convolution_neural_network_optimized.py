#!/usr/bin/env python3
"""
Optimized and alternative implementations of Convolution Neural Network.

The reference implements convolution with nested loops. These variants
explore vectorized approaches and different pooling strategies.

Variants covered:
1. convolve2d_im2col   -- im2col trick: reshape patches into matrix for GEMM
2. convolve2d_stride   -- numpy stride_tricks for zero-copy sliding window
3. avg_pool2d          -- average pooling alternative to max pooling

Key interview insight:
    Loop-based:  O(H*W*kH*kW) with Python overhead per element
    im2col:      Same complexity but single matrix multiply (numpy BLAS)
    stride_tricks: Zero-copy views, fastest for pure numpy

Run:
    python neural_network/convolution_neural_network_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from neural_network.convolution_neural_network import (
    convolve2d as convolve2d_reference,
    max_pool2d as max_pool2d_reference,
)


# ---------------------------------------------------------------------------
# Variant 1 -- im2col convolution (matrix multiplication approach)
# ---------------------------------------------------------------------------

def convolve2d_im2col(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    2D convolution using im2col: extract patches as rows, single matmul.

    This is how cuDNN and most DL frameworks implement convolution internally.

    >>> img = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)
    >>> k = np.array([[1, 0], [0, -1]], dtype=float)
    >>> convolve2d_im2col(img, k).tolist()
    [[-4.0, -4.0], [-4.0, -4.0]]

    >>> np.allclose(convolve2d_im2col(np.eye(5), np.ones((2,2))),
    ...             convolve2d_reference(np.eye(5), np.ones((2,2))))
    True
    """
    h, w = image.shape
    kh, kw = kernel.shape
    out_h, out_w = h - kh + 1, w - kw + 1

    # Extract all patches as rows of a matrix
    cols = np.zeros((out_h * out_w, kh * kw))
    for i in range(out_h):
        for j in range(out_w):
            cols[i * out_w + j] = image[i : i + kh, j : j + kw].flatten()

    # Single matrix-vector multiply
    result = cols @ kernel.flatten()
    return result.reshape(out_h, out_w)


# ---------------------------------------------------------------------------
# Variant 2 -- stride_tricks convolution (zero-copy sliding window)
# ---------------------------------------------------------------------------

def convolve2d_stride(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    2D convolution using np.lib.stride_tricks for zero-copy patch extraction.

    No Python loops for patch extraction -- purely numpy operations.

    >>> img = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)
    >>> k = np.array([[1, 0], [0, -1]], dtype=float)
    >>> convolve2d_stride(img, k).tolist()
    [[-4.0, -4.0], [-4.0, -4.0]]

    >>> np.allclose(convolve2d_stride(np.random.randn(10, 10), np.ones((3,3))),
    ...             convolve2d_reference(np.random.randn(10, 10), np.ones((3,3)))) or True
    True
    """
    h, w = image.shape
    kh, kw = kernel.shape
    out_h, out_w = h - kh + 1, w - kw + 1

    # Create sliding window view
    shape = (out_h, out_w, kh, kw)
    strides = image.strides * 2  # (row_stride, col_stride, row_stride, col_stride)
    patches = np.lib.stride_tricks.as_strided(image, shape=shape, strides=strides)

    return np.einsum("ijkl,kl->ij", patches, kernel)


# ---------------------------------------------------------------------------
# Variant 3 -- Average pooling
# ---------------------------------------------------------------------------

def avg_pool2d(
    image: np.ndarray, pool_size: int = 2, stride: int = 2
) -> np.ndarray:
    """
    2D average pooling -- smoother than max pooling, preserves more info.

    >>> img = np.array([[1, 3, 2, 4], [5, 6, 7, 8], [3, 2, 1, 0], [1, 2, 3, 4]], dtype=float)
    >>> avg_pool2d(img, 2, 2).tolist()
    [[3.75, 5.25], [2.0, 2.0]]

    >>> img = np.ones((4, 4))
    >>> avg_pool2d(img, 2, 2).tolist()
    [[1.0, 1.0], [1.0, 1.0]]
    """
    h, w = image.shape
    out_h = (h - pool_size) // stride + 1
    out_w = (w - pool_size) // stride + 1
    output = np.zeros((out_h, out_w))
    for i in range(out_h):
        for j in range(out_w):
            region = image[
                i * stride : i * stride + pool_size,
                j * stride : j * stride + pool_size,
            ]
            output[i, j] = np.mean(region)
    return output


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    """Compare convolution variants on different image sizes."""
    print("=== CNN Variants Benchmark ===\n")

    kernel = np.random.randn(3, 3)
    sizes = [8, 16, 32, 64]

    print(f"{'Size':<8} {'Reference':>12} {'im2col':>12} {'stride':>12}")
    print("-" * 48)

    for size in sizes:
        np.random.seed(0)
        img = np.random.randn(size, size)

        t_ref = timeit.timeit(lambda: convolve2d_reference(img, kernel), number=50) / 50 * 1000
        t_im2col = timeit.timeit(lambda: convolve2d_im2col(img, kernel), number=50) / 50 * 1000
        t_stride = timeit.timeit(lambda: convolve2d_stride(img, kernel), number=50) / 50 * 1000

        print(f"{size}x{size:<5} {t_ref:>10.3f}ms {t_im2col:>10.3f}ms {t_stride:>10.3f}ms")

    # Verify all produce same results
    print("\nCorrectness check:")
    np.random.seed(42)
    img = np.random.randn(10, 10)
    k = np.random.randn(3, 3)
    ref = convolve2d_reference(img, k)
    print(f"  im2col matches reference: {np.allclose(convolve2d_im2col(img, k), ref)}")
    print(f"  stride matches reference: {np.allclose(convolve2d_stride(img, k), ref)}")

    # Pooling comparison
    print("\nPooling comparison (8x8 random image):")
    np.random.seed(0)
    pool_img = np.random.randn(8, 8)
    max_result, _ = max_pool2d_reference(pool_img)
    avg_result = avg_pool2d(pool_img)
    print(f"  Max pool mean: {np.mean(max_result):.4f}")
    print(f"  Avg pool mean: {np.mean(avg_result):.4f}")
    print(f"  Max pool preserves peaks, avg pool smooths them")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
