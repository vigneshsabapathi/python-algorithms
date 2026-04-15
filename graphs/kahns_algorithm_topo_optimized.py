"""
Kahn's Algorithm - Topological Sort - Optimized Variants

BFS-based topological sort using in-degree counting. Also detects cycles.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/kahns_algorithm_topo.py
"""

import time
from collections import deque


# ---------- Variant 1: Deque-based (proper BFS) ----------
def topological_sort_deque(graph: dict[int, list[int]]) -> list[int] | None:
    """
    Kahn's with deque for O(1) popleft.

    >>> topological_sort_deque({0: [1, 2], 1: [3], 2: [3], 3: [4, 5], 4: [], 5: []})
    [0, 1, 2, 3, 4, 5]
    >>> topological_sort_deque({0: [1], 1: [2], 2: [0]}) is None
    True
    """
    n = len(graph)
    indegree = [0] * n
    for neighbors in graph.values():
        for v in neighbors:
            indegree[v] += 1

    queue = deque(i for i in range(n) if indegree[i] == 0)
    result = []

    while queue:
        u = queue.popleft()
        result.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)

    return result if len(result) == n else None


# ---------- Variant 2: All topological orderings ----------
def all_topological_sorts(graph: dict[int, list[int]]) -> list[list[int]]:
    """
    Find all possible topological orderings (useful for small graphs).

    >>> all_topological_sorts({0: [1], 1: [2], 2: []})
    [[0, 1, 2]]
    >>> len(all_topological_sorts({0: [2], 1: [2], 2: []}))
    2
    """
    n = len(graph)
    indegree = [0] * n
    for neighbors in graph.values():
        for v in neighbors:
            indegree[v] += 1

    results = []

    def backtrack(order, visited):
        if len(order) == n:
            results.append(order[:])
            return
        for v in range(n):
            if not visited[v] and indegree[v] == 0:
                visited[v] = True
                order.append(v)
                for u in graph[v]:
                    indegree[u] -= 1
                backtrack(order, visited)
                order.pop()
                visited[v] = False
                for u in graph[v]:
                    indegree[u] += 1

    backtrack([], [False] * n)
    return results


# ---------- Variant 3: Lexicographically smallest ordering ----------
def topological_sort_lexical(graph: dict[int, list[int]]) -> list[int] | None:
    """
    Returns the lexicographically smallest topological ordering using min-heap.

    >>> topological_sort_lexical({0: [1, 2], 1: [3], 2: [3], 3: [4, 5], 4: [], 5: []})
    [0, 1, 2, 3, 4, 5]
    """
    import heapq
    n = len(graph)
    indegree = [0] * n
    for neighbors in graph.values():
        for v in neighbors:
            indegree[v] += 1

    heap = [i for i in range(n) if indegree[i] == 0]
    heapq.heapify(heap)
    result = []

    while heap:
        u = heapq.heappop(heap)
        result.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                heapq.heappush(heap, v)

    return result if len(result) == n else None


# ---------- Benchmark ----------
def benchmark():
    import random
    random.seed(42)
    n = 2000
    graph = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i + 1, min(i + 4, n)):
            if random.random() < 0.5:
                graph[i].append(j)

    for name, fn in [
        ("deque_bfs", topological_sort_deque),
        ("lexical_heap", topological_sort_lexical),
    ]:
        start = time.perf_counter()
        for _ in range(50):
            fn(graph)
        elapsed = (time.perf_counter() - start) / 50 * 1000
        print(f"  {name:20s}: {elapsed:.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Kahn's Topo Sort Benchmark (2000 nodes, 50 runs) ===")
    benchmark()
