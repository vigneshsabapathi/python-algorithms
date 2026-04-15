"""
XGBoost Classifier (Pure NumPy Implementation)

Extreme Gradient Boosting for classification. Uses regularized
objective function with second-order Taylor expansion, tree pruning,
and shrinkage.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/xgboost_classifier.py
"""

import numpy as np


class XGBTreeNode:
    """Node in an XGBoost decision tree."""

    def __init__(self, value: float = 0.0):
        self.value = value
        self.feature: int | None = None
        self.threshold: float | None = None
        self.left: XGBTreeNode | None = None
        self.right: XGBTreeNode | None = None

    @property
    def is_leaf(self) -> bool:
        return self.left is None


class XGBTree:
    """Single XGBoost regression tree (used as weak learner)."""

    def __init__(
        self,
        max_depth: int = 3,
        min_child_weight: float = 1.0,
        reg_lambda: float = 1.0,
        gamma: float = 0.0,
    ) -> None:
        self.max_depth = max_depth
        self.min_child_weight = min_child_weight
        self.reg_lambda = reg_lambda
        self.gamma = gamma
        self.root: XGBTreeNode | None = None

    def _leaf_weight(self, gradient: np.ndarray, hessian: np.ndarray) -> float:
        """Optimal leaf weight: -sum(g) / (sum(h) + lambda)."""
        return float(-np.sum(gradient) / (np.sum(hessian) + self.reg_lambda))

    def _gain(self, gradient: np.ndarray, hessian: np.ndarray) -> float:
        """Node gain score."""
        return float(np.sum(gradient) ** 2 / (np.sum(hessian) + self.reg_lambda))

    def _find_best_split(
        self, x: np.ndarray, gradient: np.ndarray, hessian: np.ndarray
    ) -> tuple[int, float, float]:
        """Find best feature and threshold maximizing gain."""
        best_gain_improvement = 0.0
        best_feature = 0
        best_threshold = 0.0
        current_gain = self._gain(gradient, hessian)

        for feature in range(x.shape[1]):
            thresholds = np.unique(x[:, feature])
            for threshold in thresholds:
                left_mask = x[:, feature] <= threshold
                right_mask = ~left_mask

                if np.sum(hessian[left_mask]) < self.min_child_weight:
                    continue
                if np.sum(hessian[right_mask]) < self.min_child_weight:
                    continue

                left_gain = self._gain(gradient[left_mask], hessian[left_mask])
                right_gain = self._gain(gradient[right_mask], hessian[right_mask])
                improvement = 0.5 * (left_gain + right_gain - current_gain) - self.gamma

                if improvement > best_gain_improvement:
                    best_gain_improvement = improvement
                    best_feature = feature
                    best_threshold = threshold

        return best_feature, best_threshold, best_gain_improvement

    def _build(
        self, x: np.ndarray, gradient: np.ndarray, hessian: np.ndarray, depth: int
    ) -> XGBTreeNode:
        node = XGBTreeNode(value=self._leaf_weight(gradient, hessian))

        if depth >= self.max_depth or len(x) < 2:
            return node

        feature, threshold, gain = self._find_best_split(x, gradient, hessian)
        if gain <= 0:
            return node

        left_mask = x[:, feature] <= threshold
        right_mask = ~left_mask

        node.feature = feature
        node.threshold = threshold
        node.left = self._build(x[left_mask], gradient[left_mask], hessian[left_mask], depth + 1)
        node.right = self._build(x[right_mask], gradient[right_mask], hessian[right_mask], depth + 1)
        return node

    def fit(self, x: np.ndarray, gradient: np.ndarray, hessian: np.ndarray) -> None:
        self.root = self._build(x, gradient, hessian, 0)

    def _predict_single(self, x: np.ndarray, node: XGBTreeNode) -> float:
        if node.is_leaf:
            return node.value
        if x[node.feature] <= node.threshold:
            return self._predict_single(x, node.left)
        return self._predict_single(x, node.right)

    def predict(self, x: np.ndarray) -> np.ndarray:
        return np.array([self._predict_single(xi, self.root) for xi in x])


class XGBoostClassifier:
    """
    XGBoost binary classifier (pure numpy).

    >>> np.random.seed(42)
    >>> X = np.vstack([np.random.randn(30, 2) + [2, 2], np.random.randn(30, 2) + [-2, -2]])
    >>> y = np.array([1]*30 + [0]*30)
    >>> xgb = XGBoostClassifier(n_estimators=20, learning_rate=0.3, max_depth=3)
    >>> xgb.fit(X, y)
    >>> float(np.mean(xgb.predict(X) == y)) > 0.9
    True
    """

    def __init__(
        self,
        n_estimators: int = 100,
        learning_rate: float = 0.1,
        max_depth: int = 3,
        reg_lambda: float = 1.0,
        gamma: float = 0.0,
        min_child_weight: float = 1.0,
    ) -> None:
        self.n_estimators = n_estimators
        self.lr = learning_rate
        self.max_depth = max_depth
        self.reg_lambda = reg_lambda
        self.gamma = gamma
        self.min_child_weight = min_child_weight
        self.trees: list[XGBTree] = []
        self.base_score: float = 0.0

    @staticmethod
    def _sigmoid(z: np.ndarray) -> np.ndarray:
        return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        # Initialize with log-odds
        p = np.mean(y)
        self.base_score = np.log(p / (1 - p + 1e-15))
        raw_pred = np.full(len(y), self.base_score)

        self.trees = []
        for _ in range(self.n_estimators):
            prob = self._sigmoid(raw_pred)
            gradient = prob - y           # first derivative of log-loss
            hessian = prob * (1 - prob)    # second derivative

            tree = XGBTree(
                max_depth=self.max_depth,
                min_child_weight=self.min_child_weight,
                reg_lambda=self.reg_lambda,
                gamma=self.gamma,
            )
            tree.fit(x, gradient, hessian)
            self.trees.append(tree)

            raw_pred += self.lr * tree.predict(x)

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        raw = np.full(x.shape[0], self.base_score)
        for tree in self.trees:
            raw += self.lr * tree.predict(x)
        return self._sigmoid(raw)

    def predict(self, x: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        return (self.predict_proba(x) >= threshold).astype(int)

    def accuracy(self, x: np.ndarray, y: np.ndarray) -> float:
        return float(np.mean(self.predict(x) == y))


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- XGBoost Classifier Demo ---")
    np.random.seed(42)

    X_pos = np.random.randn(60, 2) + [2, 2]
    X_neg = np.random.randn(60, 2) + [-2, -2]
    X = np.vstack([X_pos, X_neg])
    y = np.array([1] * 60 + [0] * 60)

    idx = np.random.permutation(120)
    X, y = X[idx], y[idx]
    X_train, X_test = X[:96], X[96:]
    y_train, y_test = y[:96], y[96:]

    xgb = XGBoostClassifier(n_estimators=50, learning_rate=0.3, max_depth=3)
    xgb.fit(X_train, y_train)
    print(f"Train accuracy: {xgb.accuracy(X_train, y_train):.4f}")
    print(f"Test accuracy:  {xgb.accuracy(X_test, y_test):.4f}")
