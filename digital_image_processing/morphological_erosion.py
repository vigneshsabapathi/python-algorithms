"""
Morphological Erosion

Shrinks bright regions (foreground) in a binary or grayscale image.
For binary images: output pixel = 1 only if ALL pixels under the structuring element are 1.
For grayscale: output = min of neighborhood.

Reference: https://github.com/TheAlgorithms/Python/blob/master/digital_image_processing/morphological_operations/erosion_operation.py
"""

import numpy as np


def erosion(image: np.ndarray, kernel: np.ndarray = None) -> np.ndarray:
    """
    Apply morphological erosion to an image.

    Args:
        image: Binary or grayscale image, shape (H, W).
        kernel: Structuring element (default: 3x3 ones).

    Returns:
        Eroded image.

    >>> img = np.array([[1, 1, 1],
    ...                 [1, 1, 1],
    ...                 [1, 1, 1]], dtype=np.uint8)
    >>> erosion(img)[1, 1]
    1

    >>> img = np.array([[0, 0, 0, 0, 0],
    ...                 [0, 1, 1, 1, 0],
    ...                 [0, 1, 1, 1, 0],
    ...                 [0, 1, 1, 1, 0],
    ...                 [0, 0, 0, 0, 0]], dtype=np.uint8)
    >>> result = erosion(img)
    >>> result[2, 2]  # center survives
    1
    >>> result[1, 1]  # border pixel eroded (neighbor at [0,0] = 0)
    0

    >>> erosion(np.zeros((3, 3), dtype=np.uint8)).sum()
    0
    """
    if kernel is None:
        kernel = np.ones((3, 3), dtype=np.uint8)

    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2
    h, w = image.shape

    padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode="constant", constant_values=0)
    output = np.zeros_like(image)

    for i in range(h):
        for j in range(w):
            region = padded[i : i + kh, j : j + kw]
            output[i, j] = np.min(region[kernel == 1])

    return output


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    # Demo: erode a filled square
    img = np.zeros((9, 9), dtype=np.uint8)
    img[2:7, 2:7] = 1

    eroded = erosion(img)
    print(f"\nOriginal foreground pixels: {img.sum()}")
    print(f"Eroded foreground pixels: {eroded.sum()}")
    print(f"Original:\n{img}")
    print(f"Eroded:\n{eroded}")
