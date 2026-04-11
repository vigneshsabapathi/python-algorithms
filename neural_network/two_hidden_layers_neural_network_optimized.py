#!/usr/bin/env python3
"""
Optimized and alternative implementations of Two Hidden Layers Neural Network.

The reference uses sigmoid throughout with vanilla gradient descent.
These variants explore modern training techniques and architectures.

Variants covered:
1. two_layer_relu      -- ReLU hidden layers, sigmoid output; faster training
2. two_layer_adam      -- Adam optimizer; adaptive learning rates per parameter
3. two_layer_dropout   -- dropout regularization; prevents overfitting

Key interview insight:
    Vanilla SGD:  simple but slow convergence, sensitive to learning rate
    Adam:         adaptive LR, works well out-of-the-box, most popular
    Dropout:      randomly zeros neurons during training, acts as ensemble
    ReLU:         sparse activations, no vanishing gradient in hidden layers

Run:
    python neural_network/two_hidden_layers_neural_network_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from neural_network.two_hidden_layers_neural_network import (
    TwoHiddenLayerNetwork,
    sigmoid,
    sigmoid_derivative,
)


# ---------------------------------------------------------------------------
# Variant 1 -- ReLU hidden layers
# ---------------------------------------------------------------------------

class TwoLayerReLU:
    """
    Two hidden layers with ReLU activation, sigmoid output.

    ReLU avoids vanishing gradients in hidden layers, enabling
    faster training for deeper architectures.

    >>> np.random.seed(0)
    >>> nn = TwoLayerReLU(2, 8, 4, 1, learning_rate=0.1)
    >>> X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    >>> y = np.array([[0], [1], [1], [0]])
    >>> losses = nn.train(X, y, epochs=5000)
    >>> losses[-1] < losses[0]
    True
    """

    def __init__(self, input_size: int, h1: int, h2: int, output_size: int,
                 learning_rate: float = 0.1) -> None:
        self.lr = learning_rate
        self.w1 = np.random.randn(input_size, h1) * np.sqrt(2.0 / input_size)
        self.b1 = np.zeros((1, h1))
        self.w2 = np.random.randn(h1, h2) * np.sqrt(2.0 / h1)
        self.b2 = np.zeros((1, h2))
        self.w3 = np.random.randn(h2, output_size) * np.sqrt(2.0 / h2)
        self.b3 = np.zeros((1, output_size))

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 1000) -> list[float]:
        losses: list[float] = []
        for _ in range(epochs):
            # Forward
            z1 = X @ self.w1 + self.b1
            a1 = np.maximum(0, z1)  # ReLU
            z2 = a1 @ self.w2 + self.b2
            a2 = np.maximum(0, z2)  # ReLU
            a3 = sigmoid(a2 @ self.w3 + self.b3)

            loss = float(np.mean((y - a3) ** 2))
            losses.append(loss)

            # Backward
            d3 = (y - a3) * sigmoid_derivative(a3)
            d2 = (d3 @ self.w3.T) * (z2 > 0)
            d1 = (d2 @ self.w2.T) * (z1 > 0)

            m = X.shape[0]
            self.w3 += self.lr * (a2.T @ d3) / m
            self.b3 += self.lr * np.sum(d3, axis=0, keepdims=True) / m
            self.w2 += self.lr * (a1.T @ d2) / m
            self.b2 += self.lr * np.sum(d2, axis=0, keepdims=True) / m
            self.w1 += self.lr * (X.T @ d1) / m
            self.b1 += self.lr * np.sum(d1, axis=0, keepdims=True) / m
        return losses

    def predict(self, X: np.ndarray) -> np.ndarray:
        a1 = np.maximum(0, X @ self.w1 + self.b1)
        a2 = np.maximum(0, a1 @ self.w2 + self.b2)
        return sigmoid(a2 @ self.w3 + self.b3)


# ---------------------------------------------------------------------------
# Variant 2 -- Adam optimizer
# ---------------------------------------------------------------------------

class TwoLayerAdam:
    """
    Two hidden layers with Adam optimizer.

    Adam maintains per-parameter adaptive learning rates using
    first and second moment estimates of gradients.

    >>> np.random.seed(0)
    >>> nn = TwoLayerAdam(2, 8, 4, 1, learning_rate=0.01)
    >>> X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    >>> y = np.array([[0], [1], [1], [0]])
    >>> losses = nn.train(X, y, epochs=5000)
    >>> losses[-1] < losses[0]
    True
    """

    def __init__(self, input_size: int, h1: int, h2: int, output_size: int,
                 learning_rate: float = 0.001, beta1: float = 0.9,
                 beta2: float = 0.999, epsilon: float = 1e-8) -> None:
        self.lr = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = epsilon

        self.params = {
            'w1': np.random.randn(input_size, h1) * np.sqrt(2.0 / (input_size + h1)),
            'b1': np.zeros((1, h1)),
            'w2': np.random.randn(h1, h2) * np.sqrt(2.0 / (h1 + h2)),
            'b2': np.zeros((1, h2)),
            'w3': np.random.randn(h2, output_size) * np.sqrt(2.0 / (h2 + output_size)),
            'b3': np.zeros((1, output_size)),
        }
        # Adam state
        self.m = {k: np.zeros_like(v) for k, v in self.params.items()}
        self.v = {k: np.zeros_like(v) for k, v in self.params.items()}
        self.t = 0

    def _adam_update(self, grads: dict[str, np.ndarray]) -> None:
        """Apply Adam update to all parameters."""
        self.t += 1
        for key in self.params:
            self.m[key] = self.beta1 * self.m[key] + (1 - self.beta1) * grads[key]
            self.v[key] = self.beta2 * self.v[key] + (1 - self.beta2) * grads[key] ** 2
            m_hat = self.m[key] / (1 - self.beta1 ** self.t)
            v_hat = self.v[key] / (1 - self.beta2 ** self.t)
            self.params[key] += self.lr * m_hat / (np.sqrt(v_hat) + self.eps)

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 1000) -> list[float]:
        losses: list[float] = []
        for _ in range(epochs):
            # Forward
            a1 = sigmoid(X @ self.params['w1'] + self.params['b1'])
            a2 = sigmoid(a1 @ self.params['w2'] + self.params['b2'])
            a3 = sigmoid(a2 @ self.params['w3'] + self.params['b3'])

            loss = float(np.mean((y - a3) ** 2))
            losses.append(loss)

            # Backward
            m = X.shape[0]
            d3 = (y - a3) * sigmoid_derivative(a3)
            d2 = (d3 @ self.params['w3'].T) * sigmoid_derivative(a2)
            d1 = (d2 @ self.params['w2'].T) * sigmoid_derivative(a1)

            grads = {
                'w3': (a2.T @ d3) / m,
                'b3': np.sum(d3, axis=0, keepdims=True) / m,
                'w2': (a1.T @ d2) / m,
                'b2': np.sum(d2, axis=0, keepdims=True) / m,
                'w1': (X.T @ d1) / m,
                'b1': np.sum(d1, axis=0, keepdims=True) / m,
            }
            self._adam_update(grads)
        return losses

    def predict(self, X: np.ndarray) -> np.ndarray:
        a1 = sigmoid(X @ self.params['w1'] + self.params['b1'])
        a2 = sigmoid(a1 @ self.params['w2'] + self.params['b2'])
        return sigmoid(a2 @ self.params['w3'] + self.params['b3'])


# ---------------------------------------------------------------------------
# Variant 3 -- Dropout regularization
# ---------------------------------------------------------------------------

class TwoLayerDropout:
    """
    Two hidden layers with dropout regularization.

    During training, randomly sets neuron outputs to 0 with probability p.
    During inference, uses full network with scaled weights.

    >>> np.random.seed(0)
    >>> nn = TwoLayerDropout(2, 8, 4, 1, dropout_rate=0.3)
    >>> X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    >>> y = np.array([[0], [1], [1], [0]])
    >>> losses = nn.train(X, y, epochs=5000)
    >>> losses[-1] < losses[0]
    True
    """

    def __init__(self, input_size: int, h1: int, h2: int, output_size: int,
                 learning_rate: float = 1.0, dropout_rate: float = 0.5) -> None:
        self.lr = learning_rate
        self.drop = dropout_rate

        self.w1 = np.random.randn(input_size, h1) * np.sqrt(2.0 / (input_size + h1))
        self.b1 = np.zeros((1, h1))
        self.w2 = np.random.randn(h1, h2) * np.sqrt(2.0 / (h1 + h2))
        self.b2 = np.zeros((1, h2))
        self.w3 = np.random.randn(h2, output_size) * np.sqrt(2.0 / (h2 + output_size))
        self.b3 = np.zeros((1, output_size))

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 1000) -> list[float]:
        losses: list[float] = []
        for _ in range(epochs):
            # Forward with dropout
            a1 = sigmoid(X @ self.w1 + self.b1)
            mask1 = (np.random.rand(*a1.shape) > self.drop) / (1 - self.drop)
            a1_drop = a1 * mask1

            a2 = sigmoid(a1_drop @ self.w2 + self.b2)
            mask2 = (np.random.rand(*a2.shape) > self.drop) / (1 - self.drop)
            a2_drop = a2 * mask2

            a3 = sigmoid(a2_drop @ self.w3 + self.b3)

            loss = float(np.mean((y - a3) ** 2))
            losses.append(loss)

            # Backward (through dropped activations)
            m = X.shape[0]
            d3 = (y - a3) * sigmoid_derivative(a3)
            d2 = (d3 @ self.w3.T) * sigmoid_derivative(a2) * mask2
            d1 = (d2 @ self.w2.T) * sigmoid_derivative(a1) * mask1

            self.w3 += self.lr * (a2_drop.T @ d3) / m
            self.b3 += self.lr * np.sum(d3, axis=0, keepdims=True) / m
            self.w2 += self.lr * (a1_drop.T @ d2) / m
            self.b2 += self.lr * np.sum(d2, axis=0, keepdims=True) / m
            self.w1 += self.lr * (X.T @ d1) / m
            self.b1 += self.lr * np.sum(d1, axis=0, keepdims=True) / m
        return losses

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Inference without dropout (full network)."""
        a1 = sigmoid(X @ self.w1 + self.b1)
        a2 = sigmoid(a1 @ self.w2 + self.b2)
        return sigmoid(a2 @ self.w3 + self.b3)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    """Compare two-hidden-layer variants on XOR."""
    print("=== Two Hidden Layers Variants Benchmark (XOR, 5000 epochs) ===\n")

    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    y = np.array([[0], [1], [1], [0]], dtype=float)
    epochs = 5000

    variants = {
        "Reference (sigmoid)": lambda: TwoHiddenLayerNetwork(2, 8, 4, 1, learning_rate=1.0),
        "ReLU hidden":         lambda: TwoLayerReLU(2, 8, 4, 1, learning_rate=0.1),
        "Adam optimizer":      lambda: TwoLayerAdam(2, 8, 4, 1, learning_rate=0.01),
        "Dropout (0.3)":       lambda: TwoLayerDropout(2, 8, 4, 1, dropout_rate=0.3),
    }

    print(f"{'Variant':<25} {'Final Loss':>12} {'Time (ms)':>12} {'Correct':>8}")
    print("-" * 60)

    for name, factory in variants.items():
        def run(f=factory):
            np.random.seed(0)
            net = f()
            net.train(X, y, epochs=epochs)

        t = timeit.timeit(run, number=3) / 3 * 1000

        np.random.seed(0)
        nn = factory()
        losses = nn.train(X, y, epochs=epochs)
        preds = nn.predict(X)
        correct = int(np.sum((preds > 0.5).astype(int) == y))

        print(f"{name:<25} {losses[-1]:>12.6f} {t:>12.1f} {correct:>5}/4")

    # Show Adam's adaptive learning rate advantage
    print("\n--- Convergence speed comparison (epochs to reach loss < 0.01) ---")
    for name, factory in variants.items():
        np.random.seed(0)
        nn = factory()
        losses = nn.train(X, y, epochs=20000)
        reached = next((i for i, l in enumerate(losses) if l < 0.01), None)
        if reached:
            print(f"  {name:<25} reached loss<0.01 at epoch {reached}")
        else:
            print(f"  {name:<25} did not reach loss<0.01 in 20000 epochs (final: {losses[-1]:.4f})")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
