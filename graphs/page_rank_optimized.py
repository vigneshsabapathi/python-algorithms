"""
PageRank Algorithm - Optimized Variants

Computes the importance of web pages based on link structure.
Each page's rank is distributed equally among its outbound links.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/page_rank.py
"""

import time


# ---------- Variant 1: NumPy matrix-based PageRank ----------
def page_rank_numpy(adj_matrix: list[list[int]], d: float = 0.85, iterations: int = 100) -> dict[int, float]:
    """
    PageRank using NumPy matrix operations.

    >>> ranks = page_rank_numpy([[0, 1, 1], [0, 0, 1], [1, 0, 0]])
    >>> ranks[0] > 0.3
    True
    """
    import numpy as np
    n = len(adj_matrix)
    M = np.array(adj_matrix, dtype=float)

    # Normalize columns (each column sums to 1)
    col_sums = M.sum(axis=0)
    col_sums[col_sums == 0] = 1  # handle dangling nodes
    M = M / col_sums

    rank = np.ones(n) / n
    for _ in range(iterations):
        rank = (1 - d) / n + d * M @ rank

    return {i: round(float(rank[i]), 6) for i in range(n)}


# ---------- Variant 2: Pure Python iterative ----------
def page_rank_iterative(
    graph: dict[str, list[str]], d: float = 0.85, iterations: int = 100
) -> dict[str, float]:
    """
    Pure Python PageRank with adjacency list input.

    >>> ranks = page_rank_iterative({'A': ['B', 'C'], 'B': ['C'], 'C': ['A']})
    >>> ranks['A'] > ranks['B']
    True
    """
    nodes = list(graph.keys())
    n = len(nodes)
    ranks = {node: 1.0 / n for node in nodes}
    out_degree = {node: len(graph[node]) for node in nodes}

    for _ in range(iterations):
        new_ranks = {}
        for node in nodes:
            rank_sum = sum(
                ranks[src] / out_degree[src]
                for src in nodes
                if node in graph[src]
            )
            new_ranks[node] = (1 - d) / n + d * rank_sum
        ranks = new_ranks

    return {k: round(v, 6) for k, v in ranks.items()}


# ---------- Variant 3: Convergence-based (stops when stable) ----------
def page_rank_converge(
    graph: dict[str, list[str]], d: float = 0.85, tol: float = 1e-6, max_iter: int = 1000
) -> dict[str, float]:
    """
    PageRank with convergence check (stops early when ranks stabilize).

    >>> ranks = page_rank_converge({'A': ['B', 'C'], 'B': ['C'], 'C': ['A']})
    >>> ranks['A'] > ranks['B']
    True
    """
    nodes = list(graph.keys())
    n = len(nodes)
    ranks = {node: 1.0 / n for node in nodes}
    out_degree = {node: max(len(graph[node]), 1) for node in nodes}

    # Build reverse graph for efficiency
    reverse = {node: [] for node in nodes}
    for src in nodes:
        for dst in graph[src]:
            if dst in reverse:
                reverse[dst].append(src)

    for _ in range(max_iter):
        new_ranks = {}
        for node in nodes:
            rank_sum = sum(ranks[src] / out_degree[src] for src in reverse[node])
            new_ranks[node] = (1 - d) / n + d * rank_sum

        diff = sum(abs(new_ranks[node] - ranks[node]) for node in nodes)
        ranks = new_ranks
        if diff < tol:
            break

    return {k: round(v, 6) for k, v in ranks.items()}


# ---------- Benchmark ----------
def benchmark():
    import random
    random.seed(42)
    n = 100
    nodes = [str(i) for i in range(n)]
    graph = {node: [] for node in nodes}
    for node in nodes:
        targets = random.sample(nodes, random.randint(1, 5))
        graph[node] = [t for t in targets if t != node]

    for name, fn in [
        ("iterative_100", lambda: page_rank_iterative(graph, iterations=100)),
        ("convergence", lambda: page_rank_converge(graph)),
    ]:
        start = time.perf_counter()
        for _ in range(5):
            fn()
        elapsed = (time.perf_counter() - start) / 5 * 1000
        print(f"  {name:20s}: {elapsed:.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== PageRank Benchmark (100 nodes, 5 runs) ===")
    benchmark()
