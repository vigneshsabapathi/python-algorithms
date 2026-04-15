"""
Finding Bridges in an Undirected Graph - Optimized Variants

A bridge is an edge whose removal disconnects the graph (increases connected components).
Uses Tarjan's bridge-finding algorithm based on DFS discovery times and low-link values.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/finding_bridges.py
"""

import time
from collections import defaultdict


# ---------- Variant 1: Iterative DFS (stack-based, avoids recursion limit) ----------
def compute_bridges_iterative(graph: dict[int, list[int]]) -> list[tuple[int, int]]:
    """
    Find bridges using iterative DFS to avoid recursion depth issues.

    >>> compute_bridges_iterative({0: [1, 2], 1: [0, 2], 2: [0, 1, 3, 5], 3: [2, 4], 4: [3], 5: [2, 6, 8], 6: [5, 7], 7: [6, 8], 8: [5, 7]})
    [(3, 4), (2, 3), (2, 5)]
    >>> compute_bridges_iterative({0: [1, 3], 1: [0, 2, 4], 2: [1, 3, 4], 3: [0, 2, 4], 4: [1, 2, 3]})
    []
    >>> compute_bridges_iterative({})
    []
    """
    n = len(graph)
    if n == 0:
        return []

    disc = [-1] * n
    low = [-1] * n
    parent = [-1] * n
    bridges = []
    timer = 0

    for start in range(n):
        if disc[start] != -1:
            continue
        stack = [(start, 0)]  # (node, neighbor_index)
        disc[start] = low[start] = timer
        timer += 1

        while stack:
            u, idx = stack[-1]
            if idx < len(graph[u]):
                stack[-1] = (u, idx + 1)
                v = graph[u][idx]
                if disc[v] == -1:
                    parent[v] = u
                    disc[v] = low[v] = timer
                    timer += 1
                    stack.append((v, 0))
                elif v != parent[u]:
                    low[u] = min(low[u], disc[v])
            else:
                stack.pop()
                if stack:
                    p = stack[-1][0]
                    low[p] = min(low[p], low[u])
                    if low[u] > disc[p]:
                        bridges.append((min(p, u), max(p, u)))

    return bridges


# ---------- Variant 2: Edge-list input format ----------
def compute_bridges_from_edges(
    n: int, edges: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    """
    Find bridges given vertex count and edge list.

    >>> compute_bridges_from_edges(3, [(0, 1), (1, 2), (0, 2)])
    []
    >>> compute_bridges_from_edges(4, [(0, 1), (1, 2), (2, 3)])
    [(2, 3), (1, 2), (0, 1)]
    """
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # Pad missing vertices
    full_graph = {i: graph.get(i, []) for i in range(n)}
    return compute_bridges_iterative(full_graph)


# ---------- Variant 3: Recursive with early termination counting ----------
def compute_bridges_recursive(graph: dict[int, list[int]]) -> list[tuple[int, int]]:
    """
    Classic recursive Tarjan bridge-finding (original algorithm, cleaned up).

    >>> compute_bridges_recursive({0: [1, 2], 1: [0, 2], 2: [0, 1, 3, 5], 3: [2, 4], 4: [3], 5: [2, 6, 8], 6: [5, 7], 7: [6, 8], 8: [5, 7]})
    [(3, 4), (2, 3), (2, 5)]
    >>> compute_bridges_recursive({})
    []
    """
    n = len(graph)
    if n == 0:
        return []

    disc = [0] * n
    low = [0] * n
    visited = [False] * n
    bridges = []
    timer = [0]

    def dfs(u: int, parent: int) -> None:
        visited[u] = True
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        for v in graph[u]:
            if not visited[v]:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append((min(u, v), max(u, v)))
            elif v != parent:
                low[u] = min(low[u], disc[v])

    for i in range(n):
        if not visited[i]:
            dfs(i, -1)
    return bridges


# ---------- Benchmark ----------
def benchmark():
    import random

    random.seed(42)
    n = 500
    graph = {i: [] for i in range(n)}
    for i in range(n - 1):
        graph[i].append(i + 1)
        graph[i + 1].append(i)
    # Add some extra edges to create cycles
    for _ in range(200):
        u, v = random.randint(0, n - 1), random.randint(0, n - 1)
        if u != v and v not in graph[u]:
            graph[u].append(v)
            graph[v].append(u)

    results = {}
    for name, fn in [
        ("iterative", compute_bridges_iterative),
        ("recursive", compute_bridges_recursive),
    ]:
        start = time.perf_counter()
        for _ in range(50):
            fn(graph)
        elapsed = (time.perf_counter() - start) / 50 * 1000
        results[name] = elapsed
        print(f"  {name:20s}: {elapsed:.3f} ms (found {len(fn(graph))} bridges)")

    edges = []
    for u in graph:
        for v in graph[u]:
            if u < v:
                edges.append((u, v))
    start = time.perf_counter()
    for _ in range(50):
        compute_bridges_from_edges(n, edges)
    elapsed = (time.perf_counter() - start) / 50 * 1000
    print(f"  {'from_edges':20s}: {elapsed:.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Finding Bridges Benchmark (500 nodes, 50 runs) ===")
    benchmark()
