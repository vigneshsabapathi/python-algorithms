"""
Gabor Filter - Optimized Variants

Three approaches:
1. Spatial convolution (baseline) - standard convolve with Gabor kernel
2. FFT-based filtering - frequency domain multiplication
3. Multi-orientation bank - precompute bank, apply all orientations at once
"""

import time
import numpy as np
from scipy.ndimage import convolve


def _gabor_kernel(size, sigma, theta, lambd, gamma, psi=0.0):
    half = size // 2
    y, x = np.mgrid[-half:half + 1, -half:half + 1]
    x_t = x * np.cos(theta) + y * np.sin(theta)
    y_t = -x * np.sin(theta) + y * np.cos(theta)
    g = np.exp(-0.5 * (x_t**2 + gamma**2 * y_t**2) / sigma**2)
    return g * np.cos(2 * np.pi * x_t / lambd + psi)


def gabor_spatial(image, sigma=5.0, theta=0.0, lambd=10.0, gamma=0.5):
    """
    Standard spatial Gabor filter.

    >>> img = np.ones((5, 5))
    >>> gabor_spatial(img, 2, 0, 4, 1).shape
    (5, 5)
    """
    ks = int(6 * sigma) | 1
    kernel = _gabor_kernel(ks, sigma, theta, lambd, gamma)
    return convolve(image.astype(np.float64), kernel)


def gabor_fft(image, sigma=5.0, theta=0.0, lambd=10.0, gamma=0.5):
    """
    FFT-based Gabor filter.

    >>> img = np.ones((5, 5))
    >>> gabor_fft(img, 2, 0, 4, 1).shape
    (5, 5)
    """
    ks = int(6 * sigma) | 1
    kernel = _gabor_kernel(ks, sigma, theta, lambd, gamma)
    h, w = image.shape
    fft_shape = (h + ks - 1, w + ks - 1)
    img_fft = np.fft.fft2(image.astype(np.float64), s=fft_shape)
    kern_fft = np.fft.fft2(kernel, s=fft_shape)
    result = np.real(np.fft.ifft2(img_fft * kern_fft))
    pad = ks // 2
    return result[pad:pad + h, pad:pad + w]


def gabor_bank(image, sigma=5.0, lambd=10.0, gamma=0.5, n_orientations=8):
    """
    Multi-orientation filter bank: compute maximum response across orientations.

    >>> img = np.ones((5, 5))
    >>> gabor_bank(img, 2, 4, 1, 4).shape
    (5, 5)
    """
    ks = int(6 * sigma) | 1
    responses = np.zeros_like(image, dtype=np.float64)
    for i in range(n_orientations):
        theta = i * np.pi / n_orientations
        kernel = _gabor_kernel(ks, sigma, theta, lambd, gamma)
        resp = convolve(image.astype(np.float64), kernel)
        responses = np.maximum(responses, np.abs(resp))
    return responses


def benchmark(size: int = 128, iterations: int = 10) -> None:
    image = np.random.rand(size, size)
    variants = [
        ("Spatial", lambda: gabor_spatial(image, 3, 0, 6, 1)),
        ("FFT", lambda: gabor_fft(image, 3, 0, 6, 1)),
        ("Bank (8 orient)", lambda: gabor_bank(image, 3, 6, 1, 8)),
    ]

    print(f"Benchmark: {size}x{size} image, {iterations} iterations\n")
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
