"""
Bidirectional BFS - Optimized Variants with Benchmarks.

Variant 1: Standard bidirectional BFS (level-by-level)
Variant 2: Bidirectional BFS with smaller-frontier expansion
Variant 3: Single-source BFS (baseline comparison)

>>> graph = {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2, 4], 4: [3]}
>>> bfs_bidir_standard(graph, 0, 4)
3
>>> bfs_bidir_smaller(graph, 0, 4)
3
>>> bfs_single(graph, 0, 4)
3
"""

import time
from collections import deque


def bfs_bidir_standard(graph, source, target):
    """Standard bidirectional BFS.

    >>> bfs_bidir_standard({0:[1],1:[0,2],2:[1]}, 0, 2)
    2
    """
    if source == target: return 0
    visited_f, visited_b = {source}, {target}
    queue_f, queue_b = deque([source]), deque([target])
    dist = 0
    while queue_f or queue_b:
        dist += 1
        if queue_f:
            nxt = deque()
            while queue_f:
                u = queue_f.popleft()
                for v in graph.get(u, []):
                    if v in visited_b: return dist
                    if v not in visited_f:
                        visited_f.add(v); nxt.append(v)
            queue_f = nxt
        dist += 1
        if queue_b:
            nxt = deque()
            while queue_b:
                u = queue_b.popleft()
                for v in graph.get(u, []):
                    if v in visited_f: return dist
                    if v not in visited_b:
                        visited_b.add(v); nxt.append(v)
            queue_b = nxt
    return -1


def bfs_bidir_smaller(graph, source, target):
    """Expand smaller frontier first for optimal performance.

    >>> bfs_bidir_smaller({0:[1],1:[0,2],2:[1]}, 0, 2)
    2
    """
    if source == target: return 0
    visited_f, visited_b = {source}, {target}
    front_f, front_b = {source}, {target}
    dist = 0
    while front_f and front_b:
        dist += 1
        if len(front_f) <= len(front_b):
            nxt = set()
            for u in front_f:
                for v in graph.get(u, []):
                    if v in visited_b: return dist
                    if v not in visited_f:
                        visited_f.add(v); nxt.add(v)
            front_f = nxt
        else:
            nxt = set()
            for u in front_b:
                for v in graph.get(u, []):
                    if v in visited_f: return dist
                    if v not in visited_b:
                        visited_b.add(v); nxt.add(v)
            front_b = nxt
    return -1


def bfs_single(graph, source, target):
    """Single-source BFS for comparison.

    >>> bfs_single({0:[1],1:[0,2],2:[1]}, 0, 2)
    2
    """
    if source == target: return 0
    visited = {source}
    queue = deque([(source, 0)])
    while queue:
        u, d = queue.popleft()
        for v in graph.get(u, []):
            if v == target: return d + 1
            if v not in visited:
                visited.add(v); queue.append((v, d + 1))
    return -1


def benchmark():
    import random
    random.seed(42)
    n = 10000
    graph = {i: [] for i in range(n)}
    for i in range(1, n):
        j = random.randint(0, i-1)
        graph[i].append(j); graph[j].append(i)
    for _ in range(n*2):
        u, v = random.randint(0, n-1), random.randint(0, n-1)
        if u != v:
            graph[u].append(v); graph[v].append(u)

    variants = [
        ("BiDir BFS (standard)", lambda: bfs_bidir_standard(graph, 0, n-1)),
        ("BiDir BFS (smaller)", lambda: bfs_bidir_smaller(graph, 0, n-1)),
        ("Single BFS", lambda: bfs_single(graph, 0, n-1)),
    ]
    print(f"\nBenchmark: BFS variants on {n}-node graph")
    print("-" * 50)
    for name, func in variants:
        t0 = time.perf_counter()
        for _ in range(20):
            result = func()
        elapsed = (time.perf_counter() - t0) / 20
        print(f"{name:<25} dist={result:<5} time={elapsed*1000:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
