"""
Greedy Minimum Vertex Cover - Optimized Variants

Approximation algorithm for the minimum vertex cover problem using a greedy approach.
Picks the highest-degree vertex repeatedly until all edges are covered.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/greedy_min_vertex_cover.py
"""

import heapq
import time


# ---------- Variant 1: Max-heap with lazy deletion ----------
def greedy_vertex_cover_heap(graph: dict[int, list[int]]) -> set[int]:
    """
    Greedy vertex cover using a max-heap for efficient max-degree extraction.

    >>> greedy_vertex_cover_heap({0: [1, 3], 1: [0, 3], 2: [0, 3, 4], 3: [0, 1, 2], 4: [2, 3]})
    {0, 1, 2, 4}
    """
    adj = {v: set(neighbors) for v, neighbors in graph.items()}
    heap = [(-len(neighbors), v) for v, neighbors in adj.items()]
    heapq.heapify(heap)
    cover = set()

    while heap:
        neg_deg, v = heapq.heappop(heap)
        if not adj.get(v):
            continue
        if -neg_deg != len(adj[v]):
            if adj[v]:
                heapq.heappush(heap, (-len(adj[v]), v))
            continue
        cover.add(v)
        for u in list(adj[v]):
            adj[u].discard(v)
            if adj[u]:
                heapq.heappush(heap, (-len(adj[u]), u))
        adj[v] = set()

    return cover


# ---------- Variant 2: Simple iterative (most readable) ----------
def greedy_vertex_cover_simple(graph: dict[int, list[int]]) -> set[int]:
    """
    Simple greedy: always pick the vertex with highest remaining degree.

    >>> greedy_vertex_cover_simple({0: [1, 3], 1: [0, 3], 2: [0, 3, 4], 3: [0, 1, 2], 4: [2, 3]})
    {0, 1, 2, 4}
    """
    adj = {v: set(neighbors) for v, neighbors in graph.items()}
    cover = set()

    while any(adj.values()):
        v = max(adj, key=lambda x: len(adj[x]))
        cover.add(v)
        for u in adj[v]:
            adj[u].discard(v)
        adj[v] = set()

    return cover


# ---------- Variant 3: Edge-based 2-approximation ----------
def vertex_cover_2approx(graph: dict[int, list[int]]) -> set[int]:
    """
    2-approximation: pick both endpoints of an arbitrary uncovered edge.
    Guaranteed to be at most 2x optimal.

    >>> cover = vertex_cover_2approx({0: [1, 2], 1: [0, 2], 2: [0, 1]})
    >>> len(cover) >= 2
    True
    """
    adj = {v: set(neighbors) for v, neighbors in graph.items()}
    cover = set()

    for u in list(adj):
        if adj[u]:
            v = next(iter(adj[u]))
            cover.add(u)
            cover.add(v)
            for w in list(adj[u]):
                adj[w].discard(u)
            for w in list(adj[v]):
                adj[w].discard(v)
            adj[u] = set()
            adj[v] = set()

    return cover


# ---------- Benchmark ----------
def benchmark():
    import random
    random.seed(42)
    n = 500
    graph = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.02:
                graph[i].append(j)
                graph[j].append(i)

    for name, fn in [
        ("heap_greedy", greedy_vertex_cover_heap),
        ("simple_greedy", greedy_vertex_cover_simple),
        ("2_approximation", vertex_cover_2approx),
    ]:
        start = time.perf_counter()
        for _ in range(20):
            result = fn(graph)
        elapsed = (time.perf_counter() - start) / 20 * 1000
        print(f"  {name:20s}: {elapsed:.3f} ms (cover size: {len(result)})")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Greedy Vertex Cover Benchmark (500 nodes, 20 runs) ===")
    benchmark()
