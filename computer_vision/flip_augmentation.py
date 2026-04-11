"""
Flip Augmentation — image flipping for data augmentation in ML pipelines.

Flipping images (horizontally, vertically, or both) is one of the simplest
and most effective data augmentation techniques. It doubles or triples the
effective dataset size without distorting content.

Reference: TheAlgorithms/Python — computer_vision/flip_augmentation.py

>>> import numpy as np
>>> img = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.uint8)
>>> flip_horizontal(img)
array([[3, 2, 1],
       [6, 5, 4]], dtype=uint8)
>>> flip_vertical(img)
array([[4, 5, 6],
       [1, 2, 3]], dtype=uint8)
>>> flip_both(img)
array([[6, 5, 4],
       [3, 2, 1]], dtype=uint8)
"""

from __future__ import annotations

import numpy as np


def flip_horizontal(image: np.ndarray) -> np.ndarray:
    """
    Flip image horizontally (left-right mirror).

    Each row is reversed along the column axis.

    >>> import numpy as np
    >>> img = np.array([[1, 2], [3, 4]])
    >>> flip_horizontal(img)
    array([[2, 1],
           [4, 3]])
    """
    return image[:, ::-1].copy()


def flip_vertical(image: np.ndarray) -> np.ndarray:
    """
    Flip image vertically (top-bottom mirror).

    The row order is reversed.

    >>> import numpy as np
    >>> img = np.array([[1, 2], [3, 4]])
    >>> flip_vertical(img)
    array([[3, 4],
           [1, 2]])
    """
    return image[::-1, :].copy()


def flip_both(image: np.ndarray) -> np.ndarray:
    """
    Flip image both horizontally and vertically (180-degree rotation).

    Equivalent to rotating the image 180 degrees.

    >>> import numpy as np
    >>> img = np.array([[1, 2], [3, 4]])
    >>> flip_both(img)
    array([[4, 3],
           [2, 1]])
    """
    return image[::-1, ::-1].copy()


def random_flip(image: np.ndarray, seed: int | None = None) -> tuple[np.ndarray, str]:
    """
    Randomly apply one of: no flip, horizontal, vertical, or both.

    Returns tuple of (augmented_image, description_of_flip_applied).

    >>> import numpy as np
    >>> img = np.array([[1, 2], [3, 4]])
    >>> result, desc = random_flip(img, seed=42)
    >>> desc in ('none', 'horizontal', 'vertical', 'both')
    True
    """
    rng = np.random.default_rng(seed)
    choice = rng.integers(0, 4)
    if choice == 0:
        return image.copy(), "none"
    elif choice == 1:
        return flip_horizontal(image), "horizontal"
    elif choice == 2:
        return flip_vertical(image), "vertical"
    else:
        return flip_both(image), "both"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
