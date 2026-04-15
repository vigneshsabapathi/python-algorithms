"""
Support Vector Machines (SVM)

Linear SVM classifier using gradient descent on hinge loss with
L2 regularization. Finds the maximum-margin hyperplane.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/support_vector_machines.py
"""

import numpy as np


class SVM:
    """
    Support Vector Machine with linear kernel using sub-gradient descent.

    Loss = (1/n) * sum(max(0, 1 - y_i * (w . x_i + b))) + lambda * ||w||^2

    >>> np.random.seed(42)
    >>> X = np.vstack([np.random.randn(30, 2) + [2, 2], np.random.randn(30, 2) + [-2, -2]])
    >>> y = np.array([1]*30 + [-1]*30)
    >>> svm = SVM(learning_rate=0.001, lambda_param=0.01, n_iterations=500)
    >>> svm.fit(X, y)
    >>> svm.predict(np.array([[3, 3]]))[0]
    1
    >>> svm.predict(np.array([[-3, -3]]))[0]
    -1
    """

    def __init__(
        self,
        learning_rate: float = 0.001,
        lambda_param: float = 0.01,
        n_iterations: int = 1000,
    ) -> None:
        self.lr = learning_rate
        self.lambda_param = lambda_param
        self.n_iter = n_iterations
        self.weights: np.ndarray | None = None
        self.bias: float = 0.0
        self.cost_history: list[float] = []

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        """
        Train SVM using sub-gradient descent.
        Labels must be -1 or +1.
        """
        n_samples, n_features = x.shape
        self.weights = np.zeros(n_features)
        self.bias = 0.0
        self.cost_history = []

        for _ in range(self.n_iter):
            cost = 0.0
            for i in range(n_samples):
                condition = y[i] * (x[i] @ self.weights + self.bias) >= 1

                if condition:
                    self.weights -= self.lr * (2 * self.lambda_param * self.weights)
                else:
                    self.weights -= self.lr * (
                        2 * self.lambda_param * self.weights - y[i] * x[i]
                    )
                    self.bias -= self.lr * (-y[i])
                    cost += 1 - y[i] * (x[i] @ self.weights + self.bias)

            reg_cost = self.lambda_param * np.sum(self.weights**2)
            self.cost_history.append(cost / n_samples + reg_cost)

    def predict(self, x: np.ndarray) -> np.ndarray:
        """Predict class labels (-1 or +1)."""
        return np.sign(x @ self.weights + self.bias).astype(int)

    def decision_function(self, x: np.ndarray) -> np.ndarray:
        """Compute signed distance to decision boundary."""
        return x @ self.weights + self.bias

    def accuracy(self, x: np.ndarray, y: np.ndarray) -> float:
        return float(np.mean(self.predict(x) == y))


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- SVM Demo ---")
    np.random.seed(42)

    X_pos = np.random.randn(50, 2) + [3, 3]
    X_neg = np.random.randn(50, 2) + [-3, -3]
    X = np.vstack([X_pos, X_neg])
    y = np.array([1] * 50 + [-1] * 50)

    idx = np.random.permutation(100)
    X, y = X[idx], y[idx]

    split = 80
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    svm = SVM(learning_rate=0.001, lambda_param=0.01, n_iterations=500)
    svm.fit(X_train, y_train)

    print(f"Weights: {svm.weights}")
    print(f"Bias: {svm.bias:.4f}")
    print(f"Train accuracy: {svm.accuracy(X_train, y_train):.4f}")
    print(f"Test accuracy:  {svm.accuracy(X_test, y_test):.4f}")
    print(f"Decision values (test[:5]): {svm.decision_function(X_test[:5])}")
