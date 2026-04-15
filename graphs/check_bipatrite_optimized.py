"""
Check Bipartite - Optimized Variants with Benchmarks.

Variant 1: BFS 2-coloring
Variant 2: DFS 2-coloring (recursive)
Variant 3: Union-Find on edges (merge opposite sides)

>>> bfs_bipartite({0: [1], 1: [0, 2], 2: [1]})
True
>>> dfs_bipartite({0: [1], 1: [0, 2], 2: [1]})
True
>>> uf_bipartite(3, [(0, 1), (1, 2)])
True
>>> uf_bipartite(3, [(0, 1), (1, 2), (0, 2)])
False
"""

from collections import deque
import time
import random


def bfs_bipartite(graph):
    """BFS 2-coloring.

    >>> bfs_bipartite({0: [1], 1: [0]})
    True
    """
    color = {}
    for s in graph:
        if s in color:
            continue
        color[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if v not in color:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return False
    return True


def dfs_bipartite(graph):
    """Iterative DFS 2-coloring.

    >>> dfs_bipartite({0: [1], 1: [0]})
    True
    """
    color = {}
    for s in graph:
        if s in color:
            continue
        stack = [(s, 0)]
        color[s] = 0
        while stack:
            u, c = stack.pop()
            for v in graph[u]:
                if v not in color:
                    color[v] = 1 - c
                    stack.append((v, 1 - c))
                elif color[v] == c:
                    return False
    return True


class _UF:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            self.p[rx] = ry
            return True
        return False


def uf_bipartite(n, edges):
    """Union-Find bipartite check.

    For each edge (u,v) merge u with v+n and v with u+n; if find(u)==find(u+n) then odd cycle.

    >>> uf_bipartite(4, [(0, 1), (1, 2), (2, 3)])
    True
    """
    uf = _UF(2 * n)
    for u, v in edges:
        if uf.find(u) == uf.find(v):
            return False
        uf.union(u, v + n)
        uf.union(v, u + n)
    return True


def _random_bipartite_edges(n):
    random.seed(0)
    half = n // 2
    edges = []
    for _ in range(n * 3):
        u = random.randrange(half)
        v = random.randrange(half, n)
        edges.append((u, v))
    return edges


def _edges_to_adj(n, edges):
    g = {i: [] for i in range(n)}
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)
    return g


def benchmark():
    n = 2000
    edges = _random_bipartite_edges(n)
    adj = _edges_to_adj(n, edges)
    variants = [
        ("BFS 2-color", lambda: bfs_bipartite(adj)),
        ("DFS 2-color", lambda: dfs_bipartite(adj)),
        ("Union-Find", lambda: uf_bipartite(n, edges)),
    ]
    print(f"Benchmark: Bipartite check on n={n}, edges={len(edges)}")
    print("-" * 65)
    for name, fn in variants:
        t0 = time.perf_counter()
        for _ in range(5):
            r = fn()
        t = (time.perf_counter() - t0) * 1000 / 5
        print(f"{name:<18} result={r}   time={t:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
