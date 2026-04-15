"""
Gaussian Filter (Gaussian Blur)

Smooths an image by convolving with a 2D Gaussian kernel.
Removes high-frequency noise while preserving overall structure.

Reference: https://github.com/TheAlgorithms/Python/blob/master/digital_image_processing/filters/gaussian_filter.py
"""

import numpy as np


def gaussian_kernel(size: int = 5, sigma: float = 1.0) -> np.ndarray:
    """
    Generate a normalized 2D Gaussian kernel.

    >>> k = gaussian_kernel(3, 1.0)
    >>> k.shape
    (3, 3)
    >>> abs(k.sum() - 1.0) < 1e-10
    True
    >>> k[1, 1] > k[0, 0]  # center is maximum
    True

    >>> gaussian_kernel(1, 1.0)
    array([[1.]])
    """
    ax = np.arange(size, dtype=np.float64) - size // 2
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    return kernel / kernel.sum()


def gaussian_filter(image: np.ndarray, kernel_size: int = 5, sigma: float = 1.0) -> np.ndarray:
    """
    Apply Gaussian blur to a grayscale image.

    Args:
        image: Grayscale image, shape (H, W).
        kernel_size: Size of Gaussian kernel (odd).
        sigma: Standard deviation of Gaussian.

    Returns:
        Blurred image, same shape.

    >>> img = np.array([[0, 0, 0], [0, 100, 0], [0, 0, 0]], dtype=np.float64)
    >>> result = gaussian_filter(img, 3, 1.0)
    >>> result.shape
    (3, 3)
    >>> result[1, 1] < 100  # center is blurred down
    True
    >>> result[0, 0] > 0  # corners receive some value
    True

    >>> uniform = np.full((5, 5), 50.0)
    >>> np.allclose(gaussian_filter(uniform, 3, 1.0), 50.0)
    True
    """
    kernel = gaussian_kernel(kernel_size, sigma)
    img = image.astype(np.float64)
    h, w = img.shape
    half = kernel_size // 2

    padded = np.pad(img, half, mode="reflect")
    output = np.zeros_like(img)

    for i in range(h):
        for j in range(w):
            region = padded[i : i + kernel_size, j : j + kernel_size]
            output[i, j] = np.sum(region * kernel)

    return output


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    # Demo: blur a noisy image
    np.random.seed(42)
    clean = np.zeros((16, 16), dtype=np.float64)
    clean[4:12, 4:12] = 200.0
    noisy = clean + np.random.normal(0, 20, clean.shape)

    blurred = gaussian_filter(noisy, kernel_size=5, sigma=1.5)
    print(f"\nNoisy std: {noisy.std():.2f}")
    print(f"Blurred std: {blurred.std():.2f}")
    print(f"Center region mean (noisy): {noisy[6:10, 6:10].mean():.1f}")
    print(f"Center region mean (blurred): {blurred[6:10, 6:10].mean():.1f}")
