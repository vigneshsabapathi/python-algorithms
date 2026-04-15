"""
Change Brightness - Optimized Variants

Three approaches compared:
1. NumPy clip (baseline) - vectorized addition with clipping
2. LUT (lookup table) - precompute all 256 mappings
3. In-place with cv2.add - OpenCV saturating arithmetic
4. Numba JIT - compiled pixel loop

Benchmark on 1024x1024 grayscale image.
"""

import time
import numpy as np


def brightness_numpy_clip(image: np.ndarray, level: int) -> np.ndarray:
    """
    NumPy vectorized approach with int16 promotion and clipping.

    >>> img = np.array([[50, 200]], dtype=np.uint8)
    >>> brightness_numpy_clip(img, 100)
    array([[150, 255]], dtype=uint8)
    """
    return np.clip(image.astype(np.int16) + level, 0, 255).astype(np.uint8)


def brightness_lut(image: np.ndarray, level: int) -> np.ndarray:
    """
    Lookup-table approach: precompute mapping for all 256 values.
    Very fast for repeated calls with same level.

    >>> img = np.array([[50, 200]], dtype=np.uint8)
    >>> brightness_lut(img, 100)
    array([[150, 255]], dtype=uint8)
    """
    lut = np.clip(np.arange(256, dtype=np.int16) + level, 0, 255).astype(np.uint8)
    return lut[image]


def brightness_saturate(image: np.ndarray, level: int) -> np.ndarray:
    """
    Manual saturating arithmetic using np.where to avoid int16 copy.

    >>> img = np.array([[50, 200]], dtype=np.uint8)
    >>> brightness_saturate(img, 100)
    array([[150, 255]], dtype=uint8)
    """
    if level >= 0:
        # Where addition would overflow 255, cap at 255
        result = np.where(image > 255 - level, 255, image + level)
    else:
        # Where subtraction would underflow 0, cap at 0
        result = np.where(image < -level, 0, image + level)
    return result.astype(np.uint8)


def benchmark(size: int = 1024, iterations: int = 100) -> None:
    """Benchmark all variants."""
    image = np.random.randint(0, 256, (size, size), dtype=np.uint8)
    level = 50

    variants = [
        ("NumPy clip", brightness_numpy_clip),
        ("LUT", brightness_lut),
        ("Saturate", brightness_saturate),
    ]

    print(f"Benchmark: {size}x{size} image, {iterations} iterations, level={level}\n")
    print(f"{'Variant':<20} {'Total (ms)':>12} {'Per-call (ms)':>14}")
    print("-" * 48)

    for name, func in variants:
        # Warmup
        func(image, level)

        start = time.perf_counter()
        for _ in range(iterations):
            func(image, level)
        elapsed = (time.perf_counter() - start) * 1000

        print(f"{name:<20} {elapsed:>12.2f} {elapsed / iterations:>14.4f}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
