"""
Sepia Filter

Applies a sepia tone to an image using the standard sepia transformation matrix.
The matrix maps RGB channels to warm brownish tones.

Reference: https://github.com/TheAlgorithms/Python/blob/master/digital_image_processing/sepia.py
"""

import numpy as np

# Standard sepia transformation matrix (applied to [R, G, B])
SEPIA_MATRIX = np.array(
    [
        [0.393, 0.769, 0.189],  # new R
        [0.349, 0.686, 0.168],  # new G
        [0.272, 0.534, 0.131],  # new B
    ]
)


def apply_sepia(image: np.ndarray) -> np.ndarray:
    """
    Apply sepia tone to an RGB image.

    Args:
        image: Input RGB image, shape (H, W, 3), dtype uint8.

    Returns:
        Sepia-toned image clipped to [0, 255].

    >>> img = np.array([[[100, 150, 200]]], dtype=np.uint8)
    >>> result = apply_sepia(img)
    >>> result.shape
    (1, 1, 3)
    >>> result.dtype
    dtype('uint8')
    >>> result[0, 0].tolist()
    [192, 171, 133]

    >>> black = np.zeros((1, 1, 3), dtype=np.uint8)
    >>> apply_sepia(black)[0, 0].tolist()
    [0, 0, 0]

    >>> white = np.full((1, 1, 3), 255, dtype=np.uint8)
    >>> apply_sepia(white)[0, 0].tolist()
    [255, 255, 238]
    """
    img_float = image.astype(np.float64)
    # Apply sepia matrix: each output channel is a weighted sum of R, G, B
    sepia = img_float @ SEPIA_MATRIX.T
    return np.clip(sepia, 0, 255).astype(np.uint8)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    # Demo with gradient image
    img = np.zeros((4, 4, 3), dtype=np.uint8)
    img[:, :, 0] = np.arange(16).reshape(4, 4) * 16  # R gradient
    img[:, :, 1] = 128  # constant G
    img[:, :, 2] = 200  # constant B

    sepia_img = apply_sepia(img)
    print(f"\nOriginal pixel [0,0]: {img[0, 0]}")
    print(f"Sepia pixel [0,0]:    {sepia_img[0, 0]}")
    print(f"Original pixel [3,3]: {img[3, 3]}")
    print(f"Sepia pixel [3,3]:    {sepia_img[3, 3]}")
