"""
Basic Graph Operations - Optimized Variants with Benchmarks.

Variant 1: defaultdict adjacency list (standard)
Variant 2: Array-based adjacency list (cache-friendly)
Variant 3: Compressed sparse row (CSR) representation

>>> g1 = graph_dict_bfs({0: [1,2], 1: [0,3], 2: [0,3], 3: [1,2]}, 0)
>>> g1
[0, 1, 2, 3]
>>> g2 = graph_array_bfs(4, [(0,1),(0,2),(1,3),(2,3)], 0)
>>> g2
[0, 1, 2, 3]
>>> g3 = csr_bfs(4, [(0,1),(0,2),(1,3),(2,3)], 0)
>>> g3
[0, 1, 2, 3]
"""

import time
from collections import deque


# --- Variant 1: Dict-based adjacency list BFS ---
def graph_dict_bfs(graph: dict[int, list[int]], start: int) -> list[int]:
    """
    BFS using dict-based adjacency list.

    >>> graph_dict_bfs({0: [1], 1: [0, 2], 2: [1]}, 0)
    [0, 1, 2]
    """
    visited = {start}
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in sorted(graph.get(node, [])):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order


# --- Variant 2: Array-based adjacency list BFS ---
def graph_array_bfs(
    n: int, edges: list[tuple[int, int]], start: int
) -> list[int]:
    """
    BFS using array-based adjacency list (faster for dense integer nodes).

    >>> graph_array_bfs(3, [(0,1),(1,2)], 0)
    [0, 1, 2]
    """
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    for i in range(n):
        adj[i].sort()

    visited = [False] * n
    visited[start] = True
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in adj[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)
    return order


# --- Variant 3: CSR (Compressed Sparse Row) BFS ---
def csr_bfs(
    n: int, edges: list[tuple[int, int]], start: int
) -> list[int]:
    """
    BFS using CSR format -- most cache-friendly for large sparse graphs.

    >>> csr_bfs(3, [(0,1),(1,2)], 0)
    [0, 1, 2]
    """
    # Build CSR
    from collections import defaultdict

    adj: dict[int, list[int]] = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    for i in range(n):
        adj[i].sort()

    offsets = [0] * (n + 1)
    neighbors = []
    for i in range(n):
        offsets[i + 1] = offsets[i] + len(adj[i])
        neighbors.extend(adj[i])

    visited = [False] * n
    visited[start] = True
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for idx in range(offsets[node], offsets[node + 1]):
            neighbor = neighbors[idx]
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)
    return order


def benchmark() -> None:
    """Benchmark graph representations."""
    import random
    random.seed(42)
    n = 5000
    edges = set()
    # Ensure connected
    for i in range(1, n):
        j = random.randint(0, i - 1)
        edges.add((min(i, j), max(i, j)))
    # Add random edges
    for _ in range(n * 2):
        u, v = random.randint(0, n - 1), random.randint(0, n - 1)
        if u != v:
            edges.add((min(u, v), max(u, v)))
    edge_list = list(edges)

    # Build dict graph
    graph_dict: dict[int, list[int]] = {}
    for i in range(n):
        graph_dict[i] = []
    for u, v in edge_list:
        graph_dict[u].append(v)
        graph_dict[v].append(u)
    for i in range(n):
        graph_dict[i].sort()

    variants = [
        ("Dict adjacency BFS", lambda: graph_dict_bfs(graph_dict, 0)),
        ("Array adjacency BFS", lambda: graph_array_bfs(n, edge_list, 0)),
        ("CSR BFS", lambda: csr_bfs(n, edge_list, 0)),
    ]

    print(f"\nBenchmark: BFS on {n}-node, {len(edge_list)}-edge graph")
    print("-" * 55)
    for name, func in variants:
        t0 = time.perf_counter()
        for _ in range(5):
            result = func()
        elapsed = (time.perf_counter() - t0) / 5
        print(f"{name:<25} visited={len(result):<6} time={elapsed*1000:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
