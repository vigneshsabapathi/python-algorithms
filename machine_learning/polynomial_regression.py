"""
Polynomial Regression

Extends linear regression by fitting polynomial features:
y = w0 + w1*x + w2*x^2 + ... + wn*x^n

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/polynomial_regression.py
"""

import numpy as np


class PolynomialRegression:
    """
    Polynomial Regression using normal equation on polynomial features.

    >>> X = np.array([1, 2, 3, 4, 5], dtype=float)
    >>> y = np.array([1, 4, 9, 16, 25], dtype=float)  # y = x^2
    >>> model = PolynomialRegression(degree=2)
    >>> model.fit(X, y)
    >>> abs(model.predict(np.array([6.0]))[0] - 36.0) < 0.1
    True
    """

    def __init__(self, degree: int = 2) -> None:
        self.degree = degree
        self.coefficients: np.ndarray | None = None

    @staticmethod
    def _create_polynomial_features(x: np.ndarray, degree: int) -> np.ndarray:
        """
        Create polynomial feature matrix [1, x, x^2, ..., x^degree].

        >>> PolynomialRegression._create_polynomial_features(np.array([2.0, 3.0]), 2)
        array([[1., 2., 4.],
               [1., 3., 9.]])
        """
        x = x.ravel()
        return np.column_stack([x**i for i in range(degree + 1)])

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        """Fit polynomial regression using normal equation."""
        x_poly = self._create_polynomial_features(x, self.degree)
        # Normal equation: w = (X^T X)^(-1) X^T y
        self.coefficients = np.linalg.pinv(x_poly.T @ x_poly) @ x_poly.T @ y

    def predict(self, x: np.ndarray) -> np.ndarray:
        """Predict using fitted polynomial model."""
        x_poly = self._create_polynomial_features(x, self.degree)
        return x_poly @ self.coefficients

    def r_squared(self, x: np.ndarray, y: np.ndarray) -> float:
        """Coefficient of determination."""
        y_pred = self.predict(x)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return float(1 - ss_res / ss_tot) if ss_tot != 0 else 1.0


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- Polynomial Regression Demo ---")
    np.random.seed(42)

    # Generate data: y = 0.5*x^2 - 2*x + 3 + noise
    X = np.linspace(-3, 3, 50)
    y = 0.5 * X**2 - 2 * X + 3 + np.random.randn(50) * 0.5

    for degree in [1, 2, 3, 5]:
        model = PolynomialRegression(degree=degree)
        model.fit(X, y)
        r2 = model.r_squared(X, y)
        print(f"Degree {degree}: R^2={r2:.6f}, coefficients={np.round(model.coefficients, 3)}")

    # Prediction
    model = PolynomialRegression(degree=2)
    model.fit(X, y)
    test_x = np.array([0.0, 1.0, 2.0])
    print(f"\nPredictions at x={test_x}: {model.predict(test_x)}")
