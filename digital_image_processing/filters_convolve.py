"""
2D Convolution

Implements 2D spatial convolution (cross-correlation) of an image with a kernel.
Foundation of most image filtering operations.

Reference: https://github.com/TheAlgorithms/Python/blob/master/digital_image_processing/filters/convolve.py
"""

import numpy as np


def convolve2d(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    Apply 2D convolution to an image with the given kernel.

    Args:
        image: Input grayscale image, shape (H, W).
        kernel: Convolution kernel, shape (kH, kW).

    Returns:
        Convolved image, same shape as input.

    >>> img = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=np.float64)
    >>> identity = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.float64)
    >>> convolve2d(img, identity)
    array([[1., 2., 3.],
           [4., 5., 6.],
           [7., 8., 9.]])

    >>> box = np.ones((3, 3), dtype=np.float64) / 9
    >>> result = convolve2d(img, box)
    >>> round(result[1, 1], 4)
    5.0

    >>> edge = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]], dtype=np.float64)
    >>> convolve2d(np.ones((5, 5)), edge)[2, 2]
    0.0
    """
    img = image.astype(np.float64)
    kern = kernel.astype(np.float64)
    kh, kw = kern.shape
    pad_h, pad_w = kh // 2, kw // 2

    # Zero-pad the image
    padded = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode="constant")
    h, w = img.shape
    output = np.zeros((h, w), dtype=np.float64)

    for i in range(h):
        for j in range(w):
            region = padded[i : i + kh, j : j + kw]
            output[i, j] = np.sum(region * kern)

    return output


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    img = np.arange(1, 26, dtype=np.float64).reshape(5, 5)

    # Sharpen kernel
    sharpen = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float64)
    result = convolve2d(img, sharpen)
    print(f"\nOriginal center: {img[2, 2]}")
    print(f"Sharpened center: {result[2, 2]}")

    # Box blur
    box = np.ones((3, 3), dtype=np.float64) / 9
    blurred = convolve2d(img, box)
    print(f"Box blur center: {blurred[2, 2]:.2f}")
