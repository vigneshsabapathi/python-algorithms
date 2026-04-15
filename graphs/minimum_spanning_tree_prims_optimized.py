"""
Prim's MST (Version 1 - Custom Heap) - Optimized Variants

Prim's algorithm builds MST by greedily adding the cheapest edge from the tree
to a non-tree vertex. This version uses a custom heap implementation.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/minimum_spanning_tree_prims.py
"""

import heapq
import time
from collections import defaultdict


# ---------- Variant 1: heapq-based (stdlib, simpler) ----------
def prims_heapq(adj_list: dict[int, list[list[int]]]) -> list[tuple[int, int]]:
    """
    Prim's using Python's heapq for O((V+E) log V).

    >>> prims_heapq({0: [[1, 1], [3, 3]], 1: [[0, 1], [2, 6], [3, 5], [4, 1]],
    ...              2: [[1, 6], [4, 5], [5, 2]], 3: [[0, 3], [1, 5], [4, 1]],
    ...              4: [[1, 1], [2, 5], [3, 1], [5, 4]], 5: [[2, 2], [4, 4]]})
    [(0, 1), (1, 4), (4, 3), (4, 5), (5, 2)]
    """
    n = len(adj_list)
    visited = [False] * n
    mst = []
    heap = [(0, 0, -1)]  # (weight, vertex, parent)

    while heap and len(mst) < n:
        w, u, parent = heapq.heappop(heap)
        if visited[u]:
            continue
        visited[u] = True
        if parent != -1:
            mst.append((parent, u))
        for neighbor, weight in adj_list[u]:
            if not visited[neighbor]:
                heapq.heappush(heap, (weight, neighbor, u))

    return mst


# ---------- Variant 2: Returns total MST weight ----------
def prims_total_weight(adj_list: dict[int, list[list[int]]]) -> int:
    """
    Prim's returning only the total MST weight.

    >>> prims_total_weight({0: [[1, 1], [3, 3]], 1: [[0, 1], [2, 6], [3, 5], [4, 1]],
    ...                     2: [[1, 6], [4, 5], [5, 2]], 3: [[0, 3], [1, 5], [4, 1]],
    ...                     4: [[1, 1], [2, 5], [3, 1], [5, 4]], 5: [[2, 2], [4, 4]]})
    9
    """
    n = len(adj_list)
    visited = [False] * n
    heap = [(0, 0)]
    total = 0

    while heap:
        w, u = heapq.heappop(heap)
        if visited[u]:
            continue
        visited[u] = True
        total += w
        for neighbor, weight in adj_list[u]:
            if not visited[neighbor]:
                heapq.heappush(heap, (weight, neighbor))

    return total


# ---------- Variant 3: Dense graph O(V^2) without heap ----------
def prims_dense(adj_matrix: list[list[float]]) -> list[tuple[int, int]]:
    """
    O(V^2) Prim's for dense graphs using adjacency matrix (no heap needed).

    >>> INF = float('inf')
    >>> mat = [[0, 1, INF, 3], [1, 0, 6, 5], [INF, 6, 0, 2], [3, 5, 2, 0]]
    >>> prims_dense(mat)
    [(0, 1), (0, 3), (3, 2)]
    """
    n = len(adj_matrix)
    INF = float('inf')
    in_mst = [False] * n
    key = [INF] * n
    parent = [-1] * n
    key[0] = 0
    mst = []

    for _ in range(n):
        # Pick minimum key vertex not in MST
        u = -1
        for v in range(n):
            if not in_mst[v] and (u == -1 or key[v] < key[u]):
                u = v
        in_mst[u] = True
        if parent[u] != -1:
            mst.append((parent[u], u))

        for v in range(n):
            if not in_mst[v] and adj_matrix[u][v] < key[v]:
                key[v] = adj_matrix[u][v]
                parent[v] = u

    return mst


# ---------- Benchmark ----------
def benchmark():
    import random
    random.seed(42)
    n = 500
    adj_list = defaultdict(list)
    for i in range(n - 1):
        w = random.randint(1, 100)
        adj_list[i].append([i + 1, w])
        adj_list[i + 1].append([i, w])
    for _ in range(n):
        u, v = random.randint(0, n - 1), random.randint(0, n - 1)
        if u != v:
            w = random.randint(1, 100)
            adj_list[u].append([v, w])
            adj_list[v].append([u, w])

    for name, fn in [
        ("heapq_based", lambda: prims_heapq(adj_list)),
        ("total_weight", lambda: prims_total_weight(adj_list)),
    ]:
        start = time.perf_counter()
        for _ in range(30):
            fn()
        elapsed = (time.perf_counter() - start) / 30 * 1000
        print(f"  {name:20s}: {elapsed:.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Prim's MST v1 Benchmark (500 nodes, 30 runs) ===")
    benchmark()
