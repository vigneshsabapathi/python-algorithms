"""
Laplacian Filter

Second-order derivative filter for edge detection. Detects regions of rapid
intensity change. The Laplacian kernel highlights edges in all directions.

Reference: https://github.com/TheAlgorithms/Python/blob/master/digital_image_processing/filters/laplacian_filter.py
"""

import numpy as np


# Standard Laplacian kernels
LAPLACIAN_4 = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float64)
LAPLACIAN_8 = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=np.float64)


def laplacian_filter(image: np.ndarray, kernel: np.ndarray = None) -> np.ndarray:
    """
    Apply Laplacian filter for edge detection.

    Args:
        image: Grayscale image, shape (H, W).
        kernel: Laplacian kernel (default: 4-connected).

    Returns:
        Edge-detected image (may contain negative values).

    >>> img = np.array([[0, 0, 0, 0, 0],
    ...                 [0, 0, 0, 0, 0],
    ...                 [0, 0, 100, 0, 0],
    ...                 [0, 0, 0, 0, 0],
    ...                 [0, 0, 0, 0, 0]], dtype=np.float64)
    >>> result = laplacian_filter(img)
    >>> result[2, 2]
    -400.0
    >>> result[1, 2]
    100.0
    >>> result[2, 1]
    100.0

    >>> flat = np.full((5, 5), 50.0)
    >>> laplacian_filter(flat)[2, 2]  # interior pixels are 0
    0.0
    """
    if kernel is None:
        kernel = LAPLACIAN_4

    img = image.astype(np.float64)
    kh, kw = kernel.shape
    half = kh // 2
    h, w = img.shape

    padded = np.pad(img, half, mode="constant", constant_values=0)
    output = np.zeros_like(img)

    for i in range(h):
        for j in range(w):
            output[i, j] = np.sum(padded[i : i + kh, j : j + kw] * kernel)

    return output


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    # Demo: detect edges of a bright square
    img = np.zeros((12, 12), dtype=np.float64)
    img[3:9, 3:9] = 200.0

    edges_4 = laplacian_filter(img, LAPLACIAN_4)
    edges_8 = laplacian_filter(img, LAPLACIAN_8)
    print(f"\n4-connected: range [{edges_4.min():.0f}, {edges_4.max():.0f}]")
    print(f"8-connected: range [{edges_8.min():.0f}, {edges_8.max():.0f}]")
    print(f"Non-zero edge pixels (4-conn): {np.sum(edges_4 != 0)}")
    print(f"Non-zero edge pixels (8-conn): {np.sum(edges_8 != 0)}")
