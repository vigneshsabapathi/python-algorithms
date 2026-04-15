"""
Directed/Undirected Weighted Graph - Optimized Variants with Benchmarks.

Variant 1: List-based adjacency (directed)
Variant 2: Dict-of-dict adjacency (undirected)
Variant 3: Edge-list form (best for Kruskal / Bellman-Ford)

>>> sp_list({1: [(2, 3)], 2: []}, 1, 2)
3
>>> sp_dict({1: {2: 3}, 2: {}}, 1, 2)
3
>>> sp_edges([(1, 2, 3)], 3, 1, 2)
3
"""

import heapq
import time
import random


def sp_list(adj, s, t):
    """Dijkstra on list-of-tuples adjacency.

    >>> sp_list({0: [(1, 4)], 1: []}, 0, 1)
    4
    """
    if s == t:
        return 0
    dist = {s: 0}
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == t:
            return d
        if d > dist[u]:
            continue
        for v, w in adj.get(u, []):
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1


def sp_dict(adj, s, t):
    """Dijkstra on dict-of-dict adjacency.

    >>> sp_dict({0: {1: 4}, 1: {}}, 0, 1)
    4
    """
    if s == t:
        return 0
    dist = {s: 0}
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == t:
            return d
        if d > dist[u]:
            continue
        for v, w in adj.get(u, {}).items():
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1


def sp_edges(edges, n, s, t):
    """Bellman-Ford on edge list (handles negative weights too).

    >>> sp_edges([(0, 1, 4)], 2, 0, 1)
    4
    """
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    return dist[t] if dist[t] != INF else -1


def _random_graph(n, avg=4):
    random.seed(0)
    adj_list = {i: [] for i in range(n)}
    adj_dict = {i: {} for i in range(n)}
    edges = []
    for _ in range(n * avg):
        u, v = random.randrange(n), random.randrange(n)
        if u != v:
            w = random.randint(1, 10)
            adj_list[u].append((v, w))
            adj_list[v].append((u, w))
            adj_dict[u][v] = w
            adj_dict[v][u] = w
            edges.append((u, v, w))
            edges.append((v, u, w))
    return adj_list, adj_dict, edges


def benchmark():
    n = 1500
    al, ad, ed = _random_graph(n)
    s, t = 0, n - 1
    variants = [
        ("List adjacency", lambda: sp_list(al, s, t)),
        ("Dict-of-dict", lambda: sp_dict(ad, s, t)),
        ("Edge list (BF)", lambda: sp_edges(ed, n, s, t)),
    ]
    print(f"Benchmark: SP variants on n={n}")
    print("-" * 65)
    for name, fn in variants:
        t0 = time.perf_counter()
        for _ in range(2):
            r = fn()
        dt = (time.perf_counter() - t0) * 1000 / 2
        print(f"{name:<18} dist={r}   time={dt:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
