"""
Harris Corner Detection — detecting corners via autocorrelation matrix.

The Harris corner detector finds points where intensity changes
significantly in both x and y directions. For each pixel, it builds
a structure tensor (second-moment matrix) from image gradients,
then computes a corner response:

    R = det(M) - k * trace(M)^2

where M = [[Sxx, Sxy], [Sxy, Syy]] is the structure tensor
smoothed by a Gaussian window.

High R → corner, R ≈ 0 → flat region, R << 0 → edge.

Reference: TheAlgorithms/Python — computer_vision/harris_corner.py

>>> import numpy as np
>>> img = np.zeros((10, 10), dtype=np.float64)
>>> img[3:7, 3:7] = 255.0
>>> response = harris_corner(img, k=0.04, window_size=3)
>>> response.shape
(10, 10)
>>> bool(np.any(response > 0))
True
"""

from __future__ import annotations

import numpy as np


def _sobel_gradients(image: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute image gradients using Sobel operators (3x3).

    Returns (Ix, Iy) — gradients in x (horizontal) and y (vertical).

    >>> import numpy as np
    >>> img = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.float64)
    >>> ix, iy = _sobel_gradients(img)
    >>> ix.shape == img.shape
    True
    """
    # Sobel kernels
    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float64)
    ky = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float64)

    rows, cols = image.shape
    ix = np.zeros_like(image)
    iy = np.zeros_like(image)

    padded = np.pad(image, 1, mode="reflect")

    for i in range(rows):
        for j in range(cols):
            window = padded[i : i + 3, j : j + 3]
            ix[i, j] = np.sum(window * kx)
            iy[i, j] = np.sum(window * ky)

    return ix, iy


def harris_corner(
    image: np.ndarray,
    k: float = 0.04,
    window_size: int = 3,
    sigma: float = 1.0,
) -> np.ndarray:
    """
    Compute Harris corner response for a grayscale image.

    Args:
        image: 2D grayscale image (float or uint8).
        k: Harris detector free parameter (typically 0.04-0.06).
        window_size: size of the local window for structure tensor.
        sigma: Gaussian smoothing sigma for the structure tensor.

    Returns:
        2D array of corner response values.

    >>> import numpy as np
    >>> img = np.zeros((8, 8), dtype=np.float64)
    >>> img[2:6, 2:6] = 1.0
    >>> R = harris_corner(img, k=0.04)
    >>> R.shape
    (8, 8)
    """
    if image.ndim == 3:
        image = np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])
    img = image.astype(np.float64)

    # Compute gradients
    ix, iy = _sobel_gradients(img)

    # Products of gradients
    ixx = ix * ix
    iyy = iy * iy
    ixy = ix * iy

    # Gaussian window for smoothing the structure tensor
    half = window_size // 2
    ax = np.arange(-half, half + 1)
    xx, yy = np.meshgrid(ax, ax)
    gaussian = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    gaussian /= gaussian.sum()

    rows, cols = img.shape
    sxx = np.zeros_like(img)
    syy = np.zeros_like(img)
    sxy = np.zeros_like(img)

    padded_ixx = np.pad(ixx, half, mode="reflect")
    padded_iyy = np.pad(iyy, half, mode="reflect")
    padded_ixy = np.pad(ixy, half, mode="reflect")

    for i in range(rows):
        for j in range(cols):
            sxx[i, j] = np.sum(padded_ixx[i : i + window_size, j : j + window_size] * gaussian)
            syy[i, j] = np.sum(padded_iyy[i : i + window_size, j : j + window_size] * gaussian)
            sxy[i, j] = np.sum(padded_ixy[i : i + window_size, j : j + window_size] * gaussian)

    # Harris response: R = det(M) - k * trace(M)^2
    det_m = sxx * syy - sxy * sxy
    trace_m = sxx + syy
    response = det_m - k * trace_m * trace_m

    return response


def detect_corners(
    image: np.ndarray,
    k: float = 0.04,
    threshold_ratio: float = 0.01,
    window_size: int = 3,
) -> list[tuple[int, int]]:
    """
    Return list of (row, col) corner coordinates.

    Thresholds the Harris response at threshold_ratio * max(response).

    >>> import numpy as np
    >>> img = np.zeros((10, 10), dtype=np.float64)
    >>> img[3:7, 3:7] = 255.0
    >>> corners = detect_corners(img, threshold_ratio=0.01)
    >>> len(corners) > 0
    True
    """
    response = harris_corner(image, k=k, window_size=window_size)
    threshold = threshold_ratio * response.max()
    corners = list(zip(*np.where(response > threshold)))
    return corners


if __name__ == "__main__":
    import doctest

    doctest.testmod()
