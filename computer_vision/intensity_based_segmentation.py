"""
Intensity-Based Segmentation — partitioning images by pixel intensity.

Segments a grayscale image into regions based on intensity thresholds.
This includes:
- Simple thresholding (binary)
- Otsu's method (automatic optimal threshold)
- Multi-level thresholding (multiple intensity bands)

These are the simplest segmentation techniques and form the basis
for more advanced methods.

Reference: TheAlgorithms/Python — computer_vision/intensity_based_segmentation.py

>>> import numpy as np
>>> img = np.array([[50, 100, 150], [200, 25, 75], [125, 175, 225]], dtype=np.uint8)
>>> binary_threshold(img, 128)
array([[  0,   0, 255],
       [255,   0,   0],
       [  0, 255, 255]], dtype=uint8)
"""

from __future__ import annotations

import numpy as np


def binary_threshold(image: np.ndarray, threshold: int = 128) -> np.ndarray:
    """
    Simple binary thresholding: pixels > threshold become 255, else 0.

    >>> import numpy as np
    >>> img = np.array([[100, 200], [50, 150]], dtype=np.uint8)
    >>> binary_threshold(img, 128)
    array([[  0, 255],
           [  0, 255]], dtype=uint8)
    """
    result = np.zeros_like(image, dtype=np.uint8)
    result[image > threshold] = 255
    return result


def otsu_threshold(image: np.ndarray) -> tuple[int, np.ndarray]:
    """
    Otsu's method — find the threshold that minimizes intra-class variance.

    Exhaustively tests all thresholds 0..255 and picks the one that
    maximizes the between-class variance:

        sigma_b^2 = w0 * w1 * (mu0 - mu1)^2

    Args:
        image: 2D grayscale image (uint8).

    Returns:
        (optimal_threshold, binary_image)

    >>> import numpy as np
    >>> np.random.seed(42)
    >>> img = np.concatenate([np.full(50, 30), np.full(50, 200)]).reshape(10, 10).astype(np.uint8)
    >>> t, binary = otsu_threshold(img)
    >>> 29 < t < 200
    True
    >>> binary.dtype
    dtype('uint8')
    """
    # Compute histogram
    hist = np.zeros(256, dtype=np.float64)
    for val in image.ravel():
        hist[val] += 1
    hist /= hist.sum()  # normalize to probabilities

    best_threshold = 0
    best_variance = 0.0

    for t in range(256):
        # Class probabilities
        w0 = hist[: t + 1].sum()
        w1 = hist[t + 1 :].sum()

        if w0 == 0 or w1 == 0:
            continue

        # Class means
        mu0 = np.sum(np.arange(t + 1) * hist[: t + 1]) / w0
        mu1 = np.sum(np.arange(t + 1, 256) * hist[t + 1 :]) / w1

        # Between-class variance
        variance = w0 * w1 * (mu0 - mu1) ** 2

        if variance > best_variance:
            best_variance = variance
            best_threshold = t

    binary = binary_threshold(image, best_threshold)
    return best_threshold, binary


def multi_level_threshold(
    image: np.ndarray, thresholds: list[int]
) -> np.ndarray:
    """
    Multi-level thresholding: assign each pixel to an intensity band.

    Pixels are labeled 0, 1, 2, ... based on which threshold range
    they fall into.

    Args:
        image: 2D grayscale image.
        thresholds: sorted list of threshold values.

    Returns:
        Label image where each pixel is assigned a band index.

    >>> import numpy as np
    >>> img = np.array([[30, 100, 200], [150, 50, 250]], dtype=np.uint8)
    >>> multi_level_threshold(img, [85, 170])
    array([[0, 1, 2],
           [1, 0, 2]])
    """
    labels = np.zeros_like(image, dtype=np.int32)
    for i, t in enumerate(sorted(thresholds)):
        labels[image > t] = i + 1
    return labels


if __name__ == "__main__":
    import doctest

    doctest.testmod()
