"""
Logistic Regression

Binary classification using the sigmoid function and gradient descent.
Predicts P(y=1|X) = sigmoid(Xw + b).

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/logistic_regression.py
"""

import numpy as np


def sigmoid(z: np.ndarray) -> np.ndarray:
    """
    Sigmoid activation function.

    >>> sigmoid(np.array([0.0]))
    array([0.5])
    >>> sigmoid(np.array([100.0]))[0] > 0.99
    True
    """
    return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))


class LogisticRegression:
    """
    Logistic Regression classifier using gradient descent.

    >>> np.random.seed(42)
    >>> X = np.vstack([np.random.randn(50, 2) + [2, 2], np.random.randn(50, 2) + [-2, -2]])
    >>> y = np.array([1]*50 + [0]*50)
    >>> model = LogisticRegression(learning_rate=0.1, n_iterations=200)
    >>> model.fit(X, y)
    >>> float(np.mean(model.predict(X) == y)) > 0.9
    True
    """

    def __init__(
        self, learning_rate: float = 0.01, n_iterations: int = 1000
    ) -> None:
        self.lr = learning_rate
        self.n_iter = n_iterations
        self.weights: np.ndarray | None = None
        self.bias: float = 0.0
        self.cost_history: list[float] = []

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        """Train logistic regression with gradient descent."""
        n_samples, n_features = x.shape
        self.weights = np.zeros(n_features)
        self.bias = 0.0
        self.cost_history = []

        for _ in range(self.n_iter):
            z = x @ self.weights + self.bias
            y_pred = sigmoid(z)

            # Gradients
            dw = (1 / n_samples) * (x.T @ (y_pred - y))
            db = (1 / n_samples) * np.sum(y_pred - y)

            self.weights -= self.lr * dw
            self.bias -= self.lr * db

            # Binary cross-entropy cost
            epsilon = 1e-15
            cost = -np.mean(
                y * np.log(y_pred + epsilon)
                + (1 - y) * np.log(1 - y_pred + epsilon)
            )
            self.cost_history.append(cost)

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        """Predict probabilities."""
        return sigmoid(x @ self.weights + self.bias)

    def predict(self, x: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        """Predict binary class labels."""
        return (self.predict_proba(x) >= threshold).astype(int)

    def accuracy(self, x: np.ndarray, y: np.ndarray) -> float:
        """Compute classification accuracy."""
        return float(np.mean(self.predict(x) == y))


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- Logistic Regression Demo ---")
    np.random.seed(42)

    # Generate two-class dataset
    n = 100
    X_pos = np.random.randn(n, 2) + [2, 2]
    X_neg = np.random.randn(n, 2) + [-2, -2]
    X = np.vstack([X_pos, X_neg])
    y = np.array([1] * n + [0] * n)

    # Shuffle
    idx = np.random.permutation(2 * n)
    X, y = X[idx], y[idx]

    # Train/test split
    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = LogisticRegression(learning_rate=0.1, n_iterations=300)
    model.fit(X_train, y_train)

    print(f"Weights: {model.weights}")
    print(f"Bias: {model.bias:.4f}")
    print(f"Train accuracy: {model.accuracy(X_train, y_train):.4f}")
    print(f"Test accuracy:  {model.accuracy(X_test, y_test):.4f}")
    print(f"Final cost:     {model.cost_history[-1]:.4f}")
    print(f"Sample predictions: {model.predict(X_test[:5])}")
    print(f"Sample probas:      {model.predict_proba(X_test[:5])}")
