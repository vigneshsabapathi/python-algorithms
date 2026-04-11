#!/usr/bin/env python3
"""
Optimized and alternative implementations of Back-Propagation Neural Network.

The reference implementation uses a single hidden layer with sigmoid activation.
These variants explore different activation functions, initialization strategies,
and optimization techniques commonly asked about in interviews.

Variants covered:
1. bp_relu      -- ReLU activation + He initialization; avoids vanishing gradients
2. bp_tanh      -- tanh activation; centered outputs [-1, 1]
3. bp_momentum  -- SGD with momentum; faster convergence on flat loss surfaces
4. bp_batch     -- mini-batch gradient descent; better generalization

Key interview insight:
    Sigmoid:  vanishing gradients for deep nets, output in (0,1)
    ReLU:     dead neuron problem but faster training
    tanh:     centered around 0, still vanishes for large |x|
    Momentum: accelerates SGD in relevant direction, dampens oscillations

Run:
    python neural_network/back_propagation_neural_network_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from neural_network.back_propagation_neural_network import (
    BackPropagationNetwork,
    sigmoid,
    sigmoid_derivative,
)


# ---------------------------------------------------------------------------
# Variant 1 -- ReLU activation with He initialization
# ---------------------------------------------------------------------------

def relu(x: np.ndarray) -> np.ndarray:
    """
    ReLU activation: max(0, x).

    >>> relu(np.array([-1.0, 0.0, 1.0, 2.0])).tolist()
    [0.0, 0.0, 1.0, 2.0]
    """
    return np.maximum(0, x)


def relu_derivative(x: np.ndarray) -> np.ndarray:
    """
    Derivative of ReLU: 1 if x > 0, else 0.

    >>> relu_derivative(np.array([-1.0, 0.0, 1.0, 2.0])).tolist()
    [0.0, 0.0, 1.0, 1.0]
    """
    return (x > 0).astype(float)


class BPNetworkReLU:
    """
    Backprop network using ReLU hidden activation, sigmoid output.

    He initialization for ReLU layers prevents dead neurons at start.

    >>> np.random.seed(1)
    >>> X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    >>> y = np.array([[0], [1], [1], [0]])
    >>> nn = BPNetworkReLU(2, 8, 1, learning_rate=0.5)
    >>> losses = nn.train(X, y, epochs=5000)
    >>> losses[-1] < losses[0]
    True
    """

    def __init__(self, input_size: int, hidden_size: int, output_size: int,
                 learning_rate: float = 0.1) -> None:
        self.lr = learning_rate
        # He initialization for ReLU
        self.w1 = np.random.randn(input_size, hidden_size) * np.sqrt(2.0 / input_size)
        self.b1 = np.zeros((1, hidden_size))
        self.w2 = np.random.randn(hidden_size, output_size) * np.sqrt(2.0 / hidden_size)
        self.b2 = np.zeros((1, output_size))

    def forward(self, X: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        self.z1 = X @ self.w1 + self.b1
        self.a1 = relu(self.z1)
        self.z2 = self.a1 @ self.w2 + self.b2
        self.a2 = sigmoid(self.z2)
        return self.z1, self.a1, self.a2

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 1000) -> list[float]:
        losses: list[float] = []
        for _ in range(epochs):
            z1, a1, a2 = self.forward(X)
            loss = float(np.mean((y - a2) ** 2))
            losses.append(loss)

            d2 = (y - a2) * sigmoid_derivative(a2)
            d1 = (d2 @ self.w2.T) * relu_derivative(z1)

            self.w2 += self.lr * (a1.T @ d2)
            self.b2 += self.lr * np.sum(d2, axis=0, keepdims=True)
            self.w1 += self.lr * (X.T @ d1)
            self.b1 += self.lr * np.sum(d1, axis=0, keepdims=True)
        return losses

    def predict(self, X: np.ndarray) -> np.ndarray:
        _, _, output = self.forward(X)
        return output


# ---------------------------------------------------------------------------
# Variant 2 -- tanh activation
# ---------------------------------------------------------------------------

class BPNetworkTanh:
    """
    Backprop network using tanh hidden activation, sigmoid output.

    tanh outputs are centered around 0, which can speed convergence.

    >>> np.random.seed(2)
    >>> X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    >>> y = np.array([[0], [1], [1], [0]])
    >>> nn = BPNetworkTanh(2, 6, 1, learning_rate=0.5)
    >>> losses = nn.train(X, y, epochs=5000)
    >>> losses[-1] < losses[0]
    True
    """

    def __init__(self, input_size: int, hidden_size: int, output_size: int,
                 learning_rate: float = 0.1) -> None:
        self.lr = learning_rate
        # Xavier initialization for tanh
        self.w1 = np.random.randn(input_size, hidden_size) * np.sqrt(1.0 / input_size)
        self.b1 = np.zeros((1, hidden_size))
        self.w2 = np.random.randn(hidden_size, output_size) * np.sqrt(1.0 / hidden_size)
        self.b2 = np.zeros((1, output_size))

    def forward(self, X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        self.a1 = np.tanh(X @ self.w1 + self.b1)
        self.a2 = sigmoid(self.a1 @ self.w2 + self.b2)
        return self.a1, self.a2

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 1000) -> list[float]:
        losses: list[float] = []
        for _ in range(epochs):
            a1, a2 = self.forward(X)
            loss = float(np.mean((y - a2) ** 2))
            losses.append(loss)

            d2 = (y - a2) * sigmoid_derivative(a2)
            d1 = (d2 @ self.w2.T) * (1 - a1 ** 2)  # tanh derivative

            self.w2 += self.lr * (a1.T @ d2)
            self.b2 += self.lr * np.sum(d2, axis=0, keepdims=True)
            self.w1 += self.lr * (X.T @ d1)
            self.b1 += self.lr * np.sum(d1, axis=0, keepdims=True)
        return losses

    def predict(self, X: np.ndarray) -> np.ndarray:
        _, output = self.forward(X)
        return output


# ---------------------------------------------------------------------------
# Variant 3 -- SGD with Momentum
# ---------------------------------------------------------------------------

class BPNetworkMomentum:
    """
    Backprop network with momentum-based weight updates.

    Momentum accumulates past gradients to smooth oscillations
    and accelerate convergence through flat regions.

    >>> np.random.seed(3)
    >>> X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    >>> y = np.array([[0], [1], [1], [0]])
    >>> nn = BPNetworkMomentum(2, 6, 1, learning_rate=0.5, momentum=0.9)
    >>> losses = nn.train(X, y, epochs=5000)
    >>> losses[-1] < losses[0]
    True
    """

    def __init__(self, input_size: int, hidden_size: int, output_size: int,
                 learning_rate: float = 0.1, momentum: float = 0.9) -> None:
        self.lr = learning_rate
        self.mu = momentum
        self.w1 = np.random.randn(input_size, hidden_size) * np.sqrt(2.0 / (input_size + hidden_size))
        self.b1 = np.zeros((1, hidden_size))
        self.w2 = np.random.randn(hidden_size, output_size) * np.sqrt(2.0 / (hidden_size + output_size))
        self.b2 = np.zeros((1, output_size))
        # Velocity terms
        self.vw1 = np.zeros_like(self.w1)
        self.vb1 = np.zeros_like(self.b1)
        self.vw2 = np.zeros_like(self.w2)
        self.vb2 = np.zeros_like(self.b2)

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 1000) -> list[float]:
        losses: list[float] = []
        for _ in range(epochs):
            # Forward
            h = sigmoid(X @ self.w1 + self.b1)
            o = sigmoid(h @ self.w2 + self.b2)
            loss = float(np.mean((y - o) ** 2))
            losses.append(loss)

            # Backward
            d2 = (y - o) * sigmoid_derivative(o)
            d1 = (d2 @ self.w2.T) * sigmoid_derivative(h)

            # Momentum update
            self.vw2 = self.mu * self.vw2 + self.lr * (h.T @ d2)
            self.vb2 = self.mu * self.vb2 + self.lr * np.sum(d2, axis=0, keepdims=True)
            self.vw1 = self.mu * self.vw1 + self.lr * (X.T @ d1)
            self.vb1 = self.mu * self.vb1 + self.lr * np.sum(d1, axis=0, keepdims=True)

            self.w2 += self.vw2
            self.b2 += self.vb2
            self.w1 += self.vw1
            self.b1 += self.vb1
        return losses

    def predict(self, X: np.ndarray) -> np.ndarray:
        h = sigmoid(X @ self.w1 + self.b1)
        return sigmoid(h @ self.w2 + self.b2)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    """Compare convergence speed and training time of all variants on XOR."""
    np.random.seed(42)
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    y = np.array([[0], [1], [1], [0]], dtype=float)
    epochs = 5000

    variants = {
        "Reference (sigmoid)": lambda: BackPropagationNetwork(2, 8, 1, learning_rate=0.5),
        "ReLU + He init":      lambda: BPNetworkReLU(2, 8, 1, learning_rate=0.5),
        "tanh + Xavier":       lambda: BPNetworkTanh(2, 8, 1, learning_rate=0.5),
        "Sigmoid + Momentum":  lambda: BPNetworkMomentum(2, 8, 1, learning_rate=0.3, momentum=0.9),
    }

    print("=== Backpropagation Variants Benchmark (XOR, 5000 epochs) ===\n")
    print(f"{'Variant':<25} {'Final Loss':>12} {'Time (ms)':>12} {'Correct':>8}")
    print("-" * 60)

    for name, factory in variants.items():
        np.random.seed(42)
        nn = factory()

        def run():
            np.random.seed(42)
            net = factory()
            net.train(X, y, epochs=epochs)

        t = timeit.timeit(run, number=3) / 3 * 1000

        np.random.seed(42)
        nn = factory()
        losses = nn.train(X, y, epochs=epochs)
        preds = nn.predict(X)
        correct = int(np.sum((preds > 0.5).astype(int) == y))

        print(f"{name:<25} {losses[-1]:>12.6f} {t:>12.1f} {correct:>5}/4")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
