"""
K-Means Clustering — Pure NumPy implementation.

K-Means is an unsupervised learning algorithm that partitions n observations
into k clusters, where each observation belongs to the cluster with the
nearest centroid (mean).

Algorithm (Lloyd's):
  1. Initialize k centroids randomly from the data points
  2. Assign each point to the nearest centroid (Expectation step)
  3. Recompute centroids as the mean of assigned points (Maximization step)
  4. Repeat until convergence or max iterations

Note: The original TheAlgorithms version used TensorFlow. This is a pure
NumPy implementation that achieves the same result without the heavy dependency.

>>> import numpy as np
>>> np.random.seed(42)
>>> data = np.vstack([np.random.randn(20, 2) + [2, 2], np.random.randn(20, 2) + [-2, -2]])
>>> centroids, assignments = k_means_cluster(data, 2, max_iterations=50)
>>> len(set(assignments)) == 2
True
>>> centroids.shape
(2, 2)
"""

from __future__ import annotations

import numpy as np


def k_means_cluster(
    vectors: np.ndarray,
    num_clusters: int,
    max_iterations: int = 100,
    seed: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    K-Means clustering using pure NumPy.

    Parameters
    ----------
    vectors : np.ndarray
        n x k array where n is number of points, k is dimensionality
    num_clusters : int
        Number of clusters
    max_iterations : int
        Maximum EM iterations
    seed : int or None
        Random seed for reproducibility

    Returns
    -------
    centroids : np.ndarray
        num_clusters x k array of final centroid positions
    assignments : np.ndarray
        Length-n array of cluster assignments (0 to num_clusters-1)

    >>> import numpy as np
    >>> np.random.seed(0)
    >>> data = np.array([[1, 1], [1, 2], [2, 1], [8, 8], [8, 9], [9, 8]])
    >>> centroids, assignments = k_means_cluster(data, 2, seed=42)
    >>> sorted(set(assignments.tolist()))
    [0, 1]
    """
    num_clusters = int(num_clusters)
    assert num_clusters < len(vectors), "num_clusters must be less than number of points"

    rng = np.random.default_rng(seed)

    # Initialize centroids by randomly selecting from data points
    indices = rng.choice(len(vectors), size=num_clusters, replace=False)
    centroids = vectors[indices].copy().astype(float)

    assignments = np.zeros(len(vectors), dtype=int)

    for _ in range(max_iterations):
        # Expectation step: assign each point to nearest centroid
        # Compute distances: (n, 1, k) - (1, c, k) -> (n, c, k) -> sum -> (n, c)
        distances = np.sqrt(
            ((vectors[:, np.newaxis, :] - centroids[np.newaxis, :, :]) ** 2).sum(axis=2)
        )
        new_assignments = distances.argmin(axis=1)

        # Check for convergence
        if np.array_equal(new_assignments, assignments):
            break
        assignments = new_assignments

        # Maximization step: recompute centroids
        for c in range(num_clusters):
            mask = assignments == c
            if mask.any():
                centroids[c] = vectors[mask].mean(axis=0)

    return centroids, assignments


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    # Demo with synthetic 2D data
    np.random.seed(42)
    cluster1 = np.random.randn(30, 2) + [3, 3]
    cluster2 = np.random.randn(30, 2) + [-3, -3]
    cluster3 = np.random.randn(30, 2) + [3, -3]
    data = np.vstack([cluster1, cluster2, cluster3])

    centroids, assignments = k_means_cluster(data, 3, seed=0)
    print(f"  Data shape: {data.shape}")
    print(f"  Centroids:\n{centroids}")
    print(f"  Cluster sizes: {[int((assignments == i).sum()) for i in range(3)]}")
    print(f"  Converged with {len(set(assignments))} clusters")
