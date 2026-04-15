"""
Sepia Filter - Optimized Variants

Three approaches:
1. Matrix multiply (baseline) - dot product with sepia matrix
2. Channel arithmetic - manual weighted sums (avoids matmul overhead)
3. LUT per-channel - precomputed for each input intensity
"""

import time
import numpy as np

SEPIA_MATRIX = np.array(
    [[0.393, 0.769, 0.189],
     [0.349, 0.686, 0.168],
     [0.272, 0.534, 0.131]]
)


def sepia_matmul(image: np.ndarray) -> np.ndarray:
    """
    Matrix multiplication approach.

    >>> img = np.array([[[100, 150, 200]]], dtype=np.uint8)
    >>> sepia_matmul(img)[0, 0].tolist()
    [192, 171, 133]
    """
    return np.clip(image.astype(np.float64) @ SEPIA_MATRIX.T, 0, 255).astype(np.uint8)


def sepia_channels(image: np.ndarray) -> np.ndarray:
    """
    Manual channel arithmetic - avoids matmul for small images.

    >>> img = np.array([[[100, 150, 200]]], dtype=np.uint8)
    >>> sepia_channels(img)[0, 0].tolist()
    [192, 171, 133]
    """
    r = image[:, :, 0].astype(np.float64)
    g = image[:, :, 1].astype(np.float64)
    b = image[:, :, 2].astype(np.float64)

    out = np.empty_like(image, dtype=np.uint8)
    out[:, :, 0] = np.clip(0.393 * r + 0.769 * g + 0.189 * b, 0, 255)
    out[:, :, 1] = np.clip(0.349 * r + 0.686 * g + 0.168 * b, 0, 255)
    out[:, :, 2] = np.clip(0.272 * r + 0.534 * g + 0.131 * b, 0, 255)
    return out


def sepia_lut(image: np.ndarray) -> np.ndarray:
    """
    LUT approach: precompute contribution of each channel value.

    >>> img = np.array([[[100, 150, 200]]], dtype=np.uint8)
    >>> sepia_lut(img)[0, 0].tolist()
    [192, 171, 133]
    """
    vals = np.arange(256, dtype=np.float64)
    # Contribution LUTs: lut_rc[v] = SEPIA_MATRIX[out_ch, in_ch] * v
    # 3 output channels x 3 input channels = 9 LUTs, but we sum per output
    out = np.empty_like(image, dtype=np.uint8)
    for out_ch in range(3):
        result = np.zeros(image.shape[:2], dtype=np.float64)
        for in_ch in range(3):
            lut = (vals * SEPIA_MATRIX[out_ch, in_ch]).astype(np.float64)
            result += lut[image[:, :, in_ch]]
        out[:, :, out_ch] = np.clip(result, 0, 255)
    return out


def benchmark(size: int = 512, iterations: int = 50) -> None:
    """Benchmark all variants."""
    image = np.random.randint(0, 256, (size, size, 3), dtype=np.uint8)

    variants = [
        ("Matrix multiply", sepia_matmul),
        ("Channel arithmetic", sepia_channels),
        ("LUT per-channel", sepia_lut),
    ]

    print(f"Benchmark: {size}x{size}x3 image, {iterations} iterations\n")
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
