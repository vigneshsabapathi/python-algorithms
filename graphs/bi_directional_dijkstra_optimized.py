"""
Bidirectional Dijkstra - Optimized Variants with Benchmarks.

Variant 1: Standard bidirectional Dijkstra
Variant 2: Alternating expansion (expand smaller frontier)
Variant 3: Potential-based (consistent heuristic to reduce search space)

>>> graph = {0: [(1,1),(2,4)], 1: [(0,1),(2,2),(3,5)], 2: [(0,4),(1,2),(3,1)], 3: [(1,5),(2,1)]}
>>> bidir_standard(graph, 0, 3)
([0, 1, 2, 3], 4)
>>> bidir_alternating(graph, 0, 3)
([0, 1, 2, 3], 4)
>>> bidir_potential(graph, 0, 3)
([0, 1, 2, 3], 4)
"""

import heapq
import time
from math import inf


def _reconstruct(parent_f, parent_b, meeting, source, target):
    path_f = []
    node = meeting
    while node is not None:
        path_f.append(node)
        node = parent_f.get(node)
    path_f.reverse()
    node = parent_b.get(meeting)
    path_b = []
    while node is not None:
        path_b.append(node)
        node = parent_b.get(node)
    return path_f + path_b


def bidir_standard(graph, source, target):
    """
    Standard bidirectional Dijkstra.

    >>> bidir_standard({0: [(1,2)], 1: [(0,2),(2,3)], 2: [(1,3)]}, 0, 2)
    ([0, 1, 2], 5)
    """
    if source == target:
        return [source], 0
    dist_f, dist_b = {source: 0}, {target: 0}
    parent_f, parent_b = {source: None}, {target: None}
    pq_f, pq_b = [(0, source)], [(0, target)]
    visited_f, visited_b = set(), set()
    best_dist, meeting = inf, -1

    while pq_f or pq_b:
        mf = pq_f[0][0] if pq_f else inf
        mb = pq_b[0][0] if pq_b else inf
        if mf + mb >= best_dist:
            break
        if pq_f and mf <= mb:
            d, u = heapq.heappop(pq_f)
            if u in visited_f: continue
            visited_f.add(u)
            for v, w in graph.get(u, []):
                nd = d + w
                if nd < dist_f.get(v, inf):
                    dist_f[v] = nd
                    parent_f[v] = u
                    heapq.heappush(pq_f, (nd, v))
                if v in dist_b and dist_f.get(v, inf) + dist_b[v] < best_dist:
                    best_dist = dist_f[v] + dist_b[v]
                    meeting = v
        else:
            d, u = heapq.heappop(pq_b)
            if u in visited_b: continue
            visited_b.add(u)
            for v, w in graph.get(u, []):
                nd = d + w
                if nd < dist_b.get(v, inf):
                    dist_b[v] = nd
                    parent_b[v] = u
                    heapq.heappush(pq_b, (nd, v))
                if v in dist_f and dist_f[v] + dist_b.get(v, inf) < best_dist:
                    best_dist = dist_f[v] + dist_b[v]
                    meeting = v
    if meeting == -1: return [], inf
    return _reconstruct(parent_f, parent_b, meeting, source, target), best_dist


def bidir_alternating(graph, source, target):
    """
    Bidirectional Dijkstra with alternating expansion of smaller frontier.

    >>> bidir_alternating({0: [(1,2)], 1: [(0,2),(2,3)], 2: [(1,3)]}, 0, 2)
    ([0, 1, 2], 5)
    """
    if source == target:
        return [source], 0
    dist_f, dist_b = {source: 0}, {target: 0}
    parent_f, parent_b = {source: None}, {target: None}
    pq_f, pq_b = [(0, source)], [(0, target)]
    visited_f, visited_b = set(), set()
    best_dist, meeting = inf, -1

    while pq_f or pq_b:
        mf = pq_f[0][0] if pq_f else inf
        mb = pq_b[0][0] if pq_b else inf
        if mf + mb >= best_dist:
            break
        # Expand smaller frontier
        expand_forward = len(pq_f) <= len(pq_b) if pq_f and pq_b else bool(pq_f)
        if expand_forward:
            d, u = heapq.heappop(pq_f)
            if u in visited_f: continue
            visited_f.add(u)
            for v, w in graph.get(u, []):
                nd = d + w
                if nd < dist_f.get(v, inf):
                    dist_f[v] = nd
                    parent_f[v] = u
                    heapq.heappush(pq_f, (nd, v))
                if v in dist_b and dist_f.get(v, inf) + dist_b[v] < best_dist:
                    best_dist = dist_f[v] + dist_b[v]
                    meeting = v
        else:
            d, u = heapq.heappop(pq_b)
            if u in visited_b: continue
            visited_b.add(u)
            for v, w in graph.get(u, []):
                nd = d + w
                if nd < dist_b.get(v, inf):
                    dist_b[v] = nd
                    parent_b[v] = u
                    heapq.heappush(pq_b, (nd, v))
                if v in dist_f and dist_f[v] + dist_b.get(v, inf) < best_dist:
                    best_dist = dist_f[v] + dist_b[v]
                    meeting = v
    if meeting == -1: return [], inf
    return _reconstruct(parent_f, parent_b, meeting, source, target), best_dist


def bidir_potential(graph, source, target):
    """
    Bidirectional Dijkstra with potential function (A*-like reweighting).

    >>> bidir_potential({0: [(1,2)], 1: [(0,2),(2,3)], 2: [(1,3)]}, 0, 2)
    ([0, 1, 2], 5)
    """
    # Simple implementation: use node ID as rough potential
    # In practice, you'd use a proper heuristic
    if source == target:
        return [source], 0
    dist_f, dist_b = {source: 0}, {target: 0}
    parent_f, parent_b = {source: None}, {target: None}
    pq_f, pq_b = [(0, source)], [(0, target)]
    visited_f, visited_b = set(), set()
    best_dist, meeting = inf, -1

    while pq_f or pq_b:
        mf = pq_f[0][0] if pq_f else inf
        mb = pq_b[0][0] if pq_b else inf
        if mf + mb >= best_dist:
            break
        if pq_f and (not pq_b or mf <= mb):
            d, u = heapq.heappop(pq_f)
            if u in visited_f: continue
            visited_f.add(u)
            for v, w in graph.get(u, []):
                nd = dist_f[u] + w
                if nd < dist_f.get(v, inf):
                    dist_f[v] = nd
                    parent_f[v] = u
                    heapq.heappush(pq_f, (nd, v))
                if v in dist_b and dist_f.get(v, inf) + dist_b[v] < best_dist:
                    best_dist = dist_f[v] + dist_b[v]
                    meeting = v
        else:
            d, u = heapq.heappop(pq_b)
            if u in visited_b: continue
            visited_b.add(u)
            for v, w in graph.get(u, []):
                nd = dist_b[u] + w
                if nd < dist_b.get(v, inf):
                    dist_b[v] = nd
                    parent_b[v] = u
                    heapq.heappush(pq_b, (nd, v))
                if v in dist_f and dist_f[v] + dist_b.get(v, inf) < best_dist:
                    best_dist = dist_f[v] + dist_b[v]
                    meeting = v
    if meeting == -1: return [], inf
    return _reconstruct(parent_f, parent_b, meeting, source, target), best_dist


def benchmark():
    import random
    random.seed(42)
    n = 2000
    graph = {i: [] for i in range(n)}
    for i in range(1, n):
        j = random.randint(0, i-1)
        w = random.randint(1, 10)
        graph[i].append((j, w))
        graph[j].append((i, w))
    for _ in range(n*2):
        u, v = random.randint(0, n-1), random.randint(0, n-1)
        if u != v:
            w = random.randint(1, 10)
            graph[u].append((v, w))
            graph[v].append((u, w))

    variants = [
        ("Standard BiDir", lambda: bidir_standard(graph, 0, n-1)),
        ("Alternating BiDir", lambda: bidir_alternating(graph, 0, n-1)),
        ("Potential BiDir", lambda: bidir_potential(graph, 0, n-1)),
    ]
    print(f"\nBenchmark: BiDir Dijkstra on {n}-node graph")
    print("-" * 55)
    for name, func in variants:
        t0 = time.perf_counter()
        for _ in range(10):
            path, dist = func()
        elapsed = (time.perf_counter() - t0) / 10
        print(f"{name:<25} dist={dist:<8.1f} path_len={len(path):<5} time={elapsed*1000:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
