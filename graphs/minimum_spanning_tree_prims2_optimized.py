"""
Prim's MST (Version 2 - Priority Queue) - Optimized Variants

Full OOP Prim's with custom MinPriorityQueue using decrease-key operation.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/minimum_spanning_tree_prims2.py
"""

import heapq
import time


# ---------- Variant 1: Simplified heapq with lazy deletion ----------
def prims_lazy_heap(connections: dict[str, dict[str, int]]) -> tuple[dict[str, int], dict[str, str | None]]:
    """
    Prim's with lazy deletion heap (simpler than decrease-key).

    >>> conns = {'a': {'b': 3, 'c': 15}, 'b': {'a': 3, 'c': 10, 'd': 100}, 'c': {'a': 15, 'b': 10, 'd': 5}, 'd': {'b': 100, 'c': 5}}
    >>> dist, parent = prims_lazy_heap(conns)
    >>> dist['d']
    5
    """
    dist = {node: float('inf') for node in connections}
    parent = {node: None for node in connections}
    visited = set()

    start = next(iter(connections))
    dist[start] = 0
    heap = [(0, start)]

    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        for v, w in connections[u].items():
            if v not in visited and w < dist[v]:
                dist[v] = w
                parent[v] = u
                heapq.heappush(heap, (w, v))

    return dist, parent


# ---------- Variant 2: Returns edge list of MST ----------
def prims_edge_list(connections: dict[str, dict[str, int]]) -> list[tuple[str, str, int]]:
    """
    Returns MST as list of (u, v, weight) tuples.

    >>> edges = prims_edge_list({'a': {'b': 3, 'c': 15}, 'b': {'a': 3, 'c': 10, 'd': 100}, 'c': {'a': 15, 'b': 10, 'd': 5}, 'd': {'b': 100, 'c': 5}})
    >>> sum(w for _, _, w in edges)
    18
    """
    dist, parent = prims_lazy_heap(connections)
    edges = []
    for node, p in parent.items():
        if p is not None:
            edges.append((p, node, dist[node]))
    return edges


# ---------- Variant 3: Dense graph variant with matrix input ----------
def prims_matrix(matrix: list[list[float]]) -> list[tuple[int, int, float]]:
    """
    Prim's for adjacency matrix input. O(V^2) suitable for dense graphs.

    >>> INF = float('inf')
    >>> prims_matrix([[0, 3, INF], [3, 0, 10], [INF, 10, 0]])
    [(0, 1, 3), (1, 2, 10)]
    """
    n = len(matrix)
    INF = float('inf')
    in_mst = [False] * n
    key = [INF] * n
    parent = [-1] * n
    key[0] = 0
    edges = []

    for _ in range(n):
        u = min((k for k in range(n) if not in_mst[k]), key=lambda x: key[x])
        in_mst[u] = True
        if parent[u] != -1:
            edges.append((parent[u], u, key[u]))

        for v in range(n):
            if not in_mst[v] and matrix[u][v] != INF and matrix[u][v] < key[v]:
                key[v] = matrix[u][v]
                parent[v] = u

    return edges


# ---------- Benchmark ----------
def benchmark():
    import random
    random.seed(42)
    n = 300
    conns = {}
    for i in range(n):
        conns[str(i)] = {}
    for i in range(n - 1):
        w = random.randint(1, 100)
        conns[str(i)][str(i + 1)] = w
        conns[str(i + 1)][str(i)] = w
    for _ in range(n):
        u, v = str(random.randint(0, n - 1)), str(random.randint(0, n - 1))
        if u != v:
            w = random.randint(1, 100)
            conns[u][v] = w
            conns[v][u] = w

    for name, fn in [
        ("lazy_heap", lambda: prims_lazy_heap(conns)),
        ("edge_list", lambda: prims_edge_list(conns)),
    ]:
        start = time.perf_counter()
        for _ in range(30):
            fn()
        elapsed = (time.perf_counter() - start) / 30 * 1000
        print(f"  {name:20s}: {elapsed:.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Prim's MST v2 Benchmark (300 nodes, 30 runs) ===")
    benchmark()
