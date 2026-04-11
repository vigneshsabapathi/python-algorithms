"""
CNN Classification — forward pass of a Convolutional Neural Network in pure numpy.

Implements the core CNN building blocks without any deep learning framework:
- 2D Convolution layer (cross-correlation with learned filters)
- ReLU activation
- Max pooling
- Fully connected (dense) layer
- Softmax output

This demonstrates the math behind CNN inference. Weights are random
(not trained) — the point is understanding the forward-pass mechanics.

Reference: TheAlgorithms/Python — computer_vision/cnn_classification.py

>>> import numpy as np
>>> np.random.seed(42)
>>> img = np.random.rand(1, 8, 8)  # 1 channel, 8x8
>>> output = cnn_forward(img, num_classes=3, seed=42)
>>> output.shape
(3,)
>>> abs(output.sum() - 1.0) < 1e-6
True
"""

from __future__ import annotations

import numpy as np


def conv2d(
    image: np.ndarray, filters: np.ndarray, bias: np.ndarray
) -> np.ndarray:
    """
    2D convolution (actually cross-correlation) with multiple filters.

    Args:
        image: input of shape (C_in, H, W)
        filters: filters of shape (C_out, C_in, kH, kW)
        bias: bias of shape (C_out,)

    Returns:
        Output of shape (C_out, H - kH + 1, W - kW + 1)

    >>> import numpy as np
    >>> np.random.seed(0)
    >>> img = np.random.rand(1, 5, 5)
    >>> filt = np.random.rand(2, 1, 3, 3)
    >>> bias = np.zeros(2)
    >>> out = conv2d(img, filt, bias)
    >>> out.shape
    (2, 3, 3)
    """
    c_out, c_in, kh, kw = filters.shape
    _, h, w = image.shape
    out_h = h - kh + 1
    out_w = w - kw + 1

    output = np.zeros((c_out, out_h, out_w), dtype=np.float64)

    for f in range(c_out):
        for c in range(c_in):
            for i in range(out_h):
                for j in range(out_w):
                    window = image[c, i : i + kh, j : j + kw]
                    output[f, i, j] += np.sum(window * filters[f, c])
        output[f] += bias[f]

    return output


def relu(x: np.ndarray) -> np.ndarray:
    """
    ReLU activation: max(0, x).

    >>> import numpy as np
    >>> relu(np.array([-2, -1, 0, 1, 2]))
    array([0, 0, 0, 1, 2])
    """
    return np.maximum(0, x)


def max_pool2d(image: np.ndarray, pool_size: int = 2) -> np.ndarray:
    """
    Max pooling over each channel.

    Args:
        image: input of shape (C, H, W)
        pool_size: pooling window size

    Returns:
        Output of shape (C, H // pool_size, W // pool_size)

    >>> import numpy as np
    >>> img = np.arange(16, dtype=np.float64).reshape(1, 4, 4)
    >>> max_pool2d(img, 2)
    array([[[ 5.,  7.],
            [13., 15.]]])
    """
    c, h, w = image.shape
    out_h = h // pool_size
    out_w = w // pool_size

    output = np.zeros((c, out_h, out_w), dtype=image.dtype)
    for ch in range(c):
        for i in range(out_h):
            for j in range(out_w):
                r = i * pool_size
                col = j * pool_size
                output[ch, i, j] = np.max(
                    image[ch, r : r + pool_size, col : col + pool_size]
                )

    return output


def flatten(image: np.ndarray) -> np.ndarray:
    """
    Flatten a multi-dimensional array to 1D.

    >>> import numpy as np
    >>> flatten(np.zeros((2, 3, 4))).shape
    (24,)
    """
    return image.ravel()


def dense(x: np.ndarray, weights: np.ndarray, bias: np.ndarray) -> np.ndarray:
    """
    Fully connected (dense) layer: y = Wx + b.

    >>> import numpy as np
    >>> x = np.array([1.0, 2.0, 3.0])
    >>> w = np.ones((2, 3))
    >>> b = np.zeros(2)
    >>> dense(x, w, b)
    array([6., 6.])
    """
    return weights @ x + bias


def softmax(x: np.ndarray) -> np.ndarray:
    """
    Softmax: convert logits to probabilities.

    >>> import numpy as np
    >>> probs = softmax(np.array([1.0, 2.0, 3.0]))
    >>> abs(probs.sum() - 1.0) < 1e-6
    True
    >>> bool(probs[2] > probs[1] > probs[0])
    True
    """
    shifted = x - np.max(x)  # numerical stability
    exp_x = np.exp(shifted)
    return exp_x / exp_x.sum()


def cnn_forward(
    image: np.ndarray,
    num_classes: int = 10,
    seed: int = 42,
) -> np.ndarray:
    """
    Complete CNN forward pass: Conv -> ReLU -> Pool -> Conv -> ReLU -> Pool -> Dense -> Softmax.

    Uses random weights (for demonstration of the forward-pass math).

    Args:
        image: input of shape (C, H, W) where H, W >= 8.
        num_classes: number of output classes.
        seed: random seed for reproducible weights.

    Returns:
        Probability vector of shape (num_classes,).

    >>> import numpy as np
    >>> output = cnn_forward(np.random.rand(1, 8, 8), num_classes=5, seed=0)
    >>> output.shape
    (5,)
    """
    rng = np.random.default_rng(seed)

    # Layer 1: Conv (C_in -> 4 filters, 3x3) -> ReLU -> MaxPool
    c_in = image.shape[0]
    filters1 = rng.standard_normal((4, c_in, 3, 3)) * 0.1
    bias1 = np.zeros(4)
    x = conv2d(image, filters1, bias1)
    x = relu(x)
    if x.shape[1] >= 2 and x.shape[2] >= 2:
        x = max_pool2d(x, 2)

    # Layer 2: Conv (4 -> 8 filters, 3x3) -> ReLU -> MaxPool
    if x.shape[1] >= 3 and x.shape[2] >= 3:
        filters2 = rng.standard_normal((8, 4, 3, 3)) * 0.1
        bias2 = np.zeros(8)
        x = conv2d(x, filters2, bias2)
        x = relu(x)
        if x.shape[1] >= 2 and x.shape[2] >= 2:
            x = max_pool2d(x, 2)

    # Flatten and dense layer
    flat = flatten(x)
    fc_weights = rng.standard_normal((num_classes, flat.shape[0])) * 0.1
    fc_bias = np.zeros(num_classes)
    logits = dense(flat, fc_weights, fc_bias)

    return softmax(logits)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
