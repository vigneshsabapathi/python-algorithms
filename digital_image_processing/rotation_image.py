"""
Image Rotation

Rotates an image by an arbitrary angle using inverse mapping with
bilinear interpolation. The rotation is performed around the image center.

Reference: https://github.com/TheAlgorithms/Python/blob/master/digital_image_processing/rotation/rotation.py
"""

import numpy as np


def rotate_image(image: np.ndarray, angle_degrees: float) -> np.ndarray:
    """
    Rotate an image by the given angle (counterclockwise) around its center.

    Args:
        image: Grayscale image, shape (H, W).
        angle_degrees: Rotation angle in degrees (positive = counterclockwise).

    Returns:
        Rotated image, same shape, with bilinear interpolation.
        Out-of-bounds pixels are set to 0.

    >>> img = np.array([[1, 0], [0, 0]], dtype=np.float64)
    >>> result = rotate_image(img, 0)
    >>> result[0, 0]
    1.0

    >>> img = np.eye(3, dtype=np.float64)
    >>> result = rotate_image(img, 0)
    >>> np.allclose(result, img)
    True

    >>> img = np.ones((5, 5), dtype=np.float64)
    >>> result = rotate_image(img, 45)
    >>> result.shape
    (5, 5)
    >>> result[2, 2]  # center pixel unchanged
    1.0
    """
    h, w = image.shape
    img = image.astype(np.float64)
    angle_rad = np.radians(angle_degrees)

    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)

    # Center of image
    cy, cx = h / 2, w / 2

    output = np.zeros_like(img)

    for i in range(h):
        for j in range(w):
            # Inverse rotation: map output (i,j) to input coordinates
            dy = i - cy
            dx = j - cx

            src_y = cos_a * dy + sin_a * dx + cy
            src_x = -sin_a * dy + cos_a * dx + cx

            # Bilinear interpolation
            y0 = int(np.floor(src_y))
            x0 = int(np.floor(src_x))
            y1 = y0 + 1
            x1 = x0 + 1

            if 0 <= y0 < h and 0 <= x0 < w and y1 < h and x1 < w:
                fy = src_y - y0
                fx = src_x - x0
                output[i, j] = (
                    img[y0, x0] * (1 - fy) * (1 - fx)
                    + img[y1, x0] * fy * (1 - fx)
                    + img[y0, x1] * (1 - fy) * fx
                    + img[y1, x1] * fy * fx
                )
            elif 0 <= y0 < h and 0 <= x0 < w:
                output[i, j] = img[y0, x0]

    return output


def rotate_90(image: np.ndarray, times: int = 1) -> np.ndarray:
    """
    Rotate image by multiples of 90 degrees (fast, no interpolation).

    >>> img = np.array([[1, 2], [3, 4]])
    >>> rotate_90(img, 1).tolist()
    [[2, 4], [1, 3]]

    >>> rotate_90(img, 2).tolist()
    [[4, 3], [2, 1]]
    """
    return np.rot90(image, k=times)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    # Demo: rotate a small image
    img = np.zeros((8, 8), dtype=np.float64)
    img[1:3, 1:7] = 1.0  # horizontal bar

    rot45 = rotate_image(img, 45)
    rot90 = rotate_image(img, 90)
    print(f"\nOriginal non-zero: {np.sum(img > 0)}")
    print(f"Rotated 45deg non-zero: {np.sum(rot45 > 0.1)}")
    print(f"Rotated 90deg non-zero: {np.sum(rot90 > 0.1)}")
