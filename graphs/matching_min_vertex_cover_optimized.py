"""
Matching-Based Minimum Vertex Cover - Optimized Variants

2-approximation algorithm using maximal matching: pick both endpoints of
arbitrary edges until all edges are covered.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/matching_min_vertex_cover.py
"""

import time
import random


# ---------- Variant 1: Frozen-set edges for O(1) discard ----------
def matching_cover_frozenset(graph: dict[int, list[int]]) -> set[int]:
    """
    Uses frozensets for edges to avoid directional duplicates.

    >>> cover = matching_cover_frozenset({0: [1, 3], 1: [0, 3], 2: [0, 3, 4], 3: [0, 1, 2], 4: [2, 3]})
    >>> len(cover) >= 4
    True
    """
    edges = set()
    for u, neighbors in graph.items():
        for v in neighbors:
            edges.add(frozenset((u, v)))

    cover = set()
    while edges:
        edge = edges.pop()
        u, v = tuple(edge)
        cover.add(u)
        cover.add(v)
        edges = {e for e in edges if u not in e and v not in e}

    return cover


# ---------- Variant 2: Adjacency-set based (no explicit edge list) ----------
def matching_cover_adj_set(graph: dict[int, list[int]]) -> set[int]:
    """
    Matching using adjacency sets directly (no separate edge set).

    >>> cover = matching_cover_adj_set({0: [1, 3], 1: [0, 3], 2: [0, 3, 4], 3: [0, 1, 2], 4: [2, 3]})
    >>> len(cover) >= 4
    True
    """
    adj = {v: set(neighbors) for v, neighbors in graph.items()}
    cover = set()

    for u in list(adj):
        if adj[u]:
            v = next(iter(adj[u]))
            cover.add(u)
            cover.add(v)
            for w in list(adj[u]):
                adj[w].discard(u)
            for w in list(adj[v]):
                adj[w].discard(v)
            adj[u] = set()
            adj[v] = set()

    return cover


# ---------- Variant 3: Randomized matching (shuffle edge order) ----------
def matching_cover_random(graph: dict[int, list[int]]) -> set[int]:
    """
    Randomized matching order for potentially different covers.

    >>> cover = matching_cover_random({0: [1, 2], 1: [0, 2], 2: [0, 1]})
    >>> len(cover) >= 2
    True
    """
    edges = []
    seen = set()
    for u, neighbors in graph.items():
        for v in neighbors:
            key = (min(u, v), max(u, v))
            if key not in seen:
                seen.add(key)
                edges.append(key)

    random.shuffle(edges)
    covered_vertices = set()
    cover = set()

    for u, v in edges:
        if u not in covered_vertices and v not in covered_vertices:
            cover.add(u)
            cover.add(v)
            covered_vertices.add(u)
            covered_vertices.add(v)

    return cover


# ---------- Benchmark ----------
def benchmark():
    random.seed(42)
    n = 500
    graph = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.02:
                graph[i].append(j)
                graph[j].append(i)

    for name, fn in [
        ("frozenset_edges", matching_cover_frozenset),
        ("adj_set", matching_cover_adj_set),
        ("randomized", matching_cover_random),
    ]:
        start = time.perf_counter()
        for _ in range(20):
            result = fn(graph)
        elapsed = (time.perf_counter() - start) / 20 * 1000
        print(f"  {name:20s}: {elapsed:.3f} ms (cover size: {len(result)})")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Matching Vertex Cover Benchmark (500 nodes, 20 runs) ===")
    benchmark()
