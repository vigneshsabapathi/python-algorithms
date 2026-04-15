"""
Morphological Dilation

Expands bright regions (foreground) in a binary or grayscale image.
For binary images: output pixel = 1 if ANY pixel under the structuring element is 1.
For grayscale: output = max of neighborhood.

Reference: https://github.com/TheAlgorithms/Python/blob/master/digital_image_processing/morphological_operations/dilation_operation.py
"""

import numpy as np


def dilation(image: np.ndarray, kernel: np.ndarray = None) -> np.ndarray:
    """
    Apply morphological dilation to an image.

    Args:
        image: Binary or grayscale image, shape (H, W).
        kernel: Structuring element (default: 3x3 ones).

    Returns:
        Dilated image.

    >>> img = np.array([[0, 0, 0, 0, 0],
    ...                 [0, 0, 0, 0, 0],
    ...                 [0, 0, 1, 0, 0],
    ...                 [0, 0, 0, 0, 0],
    ...                 [0, 0, 0, 0, 0]], dtype=np.uint8)
    >>> result = dilation(img)
    >>> result[1, 1]  # diagonal neighbor of center
    1
    >>> result[2, 2]  # center stays 1
    1
    >>> result[0, 0]  # too far from center
    0

    >>> dilation(np.zeros((3, 3), dtype=np.uint8)).sum()
    0

    >>> dilation(np.ones((3, 3), dtype=np.uint8)).sum()
    9
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
            # Dilation: max of region where kernel is 1
            output[i, j] = np.max(region[kernel == 1])

    return output


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    # Demo: dilate a cross pattern
    img = np.zeros((9, 9), dtype=np.uint8)
    img[4, :] = 1  # horizontal line
    img[:, 4] = 1  # vertical line

    dilated = dilation(img)
    print(f"\nOriginal foreground pixels: {img.sum()}")
    print(f"Dilated foreground pixels: {dilated.sum()}")
    print(f"Original:\n{img}")
    print(f"Dilated:\n{dilated}")
