"""
Mosaic Augmentation — combining multiple images into a single training sample.

Mosaic augmentation (popularized by YOLOv4) stitches 4 images into a
2x2 grid with a random split point. This forces the model to learn
objects at different scales and in different contexts, improving
generalization for object detection.

For pure-numpy implementation, we work with numpy arrays representing
grayscale or single-channel images.

Reference: TheAlgorithms/Python — computer_vision/mosaic_augmentation.py

>>> import numpy as np
>>> imgs = [np.full((4, 4), i * 50, dtype=np.uint8) for i in range(1, 5)]
>>> result = mosaic_augmentation(imgs, output_size=(8, 8))
>>> result.shape
(8, 8)
>>> result.dtype
dtype('uint8')
"""

from __future__ import annotations

import numpy as np


def _resize_nearest(
    image: np.ndarray, target_h: int, target_w: int
) -> np.ndarray:
    """
    Resize image using nearest-neighbor interpolation (pure numpy).

    >>> import numpy as np
    >>> img = np.array([[1, 2], [3, 4]], dtype=np.uint8)
    >>> _resize_nearest(img, 4, 4)
    array([[1, 1, 2, 2],
           [1, 1, 2, 2],
           [3, 3, 4, 4],
           [3, 3, 4, 4]], dtype=uint8)
    """
    src_h, src_w = image.shape[:2]
    row_idx = (np.arange(target_h) * src_h / target_h).astype(int)
    col_idx = (np.arange(target_w) * src_w / target_w).astype(int)
    row_idx = np.clip(row_idx, 0, src_h - 1)
    col_idx = np.clip(col_idx, 0, src_w - 1)

    if image.ndim == 2:
        return image[np.ix_(row_idx, col_idx)]
    else:
        return image[np.ix_(row_idx, col_idx, np.arange(image.shape[2]))]


def mosaic_augmentation(
    images: list[np.ndarray],
    output_size: tuple[int, int] = (64, 64),
    split_ratio: tuple[float, float] | None = None,
    seed: int | None = None,
) -> np.ndarray:
    """
    Create a 2x2 mosaic from 4 images.

    Places 4 images in a grid with a random (or specified) split point.
    Each quadrant is cropped/resized from the corresponding input image.

    Args:
        images: list of exactly 4 grayscale images (2D numpy arrays).
        output_size: (height, width) of the output mosaic.
        split_ratio: (y_ratio, x_ratio) in [0.25, 0.75] for split position.
                     If None, chosen randomly.
        seed: random seed for reproducibility.

    Returns:
        Mosaic image of shape output_size.

    >>> import numpy as np
    >>> imgs = [np.full((10, 10), i * 60, dtype=np.uint8) for i in range(4)]
    >>> result = mosaic_augmentation(imgs, output_size=(8, 8), split_ratio=(0.5, 0.5))
    >>> result.shape
    (8, 8)
    >>> int(result[0, 0])
    0
    >>> int(result[0, -1])
    60
    >>> int(result[-1, 0])
    120
    >>> int(result[-1, -1])
    180
    """
    if len(images) != 4:
        raise ValueError("Exactly 4 images are required for mosaic augmentation")

    rng = np.random.default_rng(seed)
    out_h, out_w = output_size

    if split_ratio is None:
        y_split = rng.uniform(0.25, 0.75)
        x_split = rng.uniform(0.25, 0.75)
    else:
        y_split, x_split = split_ratio

    split_y = int(out_h * y_split)
    split_x = int(out_w * x_split)

    # Ensure minimum size
    split_y = max(1, min(split_y, out_h - 1))
    split_x = max(1, min(split_x, out_w - 1))

    mosaic = np.zeros((out_h, out_w), dtype=np.uint8)

    # Quadrant sizes
    quadrants = [
        (0, 0, split_y, split_x),             # top-left
        (0, split_x, split_y, out_w - split_x),  # top-right
        (split_y, 0, out_h - split_y, split_x),  # bottom-left
        (split_y, split_x, out_h - split_y, out_w - split_x),  # bottom-right
    ]

    for idx, (y, x, h, w) in enumerate(quadrants):
        resized = _resize_nearest(images[idx], h, w)
        mosaic[y : y + h, x : x + w] = resized

    return mosaic


def mosaic_with_labels(
    images: list[np.ndarray],
    labels: list[int],
    output_size: tuple[int, int] = (64, 64),
    seed: int | None = None,
) -> tuple[np.ndarray, list[tuple[int, float, float, float, float]]]:
    """
    Mosaic augmentation that also transforms bounding-box-style labels.

    Returns the mosaic image and a list of (label, y_center, x_center, h_frac, w_frac)
    for each quadrant (normalized to output size).

    >>> import numpy as np
    >>> imgs = [np.full((10, 10), i * 50, dtype=np.uint8) for i in range(4)]
    >>> mosaic, labels_out = mosaic_with_labels(imgs, [0, 1, 2, 3], seed=42)
    >>> len(labels_out)
    4
    """
    rng = np.random.default_rng(seed)
    out_h, out_w = output_size

    y_split = rng.uniform(0.25, 0.75)
    x_split = rng.uniform(0.25, 0.75)

    split_y = max(1, min(int(out_h * y_split), out_h - 1))
    split_x = max(1, min(int(out_w * x_split), out_w - 1))

    mosaic = np.zeros((out_h, out_w), dtype=np.uint8)
    quadrants = [
        (0, 0, split_y, split_x),
        (0, split_x, split_y, out_w - split_x),
        (split_y, 0, out_h - split_y, split_x),
        (split_y, split_x, out_h - split_y, out_w - split_x),
    ]

    labels_out = []
    for idx, (y, x, h, w) in enumerate(quadrants):
        resized = _resize_nearest(images[idx], h, w)
        mosaic[y : y + h, x : x + w] = resized
        # Normalized center + size
        yc = (y + h / 2) / out_h
        xc = (x + w / 2) / out_w
        labels_out.append((labels[idx], yc, xc, h / out_h, w / out_w))

    return mosaic, labels_out


if __name__ == "__main__":
    import doctest

    doctest.testmod()
