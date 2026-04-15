"""
Gaussian Filter - Optimized Variants

Three approaches:
1. 2D convolution (baseline) - direct kernel convolution
2. Separable filter - decompose into 1D horizontal + vertical passes (2*N vs N^2)
3. FFT convolution - frequency domain for very large kernels
"""

import time
import numpy as np


def _gaussian_kernel_2d(size, sigma):
    ax = np.arange(size, dtype=np.float64) - size // 2
    xx, yy = np.meshgrid(ax, ax)
    k = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    return k / k.sum()


def _gaussian_kernel_1d(size, sigma):
    ax = np.arange(size, dtype=np.float64) - size // 2
    k = np.exp(-ax**2 / (2 * sigma**2))
    return k / k.sum()


def gaussian_2d(image, kernel_size=5, sigma=1.0):
    """
    Standard 2D Gaussian convolution.

    >>> img = np.full((5, 5), 100.0)
    >>> np.allclose(gaussian_2d(img, 3, 1.0), 100.0)
    True
    """
    kernel = _gaussian_kernel_2d(kernel_size, sigma)
    h, w = image.shape
    half = kernel_size // 2
    padded = np.pad(image.astype(np.float64), half, mode="reflect")
    output = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            output[i, j] = np.sum(padded[i:i + kernel_size, j:j + kernel_size] * kernel)
    return output


def gaussian_separable(image, kernel_size=5, sigma=1.0):
    """
    Separable Gaussian: horizontal then vertical 1D pass.
    O(N*K) per pixel instead of O(K^2).

    >>> img = np.full((5, 5), 100.0)
    >>> np.allclose(gaussian_separable(img, 3, 1.0), 100.0)
    True
    """
    k1d = _gaussian_kernel_1d(kernel_size, sigma)
    half = kernel_size // 2
    img = image.astype(np.float64)
    h, w = img.shape

    # Horizontal pass
    padded_h = np.pad(img, ((0, 0), (half, half)), mode="reflect")
    temp = np.zeros_like(img)
    for i in range(h):
        for j in range(w):
            temp[i, j] = np.dot(padded_h[i, j:j + kernel_size], k1d)

    # Vertical pass
    padded_v = np.pad(temp, ((half, half), (0, 0)), mode="reflect")
    output = np.zeros_like(img)
    for i in range(h):
        for j in range(w):
            output[i, j] = np.dot(padded_v[i:i + kernel_size, j], k1d)

    return output


def gaussian_fft(image, kernel_size=5, sigma=1.0):
    """
    FFT-based Gaussian filter.

    >>> img = np.full((5, 5), 100.0)
    >>> result = gaussian_fft(img, 3, 1.0)
    >>> abs(result[2, 2] - 100.0) < 1.0
    True
    """
    kernel = _gaussian_kernel_2d(kernel_size, sigma)
    h, w = image.shape
    fft_h, fft_w = h + kernel_size - 1, w + kernel_size - 1
    img_fft = np.fft.fft2(image.astype(np.float64), s=(fft_h, fft_w))
    kern_fft = np.fft.fft2(kernel, s=(fft_h, fft_w))
    result = np.real(np.fft.ifft2(img_fft * kern_fft))
    pad = kernel_size // 2
    return result[pad:pad + h, pad:pad + w]


def benchmark(size=128, kernel_size=5, iterations=5):
    image = np.random.rand(size, size) * 255
    variants = [
        ("2D convolution", lambda: gaussian_2d(image, kernel_size, 1.5)),
        ("Separable 1D", lambda: gaussian_separable(image, kernel_size, 1.5)),
        ("FFT", lambda: gaussian_fft(image, kernel_size, 1.5)),
    ]

    print(f"Benchmark: {size}x{size}, kernel={kernel_size}, {iterations} iters\n")
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
