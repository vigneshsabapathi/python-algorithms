"""
Laplacian Filter - Optimized Variants

Three approaches:
1. Loop convolution (baseline) - explicit nested loops
2. scipy.ndimage.convolve - optimized C implementation
3. LoG (Laplacian of Gaussian) - Gaussian smoothing + Laplacian combined
"""

import time
import numpy as np
from scipy.ndimage import convolve

LAPLACIAN_4 = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float64)


def laplacian_loops(image, kernel=None):
    """
    Loop-based Laplacian.

    >>> flat = np.full((5, 5), 50.0)
    >>> laplacian_loops(flat)[2, 2]
    0.0
    """
    if kernel is None:
        kernel = LAPLACIAN_4
    img = image.astype(np.float64)
    kh, kw = kernel.shape
    half = kh // 2
    h, w = img.shape
    padded = np.pad(img, half, mode="constant")
    output = np.zeros_like(img)
    for i in range(h):
        for j in range(w):
            output[i, j] = np.sum(padded[i:i + kh, j:j + kw] * kernel)
    return output


def laplacian_scipy(image, kernel=None):
    """
    scipy.ndimage.convolve (C-optimized).

    >>> flat = np.full((5, 5), 50.0)
    >>> np.allclose(laplacian_scipy(flat), 0.0)
    True
    """
    if kernel is None:
        kernel = LAPLACIAN_4
    return convolve(image.astype(np.float64), kernel)


def laplacian_of_gaussian(image, sigma=1.0, size=5):
    """
    LoG: combined Gaussian smoothing + Laplacian.
    Uses the LoG kernel directly.

    >>> flat = np.full((5, 5), 50.0)
    >>> abs(laplacian_of_gaussian(flat).sum()) < 1e-6
    True
    """
    half = size // 2
    y, x = np.mgrid[-half:half + 1, -half:half + 1].astype(np.float64)
    # LoG formula
    r2 = x**2 + y**2
    s2 = sigma**2
    log_kernel = -(1 / (np.pi * s2**2)) * (1 - r2 / (2 * s2)) * np.exp(-r2 / (2 * s2))
    log_kernel -= log_kernel.mean()  # ensure zero-sum
    return convolve(image.astype(np.float64), log_kernel)


def benchmark(size=128, iterations=20):
    image = np.random.rand(size, size) * 255
    variants = [
        ("Loop-based", lambda: laplacian_loops(image)),
        ("scipy convolve", lambda: laplacian_scipy(image)),
        ("LoG (sigma=1)", lambda: laplacian_of_gaussian(image, 1.0, 5)),
    ]

    print(f"Benchmark: {size}x{size}, {iterations} iters\n")
    print(f"{'Variant':<22} {'Total (ms)':>12} {'Per-call (ms)':>14}")
    print("-" * 50)

    for name, func in variants:
        func()
        start = time.perf_counter()
        for _ in range(iterations):
            func()
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:<22} {elapsed:>12.2f} {elapsed / iterations:>14.4f}")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
