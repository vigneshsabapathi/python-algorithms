#!/usr/bin/env python3
"""
Optimized and alternative implementations of K-Means Clustering.

Three variants:
  numpy_vectorized — vectorized distance computation (reference)
  pure_python      — no NumPy dependency, plain Python lists
  kmeans_plus_plus — improved initialization for better convergence

Run:
    python dynamic_programming/k_means_clustering_tensorflow_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.k_means_clustering_tensorflow import k_means_cluster as reference


# ---------------------------------------------------------------------------
# Variant 1 — numpy_vectorized (same as reference)
# ---------------------------------------------------------------------------

def numpy_vectorized(vectors: np.ndarray, k: int, seed: int = 42) -> tuple:
    """
    >>> np.random.seed(0)
    >>> data = np.array([[1.0, 1], [1, 2], [2, 1], [8, 8], [8, 9], [9, 8]])
    >>> c, a = numpy_vectorized(data, 2, seed=42)
    >>> len(set(a.tolist())) == 2
    True
    """
    return reference(vectors, k, seed=seed)


# ---------------------------------------------------------------------------
# Variant 2 — pure_python: No NumPy dependency
# ---------------------------------------------------------------------------

def pure_python(
    vectors: list[list[float]], k: int, max_iter: int = 100, seed: int = 42
) -> tuple[list[list[float]], list[int]]:
    """
    >>> data = [[1, 1], [1, 2], [2, 1], [8, 8], [8, 9], [9, 8]]
    >>> c, a = pure_python(data, 2, seed=42)
    >>> len(set(a)) == 2
    True
    """
    import random
    rng = random.Random(seed)
    n = len(vectors)
    dim = len(vectors[0])

    indices = rng.sample(range(n), k)
    centroids = [list(vectors[i]) for i in indices]
    assignments = [0] * n

    for _ in range(max_iter):
        new_assignments = []
        for vec in vectors:
            dists = [
                sum((vec[d] - c[d]) ** 2 for d in range(dim))
                for c in centroids
            ]
            new_assignments.append(min(range(k), key=lambda i: dists[i]))

        if new_assignments == assignments:
            break
        assignments = new_assignments

        for c_idx in range(k):
            members = [vectors[i] for i in range(n) if assignments[i] == c_idx]
            if members:
                centroids[c_idx] = [
                    sum(m[d] for m in members) / len(members) for d in range(dim)
                ]

    return centroids, assignments


# ---------------------------------------------------------------------------
# Variant 3 — kmeans_plus_plus: K-Means++ initialization
# ---------------------------------------------------------------------------

def kmeans_plus_plus(
    vectors: np.ndarray, k: int, max_iter: int = 100, seed: int = 42
) -> tuple[np.ndarray, np.ndarray]:
    """
    K-Means with K-Means++ initialization for better centroid seeding.

    >>> np.random.seed(0)
    >>> data = np.array([[1.0, 1], [1, 2], [2, 1], [8, 8], [8, 9], [9, 8]])
    >>> c, a = kmeans_plus_plus(data, 2, seed=42)
    >>> len(set(a.tolist())) == 2
    True
    """
    rng = np.random.default_rng(seed)
    n = len(vectors)

    # K-Means++ initialization
    centroids = [vectors[rng.integers(n)].copy()]
    for _ in range(1, k):
        dists = np.min([
            np.sum((vectors - c) ** 2, axis=1) for c in centroids
        ], axis=0)
        probs = dists / dists.sum()
        idx = rng.choice(n, p=probs)
        centroids.append(vectors[idx].copy())

    centroids_arr = np.array(centroids, dtype=float)
    assignments = np.zeros(n, dtype=int)

    for _ in range(max_iter):
        distances = np.sqrt(
            ((vectors[:, np.newaxis, :] - centroids_arr[np.newaxis, :, :]) ** 2).sum(axis=2)
        )
        new_assignments = distances.argmin(axis=1)
        if np.array_equal(new_assignments, assignments):
            break
        assignments = new_assignments
        for c in range(k):
            mask = assignments == c
            if mask.any():
                centroids_arr[c] = vectors[mask].mean(axis=0)

    return centroids_arr, assignments


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

def run_all() -> None:
    np.random.seed(42)
    c1 = np.random.randn(30, 2) + [3, 3]
    c2 = np.random.randn(30, 2) + [-3, -3]
    c3 = np.random.randn(30, 2) + [3, -3]
    data = np.vstack([c1, c2, c3])

    print("\n=== Correctness ===")
    for name, fn in [("numpy_vectorized", numpy_vectorized), ("kmeans_plus_plus", kmeans_plus_plus)]:
        centroids, assignments = fn(data, 3, seed=0)
        sizes = [int((assignments == i).sum()) for i in range(3)]
        print(f"  {name}: clusters={len(set(assignments.tolist()))}, sizes={sorted(sizes)}")

    centroids_pp, assignments_pp = pure_python(data.tolist(), 3, seed=0)
    sizes = [assignments_pp.count(i) for i in range(3)]
    print(f"  pure_python: clusters={len(set(assignments_pp))}, sizes={sorted(sizes)}")

    REPS = 500
    print(f"\n=== Benchmark (90 points, 3 clusters): {REPS} runs ===")
    for name, fn in [("numpy_vectorized", lambda d: reference(d, 3, seed=0)),
                     ("kmeans_plus_plus", lambda d: kmeans_plus_plus(d, 3, seed=0))]:
        t = timeit.timeit(lambda: fn(data), number=REPS) * 1000 / REPS
        print(f"  {name:<22} {t:>7.2f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
