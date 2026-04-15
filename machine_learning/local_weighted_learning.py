"""
Local Weighted Learning (Locally Weighted Regression / LOESS)

Non-parametric regression that fits local models weighted by
distance from the query point. Uses Gaussian kernel weights.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/local_weighted_learning/local_weighted_learning.py
"""

import numpy as np


def local_weighted_regression(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_query: float,
    tau: float = 0.5,
) -> float:
    """
    Predict y for a single query point using locally weighted regression.

    Weight = exp(-(x - x_query)^2 / (2 * tau^2))

    >>> x = np.array([1, 2, 3, 4, 5], dtype=float)
    >>> y = np.array([2, 4, 6, 8, 10], dtype=float)
    >>> abs(local_weighted_regression(x, y, 3.0, tau=1.0) - 6.0) < 0.5
    True
    """
    m = len(x_train)
    weights = np.exp(-((x_train - x_query) ** 2) / (2 * tau**2))
    W = np.diag(weights)

    # Add bias term
    X = np.column_stack([np.ones(m), x_train])
    x_q = np.array([1, x_query])

    # Weighted normal equation: theta = (X^T W X)^(-1) X^T W y
    theta = np.linalg.pinv(X.T @ W @ X) @ X.T @ W @ y_train

    return float(x_q @ theta)


class LocalWeightedRegression:
    """
    Locally Weighted Regression (LOESS/LOWESS).

    >>> np.random.seed(42)
    >>> x = np.linspace(0, 5, 20)
    >>> y = np.sin(x) + np.random.randn(20) * 0.1
    >>> lwr = LocalWeightedRegression(tau=0.5)
    >>> lwr.fit(x, y)
    >>> pred = lwr.predict(np.array([1.0, 2.0, 3.0]))
    >>> len(pred) == 3
    True
    """

    def __init__(self, tau: float = 0.5) -> None:
        self.tau = tau
        self.x_train: np.ndarray | None = None
        self.y_train: np.ndarray | None = None

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        """Store training data (lazy learner)."""
        self.x_train = x.copy()
        self.y_train = y.copy()

    def predict(self, x_query: np.ndarray) -> np.ndarray:
        """Predict for multiple query points."""
        return np.array([
            local_weighted_regression(self.x_train, self.y_train, xq, self.tau)
            for xq in x_query
        ])


def gaussian_kernel(distance: float, tau: float) -> float:
    """
    Gaussian kernel weight.

    >>> round(gaussian_kernel(0.0, 1.0), 4)
    1.0
    >>> gaussian_kernel(10.0, 0.1) < 0.01
    True
    """
    return float(np.exp(-(distance**2) / (2 * tau**2)))


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- Local Weighted Learning Demo ---")
    np.random.seed(42)

    # Non-linear data
    x = np.linspace(0, 2 * np.pi, 50)
    y = np.sin(x) + np.random.randn(50) * 0.15

    query_points = np.linspace(0, 2 * np.pi, 10)

    for tau in [0.1, 0.5, 1.0, 2.0]:
        lwr = LocalWeightedRegression(tau=tau)
        lwr.fit(x, y)
        preds = lwr.predict(query_points)
        actual = np.sin(query_points)
        mse = np.mean((preds - actual) ** 2)
        print(f"tau={tau:.1f}: MSE={mse:.6f}")

    # Detailed predictions with tau=0.5
    lwr = LocalWeightedRegression(tau=0.5)
    lwr.fit(x, y)
    for xq in [0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi]:
        pred = lwr.predict(np.array([xq]))[0]
        print(f"  x={xq:.2f}: pred={pred:.4f}, actual={np.sin(xq):.4f}")
