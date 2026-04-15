"""
Prim's MST (Vertex-based with heapq) - Optimized Variants

OOP Prim's with Vertex class, O(mn) basic and O((m+n)log n) heap versions.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/prim.py
"""

import heapq
import time


# ---------- Variant 1: Simple edge-list Prim's ----------
def prim_simple(n: int, edges: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    """
    Prim's with simple integer vertices and edge list input.

    >>> prim_simple(4, [(0, 1, 15), (0, 2, 12), (1, 2, 6), (1, 3, 13), (2, 3, 6)])
    [(0, 2, 12), (2, 1, 6), (2, 3, 6)]
    """
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    visited = [False] * n
    mst = []
    heap = [(0, 0, -1)]  # (weight, vertex, parent)

    while heap and len(mst) < n:
        w, u, parent = heapq.heappop(heap)
        if visited[u]:
            continue
        visited[u] = True
        if parent != -1:
            mst.append((parent, u, w))
        for v, weight in adj[u]:
            if not visited[v]:
                heapq.heappush(heap, (weight, v, u))

    return mst


# ---------- Variant 2: Prim's with decrease-key emulation ----------
def prim_decrease_key(n: int, edges: list[tuple[int, int, int]]) -> int:
    """
    Prim's with key-tracking for decrease-key behavior. Returns total MST weight.

    >>> prim_decrease_key(4, [(0, 1, 15), (0, 2, 12), (1, 2, 6), (1, 3, 13), (2, 3, 6)])
    24
    """
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    INF = float('inf')
    key = [INF] * n
    in_mst = [False] * n
    key[0] = 0
    heap = [(0, 0)]
    total = 0

    while heap:
        k, u = heapq.heappop(heap)
        if in_mst[u]:
            continue
        in_mst[u] = True
        total += k
        for v, w in adj[u]:
            if not in_mst[v] and w < key[v]:
                key[v] = w
                heapq.heappush(heap, (w, v))

    return total


# ---------- Variant 3: Prim's returning adjacency list of MST ----------
def prim_adj_list(n: int, edges: list[tuple[int, int, int]]) -> dict[int, list[tuple[int, int]]]:
    """
    Returns MST as adjacency list.

    >>> mst = prim_adj_list(3, [(0, 1, 5), (1, 2, 3), (0, 2, 10)])
    >>> sorted(mst[1])
    [(0, 5), (2, 3)]
    """
    mst_edges = prim_simple(n, edges)
    result = {i: [] for i in range(n)}
    for u, v, w in mst_edges:
        result[u].append((v, w))
        result[v].append((u, w))
    return result


# ---------- Benchmark ----------
def benchmark():
    import random
    random.seed(42)
    n = 500
    edges = []
    for i in range(n - 1):
        edges.append((i, i + 1, random.randint(1, 100)))
    for _ in range(n * 2):
        u, v = random.randint(0, n - 1), random.randint(0, n - 1)
        if u != v:
            edges.append((u, v, random.randint(1, 100)))

    for name, fn in [
        ("simple_heap", lambda: prim_simple(n, edges)),
        ("decrease_key", lambda: prim_decrease_key(n, edges)),
        ("adj_list", lambda: prim_adj_list(n, edges)),
    ]:
        start = time.perf_counter()
        for _ in range(30):
            fn()
        elapsed = (time.perf_counter() - start) / 30 * 1000
        print(f"  {name:20s}: {elapsed:.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Prim MST Benchmark (500 nodes, 30 runs) ===")
    benchmark()
