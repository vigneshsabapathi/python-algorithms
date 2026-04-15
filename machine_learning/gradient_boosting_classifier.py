"""
Gradient Boosting Classifier

Ensemble method that builds trees sequentially, each correcting
the errors of the previous one. Uses gradient of the loss function.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/gradient_boosting_classifier.py
"""

import numpy as np
from collections import Counter


class DecisionStump:
    """Simple decision tree with depth 1 (used as weak learner)."""

    def __init__(self) -> None:
        self.feature_index: int = 0
        self.threshold: float = 0.0
        self.left_value: float = 0.0
        self.right_value: float = 0.0

    def fit(self, x: np.ndarray, residuals: np.ndarray) -> None:
        """Fit stump to minimize squared residuals."""
        best_mse = float("inf")
        n_samples, n_features = x.shape

        for feature in range(n_features):
            thresholds = np.unique(x[:, feature])
            for threshold in thresholds:
                left_mask = x[:, feature] <= threshold
                right_mask = ~left_mask

                if not np.any(left_mask) or not np.any(right_mask):
                    continue

                left_mean = np.mean(residuals[left_mask])
                right_mean = np.mean(residuals[right_mask])

                pred = np.where(left_mask, left_mean, right_mean)
                mse = np.mean((residuals - pred) ** 2)

                if mse < best_mse:
                    best_mse = mse
                    self.feature_index = feature
                    self.threshold = threshold
                    self.left_value = left_mean
                    self.right_value = right_mean

    def predict(self, x: np.ndarray) -> np.ndarray:
        return np.where(
            x[:, self.feature_index] <= self.threshold,
            self.left_value,
            self.right_value,
        )


class GradientBoostingClassifier:
    """
    Gradient Boosting for binary classification using log-loss.

    >>> np.random.seed(42)
    >>> X = np.vstack([np.random.randn(30, 2) + [2, 2], np.random.randn(30, 2) + [-2, -2]])
    >>> y = np.array([1]*30 + [0]*30)
    >>> gb = GradientBoostingClassifier(n_estimators=20, learning_rate=0.5)
    >>> gb.fit(X, y)
    >>> float(np.mean(gb.predict(X) == y)) > 0.9
    True
    """

    def __init__(
        self,
        n_estimators: int = 100,
        learning_rate: float = 0.1,
        max_depth: int = 1,
    ) -> None:
        self.n_estimators = n_estimators
        self.lr = learning_rate
        self.max_depth = max_depth
        self.trees: list[DecisionStump] = []
        self.initial_prediction: float = 0.0

    @staticmethod
    def _sigmoid(z: np.ndarray) -> np.ndarray:
        return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        """Fit gradient boosting model."""
        # Initial prediction: log-odds
        p = np.mean(y)
        self.initial_prediction = np.log(p / (1 - p + 1e-15))
        f = np.full(len(y), self.initial_prediction)

        self.trees = []
        for _ in range(self.n_estimators):
            probs = self._sigmoid(f)
            residuals = y - probs

            stump = DecisionStump()
            stump.fit(x, residuals)
            self.trees.append(stump)

            f += self.lr * stump.predict(x)

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        """Predict probabilities."""
        f = np.full(x.shape[0], self.initial_prediction)
        for tree in self.trees:
            f += self.lr * tree.predict(x)
        return self._sigmoid(f)

    def predict(self, x: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        """Predict class labels."""
        return (self.predict_proba(x) >= threshold).astype(int)

    def accuracy(self, x: np.ndarray, y: np.ndarray) -> float:
        return float(np.mean(self.predict(x) == y))


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- Gradient Boosting Classifier Demo ---")
    np.random.seed(42)

    X_pos = np.random.randn(60, 2) + [2, 2]
    X_neg = np.random.randn(60, 2) + [-2, -2]
    X = np.vstack([X_pos, X_neg])
    y = np.array([1] * 60 + [0] * 60)

    idx = np.random.permutation(120)
    X, y = X[idx], y[idx]
    X_train, X_test = X[:96], X[96:]
    y_train, y_test = y[:96], y[96:]

    for n_est in [10, 50, 100]:
        gb = GradientBoostingClassifier(n_estimators=n_est, learning_rate=0.1)
        gb.fit(X_train, y_train)
        print(f"n_estimators={n_est:3d}: train={gb.accuracy(X_train, y_train):.4f}, test={gb.accuracy(X_test, y_test):.4f}")
