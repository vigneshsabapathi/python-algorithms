# https://github.com/TheAlgorithms/Python/blob/master/neural_network/back_propagation_neural_network.py

"""
Back-Propagation Neural Network

A feedforward neural network trained with the backpropagation algorithm.
This implementation uses numpy for matrix operations and supports
configurable hidden layer sizes with sigmoid activation.

The network learns by:
1. Forward pass  -- compute predictions layer by layer
2. Loss          -- measure error (MSE)
3. Backward pass -- compute gradients via chain rule
4. Update        -- adjust weights with gradient descent

Reference: Rumelhart, Hinton & Williams (1986)
"""

from __future__ import annotations

import numpy as np


def sigmoid(x: np.ndarray) -> np.ndarray:
    """
    Sigmoid activation function: 1 / (1 + exp(-x)).

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
    Derivative of sigmoid: s(x) * (1 - s(x)).

    Assumes *x* has already been passed through sigmoid.

    >>> sigmoid_derivative(np.array([0.5]))
    array([0.25])
    >>> sigmoid_derivative(np.array([0.0]))
    array([0.])
    >>> sigmoid_derivative(np.array([1.0]))
    array([0.])
    """
    return x * (1.0 - x)


class BackPropagationNetwork:
    """
    A simple feedforward neural network with one hidden layer,
    trained via backpropagation.

    >>> np.random.seed(0)
    >>> X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    >>> y = np.array([[0], [1], [1], [0]])
    >>> nn = BackPropagationNetwork(input_size=2, hidden_size=4, output_size=1, learning_rate=1.0)
    >>> losses = nn.train(X, y, epochs=5000)
    >>> all(loss >= 0 for loss in losses)
    True
    >>> predictions = nn.predict(X)
    >>> predicted_classes = (predictions > 0.5).astype(int).flatten().tolist()
    >>> predicted_classes
    [0, 1, 1, 0]
    """

    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        output_size: int,
        learning_rate: float = 0.1,
    ) -> None:
        self.learning_rate = learning_rate
        # Xavier initialization
        self.weights_ih = np.random.randn(input_size, hidden_size) * np.sqrt(
            2.0 / (input_size + hidden_size)
        )
        self.bias_h = np.zeros((1, hidden_size))
        self.weights_ho = np.random.randn(hidden_size, output_size) * np.sqrt(
            2.0 / (hidden_size + output_size)
        )
        self.bias_o = np.zeros((1, output_size))

    def forward(self, X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """
        Forward pass returning (hidden_output, final_output).

        >>> np.random.seed(42)
        >>> nn = BackPropagationNetwork(2, 3, 1)
        >>> h, o = nn.forward(np.array([[1.0, 0.0]]))
        >>> h.shape
        (1, 3)
        >>> o.shape
        (1, 1)
        """
        hidden = sigmoid(X @ self.weights_ih + self.bias_h)
        output = sigmoid(hidden @ self.weights_ho + self.bias_o)
        return hidden, output

    def backward(
        self,
        X: np.ndarray,
        y: np.ndarray,
        hidden: np.ndarray,
        output: np.ndarray,
    ) -> None:
        """
        Backward pass -- compute gradients and update weights.

        >>> np.random.seed(42)
        >>> nn = BackPropagationNetwork(2, 3, 1, learning_rate=0.5)
        >>> X = np.array([[1.0, 0.0]])
        >>> y = np.array([[1.0]])
        >>> h, o = nn.forward(X)
        >>> old_w = nn.weights_ho.copy()
        >>> nn.backward(X, y, h, o)
        >>> np.array_equal(old_w, nn.weights_ho)
        False
        """
        output_error = y - output
        output_delta = output_error * sigmoid_derivative(output)

        hidden_error = output_delta @ self.weights_ho.T
        hidden_delta = hidden_error * sigmoid_derivative(hidden)

        self.weights_ho += self.learning_rate * (hidden.T @ output_delta)
        self.bias_o += self.learning_rate * np.sum(output_delta, axis=0, keepdims=True)
        self.weights_ih += self.learning_rate * (X.T @ hidden_delta)
        self.bias_h += self.learning_rate * np.sum(hidden_delta, axis=0, keepdims=True)

    def train(
        self, X: np.ndarray, y: np.ndarray, epochs: int = 1000
    ) -> list[float]:
        """
        Train network for given epochs, returning loss history.

        >>> np.random.seed(0)
        >>> nn = BackPropagationNetwork(2, 4, 1, learning_rate=1.0)
        >>> losses = nn.train(np.array([[0,0],[0,1],[1,0],[1,1]]), np.array([[0],[1],[1],[0]]), epochs=100)
        >>> losses[-1] < losses[0]
        True
        """
        losses: list[float] = []
        for _ in range(epochs):
            hidden, output = self.forward(X)
            loss = float(np.mean((y - output) ** 2))
            losses.append(loss)
            self.backward(X, y, hidden, output)
        return losses

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict output for input X.

        >>> np.random.seed(0)
        >>> nn = BackPropagationNetwork(2, 4, 1)
        >>> nn.predict(np.array([[0, 0]])).shape
        (1, 1)
        """
        _, output = self.forward(X)
        return output


def demo() -> None:
    """Demonstrate XOR learning with backpropagation."""
    np.random.seed(0)
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])

    nn = BackPropagationNetwork(
        input_size=2, hidden_size=4, output_size=1, learning_rate=1.0
    )

    print("=== Back-Propagation Neural Network: XOR ===\n")
    losses = nn.train(X, y, epochs=10000)

    print(f"Initial loss: {losses[0]:.6f}")
    print(f"Final loss:   {losses[-1]:.6f}")
    print(f"Improvement:  {losses[0] / max(losses[-1], 1e-10):.1f}x\n")

    print("Predictions:")
    for xi, yi in zip(X, y):
        pred = nn.predict(xi.reshape(1, -1))[0, 0]
        print(f"  Input: {xi} -> Predicted: {pred:.4f}  Expected: {yi[0]}")

    print(f"\nLoss at epoch 100:   {losses[99]:.6f}")
    print(f"Loss at epoch 1000:  {losses[999]:.6f}")
    print(f"Loss at epoch 10000: {losses[-1]:.6f}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    demo()
