"""
2D Convolution - Optimized Variants

Three approaches:
1. Nested loops (baseline) - explicit pixel-by-pixel
2. Sliding window with numpy - vectorized inner product
3. FFT-based convolution - O(N^2 log N) vs O(N^2 K^2) for large kernels
"""

import time
import numpy as np


def convolve_loops(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    Standard loop-based convolution.

    >>> img = np.ones((3, 3))
    >>> k = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.float64)
    >>> convolve_loops(img, k)[1, 1]
    1.0
    """
    img = image.astype(np.float64)
    kern = kernel.astype(np.float64)
    kh, kw = kern.shape
    ph, pw = kh // 2, kw // 2
    padded = np.pad(img, ((ph, ph), (pw, pw)), mode="constant")
    h, w = img.shape
    output = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            output[i, j] = np.sum(padded[i:i + kh, j:j + kw] * kern)
    return output


def convolve_im2col(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    im2col approach: reshape patches into columns for single matrix multiply.
    Trades memory for speed.

    >>> img = np.ones((3, 3))
    >>> k = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.float64)
    >>> convolve_im2col(img, k)[1, 1]
    1.0
    """
    img = image.astype(np.float64)
    kern = kernel.astype(np.float64)
    kh, kw = kern.shape
    ph, pw = kh // 2, kw // 2
    padded = np.pad(img, ((ph, ph), (pw, pw)), mode="constant")
    h, w = img.shape

    # Extract all patches as columns
    shape = (h, w, kh, kw)
    strides = padded.strides * 2
    patches = np.lib.stride_tricks.as_strided(padded, shape=shape, strides=strides)
    return np.einsum("ijkl,kl->ij", patches, kern)


def convolve_fft(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    FFT-based convolution. Faster for large kernels (k > ~11).

    >>> img = np.ones((3, 3))
    >>> k = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.float64)
    >>> np.allclose(convolve_fft(img, k), 1.0)
    True
    """
    img = image.astype(np.float64)
    kern = kernel.astype(np.float64)
    # Pad kernel to image size
    kh, kw = kern.shape
    ph, pw = kh // 2, kw // 2
    h, w = img.shape
    fft_shape = (h + kh - 1, w + kw - 1)

    img_fft = np.fft.fft2(img, s=fft_shape)
    kern_fft = np.fft.fft2(kern, s=fft_shape)
    result = np.real(np.fft.ifft2(img_fft * kern_fft))

    # Crop to original size (accounting for kernel center)
    return result[ph:ph + h, pw:pw + w]


def benchmark(size: int = 128, kernel_size: int = 5, iterations: int = 10) -> None:
    """Benchmark all variants."""
    image = np.random.rand(size, size)
    kernel = np.random.rand(kernel_size, kernel_size)

    variants = [
        ("Loops", convolve_loops),
        ("im2col + einsum", convolve_im2col),
        ("FFT", convolve_fft),
    ]

    print(f"Benchmark: {size}x{size} image, {kernel_size}x{kernel_size} kernel, {iterations} iters\n")
    print(f"{'Variant':<22} {'Total (ms)':>12} {'Per-call (ms)':>14}")
    print("-" * 50)

    for name, func in variants:
        func(image, kernel)
        start = time.perf_counter()
        for _ in range(iterations):
            func(image, kernel)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:<22} {elapsed:>12.2f} {elapsed / iterations:>14.4f}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
