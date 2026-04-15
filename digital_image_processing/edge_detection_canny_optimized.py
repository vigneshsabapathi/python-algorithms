"""
Canny Edge Detection - Optimized Variants

Three approaches:
1. Standard (baseline) - full 5-stage pipeline with loops
2. Vectorized NMS - replace inner loops with numpy operations
3. Reduced pipeline - combine stages for fewer memory allocations
"""

import time
import numpy as np
from scipy.ndimage import convolve


def _gaussian_kernel(size: int = 5, sigma: float = 1.4) -> np.ndarray:
    ax = np.arange(size) - size // 2
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    return kernel / kernel.sum()


def _sobel_gradients(image: np.ndarray) -> tuple:
    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float64)
    ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype=np.float64)
    gx = convolve(image, kx)
    gy = convolve(image, ky)
    return np.hypot(gx, gy), np.arctan2(gy, gx)


def canny_standard(image: np.ndarray, sigma: float = 1.4) -> np.ndarray:
    """
    Standard Canny with loop-based NMS and hysteresis.

    >>> img = np.zeros((10, 10), dtype=np.uint8)
    >>> img[3:7, 3:7] = 255
    >>> canny_standard(img).shape
    (10, 10)
    """
    blurred = convolve(image.astype(np.float64), _gaussian_kernel(5, sigma))
    mag, direction = _sobel_gradients(blurred)
    h, w = mag.shape
    nms = np.zeros_like(mag)
    angle = direction * 180.0 / np.pi
    angle[angle < 0] += 180

    for i in range(1, h - 1):
        for j in range(1, w - 1):
            q, r = 255.0, 255.0
            a = angle[i, j]
            if (0 <= a < 22.5) or (157.5 <= a <= 180):
                q, r = mag[i, j + 1], mag[i, j - 1]
            elif 22.5 <= a < 67.5:
                q, r = mag[i + 1, j - 1], mag[i - 1, j + 1]
            elif 67.5 <= a < 112.5:
                q, r = mag[i + 1, j], mag[i - 1, j]
            elif 112.5 <= a < 157.5:
                q, r = mag[i - 1, j - 1], mag[i + 1, j + 1]
            if mag[i, j] >= q and mag[i, j] >= r:
                nms[i, j] = mag[i, j]

    high_t = nms.max() * 0.15
    low_t = high_t * 0.05
    result = np.zeros_like(nms, dtype=np.uint8)
    result[nms >= high_t] = 255
    result[(nms >= low_t) & (nms < high_t)] = 50

    for i in range(1, h - 1):
        for j in range(1, w - 1):
            if result[i, j] == 50:
                if 255 in result[i - 1:i + 2, j - 1:j + 2]:
                    result[i, j] = 255
                else:
                    result[i, j] = 0
    return result


def canny_vectorized_nms(image: np.ndarray, sigma: float = 1.4) -> np.ndarray:
    """
    Canny with vectorized non-maximum suppression using shifted arrays.

    >>> img = np.zeros((10, 10), dtype=np.uint8)
    >>> img[3:7, 3:7] = 255
    >>> canny_vectorized_nms(img).shape
    (10, 10)
    """
    blurred = convolve(image.astype(np.float64), _gaussian_kernel(5, sigma))
    mag, direction = _sobel_gradients(blurred)
    h, w = mag.shape
    angle = direction * 180.0 / np.pi
    angle[angle < 0] += 180

    # Vectorized NMS using np.roll for neighbor comparison
    nms = np.zeros_like(mag)

    # 4 direction bins
    d0 = ((angle >= 0) & (angle < 22.5)) | ((angle >= 157.5) & (angle <= 180))
    d45 = (angle >= 22.5) & (angle < 67.5)
    d90 = (angle >= 67.5) & (angle < 112.5)
    d135 = (angle >= 112.5) & (angle < 157.5)

    # Padded magnitude for safe indexing
    m = np.pad(mag, 1, mode='constant')

    # Compare with neighbors for each direction (offset by padding)
    for mask, (dy1, dx1, dy2, dx2) in [
        (d0, (0, 1, 0, -1)),     # horizontal: left/right
        (d45, (1, -1, -1, 1)),   # 45 deg
        (d90, (1, 0, -1, 0)),    # vertical: up/down
        (d135, (-1, -1, 1, 1)),  # 135 deg
    ]:
        q = m[1 + dy1:h + 1 + dy1, 1 + dx1:w + 1 + dx1]
        r = m[1 + dy2:h + 1 + dy2, 1 + dx2:w + 1 + dx2]
        local_max = (mag >= q) & (mag >= r) & mask
        nms[local_max] = mag[local_max]

    high_t = nms.max() * 0.15
    low_t = high_t * 0.05
    result = np.zeros_like(nms, dtype=np.uint8)
    result[nms >= high_t] = 255
    result[(nms >= low_t) & (nms < high_t)] = 50

    # Vectorized hysteresis (single pass)
    from scipy.ndimage import maximum_filter
    strong_neighbors = maximum_filter(result, size=3) == 255
    result[(result == 50) & strong_neighbors] = 255
    result[result == 50] = 0

    return result


def canny_combined(image: np.ndarray, sigma: float = 1.4) -> np.ndarray:
    """
    Combined pipeline with minimal intermediate arrays.

    >>> img = np.zeros((10, 10), dtype=np.uint8)
    >>> img[3:7, 3:7] = 255
    >>> canny_combined(img).shape
    (10, 10)
    """
    # Blur + gradient in one go
    blurred = convolve(image.astype(np.float64), _gaussian_kernel(5, sigma))
    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float64)
    ky = kx.T
    gx = convolve(blurred, kx)
    gy = convolve(blurred, ky)
    mag = np.hypot(gx, gy)
    angle = np.arctan2(gy, gx) * 180.0 / np.pi
    angle[angle < 0] += 180

    h, w = mag.shape
    m = np.pad(mag, 1, mode='constant')
    nms = np.zeros_like(mag)

    d0 = ((angle >= 0) & (angle < 22.5)) | ((angle >= 157.5) & (angle <= 180))
    d45 = (angle >= 22.5) & (angle < 67.5)
    d90 = (angle >= 67.5) & (angle < 112.5)
    d135 = (angle >= 112.5) & (angle < 157.5)

    for mask, (dy1, dx1, dy2, dx2) in [
        (d0, (0, 1, 0, -1)), (d45, (1, -1, -1, 1)),
        (d90, (1, 0, -1, 0)), (d135, (-1, -1, 1, 1)),
    ]:
        q = m[1+dy1:h+1+dy1, 1+dx1:w+1+dx1]
        r = m[1+dy2:h+1+dy2, 1+dx2:w+1+dx2]
        local_max = (mag >= q) & (mag >= r) & mask
        nms[local_max] = mag[local_max]

    high_t = nms.max() * 0.15
    low_t = high_t * 0.05
    result = np.uint8(nms >= high_t) * 255

    from scipy.ndimage import maximum_filter
    weak = (nms >= low_t) & (nms < high_t)
    strong_near = maximum_filter(result, size=3) == 255
    result[weak & strong_near] = 255

    return result


def benchmark(size: int = 64, iterations: int = 5) -> None:
    """Benchmark all variants."""
    image = np.random.randint(0, 256, (size, size), dtype=np.uint8)
    image[size//4:3*size//4, size//4:3*size//4] = 200

    variants = [
        ("Standard (loops)", canny_standard),
        ("Vectorized NMS", canny_vectorized_nms),
        ("Combined pipeline", canny_combined),
    ]

    print(f"Benchmark: {size}x{size} image, {iterations} iterations\n")
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
