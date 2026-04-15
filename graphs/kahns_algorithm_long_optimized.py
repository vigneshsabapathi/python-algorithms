"""
Kahn's Algorithm - Longest Distance in DAG - Optimized Variants

Finds the longest path in a DAG using topological ordering (Kahn's algorithm).

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/kahns_algorithm_long.py
"""

import time
from collections import deque


# ---------- Variant 1: Deque-based with explicit distance tracking ----------
def longest_distance_deque(graph: dict[int, list[int]]) -> int:
    """
    Longest path in DAG using deque for BFS.

    >>> longest_distance_deque({0: [2, 3, 4], 1: [2, 7], 2: [5], 3: [5, 7], 4: [7], 5: [6], 6: [7], 7: []})
    5
    """
    n = len(graph)
    indegree = [0] * n
    for neighbors in graph.values():
        for v in neighbors:
            indegree[v] += 1

    queue = deque(i for i in range(n) if indegree[i] == 0)
    dist = [1] * n

    while queue:
        u = queue.popleft()
        for v in graph[u]:
            dist[v] = max(dist[v], dist[u] + 1)
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)

    return max(dist)


# ---------- Variant 2: Returns actual longest path ----------
def longest_path_with_trace(graph: dict[int, list[int]]) -> list[int]:
    """
    Returns the actual longest path (not just length).

    >>> longest_path_with_trace({0: [2, 3, 4], 1: [2, 7], 2: [5], 3: [5, 7], 4: [7], 5: [6], 6: [7], 7: []})
    [0, 3, 5, 6, 7]
    """
    n = len(graph)
    indegree = [0] * n
    for neighbors in graph.values():
        for v in neighbors:
            indegree[v] += 1

    queue = deque(i for i in range(n) if indegree[i] == 0)
    dist = [1] * n
    parent = [-1] * n

    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if dist[u] + 1 > dist[v]:
                dist[v] = dist[u] + 1
                parent[v] = u
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)

    # Reconstruct path from the endpoint with max distance
    end = max(range(n), key=lambda i: dist[i])
    path = []
    while end != -1:
        path.append(end)
        end = parent[end]
    return path[::-1]


# ---------- Variant 3: DFS-based longest path (memoized) ----------
def longest_distance_dfs(graph: dict[int, list[int]]) -> int:
    """
    DFS with memoization for longest path in DAG.

    >>> longest_distance_dfs({0: [2, 3, 4], 1: [2, 7], 2: [5], 3: [5, 7], 4: [7], 5: [6], 6: [7], 7: []})
    5
    """
    n = len(graph)
    memo = [-1] * n

    def dfs(u: int) -> int:
        if memo[u] != -1:
            return memo[u]
        memo[u] = 1
        for v in graph[u]:
            memo[u] = max(memo[u], 1 + dfs(v))
        return memo[u]

    return max(dfs(i) for i in range(n))


# ---------- Benchmark ----------
def benchmark():
    import random
    random.seed(42)
    n = 1000
    graph = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i + 1, min(i + 5, n)):
            if random.random() < 0.5:
                graph[i].append(j)

    for name, fn in [
        ("deque_bfs", lambda: longest_distance_deque(graph)),
        ("path_trace", lambda: len(longest_path_with_trace(graph))),
        ("dfs_memoized", lambda: longest_distance_dfs(graph)),
    ]:
        start = time.perf_counter()
        for _ in range(100):
            result = fn()
        elapsed = (time.perf_counter() - start) / 100 * 1000
        print(f"  {name:20s}: {elapsed:.3f} ms (longest: {result})")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Kahn's Longest Distance Benchmark (1000 nodes, 100 runs) ===")
    benchmark()
