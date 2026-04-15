"""
Convert Image to Negative

Inverts all pixel values: output = 255 - input.
Works for both grayscale and RGB images.

Reference: https://github.com/TheAlgorithms/Python/blob/master/digital_image_processing/convert_to_negative.py
"""

import numpy as np


def convert_to_negative(image: np.ndarray) -> np.ndarray:
    """
    Convert an image to its negative (invert pixel values).

    Args:
        image: Input image as numpy array, dtype uint8.

    Returns:
        Negative image where each pixel = 255 - original.

    >>> img = np.array([[0, 128, 255]], dtype=np.uint8)
    >>> convert_to_negative(img)
    array([[255, 127,   0]], dtype=uint8)

    >>> img = np.array([[50, 100], [150, 200]], dtype=np.uint8)
    >>> convert_to_negative(img)
    array([[205, 155],
           [105,  55]], dtype=uint8)

    >>> rgb = np.array([[[10, 20, 30]]], dtype=np.uint8)
    >>> convert_to_negative(rgb)
    array([[[245, 235, 225]]], dtype=uint8)

    >>> convert_to_negative(convert_to_negative(img)).tolist() == img.tolist()
    True
    """
    return np.uint8(255) - image


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    img = np.arange(0, 256, dtype=np.uint8).reshape(16, 16)
    neg = convert_to_negative(img)
    print(f"\nOriginal [0]: {img[0, 0]}, Negative [0]: {neg[0, 0]}")
    print(f"Original [255]: {img[15, 15]}, Negative [255]: {neg[15, 15]}")
    print(f"Double negative equals original: {np.array_equal(img, convert_to_negative(neg))}")
