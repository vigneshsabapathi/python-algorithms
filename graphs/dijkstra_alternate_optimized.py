"""
Dijkstra Alternate - Optimized Variants with Benchmarks.

Variant 1: Early-exit Dijkstra (stop at target)
Variant 2: Full Dijkstra returning all distances
Variant 3: A* with zero heuristic (equivalent to Dijkstra)

>>> early_exit({'a': {'b': 1, 'c': 5}, 'b': {'c': 2}, 'c': {}}, 'a', 'c')
3
>>> full_dijkstra({'a': {'b': 1}, 'b': {}}, 'a')['b']
1
>>> astar_zero({'a': {'b': 2}, 'b': {}}, 'a', 'b')
2
"""

import heapq
import time
import random


def early_exit(graph, start, end):
    """Dijkstra that stops the instant target is popped.

    >>> early_exit({'a': {'b': 3}, 'b': {}}, 'a', 'b')
    3
    """
    if start == end:
        return 0
    pq = [(0, start)]
    seen = set()
    while pq:
        d, u = heapq.heappop(pq)
        if u in seen:
            continue
        seen.add(u)
        if u == end:
            return d
        for v, w in graph.get(u, {}).items():
            if v not in seen:
                heapq.heappush(pq, (d + w, v))
    return -1


def full_dijkstra(graph, start):
    """Full Dijkstra returning dict of distances.

    >>> full_dijkstra({'a': {'b': 1}, 'b': {}}, 'a')['a']
    0
    """
    dist = {start: 0}
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph.get(u, {}).items():
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def astar_zero(graph, start, end):
    """A* with h = 0 -> behaves like Dijkstra.

    >>> astar_zero({'a': {'b': 2}, 'b': {}}, 'a', 'b')
    2
    """
    if start == end:
        return 0
    pq = [(0, 0, start)]
    seen = set()
    while pq:
        _, g, u = heapq.heappop(pq)
        if u in seen:
            continue
        seen.add(u)
        if u == end:
            return g
        for v, w in graph.get(u, {}).items():
            if v not in seen:
                heapq.heappush(pq, (g + w, g + w, v))
    return -1


def _random_dict(n, avg=4, max_w=10):
    random.seed(0)
    g = {i: {} for i in range(n)}
    for _ in range(n * avg):
        u, v = random.randrange(n), random.randrange(n)
        if u != v:
            w = random.randint(1, max_w)
            g[u][v] = w
            g[v][u] = w
    return g


def benchmark():
    n = 1500
    g = _random_dict(n)
    target = n - 1
    variants = [
        ("Early exit", lambda: early_exit(g, 0, target)),
        ("Full Dijkstra", lambda: full_dijkstra(g, 0).get(target, -1)),
        ("A* zero heuristic", lambda: astar_zero(g, 0, target)),
    ]
    print(f"Benchmark: Dijkstra alternate n={n}")
    print("-" * 65)
    for name, fn in variants:
        t0 = time.perf_counter()
        for _ in range(3):
            r = fn()
        t = (time.perf_counter() - t0) * 1000 / 3
        print(f"{name:<22} dist={r}   time={t:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
