"""
Multilayer Perceptron (MLP) Classifier

Feedforward neural network with backpropagation. Configurable hidden
layers, activation functions (sigmoid, relu, tanh).

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/multilayer_perceptron_classifier.py
"""

import numpy as np


def sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))


def sigmoid_derivative(z: np.ndarray) -> np.ndarray:
    s = sigmoid(z)
    return s * (1 - s)


def relu(z: np.ndarray) -> np.ndarray:
    return np.maximum(0, z)


def relu_derivative(z: np.ndarray) -> np.ndarray:
    return (z > 0).astype(float)


def tanh(z: np.ndarray) -> np.ndarray:
    return np.tanh(z)


def tanh_derivative(z: np.ndarray) -> np.ndarray:
    return 1 - np.tanh(z) ** 2


ACTIVATIONS = {
    "sigmoid": (sigmoid, sigmoid_derivative),
    "relu": (relu, relu_derivative),
    "tanh": (tanh, tanh_derivative),
}


class MLPClassifier:
    """
    Multilayer Perceptron for binary classification.

    >>> np.random.seed(42)
    >>> X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    >>> y = np.array([[0], [1], [1], [0]], dtype=float)  # XOR
    >>> mlp = MLPClassifier(layer_sizes=[2, 4, 1], learning_rate=0.5, n_iterations=2000, seed=42)
    >>> mlp.fit(X, y)
    >>> preds = (mlp.predict(X) > 0.5).astype(int)
    >>> int(np.sum(preds.ravel() == y.ravel()))
    4
    """

    def __init__(
        self,
        layer_sizes: list[int] | None = None,
        learning_rate: float = 0.01,
        n_iterations: int = 1000,
        activation: str = "sigmoid",
        seed: int | None = None,
    ) -> None:
        self.layer_sizes = layer_sizes or [2, 4, 1]
        self.lr = learning_rate
        self.n_iter = n_iterations
        self.activation_name = activation
        self.act_fn, self.act_deriv = ACTIVATIONS[activation]
        self.seed = seed
        self.weights: list[np.ndarray] = []
        self.biases: list[np.ndarray] = []
        self.cost_history: list[float] = []

    def _init_weights(self) -> None:
        """Xavier/He initialization."""
        rng = np.random.RandomState(self.seed)
        self.weights = []
        self.biases = []
        for i in range(len(self.layer_sizes) - 1):
            n_in = self.layer_sizes[i]
            n_out = self.layer_sizes[i + 1]
            scale = np.sqrt(2.0 / n_in)
            self.weights.append(rng.randn(n_in, n_out) * scale)
            self.biases.append(np.zeros((1, n_out)))

    def _forward(self, x: np.ndarray) -> tuple[list[np.ndarray], list[np.ndarray]]:
        """Forward pass. Returns (activations, pre_activations)."""
        activations = [x]
        pre_activations = []

        for i in range(len(self.weights)):
            z = activations[-1] @ self.weights[i] + self.biases[i]
            pre_activations.append(z)
            if i == len(self.weights) - 1:
                # Output layer: sigmoid for binary classification
                a = sigmoid(z)
            else:
                a = self.act_fn(z)
            activations.append(a)

        return activations, pre_activations

    def _backward(
        self,
        y: np.ndarray,
        activations: list[np.ndarray],
        pre_activations: list[np.ndarray],
    ) -> tuple[list[np.ndarray], list[np.ndarray]]:
        """Backward pass. Returns (weight_grads, bias_grads)."""
        n = y.shape[0]
        n_layers = len(self.weights)

        dw_list = [None] * n_layers
        db_list = [None] * n_layers

        # Output layer gradient (BCE loss derivative)
        delta = activations[-1] - y

        for i in range(n_layers - 1, -1, -1):
            dw_list[i] = (1 / n) * (activations[i].T @ delta)
            db_list[i] = (1 / n) * np.sum(delta, axis=0, keepdims=True)

            if i > 0:
                delta = (delta @ self.weights[i].T) * self.act_deriv(
                    pre_activations[i - 1]
                )

        return dw_list, db_list

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        """Train the MLP."""
        if y.ndim == 1:
            y = y.reshape(-1, 1)
        self._init_weights()
        self.cost_history = []

        for _ in range(self.n_iter):
            activations, pre_activations = self._forward(x)

            # Binary cross-entropy cost
            output = activations[-1]
            eps = 1e-15
            cost = -np.mean(
                y * np.log(output + eps) + (1 - y) * np.log(1 - output + eps)
            )
            self.cost_history.append(cost)

            dw_list, db_list = self._backward(y, activations, pre_activations)

            for i in range(len(self.weights)):
                self.weights[i] -= self.lr * dw_list[i]
                self.biases[i] -= self.lr * db_list[i]

    def predict(self, x: np.ndarray) -> np.ndarray:
        """Forward pass prediction."""
        activations, _ = self._forward(x)
        return activations[-1]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- MLP Classifier Demo ---")

    # XOR problem
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    y = np.array([[0], [1], [1], [0]], dtype=float)

    mlp = MLPClassifier(
        layer_sizes=[2, 8, 1], learning_rate=1.0, n_iterations=5000, seed=42
    )
    mlp.fit(X, y)

    print("XOR Problem:")
    preds = mlp.predict(X)
    for i in range(4):
        print(f"  Input: {X[i]} -> Predicted: {preds[i][0]:.4f}, Actual: {y[i][0]}")
    print(f"  Final cost: {mlp.cost_history[-1]:.6f}")

    # Larger classification
    np.random.seed(42)
    X_pos = np.random.randn(50, 2) + [2, 2]
    X_neg = np.random.randn(50, 2) + [-2, -2]
    X_data = np.vstack([X_pos, X_neg])
    y_data = np.array([[1]] * 50 + [[0]] * 50, dtype=float)

    mlp2 = MLPClassifier(
        layer_sizes=[2, 8, 4, 1], learning_rate=0.1, n_iterations=500, seed=42
    )
    mlp2.fit(X_data, y_data)
    acc = np.mean((mlp2.predict(X_data) > 0.5).astype(int) == y_data)
    print(f"\nBinary classification accuracy: {acc:.4f}")
