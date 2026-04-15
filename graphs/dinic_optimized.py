"""
Dinic's Max Flow - Optimized Variants with Benchmarks.

Variant 1: Dinic (recursive DFS)
Variant 2: Ford-Fulkerson with BFS (Edmonds-Karp)
Variant 3: Ford-Fulkerson with DFS (baseline)

>>> dinic_flow(2, [(0, 1, 5)], 0, 1)
5
>>> ek_flow(2, [(0, 1, 5)], 0, 1)
5
>>> ff_dfs_flow(2, [(0, 1, 5)], 0, 1)
5
"""

from collections import deque, defaultdict
import time
import random


def _build(n, edges):
    cap = [defaultdict(int) for _ in range(n)]
    for u, v, c in edges:
        cap[u][v] += c
    return cap


def dinic_flow(n, edges, s, t):
    """Dinic's algorithm.

    >>> dinic_flow(3, [(0, 1, 2), (1, 2, 2)], 0, 2)
    2
    """
    graph = [[] for _ in range(n)]

    def add(u, v, c):
        graph[u].append([v, c, len(graph[v])])
        graph[v].append([u, 0, len(graph[u]) - 1])

    for u, v, c in edges:
        add(u, v, c)

    INF = float("inf")
    flow = 0
    level = [-1] * n
    itr = [0] * n

    def bfs():
        for i in range(n):
            level[i] = -1
        level[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for e in graph[u]:
                v, c, _ = e
                if c > 0 and level[v] < 0:
                    level[v] = level[u] + 1
                    q.append(v)
        return level[t] >= 0

    def dfs(u, pushed):
        if u == t:
            return pushed
        while itr[u] < len(graph[u]):
            e = graph[u][itr[u]]
            v, c, rev = e
            if c > 0 and level[v] == level[u] + 1:
                d = dfs(v, min(pushed, c))
                if d > 0:
                    e[1] -= d
                    graph[v][rev][1] += d
                    return d
            itr[u] += 1
        return 0

    while bfs():
        for i in range(n):
            itr[i] = 0
        while True:
            f = dfs(s, INF)
            if f == 0:
                break
            flow += f
    return flow


def ek_flow(n, edges, s, t):
    """Edmonds-Karp (BFS augmenting path).

    >>> ek_flow(3, [(0, 1, 2), (1, 2, 2)], 0, 2)
    2
    """
    cap = _build(n, edges)
    # Ensure reverse edges exist
    for u in range(n):
        for v in list(cap[u]):
            if u not in cap[v]:
                cap[v][u] = 0
    flow = 0
    while True:
        parent = {s: None}
        q = deque([s])
        while q and t not in parent:
            u = q.popleft()
            for v, c in cap[u].items():
                if v not in parent and c > 0:
                    parent[v] = u
                    q.append(v)
        if t not in parent:
            return flow
        path_flow = float("inf")
        v = t
        while parent[v] is not None:
            path_flow = min(path_flow, cap[parent[v]][v])
            v = parent[v]
        v = t
        while parent[v] is not None:
            cap[parent[v]][v] -= path_flow
            cap[v][parent[v]] += path_flow
            v = parent[v]
        flow += path_flow


def ff_dfs_flow(n, edges, s, t):
    """Ford-Fulkerson with DFS augmenting path.

    >>> ff_dfs_flow(3, [(0, 1, 2), (1, 2, 2)], 0, 2)
    2
    """
    cap = _build(n, edges)
    for u in range(n):
        for v in list(cap[u]):
            if u not in cap[v]:
                cap[v][u] = 0
    flow = 0
    while True:
        parent = {s: None}
        stack = [s]
        while stack and t not in parent:
            u = stack.pop()
            for v, c in cap[u].items():
                if v not in parent and c > 0:
                    parent[v] = u
                    stack.append(v)
        if t not in parent:
            return flow
        pf = float("inf")
        v = t
        while parent[v] is not None:
            pf = min(pf, cap[parent[v]][v])
            v = parent[v]
        v = t
        while parent[v] is not None:
            cap[parent[v]][v] -= pf
            cap[v][parent[v]] += pf
            v = parent[v]
        flow += pf


def benchmark():
    random.seed(0)
    n = 80
    edges = []
    for _ in range(300):
        u, v = random.randrange(n), random.randrange(n)
        if u != v:
            edges.append((u, v, random.randint(1, 10)))
    s, t = 0, n - 1
    variants = [
        ("Dinic", lambda: dinic_flow(n, edges, s, t)),
        ("Edmonds-Karp", lambda: ek_flow(n, edges, s, t)),
        ("Ford-Fulkerson DFS", lambda: ff_dfs_flow(n, edges, s, t)),
    ]
    print(f"Benchmark: Max flow on n={n}, edges={len(edges)}")
    print("-" * 65)
    for name, fn in variants:
        t0 = time.perf_counter()
        for _ in range(3):
            f = fn()
        dt = (time.perf_counter() - t0) * 1000 / 3
        print(f"{name:<22} flow={f}   time={dt:.3f}ms")


if __name__ == "__main__":
    import doctest, sys
    sys.setrecursionlimit(10000)
    doctest.testmod()
    benchmark()
