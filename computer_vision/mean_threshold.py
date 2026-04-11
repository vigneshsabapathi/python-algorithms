"""
Mean Threshold — adaptive binarization using local mean intensity.

For each pixel, the threshold is the mean of its local neighborhood.
If the pixel intensity exceeds the local mean, it becomes white (255);
otherwise black (0). This handles uneven illumination better than a
single global threshold.

Reference: TheAlgorithms/Python — computer_vision/mean_threshold.py

>>> import numpy as np
>>> img = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]], dtype=np.uint8)
>>> result = mean_threshold(img, kernel_size=3)
>>> result.shape
(3, 3)
>>> result.dtype
dtype('uint8')
>>> int(result[1, 1])
0
"""

from __future__ import annotations

import numpy as np


def mean_threshold(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """
    Apply adaptive mean thresholding to a grayscale image.

    For every pixel (i, j), the local mean of the surrounding
    kernel_size x kernel_size window is computed. If the pixel value
    is above the local mean, it is set to 255; otherwise 0.

    Uses an integral image (summed-area table) for O(1) per-pixel
    local mean computation.

    Args:
        image: 2D numpy array (grayscale, uint8 or float).
        kernel_size: odd integer for the local window size.

    Returns:
        Binary image (uint8) with values 0 or 255.

    >>> import numpy as np
    >>> img = np.zeros((5, 5), dtype=np.uint8)
    >>> img[2, 2] = 200
    >>> out = mean_threshold(img, kernel_size=3)
    >>> int(out[2, 2])
    255
    >>> int(out[0, 0])
    0
    """
    if kernel_size % 2 == 0:
        raise ValueError("kernel_size must be odd")

    rows, cols = image.shape[:2]
    if image.ndim == 3:
        # Convert to grayscale via luminance
        image = np.dot(image[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.float64)
    else:
        image = image.astype(np.float64)

    # Integral image for fast local-sum computation
    integral = np.cumsum(np.cumsum(image, axis=0), axis=1)

    # Pad integral image with zeros on top and left
    padded = np.zeros((rows + 1, cols + 1), dtype=np.float64)
    padded[1:, 1:] = integral

    half = kernel_size // 2
    output = np.zeros_like(image, dtype=np.uint8)

    for i in range(rows):
        for j in range(cols):
            # Window boundaries (clamped to image edges)
            r1 = max(0, i - half)
            r2 = min(rows - 1, i + half)
            c1 = max(0, j - half)
            c2 = min(cols - 1, j + half)

            # Sum from integral image: S = I[r2,c2] - I[r1-1,c2] - I[r2,c1-1] + I[r1-1,c1-1]
            area = (r2 - r1 + 1) * (c2 - c1 + 1)
            local_sum = (
                padded[r2 + 1, c2 + 1]
                - padded[r1, c2 + 1]
                - padded[r2 + 1, c1]
                + padded[r1, c1]
            )
            local_mean = local_sum / area

            if image[i, j] > local_mean:
                output[i, j] = 255

    return output


if __name__ == "__main__":
    import doctest

    doctest.testmod()
