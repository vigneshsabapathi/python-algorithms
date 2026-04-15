"""
Median Filter

Non-linear noise reduction filter that replaces each pixel with the median
of its neighborhood. Excellent for removing salt-and-pepper noise while
preserving edges better than linear filters.

Reference: https://github.com/TheAlgorithms/Python/blob/master/digital_image_processing/filters/median_filter.py
"""

import numpy as np


def median_filter(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """
    Apply median filter to a grayscale image.

    Args:
        image: Grayscale image, shape (H, W).
        kernel_size: Size of the square neighborhood (odd number).

    Returns:
        Filtered image, same shape.

    >>> img = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=np.float64)
    >>> median_filter(img, 3)
    array([[2., 3., 3.],
           [4., 5., 6.],
           [7., 7., 8.]])

    >>> img = np.array([[0, 0, 255, 0, 0]], dtype=np.float64)
    >>> median_filter(img, 3)
    array([[0., 0., 0., 0., 0.]])

    >>> uniform = np.full((5, 5), 42.0)
    >>> np.allclose(median_filter(uniform, 3), 42.0)
    True
    """
    img = image.astype(np.float64)
    h, w = img.shape
    half = kernel_size // 2

    padded = np.pad(img, half, mode="edge")
    output = np.zeros_like(img)

    for i in range(h):
        for j in range(w):
            region = padded[i : i + kernel_size, j : j + kernel_size]
            output[i, j] = np.median(region)

    return output


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    # Demo: remove salt-and-pepper noise
    np.random.seed(42)
    clean = np.full((10, 10), 128.0)
    noisy = clean.copy()
    # Add salt & pepper
    salt = np.random.random(clean.shape) > 0.9
    pepper = np.random.random(clean.shape) > 0.9
    noisy[salt] = 255
    noisy[pepper] = 0

    filtered = median_filter(noisy, 3)
    print(f"\nNoisy unique values: {np.unique(noisy).astype(int)}")
    print(f"Filtered unique values: {np.unique(filtered).astype(int)}")
    print(f"Noisy MSE from clean: {np.mean((noisy - clean)**2):.1f}")
    print(f"Filtered MSE from clean: {np.mean((filtered - clean)**2):.1f}")
