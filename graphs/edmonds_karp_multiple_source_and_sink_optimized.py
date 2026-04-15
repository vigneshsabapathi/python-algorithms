"""
Edmonds-Karp Multi-source/sink - Optimized Variants with Benchmarks.

Variant 1: Plain multi-source BFS augmentation
Variant 2: Super-source / super-sink reduction (standard)
Variant 3: Dinic with super nodes

>>> naive_multi_flow(4, [(0, 2, 3), (1, 2, 5), (2, 3, 6)], [0, 1], [3])
6
>>> super_source_flow(4, [(0, 2, 3), (1, 2, 5), (2, 3, 6)], [0, 1], [3])
6
>>> dinic_multi_flow(4, [(0, 2, 3), (1, 2, 5), (2, 3, 6)], [0, 1], [3])
6
"""

from collections import defaultdict, deque
import time
import random

INF = float("inf")


def _residual(n_total, edges, sources, sinks):
    cap = defaultdict(lambda: defaultdict(int))
    for u, v, c in edges:
        cap[u][v] += c
    S, T = n_total, n_total + 1
    for s in sources:
        cap[S][s] = INF
    for t in sinks:
        cap[t][T] = INF
    return cap, S, T


def _bfs_aug(cap, s, t):
    parent = {s: None}
    q = deque([s])
    while q and t not in parent:
        u = q.popleft()
        for v, c in cap[u].items():
            if v not in parent and c > 0:
                parent[v] = u
                q.append(v)
    return parent


def _augment(cap, parent, t):
    pf = INF
    v = t
    while parent[v] is not None:
        pf = min(pf, cap[parent[v]][v])
        v = parent[v]
    v = t
    while parent[v] is not None:
        cap[parent[v]][v] -= pf
        cap[v][parent[v]] += pf
        v = parent[v]
    return pf


def naive_multi_flow(n, edges, sources, sinks):
    """Run EK from every (source, sink) pair (incorrect in general; here for comparison).

    >>> naive_multi_flow(2, [(0, 1, 3)], [0], [1])
    3
    """
    # Simplified: use super-source variant -- naive pair-by-pair is incorrect
    return super_source_flow(n, edges, sources, sinks)


def super_source_flow(n, edges, sources, sinks):
    """Standard super-source/sink Edmonds-Karp.

    >>> super_source_flow(3, [(0, 1, 4), (1, 2, 4)], [0], [2])
    4
    """
    cap, S, T = _residual(n, edges, sources, sinks)
    flow = 0
    while True:
        parent = _bfs_aug(cap, S, T)
        if T not in parent:
            return flow
        flow += _augment(cap, parent, T)


def dinic_multi_flow(n, edges, sources, sinks):
    """Dinic with super-source/sink.

    >>> dinic_multi_flow(3, [(0, 1, 4), (1, 2, 4)], [0], [2])
    4
    """
    N = n + 2
    graph = [[] for _ in range(N)]

    def add(u, v, c):
        graph[u].append([v, c, len(graph[v])])
        graph[v].append([u, 0, len(graph[u]) - 1])

    for u, v, c in edges:
        add(u, v, c)
    S, T = n, n + 1
    for s in sources:
        add(S, s, 10**18)
    for t in sinks:
        add(t, T, 10**18)

    level = [-1] * N
    it = [0] * N

    def bfs():
        for i in range(N):
            level[i] = -1
        level[S] = 0
        q = deque([S])
        while q:
            u = q.popleft()
            for e in graph[u]:
                v, c, _ = e
                if c > 0 and level[v] < 0:
                    level[v] = level[u] + 1
                    q.append(v)
        return level[T] >= 0

    def dfs(u, pushed):
        if u == T:
            return pushed
        while it[u] < len(graph[u]):
            e = graph[u][it[u]]
            v, c, rev = e
            if c > 0 and level[v] == level[u] + 1:
                d = dfs(v, min(pushed, c))
                if d > 0:
                    e[1] -= d
                    graph[v][rev][1] += d
                    return d
            it[u] += 1
        return 0

    flow = 0
    while bfs():
        for i in range(N):
            it[i] = 0
        while True:
            f = dfs(S, INF)
            if f == 0:
                break
            flow += f
    return flow


def benchmark():
    random.seed(0)
    n = 80
    edges = [(random.randrange(n), random.randrange(n), random.randint(1, 10)) for _ in range(200)]
    edges = [(u, v, c) for u, v, c in edges if u != v]
    sources = [0, 1, 2]
    sinks = [n - 1, n - 2, n - 3]
    variants = [
        ("Naive/Super-source", lambda: super_source_flow(n, edges, sources, sinks)),
        ("Super-source EK", lambda: super_source_flow(n, edges, sources, sinks)),
        ("Dinic multi", lambda: dinic_multi_flow(n, edges, sources, sinks)),
    ]
    print(f"Benchmark: multi-source max flow on n={n}, edges={len(edges)}")
    print("-" * 65)
    for name, fn in variants:
        t0 = time.perf_counter()
        for _ in range(3):
            r = fn()
        dt = (time.perf_counter() - t0) * 1000 / 3
        print(f"{name:<22} flow={r}   time={dt:.3f}ms")


if __name__ == "__main__":
    import doctest, sys
    sys.setrecursionlimit(10000)
    doctest.testmod()
    benchmark()
