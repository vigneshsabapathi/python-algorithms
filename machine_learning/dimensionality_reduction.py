"""
Dimensionality Reduction Techniques

Collection of methods: PCA, LDA, random projection, and feature selection
for reducing feature space while preserving important information.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/dimensionality_reduction.py
"""

import numpy as np


def pca_reduction(
    x: np.ndarray, n_components: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    PCA dimensionality reduction.

    Returns (projected_data, components, explained_variance_ratio).

    >>> np.random.seed(42)
    >>> X = np.random.randn(10, 3)
    >>> X_reduced, comps, evr = pca_reduction(X, 2)
    >>> X_reduced.shape
    (10, 2)
    >>> len(evr)
    2
    """
    mean = np.mean(x, axis=0)
    x_centered = x - mean

    cov = np.cov(x_centered, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)

    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    components = eigenvectors[:, :n_components]
    projected = x_centered @ components

    total_var = np.sum(eigenvalues)
    evr = eigenvalues[:n_components] / total_var if total_var > 0 else np.zeros(n_components)

    return projected, components, evr


def random_projection(
    x: np.ndarray, n_components: int, seed: int = 42
) -> np.ndarray:
    """
    Random projection (Johnson-Lindenstrauss lemma).
    Projects high-dimensional data to lower dimensions while
    approximately preserving pairwise distances.

    >>> np.random.seed(42)
    >>> X = np.random.randn(20, 50)
    >>> X_proj = random_projection(X, 10)
    >>> X_proj.shape
    (20, 10)
    """
    rng = np.random.RandomState(seed)
    n_features = x.shape[1]
    # Gaussian random projection matrix
    projection_matrix = rng.randn(n_features, n_components) / np.sqrt(n_components)
    return x @ projection_matrix


def variance_threshold_selection(
    x: np.ndarray, threshold: float = 0.0
) -> tuple[np.ndarray, np.ndarray]:
    """
    Remove features with variance below threshold.

    Returns (filtered_data, selected_feature_indices).

    >>> X = np.array([[1, 2, 0], [1, 3, 0], [1, 4, 0]], dtype=float)
    >>> X_filtered, idx = variance_threshold_selection(X, 0.1)
    >>> list(idx)
    [1]
    """
    variances = np.var(x, axis=0)
    selected = np.where(variances > threshold)[0]
    return x[:, selected], selected


def correlation_filter(
    x: np.ndarray, threshold: float = 0.95
) -> tuple[np.ndarray, np.ndarray]:
    """
    Remove highly correlated features (keep one of each pair).

    Returns (filtered_data, selected_feature_indices).

    >>> X = np.array([[1, 2, 1.01], [2, 4, 2.02], [3, 6, 3.03]], dtype=float)
    >>> X_filtered, idx = correlation_filter(X, 0.99)
    >>> len(idx) < 3
    True
    """
    n_features = x.shape[1]
    corr_matrix = np.corrcoef(x, rowvar=False)
    remove = set()

    for i in range(n_features):
        for j in range(i + 1, n_features):
            if abs(corr_matrix[i, j]) > threshold and j not in remove:
                remove.add(j)

    selected = np.array([i for i in range(n_features) if i not in remove])
    return x[:, selected], selected


def truncated_svd(
    x: np.ndarray, n_components: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Truncated SVD for dimensionality reduction.
    Works on non-centered data (unlike PCA).

    Returns (projected_data, components, singular_values).

    >>> np.random.seed(42)
    >>> X = np.random.randn(10, 5)
    >>> X_proj, comps, sv = truncated_svd(X, 2)
    >>> X_proj.shape
    (10, 2)
    """
    u, s, vt = np.linalg.svd(x, full_matrices=False)
    components = vt[:n_components]
    projected = u[:, :n_components] * s[:n_components]
    return projected, components, s[:n_components]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- Dimensionality Reduction Demo ---")
    np.random.seed(42)
    X = np.random.randn(100, 10)

    # PCA
    X_pca, _, evr = pca_reduction(X, 3)
    print(f"PCA: {X.shape} -> {X_pca.shape}, explained variance: {evr}")

    # Random projection
    X_rp = random_projection(X, 3)
    print(f"Random Projection: {X.shape} -> {X_rp.shape}")

    # SVD
    X_svd, _, sv = truncated_svd(X, 3)
    print(f"Truncated SVD: {X.shape} -> {X_svd.shape}, singular values: {sv}")

    # Variance threshold
    X_var = np.column_stack([X, np.zeros((100, 2))])  # add zero-variance cols
    X_filtered, idx = variance_threshold_selection(X_var, 0.01)
    print(f"Variance filter: {X_var.shape} -> {X_filtered.shape}, kept features: {idx}")
