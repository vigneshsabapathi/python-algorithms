"""
Histogram Stretching (Contrast Stretching)

Linearly maps pixel intensities to span the full [0, 255] range.
Formula: output = (pixel - min) / (max - min) * 255

Different from histogram equalization (which redistributes the CDF).

Reference: https://github.com/TheAlgorithms/Python/blob/master/digital_image_processing/histogram_equalization/histogram_stretch.py
"""

import numpy as np


def histogram_stretch(image: np.ndarray) -> np.ndarray:
    """
    Stretch image histogram to fill the full [0, 255] range.

    Args:
        image: Grayscale image, shape (H, W), any numeric dtype.

    Returns:
        Stretched image, dtype uint8.

    >>> img = np.array([[50, 100], [150, 200]], dtype=np.uint8)
    >>> result = histogram_stretch(img)
    >>> result[0, 0]  # (50-50)/(200-50)*255 = 0
    0
    >>> result[1, 1]  # (200-50)/(200-50)*255 = 255
    255
    >>> result[0, 1]  # (100-50)/(200-50)*255 = 85
    85
    >>> result[1, 0]  # (150-50)/(200-50)*255 = 170
    170

    >>> uniform = np.full((3, 3), 128, dtype=np.uint8)
    >>> histogram_stretch(uniform)
    array([[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0]], dtype=uint8)

    >>> full = np.array([[0, 255]], dtype=np.uint8)
    >>> histogram_stretch(full).tolist()
    [[0, 255]]
    """
    img = image.astype(np.float64)
    min_val = img.min()
    max_val = img.max()

    if max_val == min_val:
        return np.zeros_like(image, dtype=np.uint8)

    stretched = (img - min_val) / (max_val - min_val) * 255
    return stretched.astype(np.uint8)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    # Demo
    img = np.random.randint(80, 180, (8, 8), dtype=np.uint8)
    stretched = histogram_stretch(img)
    print(f"\nOriginal range: [{img.min()}, {img.max()}]")
    print(f"Stretched range: [{stretched.min()}, {stretched.max()}]")
