"""
Morphological Erosion - Optimized Variants

Three approaches:
1. Loop-based min (baseline)
2. scipy.ndimage.minimum_filter - C-optimized
3. Decomposed 1D passes - horizontal + vertical minimum
"""

import time
import numpy as np


def erosion_loops(image, kernel=None):
    """
    Standard loop-based erosion.

    >>> img = np.ones((3, 3), dtype=np.uint8)
    >>> erosion_loops(img)[1, 1]
    1
    """
    if kernel is None:
        kernel = np.ones((3, 3), dtype=np.uint8)
    kh, kw = kernel.shape
    ph, pw = kh // 2, kw // 2
    h, w = image.shape
    padded = np.pad(image, ((ph, ph), (pw, pw)), mode="constant", constant_values=0)
    output = np.zeros_like(image)
    for i in range(h):
        for j in range(w):
            region = padded[i:i+kh, j:j+kw]
            output[i, j] = np.min(region[kernel == 1])
    return output


def erosion_scipy(image, kernel_size=3):
    """
    scipy minimum_filter.

    >>> img = np.ones((3, 3), dtype=np.uint8)
    >>> erosion_scipy(img)[1, 1]
    1
    """
    from scipy.ndimage import minimum_filter
    return minimum_filter(image, size=kernel_size).astype(image.dtype)


def erosion_decomposed(image, kernel_size=3):
    """
    Decomposed into horizontal + vertical 1D minimum passes.

    >>> img = np.ones((3, 3), dtype=np.uint8)
    >>> erosion_decomposed(img)[1, 1]
    1
    """
    from scipy.ndimage import minimum_filter1d
    temp = minimum_filter1d(image, size=kernel_size, axis=1)
    return minimum_filter1d(temp, size=kernel_size, axis=0).astype(image.dtype)


def benchmark(size=256, iterations=20):
    image = (np.random.rand(size, size) > 0.3).astype(np.uint8)
    variants = [
        ("Loop-based", lambda: erosion_loops(image)),
        ("scipy min_filter", lambda: erosion_scipy(image)),
        ("Decomposed 1D", lambda: erosion_decomposed(image)),
    ]

    print(f"Benchmark: {size}x{size} binary, {iterations} iterations\n")
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
