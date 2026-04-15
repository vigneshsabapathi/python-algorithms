"""
BFS - Optimized Variants with Benchmarks.

Variant 1: Standard BFS using collections.deque
Variant 2: Bidirectional BFS (meets in the middle)
Variant 3: Level-by-level BFS (tracks depth)

>>> g = {i: [i+1] for i in range(9)}
>>> g[9] = []
>>> bfs_deque(g, 0, 9) == 9
True
>>> bfs_bidirectional(g, 0, 9) == 9
True
"""

from collections import deque
import time
import random


def bfs_deque(graph, start, goal):
    """Standard BFS returning shortest distance (edges).

    >>> bfs_deque({0: [1], 1: [0]}, 0, 1)
    1
    """
    if start == goal:
        return 0
    visited = {start}
    q = deque([(start, 0)])
    while q:
        node, d = q.popleft()
        for nb in graph.get(node, []):
            if nb == goal:
                return d + 1
            if nb not in visited:
                visited.add(nb)
                q.append((nb, d + 1))
    return -1


def bfs_bidirectional(graph, start, goal):
    """Bidirectional BFS. Needs undirected or reverse graph; here we assume undirected.

    >>> bfs_bidirectional({0: [1], 1: [0, 2], 2: [1]}, 0, 2)
    2
    """
    if start == goal:
        return 0
    front = {start: 0}
    back = {goal: 0}
    fq = deque([start])
    bq = deque([goal])
    while fq and bq:
        if len(fq) <= len(bq):
            node = fq.popleft()
            d = front[node]
            for nb in graph.get(node, []):
                if nb in back:
                    return d + 1 + back[nb]
                if nb not in front:
                    front[nb] = d + 1
                    fq.append(nb)
        else:
            node = bq.popleft()
            d = back[node]
            for nb in graph.get(node, []):
                if nb in front:
                    return d + 1 + front[nb]
                if nb not in back:
                    back[nb] = d + 1
                    bq.append(nb)
    return -1


def bfs_level(graph, start, goal):
    """Level-by-level BFS.

    >>> bfs_level({0: [1, 2], 1: [], 2: [3], 3: []}, 0, 3)
    2
    """
    if start == goal:
        return 0
    visited = {start}
    frontier = [start]
    depth = 0
    while frontier:
        depth += 1
        next_f = []
        for node in frontier:
            for nb in graph.get(node, []):
                if nb == goal:
                    return depth
                if nb not in visited:
                    visited.add(nb)
                    next_f.append(nb)
        frontier = next_f
    return -1


def _random_undirected(n, avg_deg):
    g = {i: set() for i in range(n)}
    edges = n * avg_deg // 2
    random.seed(42)
    for _ in range(edges):
        u = random.randrange(n)
        v = random.randrange(n)
        if u != v:
            g[u].add(v)
            g[v].add(u)
    return {k: list(v) for k, v in g.items()}


def benchmark():
    n = 3000
    g = _random_undirected(n, 6)
    start, goal = 0, n - 1
    variants = [
        ("Deque BFS", bfs_deque),
        ("Bidirectional BFS", bfs_bidirectional),
        ("Level-by-level BFS", bfs_level),
    ]
    print(f"Benchmark: BFS variants on random graph n={n}")
    print("-" * 65)
    for name, fn in variants:
        t0 = time.perf_counter()
        for _ in range(5):
            d = fn(g, start, goal)
        t = (time.perf_counter() - t0) * 1000 / 5
        print(f"{name:<25} dist={d}    time={t:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
