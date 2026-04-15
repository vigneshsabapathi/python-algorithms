"""
Lanczos Eigenvectors - Optimized Variants

Approximates largest eigenvalues/eigenvectors of a symmetric graph adjacency matrix
using the Lanczos iteration (converts to tridiagonal form first).

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/lanczos_eigenvectors.py
"""

import time
import numpy as np


# ---------- Variant 1: Sparse matrix multiplication ----------
def lanczos_sparse(graph: list[list[int]], k: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Lanczos with sparse-aware matrix-vector multiplication.

    >>> eigenvalues, eigenvectors = lanczos_sparse([[1, 2], [0, 2], [0, 1]], 2)
    >>> len(eigenvalues) == 2
    True
    """
    n = len(graph)
    Q = np.zeros((n, k))
    T = np.zeros((k, k))

    rng = np.random.default_rng(42)
    q = rng.random(n)
    q /= np.linalg.norm(q)
    Q[:, 0] = q

    beta = 0.0
    for j in range(k):
        # Sparse mat-vec: only sum neighbors
        w = np.zeros(n)
        for i, neighbors in enumerate(graph):
            for nbr in neighbors:
                w[i] += Q[nbr, j]

        if j > 0:
            w -= beta * Q[:, j - 1]
        alpha = np.dot(Q[:, j], w)
        w -= alpha * Q[:, j]

        # Re-orthogonalize (Gram-Schmidt)
        for i in range(j + 1):
            w -= np.dot(Q[:, i], w) * Q[:, i]

        beta = np.linalg.norm(w)
        if j < k - 1 and beta > 1e-10:
            Q[:, j + 1] = w / beta

        T[j, j] = alpha
        if j < k - 1:
            T[j, j + 1] = beta
            T[j + 1, j] = beta

    eigenvalues, eigvecs = np.linalg.eigh(T)
    return eigenvalues[::-1], np.dot(Q, eigvecs[:, ::-1])


# ---------- Variant 2: Power iteration (simpler, single dominant eigenvalue) ----------
def power_iteration(graph: list[list[int]], max_iter: int = 100) -> tuple[float, np.ndarray]:
    """
    Power iteration for the dominant eigenvalue/eigenvector.

    >>> val, vec = power_iteration([[1, 2], [0, 2], [0, 1]], 50)
    >>> abs(val - 2.0) < 0.1
    True
    """
    n = len(graph)
    rng = np.random.default_rng(42)
    v = rng.random(n)
    v /= np.linalg.norm(v)

    for _ in range(max_iter):
        w = np.zeros(n)
        for i, neighbors in enumerate(graph):
            for nbr in neighbors:
                w[i] += v[nbr]
        eigenvalue = np.dot(v, w)
        v = w / np.linalg.norm(w)

    return eigenvalue, v


# ---------- Variant 3: Full NumPy eigensolver (exact, for comparison) ----------
def exact_eigenvectors(graph: list[list[int]], k: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Exact eigenvalues using full adjacency matrix + numpy.

    >>> vals, vecs = exact_eigenvectors([[1, 2], [0, 2], [0, 1]], 2)
    >>> abs(vals[0] - 2.0) < 0.01
    True
    """
    n = len(graph)
    A = np.zeros((n, n))
    for i, neighbors in enumerate(graph):
        for j in neighbors:
            A[i][j] = 1

    eigenvalues, eigenvectors = np.linalg.eigh(A)
    idx = eigenvalues.argsort()[::-1][:k]
    return eigenvalues[idx], eigenvectors[:, idx]


# ---------- Benchmark ----------
def benchmark():
    import random
    random.seed(42)
    n = 200
    graph = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.05:
                graph[i].append(j)
                graph[j].append(i)

    k = 5
    for name, fn in [
        ("lanczos_sparse", lambda: lanczos_sparse(graph, k)),
        ("power_iteration", lambda: power_iteration(graph)),
        ("exact_numpy", lambda: exact_eigenvectors(graph, k)),
    ]:
        start = time.perf_counter()
        for _ in range(10):
            fn()
        elapsed = (time.perf_counter() - start) / 10 * 1000
        print(f"  {name:20s}: {elapsed:.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Lanczos Eigenvectors Benchmark (200 nodes, 10 runs) ===")
    benchmark()
