"""
Histogram Stretching - Optimized Variants

Three approaches:
1. Standard (baseline) - float division with min/max
2. LUT-based - precompute mapping for all 256 values
3. Percentile stretch - robust to outliers using p2/p98
"""

import time
import numpy as np


def stretch_standard(image):
    """
    Standard min-max histogram stretch.

    >>> img = np.array([[50, 200]], dtype=np.uint8)
    >>> stretch_standard(img).tolist()
    [[0, 255]]
    """
    img = image.astype(np.float64)
    mn, mx = img.min(), img.max()
    if mx == mn:
        return np.zeros_like(image, dtype=np.uint8)
    return ((img - mn) / (mx - mn) * 255).astype(np.uint8)


def stretch_lut(image):
    """
    LUT approach: precompute mapping for all 256 input values.

    >>> img = np.array([[50, 200]], dtype=np.uint8)
    >>> stretch_lut(img).tolist()
    [[0, 255]]
    """
    mn, mx = int(image.min()), int(image.max())
    if mx == mn:
        return np.zeros_like(image, dtype=np.uint8)
    lut = np.clip(
        ((np.arange(256) - mn) * 255.0 / (mx - mn)), 0, 255
    ).astype(np.uint8)
    return lut[image]


def stretch_percentile(image, low_pct=2, high_pct=98):
    """
    Percentile-based stretch: robust to outliers.

    >>> img = np.array([[0, 50, 100, 150, 200, 255]], dtype=np.uint8)
    >>> result = stretch_percentile(img, 0, 100)
    >>> result[0, 0], result[0, -1]
    (0, 255)
    """
    img = image.astype(np.float64)
    mn = np.percentile(img, low_pct)
    mx = np.percentile(img, high_pct)
    if mx == mn:
        return np.zeros_like(image, dtype=np.uint8)
    return np.clip((img - mn) / (mx - mn) * 255, 0, 255).astype(np.uint8)


def benchmark(size=1024, iterations=100):
    image = np.random.randint(50, 200, (size, size), dtype=np.uint8)
    variants = [
        ("Standard", stretch_standard),
        ("LUT", stretch_lut),
        ("Percentile (2-98)", lambda img: stretch_percentile(img, 2, 98)),
    ]

    print(f"Benchmark: {size}x{size}, {iterations} iterations\n")
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
