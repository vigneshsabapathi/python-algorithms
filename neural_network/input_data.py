# https://github.com/TheAlgorithms/Python/blob/master/neural_network/input_data.py

"""
Input Data Utilities for Neural Networks.

Provides common data preprocessing functions used across neural network
implementations: normalization, one-hot encoding, train/test splitting,
and synthetic dataset generation.

These are the building blocks that feed data into any neural network,
implemented from scratch without sklearn or pandas dependencies.
"""

from __future__ import annotations

import numpy as np


def normalize(data: np.ndarray) -> np.ndarray:
    """
    Min-max normalization to [0, 1] range.

    >>> normalize(np.array([0.0, 5.0, 10.0])).tolist()
    [0.0, 0.5, 1.0]
    >>> normalize(np.array([3.0, 3.0, 3.0])).tolist()
    [0.0, 0.0, 0.0]
    >>> normalize(np.array([-10.0, 0.0, 10.0])).tolist()
    [0.0, 0.5, 1.0]
    """
    min_val = np.min(data)
    max_val = np.max(data)
    if max_val - min_val == 0:
        return np.zeros_like(data)
    return (data - min_val) / (max_val - min_val)


def standardize(data: np.ndarray) -> np.ndarray:
    """
    Z-score standardization: (x - mean) / std.

    >>> result = standardize(np.array([1.0, 2.0, 3.0, 4.0, 5.0]))
    >>> abs(np.mean(result)) < 1e-10
    True
    >>> abs(np.std(result) - 1.0) < 1e-10
    True
    >>> standardize(np.array([5.0, 5.0, 5.0])).tolist()
    [0.0, 0.0, 0.0]
    """
    mean = np.mean(data)
    std = np.std(data)
    if std == 0:
        return np.zeros_like(data)
    return (data - mean) / std


def one_hot_encode(labels: np.ndarray, num_classes: int | None = None) -> np.ndarray:
    """
    Convert integer labels to one-hot encoded matrix.

    >>> one_hot_encode(np.array([0, 1, 2])).tolist()
    [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    >>> one_hot_encode(np.array([1, 3]), num_classes=5).shape
    (2, 5)
    >>> one_hot_encode(np.array([0, 0, 1])).tolist()
    [[1.0, 0.0], [1.0, 0.0], [0.0, 1.0]]
    """
    if num_classes is None:
        num_classes = int(np.max(labels)) + 1
    result = np.zeros((len(labels), num_classes))
    result[np.arange(len(labels)), labels.astype(int)] = 1.0
    return result


def train_test_split(
    X: np.ndarray,
    y: np.ndarray,
    test_ratio: float = 0.2,
    seed: int | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split data into training and test sets.

    >>> np.random.seed(42)
    >>> X = np.arange(20).reshape(10, 2)
    >>> y = np.arange(10)
    >>> X_train, X_test, y_train, y_test = train_test_split(X, y, test_ratio=0.3, seed=42)
    >>> len(X_train) + len(X_test) == 10
    True
    >>> len(X_test)
    3
    >>> len(X_train)
    7
    """
    if seed is not None:
        np.random.seed(seed)
    n = len(X)
    indices = np.random.permutation(n)
    test_size = int(n * test_ratio)
    test_idx = indices[:test_size]
    train_idx = indices[test_size:]
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]


def generate_xor_data(n_samples: int = 200, noise: float = 0.1,
                       seed: int | None = None) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate XOR-pattern dataset for binary classification.

    >>> X, y = generate_xor_data(100, seed=0)
    >>> X.shape
    (100, 2)
    >>> y.shape
    (100,)
    >>> set(y.tolist()) == {0, 1}
    True
    """
    if seed is not None:
        np.random.seed(seed)
    X = np.random.randn(n_samples, 2)
    y = ((X[:, 0] > 0) ^ (X[:, 1] > 0)).astype(int)
    X += np.random.randn(n_samples, 2) * noise
    return X, y


def generate_spiral_data(
    n_samples: int = 100, n_classes: int = 3, seed: int | None = None
) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate spiral dataset for multi-class classification.

    Classic neural network benchmark -- linearly inseparable.

    >>> X, y = generate_spiral_data(90, 3, seed=0)
    >>> X.shape
    (270, 2)
    >>> y.shape
    (270,)
    >>> len(set(y.tolist())) == 3
    True
    """
    if seed is not None:
        np.random.seed(seed)
    X = np.zeros((n_samples * n_classes, 2))
    y = np.zeros(n_samples * n_classes, dtype=int)
    for c in range(n_classes):
        ix = range(n_samples * c, n_samples * (c + 1))
        r = np.linspace(0.0, 1, n_samples)
        t = np.linspace(c * 4, (c + 1) * 4, n_samples) + np.random.randn(n_samples) * 0.2
        X[ix] = np.c_[r * np.sin(t), r * np.cos(t)]
        y[ix] = c
    return X, y


def batch_iterator(
    X: np.ndarray, y: np.ndarray, batch_size: int = 32, shuffle: bool = True
) -> list[tuple[np.ndarray, np.ndarray]]:
    """
    Generate mini-batches from data.

    >>> X = np.arange(20).reshape(10, 2)
    >>> y = np.arange(10)
    >>> batches = batch_iterator(X, y, batch_size=3, shuffle=False)
    >>> [len(b[0]) for b in batches]
    [3, 3, 3, 1]
    >>> batches[0][0].tolist()
    [[0, 1], [2, 3], [4, 5]]
    """
    n = len(X)
    if shuffle:
        indices = np.random.permutation(n)
        X, y = X[indices], y[indices]
    batches = []
    for start in range(0, n, batch_size):
        end = min(start + batch_size, n)
        batches.append((X[start:end], y[start:end]))
    return batches


def demo() -> None:
    """Demonstrate all input data utilities."""
    print("=== Input Data Utilities Demo ===\n")

    # Normalization
    data = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
    print(f"Original data:    {data}")
    print(f"Normalized:       {normalize(data)}")
    print(f"Standardized:     {standardize(data).round(4)}")

    # One-hot encoding
    labels = np.array([0, 1, 2, 1, 0])
    print(f"\nLabels:           {labels}")
    print(f"One-hot encoded:\n{one_hot_encode(labels)}")

    # Train/test split
    X = np.arange(20).reshape(10, 2)
    y = np.arange(10)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_ratio=0.3, seed=42)
    print(f"\nTrain/Test split (10 samples, 30% test):")
    print(f"  Train: {len(X_train)} samples, Test: {len(X_test)} samples")

    # XOR data
    X_xor, y_xor = generate_xor_data(200, seed=0)
    print(f"\nXOR dataset: {X_xor.shape[0]} samples, {len(set(y_xor))} classes")
    print(f"  Class distribution: {dict(zip(*np.unique(y_xor, return_counts=True)))}")

    # Spiral data
    X_spiral, y_spiral = generate_spiral_data(100, 3, seed=0)
    print(f"\nSpiral dataset: {X_spiral.shape[0]} samples, {len(set(y_spiral))} classes")
    print(f"  Class distribution: {dict(zip(*np.unique(y_spiral, return_counts=True)))}")

    # Batch iterator
    batches = batch_iterator(X, y, batch_size=3, shuffle=False)
    print(f"\nBatch iterator (10 samples, batch_size=3):")
    print(f"  Number of batches: {len(batches)}")
    print(f"  Batch sizes: {[len(b[0]) for b in batches]}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    demo()
