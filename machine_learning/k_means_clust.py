"""
K-Means Clustering

Unsupervised algorithm that partitions data into k clusters by
iteratively assigning points to nearest centroid and updating centroids.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/k_means_clust.py
"""

import numpy as np


class KMeans:
    """
    K-Means clustering algorithm.

    >>> np.random.seed(42)
    >>> X = np.vstack([np.random.randn(30, 2) + [5, 5], np.random.randn(30, 2) + [-5, -5]])
    >>> km = KMeans(n_clusters=2, max_iterations=100, seed=42)
    >>> km.fit(X)
    >>> len(set(km.labels)) == 2
    True
    >>> km.centroids.shape
    (2, 2)
    """

    def __init__(
        self,
        n_clusters: int = 3,
        max_iterations: int = 300,
        tolerance: float = 1e-4,
        seed: int | None = None,
    ) -> None:
        self.k = n_clusters
        self.max_iter = max_iterations
        self.tol = tolerance
        self.seed = seed
        self.centroids: np.ndarray | None = None
        self.labels: np.ndarray | None = None
        self.inertia: float = 0.0

    def _init_centroids(self, x: np.ndarray) -> np.ndarray:
        """Initialize centroids using k-means++ method."""
        rng = np.random.RandomState(self.seed)
        n_samples = x.shape[0]
        centroids = [x[rng.randint(n_samples)]]

        for _ in range(1, self.k):
            distances = np.min(
                [np.sum((x - c) ** 2, axis=1) for c in centroids], axis=0
            )
            probs = distances / distances.sum()
            idx = rng.choice(n_samples, p=probs)
            centroids.append(x[idx])

        return np.array(centroids)

    def _assign_clusters(self, x: np.ndarray) -> np.ndarray:
        """Assign each point to nearest centroid."""
        distances = np.array(
            [np.sum((x - c) ** 2, axis=1) for c in self.centroids]
        )
        return np.argmin(distances, axis=0)

    def _update_centroids(self, x: np.ndarray) -> np.ndarray:
        """Recompute centroids as mean of assigned points."""
        new_centroids = np.zeros_like(self.centroids)
        for i in range(self.k):
            mask = self.labels == i
            if np.any(mask):
                new_centroids[i] = x[mask].mean(axis=0)
            else:
                new_centroids[i] = self.centroids[i]
        return new_centroids

    def fit(self, x: np.ndarray) -> None:
        """Run K-Means clustering."""
        self.centroids = self._init_centroids(x)

        for _ in range(self.max_iter):
            self.labels = self._assign_clusters(x)
            new_centroids = self._update_centroids(x)

            shift = np.sum((new_centroids - self.centroids) ** 2)
            self.centroids = new_centroids

            if shift < self.tol:
                break

        self.labels = self._assign_clusters(x)
        self.inertia = sum(
            np.sum((x[self.labels == i] - self.centroids[i]) ** 2)
            for i in range(self.k)
        )

    def predict(self, x: np.ndarray) -> np.ndarray:
        """Predict cluster for new points."""
        return self._assign_clusters(x)


def elbow_method(x: np.ndarray, k_range: range, seed: int = 42) -> list[float]:
    """
    Compute inertia for different k values (for elbow plot).

    >>> np.random.seed(42)
    >>> X = np.random.randn(20, 2)
    >>> inertias = elbow_method(X, range(1, 4))
    >>> len(inertias)
    3
    >>> inertias[0] > inertias[1] > inertias[2]
    True
    """
    inertias = []
    for k in k_range:
        km = KMeans(n_clusters=k, seed=seed)
        km.fit(x)
        inertias.append(km.inertia)
    return inertias


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- K-Means Clustering Demo ---")
    np.random.seed(42)

    # 3 clusters
    c1 = np.random.randn(50, 2) + [0, 0]
    c2 = np.random.randn(50, 2) + [8, 0]
    c3 = np.random.randn(50, 2) + [4, 8]
    X = np.vstack([c1, c2, c3])

    km = KMeans(n_clusters=3, seed=42)
    km.fit(X)

    print(f"Centroids:\n{km.centroids}")
    print(f"Inertia: {km.inertia:.2f}")
    print(f"Cluster sizes: {[int(np.sum(km.labels == i)) for i in range(3)]}")

    # Elbow method
    inertias = elbow_method(X, range(1, 7))
    print(f"\nElbow method inertias:")
    for k, inertia in zip(range(1, 7), inertias):
        print(f"  k={k}: {inertia:.2f}")
