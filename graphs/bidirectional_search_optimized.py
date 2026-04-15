"""
Bidirectional Search - Optimized Variants with Benchmarks.

Variant 1: Standard bidirectional BFS
Variant 2: Frontier-set bidirectional (set operations)
Variant 3: Memory-optimized (bit vector visited)

>>> graph = {1: [2,3], 2: [1,4], 3: [1,4], 4: [2,3,5], 5: [4]}
>>> bidir_bfs(graph, 1, 5)
3
>>> bidir_frontier_set(graph, 1, 5)
3
>>> bidir_bitvec(graph, 1, 5)
3
"""

import time
from collections import deque


def bidir_bfs(graph, source, target):
    """Standard bidirectional BFS.

    >>> bidir_bfs({1:[2],2:[1,3],3:[2]}, 1, 3)
    2
    """
    if source == target: return 0
    visited_f, visited_b = {source}, {target}
    front_f, front_b = [source], [target]
    dist = 0
    while front_f and front_b:
        dist += 1
        nxt = []
        for u in front_f:
            for v in graph.get(u, []):
                if v in visited_b: return dist
                if v not in visited_f:
                    visited_f.add(v); nxt.append(v)
        front_f = nxt
        if not front_f: break
        dist += 1
        nxt = []
        for u in front_b:
            for v in graph.get(u, []):
                if v in visited_f: return dist
                if v not in visited_b:
                    visited_b.add(v); nxt.append(v)
        front_b = nxt
    return -1


def bidir_frontier_set(graph, source, target):
    """Frontier-set approach using set intersection.

    >>> bidir_frontier_set({1:[2],2:[1,3],3:[2]}, 1, 3)
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


def bidir_bitvec(graph, source, target):
    """Memory-optimized using array-based visited (for integer nodes).

    >>> bidir_bitvec({1:[2],2:[1,3],3:[2]}, 1, 3)
    2
    """
    if source == target: return 0
    max_node = max(max(graph.keys()), max(v for adj in graph.values() for v in adj)) + 1
    visited_f = [False] * max_node
    visited_b = [False] * max_node
    visited_f[source] = True
    visited_b[target] = True
    front_f, front_b = [source], [target]
    dist = 0
    while front_f and front_b:
        dist += 1
        if len(front_f) <= len(front_b):
            nxt = []
            for u in front_f:
                for v in graph.get(u, []):
                    if visited_b[v]: return dist
                    if not visited_f[v]:
                        visited_f[v] = True; nxt.append(v)
            front_f = nxt
        else:
            nxt = []
            for u in front_b:
                for v in graph.get(u, []):
                    if visited_f[v]: return dist
                    if not visited_b[v]:
                        visited_b[v] = True; nxt.append(v)
            front_b = nxt
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
        if u != v: graph[u].append(v); graph[v].append(u)

    variants = [
        ("Standard BiDir", lambda: bidir_bfs(graph, 0, n-1)),
        ("Frontier Set", lambda: bidir_frontier_set(graph, 0, n-1)),
        ("Bit Vector", lambda: bidir_bitvec(graph, 0, n-1)),
    ]
    print(f"\nBenchmark: Bidirectional Search on {n}-node graph")
    print("-" * 50)
    for name, func in variants:
        t0 = time.perf_counter()
        for _ in range(20):
            result = func()
        elapsed = (time.perf_counter() - t0) / 20
        print(f"{name:<20} dist={result:<5} time={elapsed*1000:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
