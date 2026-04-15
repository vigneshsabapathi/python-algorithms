"""
Cycle Detection - Optimized Variants with Benchmarks.

Variant 1: 3-color DFS (directed)
Variant 2: Kahn's algorithm (directed) - no cycle iff topological sort uses all nodes
Variant 3: Union-Find (undirected)

>>> cycle_dfs({0: [1], 1: [2], 2: [0]})
True
>>> cycle_kahn({0: [1], 1: [2], 2: []})
False
>>> cycle_uf_undirected(3, [(0, 1), (1, 2)])
False
>>> cycle_uf_undirected(3, [(0, 1), (1, 2), (0, 2)])
True
"""

from collections import deque, defaultdict
import time
import random


def cycle_dfs(graph):
    """3-colour DFS for directed graphs.

    >>> cycle_dfs({0: [1], 1: []})
    False
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = defaultdict(int)
    for u, nbrs in graph.items():
        color[u]
        for v in nbrs:
            color[v]

    def dfs(u):
        color[u] = GRAY
        for v in graph.get(u, []):
            if color[v] == GRAY:
                return True
            if color[v] == WHITE and dfs(v):
                return True
        color[u] = BLACK
        return False

    for n in list(color):
        if color[n] == WHITE and dfs(n):
            return True
    return False


def cycle_kahn(graph):
    """Kahn's topological sort. Cycle iff some node never reaches indegree 0.

    >>> cycle_kahn({0: [1], 1: [2]})
    False
    """
    indeg = defaultdict(int)
    nodes = set(graph)
    for u, nbrs in graph.items():
        for v in nbrs:
            indeg[v] += 1
            nodes.add(v)
    q = deque([n for n in nodes if indeg[n] == 0])
    seen = 0
    while q:
        u = q.popleft()
        seen += 1
        for v in graph.get(u, []):
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return seen != len(nodes)


def cycle_uf_undirected(n, edges):
    """Undirected cycle detection via Union-Find.

    >>> cycle_uf_undirected(2, [(0, 1)])
    False
    """
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return True
        parent[ru] = rv
    return False


def _random_dag(n, edges):
    random.seed(0)
    g = defaultdict(list)
    for _ in range(edges):
        u = random.randrange(n)
        v = random.randrange(n)
        if u < v:
            g[u].append(v)
    return g


def benchmark():
    n = 2000
    g = _random_dag(n, 6000)
    edges_undir = [(u, v) for u in g for v in g[u]]
    variants = [
        ("DFS 3-color (directed)", lambda: cycle_dfs(g)),
        ("Kahn (directed)", lambda: cycle_kahn(g)),
        ("Union-Find (undir.)", lambda: cycle_uf_undirected(n, edges_undir)),
    ]
    print(f"Benchmark: Cycle detection on n={n}, edges={len(edges_undir)}")
    print("-" * 65)
    for name, fn in variants:
        t0 = time.perf_counter()
        for _ in range(5):
            r = fn()
        t = (time.perf_counter() - t0) * 1000 / 5
        print(f"{name:<26} cycle={r}   time={t:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
