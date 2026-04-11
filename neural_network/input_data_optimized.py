#!/usr/bin/env python3
"""
Optimized and alternative implementations of Input Data utilities.

The reference provides basic normalization, encoding, and splitting.
These variants add robust alternatives and performance optimizations.

Variants covered:
1. normalize_robust   -- uses median/IQR instead of min/max; outlier-resistant
2. one_hot_sparse     -- memory-efficient sparse representation
3. stratified_split   -- maintains class proportions in train/test split

Key interview insight:
    Min-max:     sensitive to outliers, range [0, 1]
    Z-score:     assumes Gaussian, unbounded
    Robust:      median/IQR based, resistant to outliers
    Stratified:  prevents class imbalance in splits

Run:
    python neural_network/input_data_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from neural_network.input_data import (
    normalize as normalize_reference,
    standardize as standardize_reference,
    one_hot_encode as one_hot_reference,
    train_test_split as split_reference,
)


# ---------------------------------------------------------------------------
# Variant 1 -- Robust normalization (median/IQR)
# ---------------------------------------------------------------------------

def normalize_robust(data: np.ndarray) -> np.ndarray:
    """
    Robust normalization using median and interquartile range (IQR).

    Resistant to outliers -- uses Q1/Q3 instead of min/max.

    >>> result = normalize_robust(np.array([1.0, 2.0, 3.0, 4.0, 5.0]))
    >>> abs(np.median(result)) < 1e-10
    True

    >>> normalize_robust(np.array([1.0, 2.0, 3.0, 100.0]))[-1] < 50
    True

    >>> normalize_robust(np.array([5.0, 5.0, 5.0])).tolist()
    [0.0, 0.0, 0.0]
    """
    median = np.median(data)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    if iqr == 0:
        return np.zeros_like(data)
    return (data - median) / iqr


# ---------------------------------------------------------------------------
# Variant 2 -- Memory-efficient one-hot (sparse dict representation)
# ---------------------------------------------------------------------------

def one_hot_sparse(
    labels: np.ndarray, num_classes: int | None = None
) -> list[dict[int, float]]:
    """
    Sparse one-hot encoding: each label becomes {class_idx: 1.0}.

    For datasets with many classes, this uses O(n) memory vs O(n*k) dense.

    >>> one_hot_sparse(np.array([0, 2, 1]))
    [{0: 1.0}, {2: 1.0}, {1: 1.0}]

    >>> one_hot_sparse(np.array([0, 1]), num_classes=10)
    [{0: 1.0}, {1: 1.0}]
    """
    if num_classes is None:
        num_classes = int(np.max(labels)) + 1
    return [{int(label): 1.0} for label in labels]


def sparse_to_dense(sparse: list[dict[int, float]], num_classes: int) -> np.ndarray:
    """
    Convert sparse one-hot back to dense for computation.

    >>> sparse_to_dense([{0: 1.0}, {2: 1.0}], 3).tolist()
    [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    """
    result = np.zeros((len(sparse), num_classes))
    for i, d in enumerate(sparse):
        for k, v in d.items():
            result[i, k] = v
    return result


# ---------------------------------------------------------------------------
# Variant 3 -- Stratified train/test split
# ---------------------------------------------------------------------------

def train_test_split_stratified(
    X: np.ndarray,
    y: np.ndarray,
    test_ratio: float = 0.2,
    seed: int | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split data preserving class proportions in both train and test.

    Critical for imbalanced datasets where random split might
    leave a class entirely in one partition.

    >>> np.random.seed(0)
    >>> X = np.arange(20).reshape(10, 2)
    >>> y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
    >>> X_tr, X_te, y_tr, y_te = train_test_split_stratified(X, y, 0.4, seed=0)
    >>> sum(y_te == 0) == sum(y_te == 1)
    True
    >>> len(X_tr) + len(X_te) == 10
    True
    """
    if seed is not None:
        np.random.seed(seed)

    classes = np.unique(y)
    train_idx = []
    test_idx = []

    for c in classes:
        c_idx = np.where(y == c)[0]
        np.random.shuffle(c_idx)
        n_test = max(1, int(len(c_idx) * test_ratio))
        test_idx.extend(c_idx[:n_test])
        train_idx.extend(c_idx[n_test:])

    train_idx = np.array(train_idx)
    test_idx = np.array(test_idx)
    np.random.shuffle(train_idx)
    np.random.shuffle(test_idx)

    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    """Compare data utility variants."""
    print("=== Input Data Utilities Benchmark ===\n")

    # Normalization comparison
    print("--- Normalization with outliers ---")
    np.random.seed(0)
    normal_data = np.random.randn(1000)
    outlier_data = normal_data.copy()
    outlier_data[0] = 100  # extreme outlier

    print(f"{'Method':<20} {'Mean':>8} {'Std':>8} {'Min':>8} {'Max':>8}")
    print("-" * 50)

    for name, func in [
        ("Min-max", normalize_reference),
        ("Z-score", standardize_reference),
        ("Robust (IQR)", normalize_robust),
    ]:
        result = func(outlier_data)
        print(f"{name:<20} {np.mean(result):>8.4f} {np.std(result):>8.4f} "
              f"{np.min(result):>8.4f} {np.max(result):>8.4f}")

    # One-hot encoding comparison
    print("\n--- One-hot encoding memory ---")
    labels = np.random.randint(0, 100, size=10000)

    t_dense = timeit.timeit(lambda: one_hot_reference(labels, 100), number=100) / 100 * 1000
    t_sparse = timeit.timeit(lambda: one_hot_sparse(labels, 100), number=100) / 100 * 1000

    dense = one_hot_reference(labels, 100)
    sparse = one_hot_sparse(labels, 100)
    print(f"  Dense one-hot:  {t_dense:.3f}ms  memory~{dense.nbytes / 1024:.0f}KB")
    print(f"  Sparse one-hot: {t_sparse:.3f}ms  memory~{sys.getsizeof(sparse) / 1024:.0f}KB")

    # Stratified split comparison
    print("\n--- Stratified vs random split (imbalanced data) ---")
    np.random.seed(42)
    X = np.random.randn(100, 2)
    y = np.array([0] * 90 + [1] * 10)  # 90:10 imbalance

    _, _, _, y_test_rand = split_reference(X, y, 0.2, seed=42)
    _, _, _, y_test_strat = train_test_split_stratified(X, y, 0.2, seed=42)

    print(f"  Random split test:     class 0={sum(y_test_rand==0)}, class 1={sum(y_test_rand==1)}")
    print(f"  Stratified split test: class 0={sum(y_test_strat==0)}, class 1={sum(y_test_strat==1)}")
    print(f"  Stratified preserves the 90:10 ratio in test set")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
