"""
Pooling Functions — spatial downsampling operations used in CNNs.

Pooling reduces spatial dimensions by summarizing non-overlapping
(or overlapping) windows of the input. Common pooling operations:
- Max pooling:     take the maximum value in each window
- Average pooling: take the mean value in each window
- Min pooling:     take the minimum value in each window

These are fundamental building blocks in convolutional neural networks
for translation invariance and dimensionality reduction.

Reference: TheAlgorithms/Python — computer_vision/pooling_functions.py

>>> import numpy as np
>>> img = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]], dtype=np.float64)
>>> max_pool(img, pool_size=2, stride=2)
array([[ 6.,  8.],
       [14., 16.]])
>>> avg_pool(img, pool_size=2, stride=2)
array([[ 3.5,  5.5],
       [11.5, 13.5]])
"""

from __future__ import annotations

import numpy as np


def max_pool(
    image: np.ndarray, pool_size: int = 2, stride: int = 2
) -> np.ndarray:
    """
    Max pooling: select the maximum value from each non-overlapping window.

    Args:
        image: 2D numpy array.
        pool_size: height and width of pooling window.
        stride: step size between windows.

    Returns:
        Downsampled 2D array.

    >>> import numpy as np
    >>> img = np.arange(16, dtype=np.float64).reshape(4, 4)
    >>> max_pool(img, 2, 2)
    array([[ 5.,  7.],
           [13., 15.]])
    """
    rows, cols = image.shape
    out_r = (rows - pool_size) // stride + 1
    out_c = (cols - pool_size) // stride + 1
    output = np.zeros((out_r, out_c), dtype=image.dtype)

    for i in range(out_r):
        for j in range(out_c):
            r_start = i * stride
            c_start = j * stride
            window = image[r_start : r_start + pool_size, c_start : c_start + pool_size]
            output[i, j] = np.max(window)

    return output


def avg_pool(
    image: np.ndarray, pool_size: int = 2, stride: int = 2
) -> np.ndarray:
    """
    Average pooling: compute the mean of each non-overlapping window.

    Args:
        image: 2D numpy array.
        pool_size: height and width of pooling window.
        stride: step size between windows.

    Returns:
        Downsampled 2D array.

    >>> import numpy as np
    >>> img = np.arange(16, dtype=np.float64).reshape(4, 4)
    >>> avg_pool(img, 2, 2)
    array([[ 2.5,  4.5],
           [10.5, 12.5]])
    """
    rows, cols = image.shape
    out_r = (rows - pool_size) // stride + 1
    out_c = (cols - pool_size) // stride + 1
    output = np.zeros((out_r, out_c), dtype=np.float64)

    for i in range(out_r):
        for j in range(out_c):
            r_start = i * stride
            c_start = j * stride
            window = image[r_start : r_start + pool_size, c_start : c_start + pool_size]
            output[i, j] = np.mean(window)

    return output


def min_pool(
    image: np.ndarray, pool_size: int = 2, stride: int = 2
) -> np.ndarray:
    """
    Min pooling: select the minimum value from each non-overlapping window.

    >>> import numpy as np
    >>> img = np.arange(16, dtype=np.float64).reshape(4, 4)
    >>> min_pool(img, 2, 2)
    array([[ 0.,  2.],
           [ 8., 10.]])
    """
    rows, cols = image.shape
    out_r = (rows - pool_size) // stride + 1
    out_c = (cols - pool_size) // stride + 1
    output = np.zeros((out_r, out_c), dtype=image.dtype)

    for i in range(out_r):
        for j in range(out_c):
            r_start = i * stride
            c_start = j * stride
            window = image[r_start : r_start + pool_size, c_start : c_start + pool_size]
            output[i, j] = np.min(window)

    return output


if __name__ == "__main__":
    import doctest

    doctest.testmod()
