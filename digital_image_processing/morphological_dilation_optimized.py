"""
Morphological Dilation - Optimized Variants

Three approaches:
1. Loop-based max (baseline)
2. scipy.ndimage.maximum_filter - C-optimized
3. Decomposed structuring element - separate horizontal + vertical passes
"""

import time
import numpy as np


def dilation_loops(image, kernel=None):
    """
    Standard loop-based dilation.

    >>> img = np.array([[0, 1, 0], [0, 0, 0], [0, 0, 0]], dtype=np.uint8)
    >>> dilation_loops(img)[0, 0]
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
            output[i, j] = np.max(region[kernel == 1])
    return output


def dilation_scipy(image, kernel_size=3):
    """
    scipy maximum_filter (equivalent to dilation with rectangular SE).

    >>> img = np.array([[0, 1, 0], [0, 0, 0], [0, 0, 0]], dtype=np.uint8)
    >>> dilation_scipy(img)[0, 0]
    1
    """
    from scipy.ndimage import maximum_filter
    return maximum_filter(image, size=kernel_size).astype(image.dtype)


def dilation_decomposed(image, kernel_size=3):
    """
    Decompose rectangular SE into horizontal + vertical 1D passes.
    O(N*2K) instead of O(N*K^2).

    >>> img = np.array([[0, 1, 0], [0, 0, 0], [0, 0, 0]], dtype=np.uint8)
    >>> dilation_decomposed(img)[0, 0]
    1
    """
    from scipy.ndimage import maximum_filter1d
    temp = maximum_filter1d(image, size=kernel_size, axis=1)
    return maximum_filter1d(temp, size=kernel_size, axis=0).astype(image.dtype)


def benchmark(size=256, iterations=20):
    image = (np.random.rand(size, size) > 0.7).astype(np.uint8)
    variants = [
        ("Loop-based", lambda: dilation_loops(image)),
        ("scipy max_filter", lambda: dilation_scipy(image)),
        ("Decomposed 1D", lambda: dilation_decomposed(image)),
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
