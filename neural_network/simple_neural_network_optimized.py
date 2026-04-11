#!/usr/bin/env python3
"""
Optimized and alternative implementations of Simple Neural Network.

The reference uses a single-layer perceptron with sigmoid. These variants
explore different activation functions and learning approaches for the
simplest neural network architecture.

Variants covered:
1. perceptron_step   -- classic step-function perceptron (Rosenblatt, 1958)
2. perceptron_tanh   -- tanh activation for centered outputs
3. adaline           -- adaptive linear neuron with MSE on linear output

Key interview insight:
    Step perceptron: guaranteed to converge for linearly separable data
    Sigmoid:         smooth gradient but vanishing for extreme inputs
    tanh:            centered output, stronger gradients than sigmoid
    Adaline:         updates based on linear output, precursor to backprop

Run:
    python neural_network/simple_neural_network_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from neural_network.simple_neural_network import SimpleNeuralNetwork


# ---------------------------------------------------------------------------
# Variant 1 -- Classic step-function perceptron
# ---------------------------------------------------------------------------

class StepPerceptron:
    """
    Rosenblatt's perceptron with step activation.

    Guaranteed to converge for linearly separable data
    (Perceptron Convergence Theorem).

    >>> np.random.seed(1)
    >>> p = StepPerceptron(2)
    >>> X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    >>> y = np.array([0, 0, 0, 1])  # AND
    >>> _ = p.train(X, y, epochs=100)
    >>> p.predict(np.array([[1, 1]]))
    1
    >>> p.predict(np.array([[0, 1]]))
    0
    """

    def __init__(self, input_size: int) -> None:
        self.weights = np.zeros(input_size)
        self.bias = 0.0

    def predict(self, X: np.ndarray) -> int | np.ndarray:
        """
        Predict using step function: 1 if w*x + b > 0, else 0.

        >>> p = StepPerceptron(2)
        >>> p.weights = np.array([1.0, 1.0])
        >>> p.bias = -1.5
        >>> p.predict(np.array([[1, 1]]))
        1
        """
        linear = X @ self.weights + self.bias
        if linear.ndim == 0 or (isinstance(linear, np.ndarray) and linear.size == 1):
            return int(float(linear) > 0)
        return (linear > 0).astype(int)

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 100,
              learning_rate: float = 0.1) -> int:
        """
        Train with perceptron learning rule. Returns number of errors in last epoch.

        >>> np.random.seed(0)
        >>> p = StepPerceptron(2)
        >>> X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        >>> p.train(X, np.array([0, 1, 1, 1]), epochs=50)
        0
        """
        errors = 0
        for _ in range(epochs):
            errors = 0
            for xi, yi in zip(X, y):
                pred = int((xi @ self.weights + self.bias) > 0)
                update = learning_rate * (yi - pred)
                self.weights += update * xi
                self.bias += update
                if pred != yi:
                    errors += 1
        return errors


# ---------------------------------------------------------------------------
# Variant 2 -- tanh perceptron
# ---------------------------------------------------------------------------

class TanhPerceptron:
    """
    Single neuron with tanh activation.

    Output in [-1, 1], stronger gradients than sigmoid for values near 0.

    >>> np.random.seed(1)
    >>> p = TanhPerceptron(2)
    >>> X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    >>> y = np.array([[-1, -1, -1, 1]]).T  # AND with -1/1 encoding
    >>> losses = p.train(X, y, epochs=5000)
    >>> losses[-1] < losses[0]
    True
    """

    def __init__(self, input_size: int) -> None:
        self.weights = np.random.randn(input_size, 1) * 0.5
        self.bias = np.zeros((1, 1))

    def forward(self, X: np.ndarray) -> np.ndarray:
        return np.tanh(X @ self.weights + self.bias)

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 1000,
              learning_rate: float = 0.1) -> list[float]:
        losses: list[float] = []
        for _ in range(epochs):
            output = self.forward(X)
            error = y - output
            loss = float(np.mean(error ** 2))
            losses.append(loss)
            # tanh derivative: 1 - tanh^2
            gradient = error * (1 - output ** 2)
            self.weights += learning_rate * (X.T @ gradient)
            self.bias += learning_rate * np.sum(gradient, axis=0, keepdims=True)
        return losses

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.forward(X)


# ---------------------------------------------------------------------------
# Variant 3 -- Adaline (Adaptive Linear Neuron)
# ---------------------------------------------------------------------------

class Adaline:
    """
    Adaptive Linear Neuron: updates weights based on linear output (before activation).

    Key difference from perceptron: gradient computed on continuous linear
    output, not on thresholded output. This gives smoother convergence.

    >>> np.random.seed(1)
    >>> a = Adaline(2)
    >>> X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    >>> y = np.array([[0, 0, 0, 1]]).T
    >>> losses = a.train(X, y, epochs=1000, learning_rate=0.01)
    >>> losses[-1] < losses[0]
    True
    """

    def __init__(self, input_size: int) -> None:
        self.weights = np.random.randn(input_size, 1) * 0.01
        self.bias = 0.0

    def net_input(self, X: np.ndarray) -> np.ndarray:
        return X @ self.weights + self.bias

    def activation(self, z: np.ndarray) -> np.ndarray:
        """Identity activation (linear)."""
        return z

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Threshold at 0.5 for classification."""
        return (self.net_input(X) >= 0.5).astype(int)

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 100,
              learning_rate: float = 0.01) -> list[float]:
        losses: list[float] = []
        for _ in range(epochs):
            net = self.net_input(X)
            output = self.activation(net)
            error = y - output
            loss = float(0.5 * np.mean(error ** 2))
            losses.append(loss)
            self.weights += learning_rate * (X.T @ error) / len(X)
            self.bias += learning_rate * np.mean(error)
        return losses


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    """Compare single-neuron variants on logic gate learning."""
    print("=== Simple Neural Network Variants Benchmark ===\n")

    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    gates = {
        "AND": np.array([[0, 0, 0, 1]]).T,
        "OR":  np.array([[0, 1, 1, 1]]).T,
    }

    for gate_name, y in gates.items():
        print(f"--- {gate_name} Gate ---")
        print(f"{'Variant':<20} {'Correct':>8} {'Time (ms)':>12}")
        print("-" * 42)

        # Reference
        def run_ref():
            np.random.seed(1)
            nn = SimpleNeuralNetwork(2)
            nn.train(X, y, epochs=5000)
            return nn

        t = timeit.timeit(run_ref, number=5) / 5 * 1000
        nn = run_ref()
        preds = (nn.predict(X) > 0.5).astype(int).flatten()
        correct = int(np.sum(preds == y.flatten()))
        print(f"{'Sigmoid (ref)':<20} {correct:>5}/4 {t:>12.1f}")

        # Step perceptron
        def run_step():
            np.random.seed(1)
            p = StepPerceptron(2)
            p.train(X, y.flatten().astype(int), epochs=100)
            return p

        t = timeit.timeit(run_step, number=5) / 5 * 1000
        p = run_step()
        preds = np.array([p.predict(xi.reshape(1, -1)) for xi in X])
        correct = int(np.sum(preds.flatten() == y.flatten()))
        print(f"{'Step perceptron':<20} {correct:>5}/4 {t:>12.1f}")

        # Adaline
        def run_adaline():
            np.random.seed(1)
            a = Adaline(2)
            a.train(X, y, epochs=5000, learning_rate=0.01)
            return a

        t = timeit.timeit(run_adaline, number=5) / 5 * 1000
        a = run_adaline()
        preds = a.predict(X).flatten()
        correct = int(np.sum(preds == y.flatten()))
        print(f"{'Adaline':<20} {correct:>5}/4 {t:>12.1f}")

        print()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
