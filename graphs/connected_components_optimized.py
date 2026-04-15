"""
Connected Components - Optimized Variants with Benchmarks.

Variant 1: Iterative DFS
Variant 2: BFS
Variant 3: Union-Find

>>> cc_dfs({0: [1], 1: [0], 2: []})
2
>>> cc_bfs({0: [1], 1: [0], 2: []})
2
>>> cc_uf(3, [(0, 1)])
2
"""

from collections import deque
import time
import random


def cc_dfs(graph):
    """Iterative DFS, returns component count.

    >>> cc_dfs({0: [1], 1: [0]})
    1
    """
    visited = set()
    count = 0
    for s in graph:
        if s in visited:
            continue
        count += 1
        stack = [s]
        visited.add(s)
        while stack:
            n = stack.pop()
            for nb in graph[n]:
                if nb not in visited:
                    visited.add(nb)
                    stack.append(nb)
    return count


def cc_bfs(graph):
    """BFS-based counter.

    >>> cc_bfs({0: [], 1: []})
    2
    """
    visited = set()
    count = 0
    for s in graph:
        if s in visited:
            continue
        count += 1
        q = deque([s])
        visited.add(s)
        while q:
            n = q.popleft()
            for nb in graph[n]:
                if nb not in visited:
                    visited.add(nb)
                    q.append(nb)
    return count


def cc_uf(n, edges):
    """Union-Find counter.

    >>> cc_uf(4, [(0, 1), (2, 3)])
    2
    """
    parent = list(range(n))
    comp = n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            comp -= 1
    return comp


def _random_graph(n, edges):
    random.seed(0)
    adj = {i: [] for i in range(n)}
    es = []
    for _ in range(edges):
        u, v = random.randrange(n), random.randrange(n)
        if u != v:
            adj[u].append(v)
            adj[v].append(u)
            es.append((u, v))
    return adj, es


def benchmark():
    n = 3000
    adj, es = _random_graph(n, 6000)
    variants = [
        ("DFS iterative", lambda: cc_dfs(adj)),
        ("BFS", lambda: cc_bfs(adj)),
        ("Union-Find", lambda: cc_uf(n, es)),
    ]
    print(f"Benchmark: Connected components on n={n}, edges={len(es)}")
    print("-" * 65)
    for name, fn in variants:
        t0 = time.perf_counter()
        for _ in range(5):
            c = fn()
        t = (time.perf_counter() - t0) * 1000 / 5
        print(f"{name:<18} components={c}   time={t:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
