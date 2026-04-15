"""
Change Contrast - Optimized Variants

Three approaches:
1. Float64 scaling (baseline) - standard formula with float promotion
2. LUT approach - precomputed lookup table for all 256 values
3. Integer arithmetic - avoid float conversion using fixed-point math
"""

import time
import numpy as np


def contrast_float(image: np.ndarray, factor: float) -> np.ndarray:
    """
    Standard float64 approach.

    >>> img = np.array([[50, 200]], dtype=np.uint8)
    >>> contrast_float(img, 2.0)
    array([[  0, 255]], dtype=uint8)
    """
    result = factor * (image.astype(np.float64) - 128) + 128
    return np.clip(result, 0, 255).astype(np.uint8)


def contrast_lut(image: np.ndarray, factor: float) -> np.ndarray:
    """
    LUT approach: precompute contrast mapping for all 256 values.

    >>> img = np.array([[50, 200]], dtype=np.uint8)
    >>> contrast_lut(img, 2.0)
    array([[  0, 255]], dtype=uint8)
    """
    lut = np.clip(
        factor * (np.arange(256, dtype=np.float64) - 128) + 128, 0, 255
    ).astype(np.uint8)
    return lut[image]


def contrast_int16(image: np.ndarray, factor: float) -> np.ndarray:
    """
    Fixed-point integer arithmetic (factor * 256 as integer).

    >>> img = np.array([[50, 200]], dtype=np.uint8)
    >>> contrast_int16(img, 2.0)
    array([[  0, 255]], dtype=uint8)
    """
    # Scale factor to fixed-point (8-bit fractional)
    f = int(factor * 256)
    centered = image.astype(np.int32) - 128
    result = (centered * f) >> 8  # divide by 256
    result += 128
    return np.clip(result, 0, 255).astype(np.uint8)


def benchmark(size: int = 1024, iterations: int = 100) -> None:
    """Benchmark all variants."""
    image = np.random.randint(0, 256, (size, size), dtype=np.uint8)
    factor = 1.5

    variants = [
        ("Float64", contrast_float),
        ("LUT", contrast_lut),
        ("Int16 fixed-point", contrast_int16),
    ]

    print(f"Benchmark: {size}x{size} image, {iterations} iterations, factor={factor}\n")
    print(f"{'Variant':<20} {'Total (ms)':>12} {'Per-call (ms)':>14}")
    print("-" * 48)

    for name, func in variants:
        func(image, factor)
        start = time.perf_counter()
        for _ in range(iterations):
            func(image, factor)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:<20} {elapsed:>12.2f} {elapsed / iterations:>14.4f}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
