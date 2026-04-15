"""
Local Binary Pattern - Optimized Variants

Three approaches:
1. Vectorized shifts (baseline) - numpy array slicing for all 8 neighbors
2. Uniform LBP - only count patterns with <= 2 transitions (58 uniform + 1 non-uniform)
3. Rotation-invariant LBP - minimum circular rotation of the binary pattern
"""

import time
import numpy as np


def lbp_vectorized(image: np.ndarray) -> np.ndarray:
    """
    Vectorized LBP using array slicing.

    >>> img = np.full((5, 5), 100, dtype=np.uint8)
    >>> np.all(lbp_vectorized(img) == 255)
    True
    """
    img = image.astype(np.int16)
    h, w = img.shape
    center = img[1:h-1, 1:w-1]
    lbp = np.zeros((h-2, w-2), dtype=np.uint8)

    offsets = [(-1,-1,7), (-1,0,6), (-1,1,5), (0,1,4),
               (1,1,3), (1,0,2), (1,-1,1), (0,-1,0)]

    for dy, dx, bit in offsets:
        neighbor = img[1+dy:h-1+dy, 1+dx:w-1+dx]
        lbp |= ((neighbor >= center).astype(np.uint8)) << bit
    return lbp


def lbp_uniform(image: np.ndarray) -> np.ndarray:
    """
    Uniform LBP: patterns with at most 2 bit transitions (0->1 or 1->0).
    Non-uniform patterns mapped to a single bin (label = number of 1-bits + 1
    for uniform, 0 for non-uniform).

    >>> img = np.full((5, 5), 100, dtype=np.uint8)
    >>> result = lbp_uniform(img)
    >>> result[1, 1]  # all 1s = 8 ones, uniform -> 9
    9
    """
    raw = lbp_vectorized(image)

    # Count transitions in circular binary pattern
    def transitions(val):
        bits = [(val >> i) & 1 for i in range(8)]
        return sum(bits[i] != bits[(i+1) % 8] for i in range(8))

    # Build LUT
    lut = np.zeros(256, dtype=np.uint8)
    for v in range(256):
        if transitions(v) <= 2:
            lut[v] = bin(v).count('1') + 1  # 1..9 for uniform
        else:
            lut[v] = 0  # non-uniform

    return lut[raw]


def lbp_rotation_invariant(image: np.ndarray) -> np.ndarray:
    """
    Rotation-invariant LBP: use minimum value among all 8 circular rotations.

    >>> img = np.full((5, 5), 100, dtype=np.uint8)
    >>> result = lbp_rotation_invariant(img)
    >>> result[1, 1]
    255
    """
    raw = lbp_vectorized(image)

    # Build LUT: for each pattern, find minimum rotation
    lut = np.zeros(256, dtype=np.uint8)
    for v in range(256):
        min_rot = v
        rotated = v
        for _ in range(7):
            rotated = ((rotated << 1) | (rotated >> 7)) & 0xFF
            min_rot = min(min_rot, rotated)
        lut[v] = min_rot

    return lut[raw]


def benchmark(size=256, iterations=50):
    image = np.random.randint(0, 256, (size, size), dtype=np.uint8)

    variants = [
        ("Vectorized", lbp_vectorized),
        ("Uniform", lbp_uniform),
        ("Rotation-invariant", lbp_rotation_invariant),
    ]

    print(f"Benchmark: {size}x{size}, {iterations} iterations\n")
    print(f"{'Variant':<24} {'Total (ms)':>12} {'Per-call (ms)':>14}")
    print("-" * 52)

    for name, func in variants:
        func(image)
        start = time.perf_counter()
        for _ in range(iterations):
            func(image)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:<24} {elapsed:>12.2f} {elapsed / iterations:>14.4f}")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
