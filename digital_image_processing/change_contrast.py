"""
Change Contrast of an Image

Adjusts image contrast using a linear scaling factor around the mean intensity.
Formula: output = clip(factor * (pixel - 128) + 128, 0, 255)

A factor > 1 increases contrast, factor < 1 decreases contrast.

Reference: https://github.com/TheAlgorithms/Python/blob/master/digital_image_processing/change_contrast.py
"""

import numpy as np


def change_contrast(image: np.ndarray, factor: float) -> np.ndarray:
    """
    Adjust the contrast of an image.

    Args:
        image: Input image as numpy array, dtype uint8.
        factor: Contrast multiplier. >1 increases, <1 decreases, 1 = no change.

    Returns:
        Contrast-adjusted image clipped to [0, 255].

    >>> img = np.array([[50, 100], [150, 200]], dtype=np.uint8)
    >>> change_contrast(img, 1.0)
    array([[ 50, 100],
           [150, 200]], dtype=uint8)

    >>> change_contrast(img, 2.0)
    array([[  0,  72],
           [172, 255]], dtype=uint8)

    >>> change_contrast(img, 0.5)
    array([[ 89, 114],
           [139, 164]], dtype=uint8)

    >>> change_contrast(img, 0.0)
    array([[128, 128],
           [128, 128]], dtype=uint8)
    """
    result = factor * (image.astype(np.float64) - 128) + 128
    return np.clip(result, 0, 255).astype(np.uint8)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    img = np.arange(0, 256, dtype=np.uint8).reshape(16, 16)
    print(f"\nOriginal range: [{img.min()}, {img.max()}]")

    high = change_contrast(img, 2.0)
    print(f"Contrast x2.0: [{high.min()}, {high.max()}]")

    low = change_contrast(img, 0.5)
    print(f"Contrast x0.5: [{low.min()}, {low.max()}]")
