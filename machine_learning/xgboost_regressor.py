"""
XGBoost Regressor (Pure NumPy Implementation)

Extreme Gradient Boosting for regression tasks. Uses MSE loss
with second-order gradient boosting and regularization.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/xgboost_regressor.py
"""

import numpy as np


class XGBRegTree:
    """Regression tree for XGBoost."""

    def __init__(
        self, max_depth: int = 3, reg_lambda: float = 1.0, gamma: float = 0.0,
        min_child_weight: float = 1.0,
    ) -> None:
        self.max_depth = max_depth
        self.reg_lambda = reg_lambda
        self.gamma = gamma
        self.min_child_weight = min_child_weight
        self.feature: int | None = None
        self.threshold: float | None = None
        self.value: float = 0.0
        self.left: XGBRegTree | None = None
        self.right: XGBRegTree | None = None

    @property
    def is_leaf(self) -> bool:
        return self.left is None

    def _leaf_weight(self, g: np.ndarray, h: np.ndarray) -> float:
        return float(-np.sum(g) / (np.sum(h) + self.reg_lambda))

    def _score(self, g: np.ndarray, h: np.ndarray) -> float:
        return float(np.sum(g) ** 2 / (np.sum(h) + self.reg_lambda))

    def fit(self, x: np.ndarray, g: np.ndarray, h: np.ndarray, depth: int = 0) -> None:
        self.value = self._leaf_weight(g, h)

        if depth >= self.max_depth or len(x) < 2:
            return

        best_gain = 0.0
        best_feat, best_thresh = 0, 0.0
        parent_score = self._score(g, h)

        for feat in range(x.shape[1]):
            for thresh in np.unique(x[:, feat]):
                left = x[:, feat] <= thresh
                right = ~left
                if np.sum(h[left]) < self.min_child_weight or np.sum(h[right]) < self.min_child_weight:
                    continue
                gain = 0.5 * (self._score(g[left], h[left]) + self._score(g[right], h[right]) - parent_score) - self.gamma
                if gain > best_gain:
                    best_gain = gain
                    best_feat, best_thresh = feat, thresh

        if best_gain <= 0:
            return

        left_mask = x[:, best_feat] <= best_thresh
        self.feature = best_feat
        self.threshold = best_thresh
        self.left = XGBRegTree(self.max_depth, self.reg_lambda, self.gamma, self.min_child_weight)
        self.right = XGBRegTree(self.max_depth, self.reg_lambda, self.gamma, self.min_child_weight)
        self.left.fit(x[left_mask], g[left_mask], h[left_mask], depth + 1)
        self.right.fit(x[~left_mask], g[~left_mask], h[~left_mask], depth + 1)

    def predict_single(self, x: np.ndarray) -> float:
        if self.is_leaf:
            return self.value
        if x[self.feature] <= self.threshold:
            return self.left.predict_single(x)
        return self.right.predict_single(x)

    def predict(self, x: np.ndarray) -> np.ndarray:
        return np.array([self.predict_single(xi) for xi in x])


class XGBoostRegressor:
    """
    XGBoost regressor (pure numpy, MSE loss).

    >>> np.random.seed(42)
    >>> X = np.random.rand(50, 1) * 10
    >>> y = 3 * X.ravel() + 5 + np.random.randn(50) * 0.5
    >>> xgb = XGBoostRegressor(n_estimators=30, learning_rate=0.3, max_depth=3)
    >>> xgb.fit(X, y)
    >>> pred = xgb.predict(np.array([[5.0]]))
    >>> abs(float(pred[0]) - 20.0) < 3.0
    True
    """

    def __init__(
        self,
        n_estimators: int = 100,
        learning_rate: float = 0.1,
        max_depth: int = 3,
        reg_lambda: float = 1.0,
        gamma: float = 0.0,
    ) -> None:
        self.n_estimators = n_estimators
        self.lr = learning_rate
        self.max_depth = max_depth
        self.reg_lambda = reg_lambda
        self.gamma = gamma
        self.trees: list[XGBRegTree] = []
        self.base_score: float = 0.0

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        self.base_score = float(np.mean(y))
        pred = np.full(len(y), self.base_score)
        self.trees = []

        for _ in range(self.n_estimators):
            gradient = pred - y        # d/dy 0.5*(y-pred)^2 = pred - y
            hessian = np.ones(len(y))   # second derivative = 1

            tree = XGBRegTree(self.max_depth, self.reg_lambda, self.gamma)
            tree.fit(x, gradient, hessian)
            self.trees.append(tree)
            pred += self.lr * tree.predict(x)

    def predict(self, x: np.ndarray) -> np.ndarray:
        pred = np.full(x.shape[0], self.base_score)
        for tree in self.trees:
            pred += self.lr * tree.predict(x)
        return pred

    def mse(self, x: np.ndarray, y: np.ndarray) -> float:
        return float(np.mean((self.predict(x) - y) ** 2))

    def r_squared(self, x: np.ndarray, y: np.ndarray) -> float:
        ss_res = np.sum((y - self.predict(x)) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return float(1 - ss_res / ss_tot) if ss_tot != 0 else 1.0


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- XGBoost Regressor Demo ---")
    np.random.seed(42)

    X = np.random.rand(100, 1) * 10
    y = 2 * np.sin(X.ravel()) + X.ravel() * 0.5 + np.random.randn(100) * 0.3

    split = 80
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    xgb = XGBoostRegressor(n_estimators=50, learning_rate=0.3, max_depth=4)
    xgb.fit(X_train, y_train)

    print(f"Train MSE:    {xgb.mse(X_train, y_train):.4f}")
    print(f"Test MSE:     {xgb.mse(X_test, y_test):.4f}")
    print(f"Train R^2:    {xgb.r_squared(X_train, y_train):.4f}")
    print(f"Test R^2:     {xgb.r_squared(X_test, y_test):.4f}")
