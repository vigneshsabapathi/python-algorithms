"""
Similarity Search

Functions for computing similarity and distance between vectors:
cosine similarity, Euclidean distance, Jaccard similarity, etc.
Used in recommendation systems, nearest-neighbor search, and clustering.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/similarity_search.py
"""

import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Cosine similarity: cos(theta) = (a . b) / (||a|| * ||b||).
    Range: [-1, 1]. 1 means identical direction.

    >>> cosine_similarity(np.array([1, 0, 0]), np.array([1, 0, 0]))
    1.0
    >>> cosine_similarity(np.array([1, 0]), np.array([0, 1]))
    0.0
    >>> round(cosine_similarity(np.array([1, 1]), np.array([1, 0])), 4)
    0.7071
    """
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    """
    Euclidean (L2) distance between two vectors.

    >>> euclidean_distance(np.array([0, 0]), np.array([3, 4]))
    5.0
    >>> euclidean_distance(np.array([1, 1, 1]), np.array([1, 1, 1]))
    0.0
    """
    return float(np.linalg.norm(a - b))


def manhattan_distance(a: np.ndarray, b: np.ndarray) -> float:
    """
    Manhattan (L1) distance between two vectors.

    >>> manhattan_distance(np.array([0, 0]), np.array([3, 4]))
    7.0
    """
    return float(np.sum(np.abs(a - b)))


def jaccard_similarity(set_a: set, set_b: set) -> float:
    """
    Jaccard similarity: |A intersect B| / |A union B|.

    >>> jaccard_similarity({1, 2, 3}, {2, 3, 4})
    0.5
    >>> jaccard_similarity({1, 2}, {1, 2})
    1.0
    >>> jaccard_similarity({1}, {2})
    0.0
    """
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    if union == 0:
        return 0.0
    return intersection / union


def pearson_correlation(a: np.ndarray, b: np.ndarray) -> float:
    """
    Pearson correlation coefficient between two vectors.

    >>> round(pearson_correlation(np.array([1, 2, 3, 4, 5]), np.array([2, 4, 6, 8, 10])), 4)
    1.0
    >>> round(pearson_correlation(np.array([1, 2, 3]), np.array([3, 2, 1])), 4)
    -1.0
    """
    a_mean = a - np.mean(a)
    b_mean = b - np.mean(b)
    numerator = np.dot(a_mean, b_mean)
    denominator = np.linalg.norm(a_mean) * np.linalg.norm(b_mean)
    if denominator == 0:
        return 0.0
    return float(numerator / denominator)


def hamming_distance(a: np.ndarray, b: np.ndarray) -> int:
    """
    Hamming distance: number of positions where elements differ.

    >>> hamming_distance(np.array([1, 0, 1, 1]), np.array([1, 1, 0, 1]))
    2
    >>> hamming_distance(np.array([1, 1, 1]), np.array([1, 1, 1]))
    0
    """
    return int(np.sum(a != b))


def knn_search(
    query: np.ndarray,
    data: np.ndarray,
    k: int = 5,
    metric: str = "euclidean",
) -> tuple[np.ndarray, np.ndarray]:
    """
    Find k nearest neighbors to query point.

    Returns (indices, distances).

    >>> data = np.array([[0, 0], [1, 1], [2, 2], [10, 10]], dtype=float)
    >>> query = np.array([0.5, 0.5])
    >>> indices, dists = knn_search(query, data, k=2)
    >>> list(indices)
    [0, 1]
    """
    if metric == "cosine":
        # Convert to distances (1 - similarity)
        norms = np.linalg.norm(data, axis=1)
        norms[norms == 0] = 1e-15
        similarities = data @ query / (norms * np.linalg.norm(query))
        distances = 1 - similarities
    elif metric == "manhattan":
        distances = np.sum(np.abs(data - query), axis=1)
    else:  # euclidean
        distances = np.sqrt(np.sum((data - query) ** 2, axis=1))

    indices = np.argsort(distances)[:k]
    return indices, distances[indices]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- Similarity Search Demo ---")
    a = np.array([1.0, 2.0, 3.0, 4.0])
    b = np.array([2.0, 3.0, 4.0, 5.0])

    print(f"Vectors: a={a}, b={b}")
    print(f"Cosine similarity:    {cosine_similarity(a, b):.4f}")
    print(f"Euclidean distance:   {euclidean_distance(a, b):.4f}")
    print(f"Manhattan distance:   {manhattan_distance(a, b):.4f}")
    print(f"Pearson correlation:  {pearson_correlation(a, b):.4f}")

    # KNN search
    np.random.seed(42)
    data = np.random.randn(100, 3)
    query = np.array([0.0, 0.0, 0.0])

    for metric in ["euclidean", "manhattan", "cosine"]:
        idx, dists = knn_search(query, data, k=3, metric=metric)
        print(f"\n{metric} KNN: indices={idx}, distances={np.round(dists, 3)}")
