"""
Sobel Filter - Optimized Variants

Three approaches:
1. Loop-based (baseline) - explicit convolution loops
2. scipy.ndimage.convolve - C-optimized
3. Separable Sobel - exploit that Sobel = outer product of [1,2,1] and [-1,0,1]
"""

import time
import numpy as np
from scipy.ndimage import convolve

SOBEL_X = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float64)
SOBEL_Y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype=np.float64)


def sobel_loops(image):
    """
    Loop-based Sobel.

    >>> flat = np.full((5, 5), 100.0)
    >>> sobel_loops(flat)[2, 2]
    0.0
    """
    img = image.astype(np.float64)
    h, w = img.shape
    padded = np.pad(img, 1, mode="constant")
    gx = np.zeros_like(img)
    gy = np.zeros_like(img)
    for i in range(h):
        for j in range(w):
            region = padded[i:i+3, j:j+3]
            gx[i, j] = np.sum(region * SOBEL_X)
            gy[i, j] = np.sum(region * SOBEL_Y)
    return np.hypot(gx, gy)


def sobel_scipy(image):
    """
    scipy convolve-based Sobel.

    >>> flat = np.full((5, 5), 100.0)
    >>> np.allclose(sobel_scipy(flat), 0.0)
    True
    """
    img = image.astype(np.float64)
    gx = convolve(img, SOBEL_X)
    gy = convolve(img, SOBEL_Y)
    return np.hypot(gx, gy)


def sobel_separable(image):
    """
    Separable Sobel: Sobel_X = [1,2,1]^T * [-1,0,1].
    Two 1D passes instead of one 2D convolution.

    >>> flat = np.full((5, 5), 100.0)
    >>> np.allclose(sobel_separable(flat), 0.0)
    True
    """
    img = image.astype(np.float64)
    smooth = np.array([[1], [2], [1]], dtype=np.float64)
    diff = np.array([[-1, 0, 1]], dtype=np.float64)

    # Gx = smooth vertically then diff horizontally
    gx = convolve(convolve(img, smooth), diff)
    # Gy = diff vertically then smooth horizontally
    gy = convolve(convolve(img, diff.T), smooth.T)
    return np.hypot(gx, gy)


def benchmark(size=256, iterations=20):
    image = np.random.rand(size, size) * 255
    variants = [
        ("Loops", sobel_loops),
        ("scipy convolve", sobel_scipy),
        ("Separable", sobel_separable),
    ]

    print(f"Benchmark: {size}x{size}, {iterations} iters\n")
    print(f"{'Variant':<22} {'Total (ms)':>12} {'Per-call (ms)':>14}")
    print("-" * 50)

    for name, func in variants:
        func(image)
        start = time.perf_counter()
        for _ in range(iterations):
            func(image)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:<22} {elapsed:>12.2f} {elapsed / iterations:>14.4f}")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
