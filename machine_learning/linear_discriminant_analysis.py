"""
Linear Discriminant Analysis (LDA)

Supervised dimensionality reduction that maximizes class separability.
Projects data onto axes that maximize the ratio of between-class
to within-class scatter.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/linear_discriminant_analysis.py
"""

import numpy as np


class LDA:
    """
    Linear Discriminant Analysis for dimensionality reduction.

    >>> X = np.array([[1, 2], [2, 3], [3, 3], [6, 6], [7, 8], [8, 7]], dtype=float)
    >>> y = np.array([0, 0, 0, 1, 1, 1])
    >>> lda = LDA(n_components=1)
    >>> X_proj = lda.fit_transform(X, y)
    >>> X_proj.shape
    (6, 1)
    """

    def __init__(self, n_components: int = 1) -> None:
        self.n_components = n_components
        self.linear_discriminants: np.ndarray | None = None

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        """Compute LDA projection matrix."""
        n_features = x.shape[1]
        classes = np.unique(y)
        overall_mean = np.mean(x, axis=0)

        # Within-class scatter matrix S_W
        s_w = np.zeros((n_features, n_features))
        # Between-class scatter matrix S_B
        s_b = np.zeros((n_features, n_features))

        for c in classes:
            x_c = x[y == c]
            mean_c = np.mean(x_c, axis=0)
            n_c = x_c.shape[0]

            # S_W += sum of (x - mean_c)(x - mean_c)^T
            diff = x_c - mean_c
            s_w += diff.T @ diff

            # S_B += n_c * (mean_c - overall_mean)(mean_c - overall_mean)^T
            mean_diff = (mean_c - overall_mean).reshape(-1, 1)
            s_b += n_c * (mean_diff @ mean_diff.T)

        # Solve S_W^(-1) S_B
        eigenvalues, eigenvectors = np.linalg.eig(np.linalg.pinv(s_w) @ s_b)

        # Sort by eigenvalue magnitude (descending)
        sorted_idx = np.argsort(np.abs(eigenvalues))[::-1]
        eigenvectors = eigenvectors[:, sorted_idx].real

        self.linear_discriminants = eigenvectors[:, : self.n_components]

    def transform(self, x: np.ndarray) -> np.ndarray:
        """Project data onto discriminant axes."""
        return x @ self.linear_discriminants

    def fit_transform(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Fit and transform in one step."""
        self.fit(x, y)
        return self.transform(x)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- LDA Demo ---")
    np.random.seed(42)

    # 3-class dataset in 4D
    c0 = np.random.randn(40, 4) + [1, 1, 1, 1]
    c1 = np.random.randn(40, 4) + [5, 5, 5, 5]
    c2 = np.random.randn(40, 4) + [9, 1, 9, 1]
    X = np.vstack([c0, c1, c2])
    y = np.array([0] * 40 + [1] * 40 + [2] * 40)

    lda = LDA(n_components=2)
    X_proj = lda.fit_transform(X, y)
    print(f"Original shape: {X.shape}")
    print(f"Projected shape: {X_proj.shape}")
    print(f"Discriminant vectors:\n{lda.linear_discriminants}")

    # Check class separation in projected space
    for c in [0, 1, 2]:
        mean = np.mean(X_proj[y == c], axis=0)
        print(f"Class {c} mean in projected space: {mean}")
