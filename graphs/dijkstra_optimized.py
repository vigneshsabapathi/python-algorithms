"""
Dijkstra - Optimized Variants with Benchmarks.

Variant 1: Binary heap (heapq)
Variant 2: Lazy deletion variant (skip stale entries)
Variant 3: Bucket / array-based for small int weights (not implemented here; use heap variant)
Variant 4: Bidirectional Dijkstra (meet in middle)

>>> heap_dijkstra({0: [(1, 5)], 1: []}, 0)[1]
5
>>> lazy_dijkstra({0: [(1, 5)], 1: []}, 0)[1]
5
>>> bidir_dijkstra({0: [(1, 3)], 1: [(2, 4)], 2: []}, 0, 2)
7
"""

import heapq
import time
import random
from collections import defaultdict


def heap_dijkstra(graph, source):
    """Standard heap-based Dijkstra.

    >>> heap_dijkstra({0: [(1, 2)], 1: []}, 0)
    {0: 0, 1: 2}
    """
    dist = {source: 0}
    pq = [(0, source)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def lazy_dijkstra(graph, source):
    """Same as heap, but explicit 'skip stale' structure.

    >>> lazy_dijkstra({0: [(1, 2)], 1: []}, 0)
    {0: 0, 1: 2}
    """
    dist = defaultdict(lambda: float("inf"))
    dist[source] = 0
    finalized = set()
    pq = [(0, source)]
    while pq:
        d, u = heapq.heappop(pq)
        if u in finalized:
            continue
        finalized.add(u)
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dict(dist)


def bidir_dijkstra(graph, source, target):
    """Bidirectional Dijkstra on symmetric graph (computes one distance).

    >>> bidir_dijkstra({0: [(1, 1)], 1: [(0, 1)]}, 0, 1)
    1
    """
    if source == target:
        return 0
    # Reverse graph
    rev = defaultdict(list)
    for u, nbrs in graph.items():
        for v, w in nbrs:
            rev[v].append((u, w))

    INF = float("inf")
    df = defaultdict(lambda: INF); df[source] = 0
    db = defaultdict(lambda: INF); db[target] = 0
    pf, pb = [(0, source)], [(0, target)]
    best = INF
    vf, vb = {}, {}
    while pf and pb:
        if pf[0][0] + pb[0][0] >= best:
            return best
        d, u = heapq.heappop(pf)
        if u in vf:
            continue
        vf[u] = d
        if u in vb:
            best = min(best, d + vb[u])
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < df[v]:
                df[v] = nd
                heapq.heappush(pf, (nd, v))
        d, u = heapq.heappop(pb)
        if u in vb:
            continue
        vb[u] = d
        if u in vf:
            best = min(best, d + vf[u])
        for v, w in rev.get(u, []):
            nd = d + w
            if nd < db[v]:
                db[v] = nd
                heapq.heappush(pb, (nd, v))
    return best if best != INF else -1


def _random_weighted(n, avg, max_w=10):
    random.seed(0)
    g = defaultdict(list)
    for _ in range(n * avg):
        u, v = random.randrange(n), random.randrange(n)
        if u != v:
            w = random.randint(1, max_w)
            g[u].append((v, w))
            g[v].append((u, w))
    return g


def benchmark():
    n = 2000
    g = _random_weighted(n, 4)
    variants = [
        ("Heap Dijkstra", lambda: heap_dijkstra(g, 0)),
        ("Lazy Dijkstra", lambda: lazy_dijkstra(g, 0)),
        ("Bidir Dijkstra", lambda: bidir_dijkstra(g, 0, n - 1)),
    ]
    print(f"Benchmark: Dijkstra variants on n={n}")
    print("-" * 65)
    for name, fn in variants:
        t0 = time.perf_counter()
        for _ in range(3):
            r = fn()
        t = (time.perf_counter() - t0) * 1000 / 3
        size = len(r) if isinstance(r, dict) else r
        print(f"{name:<18} result={size}   time={t:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
