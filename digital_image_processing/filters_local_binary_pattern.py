"""
Local Binary Pattern (LBP)

Texture descriptor that labels each pixel by thresholding its neighborhood
against the center pixel value, producing a binary pattern encoded as an integer.

Reference: https://github.com/TheAlgorithms/Python/blob/master/digital_image_processing/filters/local_binary_pattern.py
"""

import numpy as np


def local_binary_pattern(image: np.ndarray) -> np.ndarray:
    """
    Compute the Local Binary Pattern of a grayscale image.

    For each pixel, compare the 8 neighbors (clockwise from top-left).
    If neighbor >= center, set bit to 1; else 0.
    The 8-bit pattern is the LBP value (0-255).

    Args:
        image: Grayscale image, shape (H, W), dtype uint8 or float.

    Returns:
        LBP image, shape (H-2, W-2), dtype uint8.

    >>> img = np.array([[6, 5, 2],
    ...                 [7, 6, 1],
    ...                 [9, 8, 7]], dtype=np.uint8)
    >>> lbp = local_binary_pattern(img)
    >>> lbp.shape
    (1, 1)
    >>> lbp[0, 0]  # TL(6>=6)=1, T(5>=6)=0, TR(2>=6)=0, R(1>=6)=0, BR(7>=6)=1, B(8>=6)=1, BL(9>=6)=1, L(7>=6)=1
    143

    >>> uniform = np.full((5, 5), 100, dtype=np.uint8)
    >>> result = local_binary_pattern(uniform)
    >>> np.all(result == 255)  # all neighbors equal to center -> all bits 1
    True
    """
    img = image.astype(np.int16)
    h, w = img.shape
    lbp = np.zeros((h - 2, w - 2), dtype=np.uint8)

    # 8 neighbors clockwise from top-left
    # Bit positions: TL=7, T=6, TR=5, R=4, BR=3, B=2, BL=1, L=0
    offsets = [
        (-1, -1, 7),  # top-left
        (-1, 0, 6),   # top
        (-1, 1, 5),   # top-right
        (0, 1, 4),    # right
        (1, 1, 3),    # bottom-right
        (1, 0, 2),    # bottom
        (1, -1, 1),   # bottom-left
        (0, -1, 0),   # left
    ]

    for dy, dx, bit in offsets:
        neighbor = img[1 + dy : h - 1 + dy, 1 + dx : w - 1 + dx]
        center = img[1 : h - 1, 1 : w - 1]
        lbp |= ((neighbor >= center).astype(np.uint8)) << bit

    return lbp


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    # Demo
    np.random.seed(42)
    img = np.random.randint(0, 256, (8, 8), dtype=np.uint8)
    lbp = local_binary_pattern(img)
    print(f"\nInput shape: {img.shape}")
    print(f"LBP shape: {lbp.shape}")
    print(f"LBP unique values: {len(np.unique(lbp))}")
    print(f"LBP range: [{lbp.min()}, {lbp.max()}]")
    print(f"LBP:\n{lbp}")
