# https://github.com/TheAlgorithms/Python/blob/master/neural_network/two_hidden_layers_neural_network.py

"""
Two Hidden Layers Neural Network.

A feedforward neural network with two hidden layers, trained via
backpropagation. The additional hidden layer allows the network
to learn more complex decision boundaries than a single hidden layer.

Architecture: Input -> Hidden1 -> Hidden2 -> Output
Activation:   Sigmoid throughout (configurable)

The two-layer architecture is the simplest "deep" network and can
approximate any continuous function (Universal Approximation Theorem).

Reference: Cybenko (1989), Hornik et al. (1989)
"""

from __future__ import annotations

import numpy as np


def sigmoid(x: np.ndarray) -> np.ndarray:
    """
    Sigmoid activation function.

    >>> sigmoid(np.array([0.0]))
    array([0.5])
    >>> sigmoid(np.array([100.0]))[0] > 0.99
    True
    >>> sigmoid(np.array([-100.0]))[0] < 0.01
    True
    """
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))


def sigmoid_derivative(x: np.ndarray) -> np.ndarray:
    """
    Derivative of sigmoid (assumes x already passed through sigmoid).

    >>> sigmoid_derivative(np.array([0.5]))
    array([0.25])
    """
    return x * (1.0 - x)


class TwoHiddenLayerNetwork:
    """
    Neural network with two hidden layers.

    >>> np.random.seed(0)
    >>> X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    >>> y = np.array([[0], [1], [1], [0]])
    >>> nn = TwoHiddenLayerNetwork(2, 8, 4, 1, learning_rate=1.0)
    >>> losses = nn.train(X, y, epochs=5000)
    >>> losses[-1] < 0.01
    True
    >>> predictions = nn.predict(X)
    >>> (predictions > 0.5).astype(int).flatten().tolist()
    [0, 1, 1, 0]
    """

    def __init__(
        self,
        input_size: int,
        hidden1_size: int,
        hidden2_size: int,
        output_size: int,
        learning_rate: float = 0.1,
    ) -> None:
        """
        Initialize network with Xavier initialization.

        >>> nn = TwoHiddenLayerNetwork(2, 4, 3, 1)
        >>> nn.w1.shape
        (2, 4)
        >>> nn.w2.shape
        (4, 3)
        >>> nn.w3.shape
        (3, 1)
        """
        self.lr = learning_rate

        # Xavier initialization
        self.w1 = np.random.randn(input_size, hidden1_size) * np.sqrt(
            2.0 / (input_size + hidden1_size)
        )
        self.b1 = np.zeros((1, hidden1_size))

        self.w2 = np.random.randn(hidden1_size, hidden2_size) * np.sqrt(
            2.0 / (hidden1_size + hidden2_size)
        )
        self.b2 = np.zeros((1, hidden2_size))

        self.w3 = np.random.randn(hidden2_size, output_size) * np.sqrt(
            2.0 / (hidden2_size + output_size)
        )
        self.b3 = np.zeros((1, output_size))

    def forward(
        self, X: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Forward pass through both hidden layers.

        Returns (hidden1_output, hidden2_output, final_output).

        >>> np.random.seed(42)
        >>> nn = TwoHiddenLayerNetwork(2, 4, 3, 1)
        >>> h1, h2, out = nn.forward(np.array([[1.0, 0.0]]))
        >>> h1.shape, h2.shape, out.shape
        ((1, 4), (1, 3), (1, 1))
        """
        self.a1 = sigmoid(X @ self.w1 + self.b1)
        self.a2 = sigmoid(self.a1 @ self.w2 + self.b2)
        self.a3 = sigmoid(self.a2 @ self.w3 + self.b3)
        return self.a1, self.a2, self.a3

    def backward(
        self,
        X: np.ndarray,
        y: np.ndarray,
        a1: np.ndarray,
        a2: np.ndarray,
        a3: np.ndarray,
    ) -> None:
        """
        Backward pass: compute gradients for all three weight matrices.

        >>> np.random.seed(42)
        >>> nn = TwoHiddenLayerNetwork(2, 4, 3, 1, learning_rate=0.5)
        >>> X = np.array([[1.0, 0.0]])
        >>> y = np.array([[1.0]])
        >>> a1, a2, a3 = nn.forward(X)
        >>> old_w3 = nn.w3.copy()
        >>> nn.backward(X, y, a1, a2, a3)
        >>> np.array_equal(old_w3, nn.w3)
        False
        """
        m = X.shape[0]

        # Output layer error
        d3 = (y - a3) * sigmoid_derivative(a3)

        # Hidden layer 2 error
        d2 = (d3 @ self.w3.T) * sigmoid_derivative(a2)

        # Hidden layer 1 error
        d1 = (d2 @ self.w2.T) * sigmoid_derivative(a1)

        # Update weights and biases
        self.w3 += self.lr * (a2.T @ d3) / m
        self.b3 += self.lr * np.sum(d3, axis=0, keepdims=True) / m
        self.w2 += self.lr * (a1.T @ d2) / m
        self.b2 += self.lr * np.sum(d2, axis=0, keepdims=True) / m
        self.w1 += self.lr * (X.T @ d1) / m
        self.b1 += self.lr * np.sum(d1, axis=0, keepdims=True) / m

    def train(
        self, X: np.ndarray, y: np.ndarray, epochs: int = 1000
    ) -> list[float]:
        """
        Train for given epochs, returning loss history.

        >>> np.random.seed(0)
        >>> nn = TwoHiddenLayerNetwork(2, 4, 3, 1, learning_rate=1.0)
        >>> losses = nn.train(np.array([[0,0],[0,1],[1,0],[1,1]]),
        ...                   np.array([[0],[1],[1],[0]]), epochs=100)
        >>> losses[-1] < losses[0]
        True
        """
        losses: list[float] = []
        for _ in range(epochs):
            a1, a2, a3 = self.forward(X)
            loss = float(np.mean((y - a3) ** 2))
            losses.append(loss)
            self.backward(X, y, a1, a2, a3)
        return losses

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict output for given input.

        >>> np.random.seed(0)
        >>> nn = TwoHiddenLayerNetwork(2, 4, 3, 1)
        >>> nn.predict(np.array([[0, 0]])).shape
        (1, 1)
        """
        _, _, output = self.forward(X)
        return output


def demo() -> None:
    """Demonstrate two hidden layer network on XOR and more complex patterns."""
    np.random.seed(0)

    print("=== Two Hidden Layers Neural Network ===\n")

    # XOR problem
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])

    nn = TwoHiddenLayerNetwork(
        input_size=2, hidden1_size=8, hidden2_size=4,
        output_size=1, learning_rate=1.0,
    )

    print("--- XOR Problem ---")
    losses = nn.train(X, y, epochs=10000)

    print(f"Initial loss: {losses[0]:.6f}")
    print(f"Final loss:   {losses[-1]:.6f}")

    print("\nPredictions:")
    for xi, yi in zip(X, y):
        pred = nn.predict(xi.reshape(1, -1))[0, 0]
        print(f"  Input: {xi} -> Predicted: {pred:.4f}  Expected: {yi[0]}")

    # Multi-output: encode decimal to binary
    print("\n--- Decimal to Binary (multi-output) ---")
    np.random.seed(42)
    # Input: 4 patterns, Output: 2-bit binary encoding
    X_bin = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y_bin = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])  # Identity mapping

    nn2 = TwoHiddenLayerNetwork(2, 8, 4, 2, learning_rate=2.0)
    losses2 = nn2.train(X_bin, y_bin, epochs=10000)

    print(f"Final loss: {losses2[-1]:.6f}")
    for xi, yi in zip(X_bin, y_bin):
        pred = nn2.predict(xi.reshape(1, -1))[0]
        print(f"  Input: {xi} -> Predicted: [{pred[0]:.3f}, {pred[1]:.3f}]  Expected: {yi}")

    # Network architecture summary
    print(f"\nNetwork architecture:")
    print(f"  Layer 1: {nn.w1.shape[0]} -> {nn.w1.shape[1]} neurons ({nn.w1.size + nn.b1.size} params)")
    print(f"  Layer 2: {nn.w2.shape[0]} -> {nn.w2.shape[1]} neurons ({nn.w2.size + nn.b2.size} params)")
    print(f"  Layer 3: {nn.w3.shape[0]} -> {nn.w3.shape[1]} neurons ({nn.w3.size + nn.b3.size} params)")
    total = nn.w1.size + nn.b1.size + nn.w2.size + nn.b2.size + nn.w3.size + nn.b3.size
    print(f"  Total:   {total} trainable parameters")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    demo()
