"""
Sobel Filter

First-order gradient operator for edge detection. Uses two 3x3 kernels to
compute horizontal (Gx) and vertical (Gy) gradients, then combines them
to produce the gradient magnitude.

Reference: https://github.com/TheAlgorithms/Python/blob/master/digital_image_processing/filters/sobel_filter.py
"""

import numpy as np


SOBEL_X = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float64)
SOBEL_Y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype=np.float64)


def sobel_filter(image: np.ndarray) -> np.ndarray:
    """
    Apply Sobel edge detection to a grayscale image.

    Returns the gradient magnitude sqrt(Gx^2 + Gy^2).

    >>> img = np.array([[0, 0, 0, 0, 0],
    ...                 [0, 0, 0, 0, 0],
    ...                 [0, 0, 0, 0, 0],
    ...                 [255, 255, 255, 255, 255],
    ...                 [255, 255, 255, 255, 255]], dtype=np.float64)
    >>> result = sobel_filter(img)
    >>> result.shape
    (5, 5)
    >>> result[2, 2] > 0  # edge detected at boundary row
    True

    >>> flat = np.full((5, 5), 100.0)
    >>> sobel_filter(flat)[2, 2]  # interior pixel has zero gradient
    0.0
    """
    img = image.astype(np.float64)
    h, w = img.shape
    padded = np.pad(img, 1, mode="constant", constant_values=0)

    gx = np.zeros_like(img)
    gy = np.zeros_like(img)

    for i in range(h):
        for j in range(w):
            region = padded[i : i + 3, j : j + 3]
            gx[i, j] = np.sum(region * SOBEL_X)
            gy[i, j] = np.sum(region * SOBEL_Y)

    return np.hypot(gx, gy)


def sobel_direction(image: np.ndarray) -> tuple:
    """
    Return both magnitude and gradient direction (in radians).

    >>> img = np.zeros((5, 5))
    >>> img[2:, :] = 255
    >>> mag, angle = sobel_direction(img)
    >>> mag.shape == angle.shape
    True
    """
    img = image.astype(np.float64)
    h, w = img.shape
    padded = np.pad(img, 1, mode="constant")
    gx = np.zeros_like(img)
    gy = np.zeros_like(img)
    for i in range(h):
        for j in range(w):
            region = padded[i:i+3, j:j+3]
            gx[i, j] = np.sum(region * SOBEL_X)
            gy[i, j] = np.sum(region * SOBEL_Y)
    return np.hypot(gx, gy), np.arctan2(gy, gx)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    # Demo: detect edges of a rectangle
    img = np.zeros((12, 12), dtype=np.float64)
    img[3:9, 3:9] = 200.0

    edges = sobel_filter(img)
    print(f"\nEdge magnitude range: [{edges.min():.1f}, {edges.max():.1f}]")
    print(f"Non-zero pixels: {np.sum(edges > 0)}")
