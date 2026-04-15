"""
Convert to Negative - Optimized Variants

Three approaches:
1. Subtraction (255 - image) - standard NumPy
2. Bitwise NOT - XOR with 0xFF
3. LUT inversion - precomputed lookup
"""

import time
import numpy as np


def negative_subtract(image: np.ndarray) -> np.ndarray:
    """
    Standard subtraction approach.

    >>> img = np.array([[0, 128, 255]], dtype=np.uint8)
    >>> negative_subtract(img)
    array([[255, 127,   0]], dtype=uint8)
    """
    return np.uint8(255) - image


def negative_bitwise(image: np.ndarray) -> np.ndarray:
    """
    Bitwise NOT (XOR with 0xFF). Works because uint8 NOT(x) = 255 - x.

    >>> img = np.array([[0, 128, 255]], dtype=np.uint8)
    >>> negative_bitwise(img)
    array([[255, 127,   0]], dtype=uint8)
    """
    return np.bitwise_not(image)


def negative_lut(image: np.ndarray) -> np.ndarray:
    """
    Lookup table approach.

    >>> img = np.array([[0, 128, 255]], dtype=np.uint8)
    >>> negative_lut(img)
    array([[255, 127,   0]], dtype=uint8)
    """
    lut = np.arange(255, -1, -1, dtype=np.uint8)
    return lut[image]


def benchmark(size: int = 1024, iterations: int = 200) -> None:
    """Benchmark all variants."""
    image = np.random.randint(0, 256, (size, size), dtype=np.uint8)

    variants = [
        ("Subtract (255-x)", negative_subtract),
        ("Bitwise NOT", negative_bitwise),
        ("LUT", negative_lut),
    ]

    print(f"Benchmark: {size}x{size} image, {iterations} iterations\n")
    print(f"{'Variant':<20} {'Total (ms)':>12} {'Per-call (ms)':>14}")
    print("-" * 48)

    for name, func in variants:
        func(image)
        start = time.perf_counter()
        for _ in range(iterations):
            func(image, )
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:<20} {elapsed:>12.2f} {elapsed / iterations:>14.4f}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
