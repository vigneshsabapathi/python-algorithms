"""
Topological Sort using DFS - Optimized Variants

Topological sorting orders vertices in a DAG so that for every directed edge u->v,
u comes before v. Uses DFS-based approach (clothing dependency example).

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/g_topological_sort.py
"""

import time
from collections import deque


# ---------- Variant 1: Iterative DFS with explicit stack ----------
def topological_sort_iterative(graph: list[list[int]]) -> list[int]:
    """
    Iterative DFS topological sort using explicit stack.

    >>> topological_sort_iterative([[1, 4], [2, 4], [3], [], [], [4], [2, 7], [3], []])
    [8, 6, 7, 5, 0, 1, 4, 2, 3]
    """
    n = len(graph)
    visited = [False] * n
    result = []

    for start in range(n):
        if visited[start]:
            continue
        stack = [(start, False)]
        while stack:
            node, processed = stack[-1]
            if processed:
                stack.pop()
                if node not in result:
                    result.append(node)
                continue
            if visited[node]:
                stack.pop()
                continue
            visited[node] = True
            stack[-1] = (node, True)
            for neighbor in reversed(graph[node]):
                if not visited[neighbor]:
                    stack.append((neighbor, False))

    result.reverse()
    return result


# ---------- Variant 2: Kahn's BFS-based (in-degree) ----------
def topological_sort_bfs(graph: list[list[int]]) -> list[int]:
    """
    BFS-based topological sort (Kahn's algorithm).

    >>> topological_sort_bfs([[1, 4], [2, 4], [3], [], [], [4], [2, 7], [3], []])
    [0, 5, 6, 8, 1, 7, 2, 4, 3]
    """
    n = len(graph)
    in_degree = [0] * n
    for neighbors in graph:
        for v in neighbors:
            in_degree[v] += 1

    queue = deque(i for i in range(n) if in_degree[i] == 0)
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for v in graph[node]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    return result if len(result) == n else []


# ---------- Variant 3: Recursive DFS (original style, cleaned up) ----------
def topological_sort_recursive(graph: list[list[int]]) -> list[int]:
    """
    Recursive DFS topological sort.

    >>> result = topological_sort_recursive([[1, 4], [2, 4], [3], [], [], [4], [2, 7], [3], []])
    >>> len(result) == 9
    True
    """
    n = len(graph)
    visited = [False] * n
    stack = []

    def dfs(u: int) -> None:
        visited[u] = True
        for v in graph[u]:
            if not visited[v]:
                dfs(v)
        stack.append(u)

    for v in range(n):
        if not visited[v]:
            dfs(v)

    stack.reverse()
    return stack


# ---------- Benchmark ----------
def benchmark():
    import random
    random.seed(42)
    n = 1000
    graph = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, min(i + 5, n)):
            if random.random() < 0.6:
                graph[i].append(j)

    for name, fn in [
        ("iterative_dfs", topological_sort_iterative),
        ("bfs_kahns", topological_sort_bfs),
        ("recursive_dfs", topological_sort_recursive),
    ]:
        start = time.perf_counter()
        for _ in range(100):
            fn(graph)
        elapsed = (time.perf_counter() - start) / 100 * 1000
        result = fn(graph)
        print(f"  {name:20s}: {elapsed:.3f} ms (first 5: {result[:5]})")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Topological Sort Benchmark (1000 nodes, 100 runs) ===")
    benchmark()
