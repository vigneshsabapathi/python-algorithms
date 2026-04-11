# https://github.com/TheAlgorithms/Python/blob/master/neural_network/simple_neural_network.py

"""
Simple Neural Network -- single-layer perceptron.

The simplest possible neural network: one neuron with sigmoid activation,
trained by gradient descent. This is the foundation for understanding
how neural networks learn.

Architecture: Input -> Weights -> Sum -> Sigmoid -> Output
Training:     Mean Squared Error loss with gradient descent

This can learn linearly separable patterns (AND, OR) but NOT XOR.
"""

from __future__ import annotations

import numpy as np


class SimpleNeuralNetwork:
    """
    Single-layer neural network (perceptron) with sigmoid activation.

    >>> np.random.seed(1)
    >>> nn = SimpleNeuralNetwork(3)
    >>> X = np.array([[0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]])
    >>> y = np.array([[0, 1, 1, 0]]).T
    >>> _ = nn.train(X, y, epochs=10000)
    >>> predictions = nn.predict(X)
    >>> all((predictions > 0.5).flatten() == y.flatten())
    True
    """

    def __init__(self, input_size: int) -> None:
        """
        Initialize with random weights.

        >>> nn = SimpleNeuralNetwork(3)
        >>> nn.weights.shape
        (3, 1)
        """
        self.weights = 2 * np.random.random((input_size, 1)) - 1

    @staticmethod
    def sigmoid(x: np.ndarray) -> np.ndarray:
        """
        Sigmoid activation function.

        >>> SimpleNeuralNetwork.sigmoid(np.array([0.0]))
        array([0.5])
        >>> SimpleNeuralNetwork.sigmoid(np.array([100.0]))[0] > 0.99
        True
        """
        return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))

    @staticmethod
    def sigmoid_derivative(x: np.ndarray) -> np.ndarray:
        """
        Derivative of sigmoid (assumes x already passed through sigmoid).

        >>> SimpleNeuralNetwork.sigmoid_derivative(np.array([0.5]))
        array([0.25])
        """
        return x * (1.0 - x)

    def forward(self, X: np.ndarray) -> np.ndarray:
        """
        Forward pass: weighted sum -> sigmoid.

        >>> np.random.seed(1)
        >>> nn = SimpleNeuralNetwork(2)
        >>> nn.forward(np.array([[1.0, 0.0]])).shape
        (1, 1)
        """
        return self.sigmoid(X @ self.weights)

    def train(
        self,
        X: np.ndarray,
        y: np.ndarray,
        epochs: int = 10000,
        learning_rate: float = 1.0,
    ) -> list[float]:
        """
        Train the network using gradient descent.

        Returns loss history.

        >>> np.random.seed(1)
        >>> nn = SimpleNeuralNetwork(2)
        >>> X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        >>> y = np.array([[0, 0, 0, 1]]).T  # AND gate
        >>> losses = nn.train(X, y, epochs=1000)
        >>> losses[-1] < losses[0]
        True
        """
        losses: list[float] = []
        for _ in range(epochs):
            output = self.forward(X)
            error = y - output
            loss = float(np.mean(error ** 2))
            losses.append(loss)
            adjustment = learning_rate * (X.T @ (error * self.sigmoid_derivative(output)))
            self.weights += adjustment
        return losses

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict output for given input.

        >>> np.random.seed(1)
        >>> nn = SimpleNeuralNetwork(2)
        >>> _ = nn.train(np.array([[0,0],[0,1],[1,0],[1,1]]), np.array([[0,1,1,1]]).T, epochs=5000)
        >>> (nn.predict(np.array([[1, 1]])) > 0.5)[0, 0]
        True
        """
        return self.forward(X)


def demo() -> None:
    """Demonstrate simple neural network on logic gates."""
    np.random.seed(1)

    print("=== Simple Neural Network ===\n")

    # Training data: 3-input pattern
    X = np.array([[0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]])
    y = np.array([[0, 1, 1, 0]]).T

    nn = SimpleNeuralNetwork(3)

    print(f"Initial weights:\n{nn.weights.flatten().round(4)}\n")

    losses = nn.train(X, y, epochs=10000)

    print(f"Final weights:\n{nn.weights.flatten().round(4)}\n")
    print(f"Initial loss: {losses[0]:.6f}")
    print(f"Final loss:   {losses[-1]:.6f}\n")

    print("Training data predictions:")
    for xi, yi in zip(X, y):
        pred = nn.predict(xi.reshape(1, -1))[0, 0]
        print(f"  Input: {xi} -> Predicted: {pred:.4f}  Expected: {yi[0]}")

    # Test on new input
    test = np.array([[1, 0, 0]])
    print(f"\nNew input {test[0]} -> {nn.predict(test)[0, 0]:.4f}")

    # Logic gates demo
    print("\n--- Logic Gates ---")
    X_logic = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])

    for gate_name, y_gate in [
        ("AND", np.array([[0, 0, 0, 1]]).T),
        ("OR", np.array([[0, 1, 1, 1]]).T),
    ]:
        np.random.seed(1)
        gate_nn = SimpleNeuralNetwork(2)
        gate_nn.train(X_logic, y_gate, epochs=10000)
        preds = gate_nn.predict(X_logic)
        results = (preds > 0.5).astype(int).flatten()
        expected = y_gate.flatten()
        match = "PASS" if all(results == expected) else "FAIL"
        print(f"\n{gate_name} gate [{match}]:")
        for xi, pred, exp in zip(X_logic, preds.flatten(), expected):
            print(f"  {xi} -> {pred:.4f} (expected {exp})")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    demo()
