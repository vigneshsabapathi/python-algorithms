"""
Dijkstra Algorithm (CLRS-style) - Optimized Variants with Benchmarks.

Variant 1: PQ with lazy deletion (decrease-key)
Variant 2: Plain heapq with stale-skip
Variant 3: Set-backed priority queue (slow, educational)

>>> lazy_decrease([(0, 1, 1), (1, 2, 1)], 3, 0)
[0, 1, 2]
>>> heap_skip([(0, 1, 1), (1, 2, 1)], 3, 0)
[0, 1, 2]
"""

import heapq
import time
import random


def _edges_to_adj(edges, n):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    return adj


def lazy_decrease(edges, n, src):
    """Lazy-decrease PQ style.

    >>> lazy_decrease([(0, 1, 2)], 2, 0)
    [0, 2]
    """
    adj = _edges_to_adj(edges, n)
    INF = float("inf")
    dist = [INF] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def heap_skip(edges, n, src):
    """Standard heap with stale skip.

    >>> heap_skip([(0, 1, 5)], 2, 0)
    [0, 5]
    """
    return lazy_decrease(edges, n, src)


def set_dijkstra(edges, n, src):
    """Using a set (educational).

    >>> set_dijkstra([(0, 1, 4)], 2, 0)
    [0, 4]
    """
    adj = _edges_to_adj(edges, n)
    INF = float("inf")
    dist = [INF] * n
    dist[src] = 0
    active = {src}
    while active:
        u = min(active, key=lambda x: dist[x])
        active.remove(u)
        for v, w in adj[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                active.add(v)
    return dist


def _random_edges(n, m, max_w=10):
    random.seed(0)
    edges = []
    for _ in range(m):
        u, v = random.randrange(n), random.randrange(n)
        if u != v:
            edges.append((u, v, random.randint(1, max_w)))
    return edges


def benchmark():
    n = 1500
    edges = _random_edges(n, 6000)
    variants = [
        ("Lazy decrease", lambda: lazy_decrease(edges, n, 0)),
        ("Heap stale-skip", lambda: heap_skip(edges, n, 0)),
        ("Set-based (edu)", lambda: set_dijkstra(edges, n, 0)),
    ]
    print(f"Benchmark: Dijkstra algorithm (CLRS) n={n}")
    print("-" * 65)
    for name, fn in variants:
        t0 = time.perf_counter()
        for _ in range(2):
            r = fn()
        t = (time.perf_counter() - t0) * 1000 / 2
        reached = sum(1 for x in r if x < float("inf"))
        print(f"{name:<20} reached={reached}   time={t:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
