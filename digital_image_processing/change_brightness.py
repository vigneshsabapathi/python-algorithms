"""
Change Brightness of an Image

Adjusts image brightness by adding/subtracting a constant value to each pixel.
Pixel values are clipped to the valid range [0, 255].

Reference: https://github.com/TheAlgorithms/Python/blob/master/digital_image_processing/change_brightness.py
"""

import numpy as np


def change_brightness(image: np.ndarray, level: int) -> np.ndarray:
    """
    Change the brightness of an image by adding a constant value.

    Args:
        image: Input image as a numpy array (grayscale or RGB), dtype uint8.
        level: Brightness adjustment value. Positive brightens, negative darkens.

    Returns:
        Brightness-adjusted image clipped to [0, 255].

    >>> img = np.array([[50, 100], [150, 200]], dtype=np.uint8)
    >>> change_brightness(img, 50)
    array([[100, 150],
           [200, 250]], dtype=uint8)

    >>> change_brightness(img, -60)
    array([[  0,  40],
           [ 90, 140]], dtype=uint8)

    >>> change_brightness(img, 200)
    array([[250, 255],
           [255, 255]], dtype=uint8)

    >>> rgb = np.array([[[100, 150, 200]]], dtype=np.uint8)
    >>> change_brightness(rgb, 30)
    array([[[130, 180, 230]]], dtype=uint8)
    """
    return np.clip(image.astype(np.int16) + level, 0, 255).astype(np.uint8)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    # Live demo with a gradient image
    img = np.arange(0, 256, dtype=np.uint8).reshape(16, 16)
    print(f"\nOriginal image shape: {img.shape}")
    print(f"Original range: [{img.min()}, {img.max()}]")

    bright = change_brightness(img, 100)
    print(f"After +100 brightness: [{bright.min()}, {bright.max()}]")

    dark = change_brightness(img, -100)
    print(f"After -100 brightness: [{dark.min()}, {dark.max()}]")
