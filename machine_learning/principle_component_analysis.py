"""
Principal Component Analysis (PCA)

Dimensionality reduction technique that projects data onto the
directions of maximum variance (eigenvectors of covariance matrix).

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/principle_component_analysis.py
"""

import numpy as np


class PCA:
    """
    Principal Component Analysis.

    >>> X = np.array([[2.5, 2.4], [0.5, 0.7], [2.2, 2.9], [1.9, 2.2], [3.1, 3.0]])
    >>> pca = PCA(n_components=1)
    >>> X_reduced = pca.fit_transform(X)
    >>> X_reduced.shape
    (5, 1)
    >>> pca.explained_variance_ratio[0] > 0.9
    True
    """

    def __init__(self, n_components: int = 2) -> None:
        self.n_components = n_components
        self.components: np.ndarray | None = None
        self.mean: np.ndarray | None = None
        self.explained_variance: np.ndarray | None = None
        self.explained_variance_ratio: np.ndarray | None = None

    def fit(self, x: np.ndarray) -> None:
        """Fit PCA: compute eigenvectors of covariance matrix."""
        self.mean = np.mean(x, axis=0)
        x_centered = x - self.mean

        # Covariance matrix
        cov_matrix = np.cov(x_centered, rowvar=False)

        # Eigendecomposition
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

        # Sort by descending eigenvalue
        sorted_idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[sorted_idx]
        eigenvectors = eigenvectors[:, sorted_idx]

        self.components = eigenvectors[:, : self.n_components]
        self.explained_variance = eigenvalues[: self.n_components]
        total_var = np.sum(eigenvalues)
        self.explained_variance_ratio = (
            eigenvalues[: self.n_components] / total_var if total_var > 0 else eigenvalues[: self.n_components]
        )

    def transform(self, x: np.ndarray) -> np.ndarray:
        """Project data onto principal components."""
        x_centered = x - self.mean
        return x_centered @ self.components

    def fit_transform(self, x: np.ndarray) -> np.ndarray:
        """Fit and transform in one step."""
        self.fit(x)
        return self.transform(x)

    def inverse_transform(self, x_reduced: np.ndarray) -> np.ndarray:
        """Reconstruct data from reduced representation."""
        return x_reduced @ self.components.T + self.mean


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- PCA Demo ---")
    np.random.seed(42)

    # Generate correlated 3D data
    n = 100
    X = np.random.randn(n, 3)
    X[:, 1] = X[:, 0] * 2 + np.random.randn(n) * 0.1
    X[:, 2] = X[:, 0] * -1 + np.random.randn(n) * 0.3

    print(f"Original shape: {X.shape}")

    for n_comp in [1, 2, 3]:
        pca = PCA(n_components=n_comp)
        X_reduced = pca.fit_transform(X)
        print(f"\nn_components={n_comp}:")
        print(f"  Reduced shape: {X_reduced.shape}")
        print(f"  Explained variance ratio: {pca.explained_variance_ratio}")
        print(f"  Total explained: {sum(pca.explained_variance_ratio):.4f}")

    # Reconstruction error
    pca = PCA(n_components=2)
    X_reduced = pca.fit_transform(X)
    X_reconstructed = pca.inverse_transform(X_reduced)
    error = np.mean((X - X_reconstructed) ** 2)
    print(f"\nReconstruction error (2 components): {error:.6f}")
