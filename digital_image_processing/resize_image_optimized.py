"""
Image Resize - Optimized Variants

Three approaches:
1. Loop bilinear (baseline) - pixel-by-pixel interpolation
2. Vectorized bilinear - precompute all coordinates, use fancy indexing
3. Nearest neighbor (fast, lower quality) - simple index mapping
"""

import time
import numpy as np


def resize_loop(image, new_h, new_w):
    """
    Loop-based bilinear interpolation.

    >>> img = np.array([[0, 10], [20, 30]], dtype=np.float64)
    >>> resize_loop(img, 2, 2)[0, 0]
    0.0
    """
    h, w = image.shape[:2]
    img = image.astype(np.float64)
    rs = (h - 1) / max(new_h - 1, 1)
    cs = (w - 1) / max(new_w - 1, 1)
    out = np.zeros((new_h, new_w) + image.shape[2:])
    for i in range(new_h):
        for j in range(new_w):
            sy, sx = i * rs, j * cs
            y0, x0 = int(sy), int(sx)
            y1, x1 = min(y0+1, h-1), min(x0+1, w-1)
            dy, dx = sy - y0, sx - x0
            out[i, j] = (img[y0,x0]*(1-dy)*(1-dx) + img[y1,x0]*dy*(1-dx) +
                          img[y0,x1]*(1-dy)*dx + img[y1,x1]*dy*dx)
    return out


def resize_vectorized(image, new_h, new_w):
    """
    Fully vectorized bilinear interpolation using meshgrid.

    >>> img = np.array([[0, 10], [20, 30]], dtype=np.float64)
    >>> resize_vectorized(img, 2, 2)[0, 0]
    0.0
    """
    h, w = image.shape[:2]
    img = image.astype(np.float64)
    rs = (h - 1) / max(new_h - 1, 1)
    cs = (w - 1) / max(new_w - 1, 1)

    yi = np.arange(new_h) * rs
    xi = np.arange(new_w) * cs
    yy, xx = np.meshgrid(yi, xi, indexing='ij')

    y0 = np.floor(yy).astype(int)
    x0 = np.floor(xx).astype(int)
    y1 = np.minimum(y0 + 1, h - 1)
    x1 = np.minimum(x0 + 1, w - 1)

    dy = yy - y0
    dx = xx - x0

    return (img[y0, x0] * (1-dy) * (1-dx) +
            img[y1, x0] * dy * (1-dx) +
            img[y0, x1] * (1-dy) * dx +
            img[y1, x1] * dy * dx)


def resize_nearest(image, new_h, new_w):
    """
    Nearest neighbor (fastest, lowest quality).

    >>> img = np.array([[0, 10], [20, 30]], dtype=np.float64)
    >>> resize_nearest(img, 2, 2)[0, 0]
    0.0
    """
    h, w = image.shape[:2]
    ri = np.clip((np.arange(new_h) * h / new_h).astype(int), 0, h-1)
    ci = np.clip((np.arange(new_w) * w / new_w).astype(int), 0, w-1)
    return image[np.ix_(ri, ci)]


def benchmark(src_size=128, dst_size=512, iterations=10):
    image = np.random.rand(src_size, src_size)
    variants = [
        ("Loop bilinear", lambda: resize_loop(image, dst_size, dst_size)),
        ("Vectorized bilinear", lambda: resize_vectorized(image, dst_size, dst_size)),
        ("Nearest neighbor", lambda: resize_nearest(image, dst_size, dst_size)),
    ]

    print(f"Benchmark: {src_size}x{src_size} -> {dst_size}x{dst_size}, {iterations} iters\n")
    print(f"{'Variant':<24} {'Total (ms)':>12} {'Per-call (ms)':>14}")
    print("-" * 52)

    for name, func in variants:
        func()
        start = time.perf_counter()
        for _ in range(iterations):
            func()
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:<24} {elapsed:>12.2f} {elapsed / iterations:>14.4f}")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
