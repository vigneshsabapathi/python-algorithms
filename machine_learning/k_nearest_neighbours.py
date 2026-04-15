"""
K-Nearest Neighbours (KNN) Classifier

Non-parametric lazy learning algorithm. Classifies based on
majority vote of k closest training samples.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/k_nearest_neighbours.py
"""

import numpy as np
from collections import Counter


class KNearestNeighbours:
    """
    K-Nearest Neighbours classifier.

    >>> X_train = np.array([[1, 1], [2, 2], [3, 3], [6, 6], [7, 7], [8, 8]], dtype=float)
    >>> y_train = np.array([0, 0, 0, 1, 1, 1])
    >>> knn = KNearestNeighbours(k=3)
    >>> knn.fit(X_train, y_train)
    >>> knn.predict(np.array([[2, 2]]))[0]
    0
    >>> knn.predict(np.array([[7, 7]]))[0]
    1
    """

    def __init__(self, k: int = 3) -> None:
        if k < 1:
            raise ValueError("k must be >= 1")
        self.k = k
        self.x_train: np.ndarray | None = None
        self.y_train: np.ndarray | None = None

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        """Store training data (lazy learner)."""
        self.x_train = x.copy()
        self.y_train = y.copy()

    def _euclidean_distances(self, point: np.ndarray) -> np.ndarray:
        """Compute Euclidean distances from point to all training samples."""
        return np.sqrt(np.sum((self.x_train - point) ** 2, axis=1))

    def _predict_single(self, point: np.ndarray) -> int:
        """Predict class for a single point."""
        distances = self._euclidean_distances(point)
        k_indices = np.argsort(distances)[: self.k]
        k_labels = self.y_train[k_indices]
        most_common = Counter(k_labels).most_common(1)
        return int(most_common[0][0])

    def predict(self, x: np.ndarray) -> np.ndarray:
        """Predict class labels for array of points."""
        return np.array([self._predict_single(point) for point in x])

    def accuracy(self, x: np.ndarray, y: np.ndarray) -> float:
        """Compute classification accuracy."""
        return float(np.mean(self.predict(x) == y))


def manhattan_distance(a: np.ndarray, b: np.ndarray) -> float:
    """
    Manhattan (L1) distance between two points.

    >>> manhattan_distance(np.array([0, 0]), np.array([3, 4]))
    7.0
    """
    return float(np.sum(np.abs(a - b)))


def minkowski_distance(a: np.ndarray, b: np.ndarray, p: int = 2) -> float:
    """
    Minkowski distance (generalized Lp norm).

    >>> minkowski_distance(np.array([0, 0]), np.array([3, 4]), 2)
    5.0
    >>> minkowski_distance(np.array([0, 0]), np.array([3, 4]), 1)
    7.0
    """
    return float(np.sum(np.abs(a - b) ** p) ** (1 / p))


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- K-Nearest Neighbours Demo ---")
    np.random.seed(42)

    # Generate 3-class dataset
    c0 = np.random.randn(30, 2) + [0, 0]
    c1 = np.random.randn(30, 2) + [5, 5]
    c2 = np.random.randn(30, 2) + [10, 0]
    X = np.vstack([c0, c1, c2])
    y = np.array([0] * 30 + [1] * 30 + [2] * 30)

    idx = np.random.permutation(90)
    X, y = X[idx], y[idx]

    X_train, X_test = X[:70], X[70:]
    y_train, y_test = y[:70], y[70:]

    for k in [1, 3, 5, 7]:
        knn = KNearestNeighbours(k=k)
        knn.fit(X_train, y_train)
        acc = knn.accuracy(X_test, y_test)
        print(f"k={k}: accuracy={acc:.4f}")
