"""
Markov Chain - Optimized Variants

Simulates random walks on a Markov chain (graph with transition probabilities)
and counts visit frequencies to approximate stationary distribution.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/markov_chain.py
"""

import time
import random
from collections import Counter


# ---------- Variant 1: Matrix-based stationary distribution ----------
def stationary_distribution_matrix(transitions: list[tuple[str, str, float]]) -> dict[str, float]:
    """
    Compute exact stationary distribution by solving pi * P = pi.

    >>> transitions = [('a', 'a', 0.9), ('a', 'b', 0.1), ('b', 'a', 0.5), ('b', 'b', 0.5)]
    >>> dist = stationary_distribution_matrix(transitions)
    >>> dist['a'] > dist['b']
    True
    """
    import numpy as np

    nodes = sorted({t[0] for t in transitions} | {t[1] for t in transitions})
    n = len(nodes)
    idx = {node: i for i, node in enumerate(nodes)}

    P = np.zeros((n, n))
    for src, dst, prob in transitions:
        P[idx[src]][idx[dst]] = prob

    # Solve (P^T - I)pi = 0 with constraint sum(pi) = 1
    A = P.T - np.eye(n)
    A[-1] = np.ones(n)
    b = np.zeros(n)
    b[-1] = 1.0

    pi = np.linalg.solve(A, b)
    return {nodes[i]: round(float(pi[i]), 6) for i in range(n)}


# ---------- Variant 2: Optimized random walk with bisect ----------
def markov_walk_bisect(
    start: str, transitions: list[tuple[str, str, float]], steps: int
) -> dict[str, int]:
    """
    Random walk using bisect for O(log k) transition selection.

    >>> random.seed(42)
    >>> t = [('a', 'a', 0.9), ('a', 'b', 0.075), ('a', 'c', 0.025),
    ...      ('b', 'a', 0.15), ('b', 'b', 0.8), ('b', 'c', 0.05),
    ...      ('c', 'a', 0.25), ('c', 'b', 0.25), ('c', 'c', 0.5)]
    >>> result = markov_walk_bisect('a', t, 5000)
    >>> result['a'] > result['b'] > result['c']
    True
    """
    from bisect import bisect_left

    # Build cumulative distribution per state
    trans = {}
    for src, dst, prob in transitions:
        if src not in trans:
            trans[src] = ([], [])
        cum = trans[src][1][-1] + prob if trans[src][1] else prob
        trans[src][0].append(dst)
        trans[src][1].append(cum)

    visited = Counter()
    node = start
    for _ in range(steps):
        dsts, cdf = trans[node]
        r = random.random()
        idx = bisect_left(cdf, r)
        node = dsts[min(idx, len(dsts) - 1)]
        visited[node] += 1

    return dict(visited)


# ---------- Variant 3: NumPy matrix power for distribution ----------
def markov_power(transitions: list[tuple[str, str, float]], steps: int) -> dict[str, float]:
    """
    Compute distribution after k steps using matrix exponentiation.

    >>> t = [('a', 'a', 0.9), ('a', 'b', 0.1), ('b', 'a', 0.5), ('b', 'b', 0.5)]
    >>> dist = markov_power(t, 100)
    >>> dist['a'] > dist['b']
    True
    """
    import numpy as np

    nodes = sorted({t[0] for t in transitions} | {t[1] for t in transitions})
    n = len(nodes)
    idx = {node: i for i, node in enumerate(nodes)}

    P = np.zeros((n, n))
    for src, dst, prob in transitions:
        P[idx[src]][idx[dst]] = prob

    # Start with uniform distribution
    state = np.ones(n) / n
    Pk = np.linalg.matrix_power(P, steps)
    result = state @ Pk
    return {nodes[i]: round(float(result[i]), 6) for i in range(n)}


# ---------- Benchmark ----------
def benchmark():
    transitions = [
        ('a', 'a', 0.9), ('a', 'b', 0.075), ('a', 'c', 0.025),
        ('b', 'a', 0.15), ('b', 'b', 0.8), ('b', 'c', 0.05),
        ('c', 'a', 0.25), ('c', 'b', 0.25), ('c', 'c', 0.5),
    ]

    for name, fn in [
        ("matrix_stationary", lambda: stationary_distribution_matrix(transitions)),
        ("walk_bisect_5k", lambda: markov_walk_bisect('a', transitions, 5000)),
        ("matrix_power_100", lambda: markov_power(transitions, 100)),
    ]:
        start = time.perf_counter()
        for _ in range(200):
            fn()
        elapsed = (time.perf_counter() - start) / 200 * 1000
        print(f"  {name:25s}: {elapsed:.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Markov Chain Benchmark (200 runs) ===")
    benchmark()
