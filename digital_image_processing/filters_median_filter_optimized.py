"""
Median Filter - Optimized Variants

Three approaches:
1. Loop with np.median (baseline)
2. Histogram-based sliding median - O(1) per pixel for uint8 images
3. scipy.ndimage.median_filter - optimized C implementation
"""

import time
import numpy as np


def median_loop(image, kernel_size=3):
    """
    Standard loop with np.median.

    >>> np.allclose(median_loop(np.full((3, 3), 5.0), 3), 5.0)
    True
    """
    img = image.astype(np.float64)
    h, w = img.shape
    half = kernel_size // 2
    padded = np.pad(img, half, mode="edge")
    output = np.zeros_like(img)
    for i in range(h):
        for j in range(w):
            output[i, j] = np.median(padded[i:i+kernel_size, j:j+kernel_size])
    return output


def median_histogram(image, kernel_size=3):
    """
    Histogram-based sliding window median for uint8 images.
    Updates histogram incrementally as window slides right.

    >>> np.allclose(median_histogram(np.full((3, 3), 5, dtype=np.uint8), 3), 5)
    True
    """
    img = image.astype(np.uint8)
    h, w = img.shape
    half = kernel_size // 2
    padded = np.pad(img, half, mode="edge")
    output = np.zeros((h, w), dtype=np.uint8)
    ks = kernel_size
    median_idx = (ks * ks) // 2

    for i in range(h):
        # Initialize histogram for first window in row
        hist = np.zeros(256, dtype=np.int32)
        for dy in range(ks):
            for dx in range(ks):
                hist[padded[i + dy, dx]] += 1

        # Find median
        cumsum = 0
        median_val = 0
        for v in range(256):
            cumsum += hist[v]
            if cumsum > median_idx:
                median_val = v
                break
        output[i, 0] = median_val

        # Slide window right
        for j in range(1, w):
            # Remove left column, add right column
            for dy in range(ks):
                hist[padded[i + dy, j - 1]] -= 1
                hist[padded[i + dy, j + ks - 1]] += 1

            # Find new median
            cumsum = 0
            for v in range(256):
                cumsum += hist[v]
                if cumsum > median_idx:
                    output[i, j] = v
                    break

    return output


def median_scipy(image, kernel_size=3):
    """
    scipy.ndimage.median_filter wrapper.

    >>> from scipy.ndimage import median_filter as mf
    >>> np.allclose(median_scipy(np.full((3, 3), 5.0), 3), 5.0)
    True
    """
    from scipy.ndimage import median_filter as mf
    return mf(image.astype(np.float64), size=kernel_size)


def benchmark(size=64, kernel_size=3, iterations=5):
    image = np.random.randint(0, 256, (size, size), dtype=np.uint8)
    variants = [
        ("Loop np.median", lambda: median_loop(image.astype(np.float64), kernel_size)),
        ("Histogram sliding", lambda: median_histogram(image, kernel_size)),
        ("scipy.ndimage", lambda: median_scipy(image, kernel_size)),
    ]

    print(f"Benchmark: {size}x{size}, kernel={kernel_size}, {iterations} iters\n")
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
