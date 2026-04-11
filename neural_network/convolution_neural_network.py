# https://github.com/TheAlgorithms/Python/blob/master/neural_network/convolution_neural_network.py

"""
Convolution Neural Network (CNN) -- pure NumPy implementation.

Implements the core CNN building blocks from scratch:
- 2D Convolution (cross-correlation)
- Max pooling
- Flatten + fully connected layer
- Forward and backward passes

This is a minimal educational CNN that can learn simple patterns.
No TensorFlow/Keras dependency -- pure numpy for interview clarity.

Reference: LeCun et al. (1998) "Gradient-Based Learning Applied to Document Recognition"
"""

from __future__ import annotations

import numpy as np


def convolve2d(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    2D cross-correlation (valid mode) between image and kernel.

    Args:
        image:  2D array of shape (H, W)
        kernel: 2D array of shape (kH, kW)

    Returns:
        2D array of shape (H - kH + 1, W - kW + 1)

    >>> img = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)
    >>> k = np.array([[1, 0], [0, -1]], dtype=float)
    >>> convolve2d(img, k).tolist()
    [[-4.0, -4.0], [-4.0, -4.0]]

    >>> img = np.ones((4, 4))
    >>> k = np.ones((2, 2))
    >>> convolve2d(img, k).tolist()
    [[4.0, 4.0, 4.0], [4.0, 4.0, 4.0], [4.0, 4.0, 4.0]]

    >>> convolve2d(np.eye(3), np.array([[1]])).tolist()
    [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    """
    h, w = image.shape
    kh, kw = kernel.shape
    out_h, out_w = h - kh + 1, w - kw + 1
    output = np.zeros((out_h, out_w))
    for i in range(out_h):
        for j in range(out_w):
            output[i, j] = np.sum(image[i : i + kh, j : j + kw] * kernel)
    return output


def max_pool2d(
    image: np.ndarray, pool_size: int = 2, stride: int = 2
) -> tuple[np.ndarray, np.ndarray]:
    """
    2D max pooling with given pool size and stride.

    Returns (pooled_output, mask_of_max_positions).

    >>> img = np.array([[1, 3, 2, 4], [5, 6, 7, 8], [3, 2, 1, 0], [1, 2, 3, 4]], dtype=float)
    >>> pooled, mask = max_pool2d(img, 2, 2)
    >>> pooled.tolist()
    [[6.0, 8.0], [3.0, 4.0]]
    >>> mask.shape
    (4, 4)

    >>> img = np.arange(9, dtype=float).reshape(3, 3)
    >>> pooled, _ = max_pool2d(img, 2, 1)
    >>> pooled.tolist()
    [[4.0, 5.0], [7.0, 8.0]]
    """
    h, w = image.shape
    out_h = (h - pool_size) // stride + 1
    out_w = (w - pool_size) // stride + 1
    output = np.zeros((out_h, out_w))
    mask = np.zeros_like(image)

    for i in range(out_h):
        for j in range(out_w):
            region = image[
                i * stride : i * stride + pool_size,
                j * stride : j * stride + pool_size,
            ]
            max_val = np.max(region)
            output[i, j] = max_val
            # Record position of max for backprop
            local_mask = (region == max_val)
            mask[
                i * stride : i * stride + pool_size,
                j * stride : j * stride + pool_size,
            ] += local_mask
    return output, mask


def relu(x: np.ndarray) -> np.ndarray:
    """
    ReLU activation.

    >>> relu(np.array([-2.0, -1.0, 0.0, 1.0, 2.0])).tolist()
    [0.0, 0.0, 0.0, 1.0, 2.0]
    """
    return np.maximum(0, x)


def softmax(x: np.ndarray) -> np.ndarray:
    """
    Softmax function for classification output.

    >>> probs = softmax(np.array([1.0, 2.0, 3.0]))
    >>> abs(sum(probs) - 1.0) < 1e-10
    True
    >>> probs[2] > probs[1] > probs[0]
    True
    """
    shifted = x - np.max(x)
    exp_x = np.exp(shifted)
    return exp_x / np.sum(exp_x)


class SimpleCNN:
    """
    Minimal CNN: Conv -> ReLU -> MaxPool -> Flatten -> FC -> Softmax.

    Single 3x3 filter, designed for tiny images to demonstrate CNN mechanics.

    >>> np.random.seed(0)
    >>> cnn = SimpleCNN(num_filters=1, filter_size=3, num_classes=2)
    >>> img = np.random.randn(6, 6)
    >>> probs = cnn.forward(img)
    >>> abs(sum(probs) - 1.0) < 1e-10
    True
    >>> len(probs) == 2
    True
    """

    def __init__(
        self,
        num_filters: int = 1,
        filter_size: int = 3,
        num_classes: int = 2,
    ) -> None:
        self.num_filters = num_filters
        self.filter_size = filter_size
        self.num_classes = num_classes
        # He initialization for filters
        self.filters = np.random.randn(
            num_filters, filter_size, filter_size
        ) * np.sqrt(2.0 / (filter_size * filter_size))
        self.fc_weights: np.ndarray | None = None
        self.fc_bias = np.zeros(num_classes)

    def forward(self, image: np.ndarray) -> np.ndarray:
        """
        Forward pass: conv -> relu -> pool -> flatten -> FC -> softmax.

        >>> np.random.seed(1)
        >>> cnn = SimpleCNN(1, 3, 3)
        >>> probs = cnn.forward(np.random.randn(8, 8))
        >>> probs.shape
        (3,)
        """
        self._input = image

        # Convolution
        conv_outputs = []
        for f in range(self.num_filters):
            conv_out = convolve2d(image, self.filters[f])
            conv_outputs.append(conv_out)
        self._conv_out = np.array(conv_outputs)

        # ReLU
        self._relu_out = relu(self._conv_out)

        # Max pool each filter output
        pooled_list = []
        self._pool_masks = []
        for f in range(self.num_filters):
            pooled, mask = max_pool2d(self._relu_out[f])
            pooled_list.append(pooled)
            self._pool_masks.append(mask)
        self._pooled = np.array(pooled_list)

        # Flatten
        self._flat = self._pooled.flatten()

        # Lazy init FC weights
        if self.fc_weights is None:
            fan_in = len(self._flat)
            self.fc_weights = np.random.randn(
                fan_in, self.num_classes
            ) * np.sqrt(2.0 / fan_in)

        # Fully connected + softmax
        logits = self._flat @ self.fc_weights + self.fc_bias
        return softmax(logits)

    def compute_loss(self, probs: np.ndarray, label: int) -> float:
        """
        Cross-entropy loss for single sample.

        >>> probs = np.array([0.7, 0.2, 0.1])
        >>> loss = SimpleCNN().compute_loss(probs, 0)
        >>> loss > 0
        True
        """
        return -np.log(max(probs[label], 1e-10))

    def train_step(
        self, image: np.ndarray, label: int, learning_rate: float = 0.01
    ) -> float:
        """
        Single training step: forward + backward + update.

        Returns the loss.

        >>> np.random.seed(42)
        >>> cnn = SimpleCNN(1, 3, 2)
        >>> loss = cnn.train_step(np.random.randn(6, 6), 1, learning_rate=0.01)
        >>> loss > 0
        True
        """
        probs = self.forward(image)
        loss = self.compute_loss(probs, label)

        # Gradient of cross-entropy + softmax
        d_logits = probs.copy()
        d_logits[label] -= 1  # d_loss/d_logits

        # FC gradients
        d_fc_weights = np.outer(self._flat, d_logits)
        d_fc_bias = d_logits
        d_flat = self.fc_weights @ d_logits

        # Update FC
        self.fc_weights -= learning_rate * d_fc_weights
        self.fc_bias -= learning_rate * d_fc_bias

        # Reshape back to pooled shape
        d_pooled = d_flat.reshape(self._pooled.shape)

        # Backprop through pool (upsample with mask)
        d_relu = np.zeros_like(self._relu_out)
        for f in range(self.num_filters):
            ph, pw = d_pooled[f].shape
            for i in range(ph):
                for j in range(pw):
                    region_mask = self._pool_masks[f][
                        i * 2 : i * 2 + 2, j * 2 : j * 2 + 2
                    ]
                    region_mask_norm = region_mask / max(np.sum(region_mask), 1)
                    d_relu[f][i * 2 : i * 2 + 2, j * 2 : j * 2 + 2] = (
                        d_pooled[f][i, j] * region_mask_norm
                    )

        # Backprop through ReLU
        d_conv = d_relu * (self._conv_out > 0)

        # Update filters
        for f in range(self.num_filters):
            d_filter = convolve2d(self._input, d_conv[f])
            # Crop if shapes don't match
            fs = self.filter_size
            self.filters[f] -= learning_rate * d_filter[:fs, :fs]

        return loss


def demo() -> None:
    """Demonstrate CNN on synthetic binary classification."""
    np.random.seed(0)

    print("=== Convolution Neural Network Demo ===\n")

    # Generate tiny synthetic data: class 0 = random, class 1 = has diagonal
    n_samples = 20
    images = []
    labels = []
    for i in range(n_samples):
        if i % 2 == 0:
            img = np.random.randn(8, 8) * 0.1
            labels.append(0)
        else:
            img = np.random.randn(8, 8) * 0.1
            img += np.eye(8) * 2  # add strong diagonal pattern
            labels.append(1)
        images.append(img)

    cnn = SimpleCNN(num_filters=2, filter_size=3, num_classes=2)

    print("Training for 50 epochs on 20 synthetic 8x8 images...")
    for epoch in range(50):
        total_loss = 0.0
        correct = 0
        for img, lbl in zip(images, labels):
            probs = cnn.forward(img)
            total_loss += cnn.compute_loss(probs, lbl)
            if np.argmax(probs) == lbl:
                correct += 1
            cnn.train_step(img, lbl, learning_rate=0.005)
        if epoch % 10 == 0 or epoch == 49:
            print(f"  Epoch {epoch:>2}: loss={total_loss / n_samples:.4f}  acc={correct}/{n_samples}")

    # Test predictions
    print("\nSample predictions:")
    for i in [0, 1, 2, 3]:
        probs = cnn.forward(images[i])
        print(f"  Image {i} (label={labels[i]}): pred={np.argmax(probs)}  probs={probs.round(3)}")

    # Show convolution operation
    print("\nConvolution example:")
    test_img = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)
    test_kernel = np.array([[1, 0], [0, -1]], dtype=float)
    result = convolve2d(test_img, test_kernel)
    print(f"  Image:\n{test_img}")
    print(f"  Kernel:\n{test_kernel}")
    print(f"  Result:\n{result}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    demo()
