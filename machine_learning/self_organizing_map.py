"""
Self-Organizing Map (SOM / Kohonen Map)

Unsupervised neural network for topology-preserving dimensionality
reduction. Maps high-dimensional data to a 2D grid while preserving
neighborhood relationships.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/self_organizing_map.py
"""

import numpy as np


class SelfOrganizingMap:
    """
    Self-Organizing Map (Kohonen Network).

    >>> np.random.seed(42)
    >>> X = np.random.randn(50, 3)
    >>> som = SelfOrganizingMap(grid_size=(3, 3), n_features=3, seed=42)
    >>> som.fit(X, n_iterations=100)
    >>> som.weights.shape
    (3, 3, 3)
    >>> bmu = som.find_bmu(X[0])
    >>> len(bmu) == 2
    True
    """

    def __init__(
        self,
        grid_size: tuple[int, int] = (10, 10),
        n_features: int = 2,
        learning_rate: float = 0.5,
        sigma: float | None = None,
        seed: int | None = None,
    ) -> None:
        self.grid_size = grid_size
        self.n_features = n_features
        self.initial_lr = learning_rate
        self.initial_sigma = sigma or max(grid_size) / 2.0
        self.seed = seed

        rng = np.random.RandomState(seed)
        self.weights = rng.randn(grid_size[0], grid_size[1], n_features) * 0.1

    def find_bmu(self, x: np.ndarray) -> tuple[int, int]:
        """Find Best Matching Unit (BMU) for input vector x."""
        distances = np.sum((self.weights - x) ** 2, axis=2)
        bmu_idx = np.unravel_index(np.argmin(distances), self.grid_size)
        return (int(bmu_idx[0]), int(bmu_idx[1]))

    def _neighborhood(
        self, bmu: tuple[int, int], sigma: float
    ) -> np.ndarray:
        """Compute Gaussian neighborhood function."""
        rows, cols = self.grid_size
        row_indices, col_indices = np.meshgrid(
            np.arange(rows), np.arange(cols), indexing="ij"
        )
        dist_sq = (row_indices - bmu[0]) ** 2 + (col_indices - bmu[1]) ** 2
        return np.exp(-dist_sq / (2 * sigma**2))

    def fit(
        self, x: np.ndarray, n_iterations: int = 1000
    ) -> None:
        """Train the SOM."""
        rng = np.random.RandomState(self.seed)
        n_samples = x.shape[0]

        for iteration in range(n_iterations):
            # Decay learning rate and neighborhood radius
            t = iteration / n_iterations
            lr = self.initial_lr * np.exp(-t * 3)
            sigma = self.initial_sigma * np.exp(-t * 3)
            sigma = max(sigma, 0.01)

            # Pick random sample
            idx = rng.randint(n_samples)
            sample = x[idx]

            # Find BMU
            bmu = self.find_bmu(sample)

            # Update weights
            h = self._neighborhood(bmu, sigma)
            for i in range(self.grid_size[0]):
                for j in range(self.grid_size[1]):
                    self.weights[i, j] += lr * h[i, j] * (sample - self.weights[i, j])

    def quantization_error(self, x: np.ndarray) -> float:
        """Average distance from each input to its BMU."""
        total = 0.0
        for sample in x:
            bmu = self.find_bmu(sample)
            total += np.linalg.norm(sample - self.weights[bmu[0], bmu[1]])
        return float(total / len(x))

    def map_data(self, x: np.ndarray) -> list[tuple[int, int]]:
        """Map each data point to its BMU coordinates."""
        return [self.find_bmu(sample) for sample in x]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- Self-Organizing Map Demo ---")
    np.random.seed(42)

    # 3 clusters in 4D space
    c1 = np.random.randn(30, 4) + [0, 0, 0, 0]
    c2 = np.random.randn(30, 4) + [5, 5, 5, 5]
    c3 = np.random.randn(30, 4) + [10, 0, 10, 0]
    X = np.vstack([c1, c2, c3])

    som = SelfOrganizingMap(grid_size=(5, 5), n_features=4, seed=42)
    som.fit(X, n_iterations=500)

    print(f"Grid size: {som.grid_size}")
    print(f"Quantization error: {som.quantization_error(X):.4f}")

    # Map data to grid
    mappings = som.map_data(X)
    print(f"\nCluster 1 BMUs: {set(mappings[:30])}")
    print(f"Cluster 2 BMUs: {set(mappings[30:60])}")
    print(f"Cluster 3 BMUs: {set(mappings[60:])}")
