"""
t-Distributed Stochastic Neighbor Embedding (t-SNE)

Non-linear dimensionality reduction technique for visualization.
Converts high-dimensional distances to probabilities and minimizes
KL divergence between high-D and low-D distributions.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/t_stochastic_neighbour_embedding.py
"""

import numpy as np


class TSNE:
    """
    t-SNE for 2D visualization of high-dimensional data.

    >>> np.random.seed(42)
    >>> X = np.random.randn(30, 5)
    >>> tsne = TSNE(n_components=2, perplexity=5.0, n_iterations=100, seed=42)
    >>> Y = tsne.fit_transform(X)
    >>> Y.shape
    (30, 2)
    """

    def __init__(
        self,
        n_components: int = 2,
        perplexity: float = 30.0,
        learning_rate: float = 200.0,
        n_iterations: int = 1000,
        seed: int | None = None,
    ) -> None:
        self.n_components = n_components
        self.perplexity = perplexity
        self.lr = learning_rate
        self.n_iter = n_iterations
        self.seed = seed
        self.embedding: np.ndarray | None = None

    @staticmethod
    def _pairwise_distances(x: np.ndarray) -> np.ndarray:
        """Compute pairwise squared Euclidean distances."""
        sum_sq = np.sum(x**2, axis=1)
        return sum_sq[:, np.newaxis] + sum_sq[np.newaxis, :] - 2 * x @ x.T

    @staticmethod
    def _binary_search_sigma(
        distances_i: np.ndarray, target_perplexity: float, tol: float = 1e-5
    ) -> float:
        """Binary search for sigma that gives target perplexity."""
        sigma_min, sigma_max = 1e-10, 1e4
        sigma = 1.0

        for _ in range(50):
            p = np.exp(-distances_i / (2 * sigma**2))
            p = p / (np.sum(p) + 1e-15)
            p = np.maximum(p, 1e-15)
            entropy = -np.sum(p * np.log2(p))
            perplexity = 2**entropy

            if abs(perplexity - target_perplexity) < tol:
                break
            if perplexity > target_perplexity:
                sigma_max = sigma
            else:
                sigma_min = sigma
            sigma = (sigma_min + sigma_max) / 2

        return sigma

    def _compute_pairwise_affinities(self, x: np.ndarray) -> np.ndarray:
        """Compute symmetric pairwise affinities P."""
        n = x.shape[0]
        distances = self._pairwise_distances(x)
        P = np.zeros((n, n))

        for i in range(n):
            dist_i = distances[i].copy()
            dist_i[i] = np.inf
            sigma = self._binary_search_sigma(dist_i, self.perplexity)
            p_i = np.exp(-dist_i / (2 * sigma**2))
            p_i[i] = 0
            p_i = p_i / (np.sum(p_i) + 1e-15)
            P[i] = p_i

        # Symmetrize
        P = (P + P.T) / (2 * n)
        P = np.maximum(P, 1e-12)
        return P

    @staticmethod
    def _compute_low_dim_affinities(y: np.ndarray) -> np.ndarray:
        """Compute low-dimensional affinities Q using Student-t distribution."""
        n = y.shape[0]
        distances = np.sum((y[:, np.newaxis] - y[np.newaxis, :]) ** 2, axis=2)
        inv_dist = 1.0 / (1.0 + distances)
        np.fill_diagonal(inv_dist, 0)
        Q = inv_dist / (np.sum(inv_dist) + 1e-15)
        Q = np.maximum(Q, 1e-12)
        return Q

    def fit_transform(self, x: np.ndarray) -> np.ndarray:
        """Run t-SNE and return low-dimensional embedding."""
        rng = np.random.RandomState(self.seed)
        n = x.shape[0]

        # Compute high-dimensional affinities
        P = self._compute_pairwise_affinities(x)
        # Early exaggeration
        P *= 4.0

        # Initialize embedding
        Y = rng.randn(n, self.n_components) * 0.01
        velocity = np.zeros_like(Y)
        momentum = 0.5

        for iteration in range(self.n_iter):
            # Remove early exaggeration after 100 iterations
            if iteration == 100:
                P /= 4.0

            if iteration == 250:
                momentum = 0.8

            Q = self._compute_low_dim_affinities(Y)

            # Compute gradients
            PQ_diff = P - Q
            distances = np.sum((Y[:, np.newaxis] - Y[np.newaxis, :]) ** 2, axis=2)
            inv_dist = 1.0 / (1.0 + distances)

            grad = np.zeros_like(Y)
            for i in range(n):
                diff = Y[i] - Y
                grad[i] = 4 * np.sum(
                    (PQ_diff[i] * inv_dist[i])[:, np.newaxis] * diff, axis=0
                )

            # Update with momentum
            velocity = momentum * velocity - self.lr * grad
            Y += velocity

            # Center
            Y -= np.mean(Y, axis=0)

        self.embedding = Y
        return Y

    @staticmethod
    def kl_divergence(P: np.ndarray, Q: np.ndarray) -> float:
        """KL divergence between P and Q distributions."""
        return float(np.sum(P * np.log(P / Q)))


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- t-SNE Demo ---")
    np.random.seed(42)

    # 3 clusters in 10D
    c1 = np.random.randn(20, 10) + 0
    c2 = np.random.randn(20, 10) + 5
    c3 = np.random.randn(20, 10) + 10
    X = np.vstack([c1, c2, c3])
    labels = [0] * 20 + [1] * 20 + [2] * 20

    tsne = TSNE(n_components=2, perplexity=10.0, n_iterations=300, seed=42)
    Y = tsne.fit_transform(X)

    print(f"Input shape: {X.shape}")
    print(f"Output shape: {Y.shape}")
    for c in [0, 1, 2]:
        mask = np.array(labels) == c
        center = np.mean(Y[mask], axis=0)
        print(f"Cluster {c} center: ({center[0]:.2f}, {center[1]:.2f})")
