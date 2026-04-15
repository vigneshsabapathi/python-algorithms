"""
Decision Tree Classifier

Classification tree using information gain (entropy) or gini impurity
for splitting. Builds a binary tree recursively.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/decision_tree.py
"""

import numpy as np
from collections import Counter


class DecisionNode:
    """Node in a decision tree."""

    def __init__(
        self,
        feature_index: int | None = None,
        threshold: float | None = None,
        left=None,
        right=None,
        value: int | None = None,
    ):
        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value  # leaf node class label


class DecisionTree:
    """
    Decision Tree Classifier using entropy-based information gain.

    >>> X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    >>> y = np.array([0, 1, 1, 1])
    >>> tree = DecisionTree(max_depth=3)
    >>> tree.fit(X, y)
    >>> tree.predict(np.array([[0, 0]]))[0]
    0
    >>> tree.predict(np.array([[1, 1]]))[0]
    1
    """

    def __init__(
        self,
        max_depth: int = 10,
        min_samples_split: int = 2,
        criterion: str = "entropy",
    ) -> None:
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.criterion = criterion
        self.root: DecisionNode | None = None

    @staticmethod
    def _entropy(y: np.ndarray) -> float:
        """
        Shannon entropy of label array.

        >>> DecisionTree._entropy(np.array([0, 0, 1, 1]))
        1.0
        >>> DecisionTree._entropy(np.array([0, 0, 0])) == 0
        True
        """
        counts = np.bincount(y)
        probs = counts[counts > 0] / len(y)
        return float(-np.sum(probs * np.log2(probs)))

    @staticmethod
    def _gini(y: np.ndarray) -> float:
        """
        Gini impurity of label array.

        >>> DecisionTree._gini(np.array([0, 0, 1, 1]))
        0.5
        >>> DecisionTree._gini(np.array([0, 0, 0]))
        0.0
        """
        counts = np.bincount(y)
        probs = counts[counts > 0] / len(y)
        return float(1 - np.sum(probs**2))

    def _impurity(self, y: np.ndarray) -> float:
        """Compute impurity based on chosen criterion."""
        if self.criterion == "gini":
            return self._gini(y)
        return self._entropy(y)

    def _information_gain(
        self, y: np.ndarray, left_idx: np.ndarray, right_idx: np.ndarray
    ) -> float:
        """Compute information gain for a split."""
        if len(left_idx) == 0 or len(right_idx) == 0:
            return 0.0
        n = len(y)
        parent_impurity = self._impurity(y)
        left_impurity = self._impurity(y[left_idx])
        right_impurity = self._impurity(y[right_idx])
        child_impurity = (
            len(left_idx) / n * left_impurity
            + len(right_idx) / n * right_impurity
        )
        return parent_impurity - child_impurity

    def _best_split(
        self, x: np.ndarray, y: np.ndarray
    ) -> tuple[int, float, float]:
        """Find best feature and threshold to split on."""
        best_gain = -1.0
        best_feature = 0
        best_threshold = 0.0

        for feature in range(x.shape[1]):
            thresholds = np.unique(x[:, feature])
            for threshold in thresholds:
                left_idx = np.where(x[:, feature] <= threshold)[0]
                right_idx = np.where(x[:, feature] > threshold)[0]
                gain = self._information_gain(y, left_idx, right_idx)
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = threshold

        return best_feature, best_threshold, best_gain

    def _build_tree(
        self, x: np.ndarray, y: np.ndarray, depth: int
    ) -> DecisionNode:
        """Recursively build the decision tree."""
        n_samples = len(y)
        n_classes = len(np.unique(y))

        # Stopping conditions
        if depth >= self.max_depth or n_classes == 1 or n_samples < self.min_samples_split:
            leaf_value = int(Counter(y).most_common(1)[0][0])
            return DecisionNode(value=leaf_value)

        feature, threshold, gain = self._best_split(x, y)

        if gain <= 0:
            leaf_value = int(Counter(y).most_common(1)[0][0])
            return DecisionNode(value=leaf_value)

        left_idx = np.where(x[:, feature] <= threshold)[0]
        right_idx = np.where(x[:, feature] > threshold)[0]

        left = self._build_tree(x[left_idx], y[left_idx], depth + 1)
        right = self._build_tree(x[right_idx], y[right_idx], depth + 1)

        return DecisionNode(
            feature_index=feature, threshold=threshold, left=left, right=right
        )

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        """Build the decision tree from training data."""
        self.root = self._build_tree(x, y, 0)

    def _predict_single(self, x: np.ndarray, node: DecisionNode) -> int:
        """Traverse tree to predict single sample."""
        if node.value is not None:
            return node.value
        if x[node.feature_index] <= node.threshold:
            return self._predict_single(x, node.left)
        return self._predict_single(x, node.right)

    def predict(self, x: np.ndarray) -> np.ndarray:
        """Predict class labels for samples."""
        return np.array([self._predict_single(xi, self.root) for xi in x])

    def accuracy(self, x: np.ndarray, y: np.ndarray) -> float:
        return float(np.mean(self.predict(x) == y))


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- Decision Tree Demo ---")
    np.random.seed(42)

    # Iris-like dataset (2 features, 3 classes)
    c0 = np.random.randn(40, 2) + [0, 0]
    c1 = np.random.randn(40, 2) + [3, 3]
    c2 = np.random.randn(40, 2) + [6, 0]
    X = np.vstack([c0, c1, c2])
    y = np.array([0] * 40 + [1] * 40 + [2] * 40)

    idx = np.random.permutation(120)
    X, y = X[idx], y[idx]
    X_train, X_test = X[:96], X[96:]
    y_train, y_test = y[:96], y[96:]

    for criterion in ["entropy", "gini"]:
        tree = DecisionTree(max_depth=5, criterion=criterion)
        tree.fit(X_train, y_train)
        train_acc = tree.accuracy(X_train, y_train)
        test_acc = tree.accuracy(X_test, y_test)
        print(f"{criterion:8s}: train_acc={train_acc:.4f}, test_acc={test_acc:.4f}")
