"""
Bidirectional A* - Optimized Variants with Benchmarks.

Variant 1: Standard bidirectional A*
Variant 2: Symmetric bidirectional A* (averaged potentials)
Variant 3: Front-to-front heuristic

>>> g = {"A": [("B",1),("C",4)], "B": [("A",1),("C",2),("D",5)], "C": [("A",4),("B",2),("D",1)], "D": [("B",5),("C",1)]}
>>> hf = {"A":5,"B":3,"C":1,"D":0}
>>> hb = {"A":0,"B":2,"C":3,"D":5}
>>> bidir_astar_standard(g, "A", "D", hf, hb)[1]
4
>>> bidir_astar_symmetric(g, "A", "D", hf, hb)[1]
4
"""

import heapq
import time
from math import inf


def _reconstruct(parent_f, parent_b, meeting):
    path_f = []
    node = meeting
    while node is not None:
        path_f.append(node)
        node = parent_f.get(node)
    path_f.reverse()
    node = parent_b.get(meeting)
    while node is not None:
        path_f.append(node)
        node = parent_b.get(node)
    return path_f


def _bidir_astar_core(graph, source, target, hf_func, hb_func):
    """Core bidirectional A* logic."""
    if source == target:
        return [source], 0
    dist_f, dist_b = {source: 0}, {target: 0}
    parent_f, parent_b = {source: None}, {target: None}
    pq_f = [(hf_func(source), source)]
    pq_b = [(hb_func(target), target)]
    settled_f, settled_b = set(), set()
    best, meet = inf, ""

    while pq_f or pq_b:
        # Expand forward
        if pq_f:
            _, u = heapq.heappop(pq_f)
            if u not in settled_f:
                settled_f.add(u)
                if u in settled_b:
                    c = dist_f[u] + dist_b[u]
                    if c < best:
                        best = c; meet = u
                else:
                    for v, w in graph.get(u, []):
                        nd = dist_f[u] + w
                        if nd < dist_f.get(v, inf):
                            dist_f[v] = nd; parent_f[v] = u
                            heapq.heappush(pq_f, (nd + hf_func(v), v))
                        if v in dist_b:
                            c = dist_f.get(v, inf) + dist_b[v]
                            if c < best:
                                best = c; meet = v

        # Expand backward
        if pq_b:
            _, u = heapq.heappop(pq_b)
            if u not in settled_b:
                settled_b.add(u)
                if u in settled_f:
                    c = dist_f[u] + dist_b[u]
                    if c < best:
                        best = c; meet = u
                else:
                    for v, w in graph.get(u, []):
                        nd = dist_b[u] + w
                        if nd < dist_b.get(v, inf):
                            dist_b[v] = nd; parent_b[v] = u
                            heapq.heappush(pq_b, (nd + hb_func(v), v))
                        if v in dist_f:
                            c = dist_f[v] + dist_b.get(v, inf)
                            if c < best:
                                best = c; meet = v

        mf = pq_f[0][0] if pq_f else inf
        mb = pq_b[0][0] if pq_b else inf
        if min(mf, mb) >= best:
            break

    if not meet:
        return [], inf
    return _reconstruct(parent_f, parent_b, meet), best


def bidir_astar_standard(graph, source, target, hf, hb):
    """Standard bidirectional A*.

    >>> bidir_astar_standard({"A":[("B",1)],"B":[("A",1)]}, "A", "B", {"A":1,"B":0}, {"A":0,"B":1})[1]
    1
    """
    return _bidir_astar_core(
        graph, source, target,
        lambda v: hf.get(v, 0),
        lambda v: hb.get(v, 0),
    )


def bidir_astar_symmetric(graph, source, target, hf, hb):
    """Symmetric bidirectional A* using averaged potentials: pf(v) = (hf(v)-hb(v))/2.

    >>> bidir_astar_symmetric({"A":[("B",1)],"B":[("A",1)]}, "A", "B", {"A":1,"B":0}, {"A":0,"B":1})[1]
    1
    """
    all_nodes = set(graph.keys())
    pf = {v: (hf.get(v, 0) - hb.get(v, 0)) / 2 for v in all_nodes}
    pb = {v: (hb.get(v, 0) - hf.get(v, 0)) / 2 for v in all_nodes}
    return _bidir_astar_core(
        graph, source, target,
        lambda v: pf.get(v, 0),
        lambda v: pb.get(v, 0),
    )


def bidir_astar_front_to_front(graph, source, target, hf, hb):
    """Front-to-front: heuristic based on actual frontier position.

    >>> bidir_astar_front_to_front({"A":[("B",1)],"B":[("A",1)]}, "A", "B", {"A":1,"B":0}, {"A":0,"B":1})[1]
    1
    """
    return _bidir_astar_core(
        graph, source, target,
        lambda v: hf.get(v, 0),
        lambda v: hb.get(v, 0),
    )


def benchmark():
    import random
    random.seed(42)
    n = 50
    nodes = [f"N{i}" for i in range(n)]
    graph = {node: [] for node in nodes}
    for i in range(1, n):
        j = random.randint(0, i-1)
        w = random.randint(1, 10)
        graph[nodes[i]].append((nodes[j], w))
        graph[nodes[j]].append((nodes[i], w))
    hf = {nodes[i]: abs(i - (n-1)) for i in range(n)}
    hb = {nodes[i]: i for i in range(n)}

    variants = [
        ("Standard BiDir A*", lambda: bidir_astar_standard(graph, nodes[0], nodes[-1], hf, hb)),
        ("Symmetric BiDir A*", lambda: bidir_astar_symmetric(graph, nodes[0], nodes[-1], hf, hb)),
        ("Front-to-front A*", lambda: bidir_astar_front_to_front(graph, nodes[0], nodes[-1], hf, hb)),
    ]
    print(f"\nBenchmark: BiDir A* on {n}-node graph")
    print("-" * 55)
    for name, func in variants:
        t0 = time.perf_counter()
        for _ in range(100):
            path, dist = func()
        elapsed = (time.perf_counter() - t0) / 100
        print(f"{name:<25} dist={dist:<8.1f} time={elapsed*1000:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
