"""
Burkes Dithering Algorithm

Error-diffusion dithering that distributes quantization error to neighboring
pixels using the Burkes error diffusion kernel:

            *   8/32  4/32
  2/32  4/32  8/32  4/32  2/32

Converts a grayscale image to a binary (black/white) image while preserving
the appearance of gray tones through dot patterns.

Reference: https://github.com/TheAlgorithms/Python/blob/master/digital_image_processing/dithering/burkes.py
"""

import numpy as np


def burkes_dithering(image: np.ndarray, threshold: int = 128) -> np.ndarray:
    """
    Apply Burkes error-diffusion dithering to a grayscale image.

    Args:
        image: Input grayscale image, shape (H, W), dtype uint8.
        threshold: Threshold for binarization (default 128).

    Returns:
        Binary image with values 0 or 255, dtype uint8.

    >>> img = np.array([[100, 150, 200], [120, 180, 80], [90, 160, 140]], dtype=np.uint8)
    >>> result = burkes_dithering(img)
    >>> result.dtype
    dtype('uint8')
    >>> set(np.unique(result)).issubset({0, 255})
    True
    >>> result.shape
    (3, 3)

    >>> uniform = np.full((3, 3), 128, dtype=np.uint8)
    >>> result = burkes_dithering(uniform)
    >>> set(np.unique(result)).issubset({0, 255})
    True
    """
    img = image.astype(np.float64)
    h, w = img.shape

    for y in range(h):
        for x in range(w):
            old_pixel = img[y, x]
            new_pixel = 255.0 if old_pixel >= threshold else 0.0
            img[y, x] = new_pixel
            error = old_pixel - new_pixel

            # Burkes diffusion pattern
            # Right side of current row
            if x + 1 < w:
                img[y, x + 1] += error * 8 / 32
            if x + 2 < w:
                img[y, x + 2] += error * 4 / 32

            # Next row
            if y + 1 < h:
                for dx, weight in [(-2, 2), (-1, 4), (0, 8), (1, 4), (2, 2)]:
                    nx = x + dx
                    if 0 <= nx < w:
                        img[y + 1, nx] += error * weight / 32

    return np.clip(img, 0, 255).astype(np.uint8)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    # Demo with gradient image
    gradient = np.tile(np.arange(0, 256, dtype=np.uint8), (8, 1))
    # Crop to make it small for demo
    small = gradient[:8, :16]
    result = burkes_dithering(small)
    print(f"\nInput shape: {small.shape}")
    print(f"Output unique values: {np.unique(result)}")
    print(f"Input mean: {small.mean():.1f}")
    print(f"Output mean: {result.mean():.1f}")
    print(f"Output:\n{result}")
