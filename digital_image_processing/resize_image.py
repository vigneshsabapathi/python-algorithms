"""
Image Resize

Implements image resizing using bilinear interpolation.
Maps each output pixel to its corresponding position in the input image
and interpolates the value from the 4 nearest neighbors.

Reference: https://github.com/TheAlgorithms/Python/blob/master/digital_image_processing/resize/resize.py
"""

import numpy as np


def resize_nearest(image: np.ndarray, new_h: int, new_w: int) -> np.ndarray:
    """
    Resize using nearest-neighbor interpolation.

    >>> img = np.array([[1, 2], [3, 4]], dtype=np.float64)
    >>> resize_nearest(img, 4, 4)
    array([[1., 1., 2., 2.],
           [1., 1., 2., 2.],
           [3., 3., 4., 4.],
           [3., 3., 4., 4.]])

    >>> resize_nearest(img, 1, 1)
    array([[1.]])
    """
    h, w = image.shape[:2]
    row_ratio = h / new_h
    col_ratio = w / new_w

    row_idx = (np.arange(new_h) * row_ratio).astype(int)
    col_idx = (np.arange(new_w) * col_ratio).astype(int)

    row_idx = np.clip(row_idx, 0, h - 1)
    col_idx = np.clip(col_idx, 0, w - 1)

    return image[np.ix_(row_idx, col_idx)]


def resize_bilinear(image: np.ndarray, new_h: int, new_w: int) -> np.ndarray:
    """
    Resize using bilinear interpolation.

    Args:
        image: Input image, shape (H, W) or (H, W, C).
        new_h: Target height.
        new_w: Target width.

    Returns:
        Resized image.

    >>> img = np.array([[0, 10], [20, 30]], dtype=np.float64)
    >>> result = resize_bilinear(img, 3, 3)
    >>> result.shape
    (3, 3)
    >>> result[0, 0]  # top-left corner
    0.0
    >>> result[2, 2]  # bottom-right corner
    30.0

    >>> img = np.array([[100]], dtype=np.float64)
    >>> resize_bilinear(img, 3, 3)
    array([[100., 100., 100.],
           [100., 100., 100.],
           [100., 100., 100.]])
    """
    h, w = image.shape[:2]
    img = image.astype(np.float64)

    # Map output coordinates to input coordinates
    row_scale = (h - 1) / max(new_h - 1, 1)
    col_scale = (w - 1) / max(new_w - 1, 1)

    output = np.zeros((new_h, new_w) + image.shape[2:], dtype=np.float64)

    for i in range(new_h):
        for j in range(new_w):
            src_y = i * row_scale
            src_x = j * col_scale

            y0 = int(np.floor(src_y))
            x0 = int(np.floor(src_x))
            y1 = min(y0 + 1, h - 1)
            x1 = min(x0 + 1, w - 1)

            dy = src_y - y0
            dx = src_x - x0

            # Bilinear interpolation
            output[i, j] = (
                img[y0, x0] * (1 - dy) * (1 - dx)
                + img[y1, x0] * dy * (1 - dx)
                + img[y0, x1] * (1 - dy) * dx
                + img[y1, x1] * dy * dx
            )

    return output


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    # Demo: upscale and downscale
    img = np.arange(16, dtype=np.float64).reshape(4, 4)
    upscaled = resize_bilinear(img, 8, 8)
    downscaled = resize_bilinear(img, 2, 2)
    print(f"\nOriginal (4x4):\n{img}")
    print(f"Upscaled (8x8) corner: {upscaled[0, 0]}")
    print(f"Downscaled (2x2):\n{downscaled}")
    print(f"Nearest (4x4 -> 2x2):\n{resize_nearest(img, 2, 2)}")
