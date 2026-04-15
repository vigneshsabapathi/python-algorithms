"""
BFS class variant - Optimized Variants with Benchmarks.

Variant 1: Class-based BFS with defaultdict
Variant 2: Iterative BFS with set-based visited
Variant 3: BFS returning distance dict

>>> bfs_class_based({0: [1, 2], 1: [2], 2: [0, 3], 3: [3]}, 2)
[2, 0, 3, 1]
"""

from collections import defaultdict, deque
import time
import random


def bfs_class_based(adj, start):
    """Class-like BFS via dict.

    >>> bfs_class_based({0: [1]}, 0)
    [0, 1]
    """
    visited = {start}
    order = []
    q = deque([start])
    while q:
        n = q.popleft()
        order.append(n)
        for nb in adj.get(n, []):
            if nb not in visited:
                visited.add(nb)
                q.append(nb)
    return order


def bfs_set_visited(adj, start):
    """BFS using pre-sized visited array when keys are ints.

    >>> bfs_set_visited({0: [1, 2], 1: [], 2: []}, 0)
    [0, 1, 2]
    """
    visited = set()
    visited.add(start)
    out = []
    q = deque([start])
    while q:
        n = q.popleft()
        out.append(n)
        for nb in adj.get(n, []):
            if nb not in visited:
                visited.add(nb)
                q.append(nb)
    return out


def bfs_distances(adj, start):
    """Return distance from start to every reachable node.

    >>> bfs_distances({0: [1], 1: [2], 2: []}, 0) == {0: 0, 1: 1, 2: 2}
    True
    """
    dist = {start: 0}
    q = deque([start])
    while q:
        n = q.popleft()
        for nb in adj.get(n, []):
            if nb not in dist:
                dist[nb] = dist[n] + 1
                q.append(nb)
    return dist


def _random_adj(n, avg):
    random.seed(1)
    g = defaultdict(list)
    for _ in range(n * avg // 2):
        u, v = random.randrange(n), random.randrange(n)
        if u != v:
            g[u].append(v)
            g[v].append(u)
    return g


def benchmark():
    n = 3000
    g = _random_adj(n, 6)
    variants = [
        ("Class-based BFS", bfs_class_based),
        ("Set-visited BFS", bfs_set_visited),
        ("Distances BFS", bfs_distances),
    ]
    print(f"Benchmark: BFS (variant 2) on n={n}")
    print("-" * 65)
    for name, fn in variants:
        t0 = time.perf_counter()
        for _ in range(10):
            r = fn(g, 0)
        t = (time.perf_counter() - t0) * 1000 / 10
        size = len(r) if isinstance(r, (list, dict)) else 0
        print(f"{name:<22} visited={size}   time={t:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
