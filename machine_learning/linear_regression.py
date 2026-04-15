"""
Linear Regression

Fits a linear model y = Xw + b using ordinary least squares (OLS)
and gradient descent approaches.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/linear_regression.py
"""

import numpy as np


class LinearRegression:
    """
    Linear Regression using the Normal Equation (OLS).

    w = (X^T X)^(-1) X^T y

    >>> X = np.array([[1], [2], [3], [4], [5]], dtype=float)
    >>> y = np.array([2, 4, 6, 8, 10], dtype=float)
    >>> model = LinearRegression()
    >>> model.fit(X, y)
    >>> float(round(model.predict(np.array([[6]]))[0], 1))
    12.0
    >>> round(model.r_squared(X, y), 4)
    1.0
    """

    def __init__(self) -> None:
        self.weights: np.ndarray | None = None
        self.bias: float = 0.0

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        """Fit using normal equation."""
        n = x.shape[0]
        x_bias = np.column_stack([np.ones(n), x])
        # w = (X^T X)^(-1) X^T y
        theta = np.linalg.pinv(x_bias.T @ x_bias) @ x_bias.T @ y
        self.bias = theta[0]
        self.weights = theta[1:]

    def predict(self, x: np.ndarray) -> np.ndarray:
        """Predict target values."""
        return x @ self.weights + self.bias

    def r_squared(self, x: np.ndarray, y: np.ndarray) -> float:
        """Coefficient of determination."""
        y_pred = self.predict(x)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return float(1 - ss_res / ss_tot) if ss_tot != 0 else 1.0


class LinearRegressionGD:
    """
    Linear Regression using Gradient Descent.

    >>> X = np.array([[1], [2], [3], [4], [5]], dtype=float)
    >>> y = np.array([2, 4, 6, 8, 10], dtype=float)
    >>> model = LinearRegressionGD(learning_rate=0.01, n_iterations=1000)
    >>> model.fit(X, y)
    >>> pred = model.predict(np.array([[6]]))
    >>> 11.5 < float(pred[0]) < 12.5
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
        n_samples, n_features = x.shape
        self.weights = np.zeros(n_features)
        self.bias = 0.0
        self.cost_history = []

        for _ in range(self.n_iter):
            y_pred = x @ self.weights + self.bias
            error = y_pred - y

            dw = (1 / n_samples) * (x.T @ error)
            db = (1 / n_samples) * np.sum(error)

            self.weights -= self.lr * dw
            self.bias -= self.lr * db

            cost = (1 / (2 * n_samples)) * np.sum(error**2)
            self.cost_history.append(cost)

    def predict(self, x: np.ndarray) -> np.ndarray:
        return x @ self.weights + self.bias


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- Linear Regression Demo ---")
    np.random.seed(42)
    X = np.random.rand(100, 1) * 10
    y = 3 * X.ravel() + 7 + np.random.randn(100) * 0.5

    # OLS
    model_ols = LinearRegression()
    model_ols.fit(X, y)
    print(f"OLS weights: {model_ols.weights}, bias: {model_ols.bias:.4f}")
    print(f"OLS R^2: {model_ols.r_squared(X, y):.6f}")

    # Gradient Descent
    model_gd = LinearRegressionGD(learning_rate=0.01, n_iterations=1000)
    model_gd.fit(X, y)
    print(f"GD  weights: {model_gd.weights}, bias: {model_gd.bias:.4f}")
    print(f"GD  final cost: {model_gd.cost_history[-1]:.6f}")
    print(f"GD  predict(X=6): {model_gd.predict(np.array([[6.0]]))}")
