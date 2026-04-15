"""
Random Graph Generator - Optimized Variants

Generates random graphs with given vertex count and edge probability.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/random_graph_generator.py
"""

import random
import time


# ---------- Variant 1: NumPy-accelerated generation ----------
def random_graph_numpy(n: int, p: float, directed: bool = False) -> dict[int, list[int]]:
    """
    Generate random graph using NumPy for fast random number generation.

    >>> random.seed(1)
    >>> g = random_graph_numpy(4, 1.0)
    >>> all(len(g[i]) > 0 for i in range(4))
    True
    """
    import numpy as np
    rng = np.random.default_rng(random.randint(0, 2**31))

    if p >= 1:
        return {i: [j for j in range(n) if j != i] for i in range(n)}
    if p <= 0:
        return {i: [] for i in range(n)}

    graph = {i: [] for i in range(n)}
    rand_matrix = rng.random((n, n))

    for i in range(n):
        for j in range(i + 1, n):
            if rand_matrix[i][j] < p:
                graph[i].append(j)
                if not directed:
                    graph[j].append(i)
                elif rand_matrix[j][i] < p:
                    graph[j].append(i)

    return graph


# ---------- Variant 2: Erdos-Renyi G(n, m) model ----------
def random_graph_edges(n: int, m: int, directed: bool = False) -> dict[int, list[int]]:
    """
    Erdos-Renyi G(n,m) model: exactly m edges chosen uniformly at random.

    >>> random.seed(42)
    >>> g = random_graph_edges(5, 4)
    >>> sum(len(v) for v in g.values()) // 2 == 4 or sum(len(v) for v in g.values()) <= 8
    True
    """
    graph = {i: [] for i in range(n)}
    possible_edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    if m > len(possible_edges):
        m = len(possible_edges)

    chosen = random.sample(possible_edges, m)
    for u, v in chosen:
        graph[u].append(v)
        if not directed:
            graph[v].append(u)

    return graph


# ---------- Variant 3: Scale-free graph (Barabasi-Albert) ----------
def barabasi_albert(n: int, m: int = 2) -> dict[int, list[int]]:
    """
    Generate a scale-free graph using preferential attachment.
    Each new node connects to m existing nodes proportional to their degree.

    >>> random.seed(42)
    >>> g = barabasi_albert(10, 2)
    >>> len(g) == 10
    True
    >>> all(len(g[i]) >= 1 for i in range(2, 10))
    True
    """
    graph = {i: [] for i in range(n)}
    # Start with a complete graph on m+1 nodes
    for i in range(m + 1):
        for j in range(i + 1, m + 1):
            graph[i].append(j)
            graph[j].append(i)

    # Degree list for preferential attachment
    degree_list = []
    for i in range(m + 1):
        degree_list.extend([i] * len(graph[i]))

    for new_node in range(m + 1, n):
        targets = set()
        while len(targets) < m:
            target = random.choice(degree_list)
            if target != new_node:
                targets.add(target)

        for target in targets:
            graph[new_node].append(target)
            graph[target].append(new_node)
            degree_list.extend([new_node, target])

    return graph


# ---------- Benchmark ----------
def benchmark():
    for name, fn in [
        ("erdos_renyi_prob", lambda: random_graph_numpy(500, 0.05)),
        ("erdos_renyi_edges", lambda: random_graph_edges(500, 2500)),
        ("barabasi_albert", lambda: barabasi_albert(500, 3)),
    ]:
        random.seed(42)
        start = time.perf_counter()
        for _ in range(20):
            g = fn()
        elapsed = (time.perf_counter() - start) / 20 * 1000
        edge_count = sum(len(v) for v in g.values()) // 2
        print(f"  {name:25s}: {elapsed:.3f} ms ({edge_count} edges)")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Random Graph Generator Benchmark (500 nodes, 20 runs) ===")
    benchmark()
