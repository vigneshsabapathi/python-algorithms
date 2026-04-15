"""
Image Rotation - Optimized Variants

Three approaches:
1. Loop bilinear (baseline) - pixel-by-pixel inverse mapping
2. Vectorized inverse mapping - meshgrid for all output coordinates
3. Three-shear rotation - decompose rotation into 3 horizontal/vertical shears
"""

import time
import numpy as np


def rotate_loop(image, angle_deg):
    """
    Loop-based rotation with bilinear interpolation.

    >>> img = np.eye(5)
    >>> np.allclose(rotate_loop(img, 0)[1:-1, 1:-1], img[1:-1, 1:-1])
    True
    """
    h, w = image.shape
    img = image.astype(np.float64)
    rad = np.radians(angle_deg)
    ca, sa = np.cos(rad), np.sin(rad)
    cy, cx = h / 2, w / 2
    out = np.zeros_like(img)
    for i in range(h):
        for j in range(w):
            dy, dx = i - cy, j - cx
            sy = ca * dy + sa * dx + cy
            sx = -sa * dy + ca * dx + cx
            y0, x0 = int(np.floor(sy)), int(np.floor(sx))
            y1, x1 = y0 + 1, x0 + 1
            if 0 <= y0 < h and 0 <= x0 < w and y1 < h and x1 < w:
                fy, fx = sy - y0, sx - x0
                out[i, j] = (img[y0,x0]*(1-fy)*(1-fx) + img[y1,x0]*fy*(1-fx) +
                              img[y0,x1]*(1-fy)*fx + img[y1,x1]*fy*fx)
    return out


def rotate_vectorized(image, angle_deg):
    """
    Vectorized rotation: compute all source coordinates at once.

    >>> img = np.eye(5)
    >>> np.allclose(rotate_vectorized(img, 0)[1:-1, 1:-1], img[1:-1, 1:-1])
    True
    """
    h, w = image.shape
    img = image.astype(np.float64)
    rad = np.radians(angle_deg)
    ca, sa = np.cos(rad), np.sin(rad)
    cy, cx = h / 2, w / 2

    yi, xi = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')
    dy, dx = yi - cy, xi - cx

    sy = ca * dy + sa * dx + cy
    sx = -sa * dy + ca * dx + cx

    y0 = np.floor(sy).astype(int)
    x0 = np.floor(sx).astype(int)
    y1, x1 = y0 + 1, x0 + 1

    valid = (y0 >= 0) & (x0 >= 0) & (y1 < h) & (x1 < w)
    y0c = np.clip(y0, 0, h-1)
    x0c = np.clip(x0, 0, w-1)
    y1c = np.clip(y1, 0, h-1)
    x1c = np.clip(x1, 0, w-1)

    fy = sy - y0
    fx = sx - x0

    out = np.zeros_like(img)
    interp = (img[y0c,x0c]*(1-fy)*(1-fx) + img[y1c,x0c]*fy*(1-fx) +
              img[y0c,x1c]*(1-fy)*fx + img[y1c,x1c]*fy*fx)
    out[valid] = interp[valid]
    return out


def rotate_three_shear(image, angle_deg):
    """
    Three-shear decomposition: R(theta) = Shear_X * Shear_Y * Shear_X.
    Avoids holes in output, each shear is a 1D operation.

    >>> img = np.eye(5)
    >>> result = rotate_three_shear(img, 0)
    >>> np.allclose(result, img, atol=0.1)
    True
    """
    h, w = image.shape
    img = image.astype(np.float64)
    rad = np.radians(angle_deg)

    alpha = -np.tan(rad / 2)
    beta = np.sin(rad)

    cy, cx = h / 2, w / 2

    # Shear 1: horizontal
    temp1 = np.zeros_like(img)
    for i in range(h):
        shift = alpha * (i - cy)
        for j in range(w):
            src_j = j - shift
            j0 = int(np.floor(src_j))
            frac = src_j - j0
            if 0 <= j0 < w and j0 + 1 < w:
                temp1[i, j] = img[i, j0] * (1 - frac) + img[i, j0 + 1] * frac
            elif 0 <= j0 < w:
                temp1[i, j] = img[i, j0]

    # Shear 2: vertical
    temp2 = np.zeros_like(img)
    for j in range(w):
        shift = beta * (j - cx)
        for i in range(h):
            src_i = i - shift
            i0 = int(np.floor(src_i))
            frac = src_i - i0
            if 0 <= i0 < h and i0 + 1 < h:
                temp2[i, j] = temp1[i0, j] * (1 - frac) + temp1[i0 + 1, j] * frac
            elif 0 <= i0 < h:
                temp2[i, j] = temp1[i0, j]

    # Shear 3: horizontal again
    result = np.zeros_like(img)
    for i in range(h):
        shift = alpha * (i - cy)
        for j in range(w):
            src_j = j - shift
            j0 = int(np.floor(src_j))
            frac = src_j - j0
            if 0 <= j0 < w and j0 + 1 < w:
                result[i, j] = temp2[i, j0] * (1 - frac) + temp2[i, j0 + 1] * frac
            elif 0 <= j0 < w:
                result[i, j] = temp2[i, j0]

    return result


def benchmark(size=64, iterations=5):
    image = np.random.rand(size, size)
    angle = 30
    variants = [
        ("Loop bilinear", lambda: rotate_loop(image, angle)),
        ("Vectorized", lambda: rotate_vectorized(image, angle)),
        ("Three-shear", lambda: rotate_three_shear(image, angle)),
    ]

    print(f"Benchmark: {size}x{size}, angle={angle}deg, {iterations} iters\n")
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
