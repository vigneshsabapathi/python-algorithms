"""
Dijkstra (matrix) - Optimized Variants with Benchmarks.

Variant 1: O(V^2) matrix scan (best for dense graphs)
Variant 2: Heap-based on same matrix (better for sparse)
Variant 3: Heap-based on adjacency list (standard)

>>> matrix_dijkstra([[0, 1], [1, 0]], 0)
[0, 1]
>>> heap_matrix_dijkstra([[0, 1], [1, 0]], 0)
[0, 1]
"""

import heapq
import time
import random


def matrix_dijkstra(mat, src):
    """O(V^2) Dijkstra.

    >>> matrix_dijkstra([[0, 1], [1, 0]], 0)
    [0, 1]
    """
    n = len(mat)
    INF = float("inf")
    dist = [INF] * n
    visited = [False] * n
    dist[src] = 0
    for _ in range(n):
        u, best = -1, INF
        for i in range(n):
            if not visited[i] and dist[i] < best:
                best, u = dist[i], i
        if u == -1:
            break
        visited[u] = True
        for v in range(n):
            if mat[u][v] and mat[u][v] != INF:
                nd = dist[u] + mat[u][v]
                if nd < dist[v]:
                    dist[v] = nd
    return dist


def heap_matrix_dijkstra(mat, src):
    """Heap Dijkstra over a matrix.

    >>> heap_matrix_dijkstra([[0, 1], [1, 0]], 0)
    [0, 1]
    """
    n = len(mat)
    INF = float("inf")
    dist = [INF] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v in range(n):
            if mat[u][v] and mat[u][v] != INF:
                nd = d + mat[u][v]
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
    return dist


def heap_list_dijkstra(adj, src, n):
    """Heap Dijkstra over adjacency list.

    >>> heap_list_dijkstra({0: [(1, 1)], 1: []}, 0, 2)
    [0, 1]
    """
    INF = float("inf")
    dist = [INF] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj.get(u, []):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def _random_dense(n, p=0.3, max_w=10):
    random.seed(0)
    mat = [[0]*n for _ in range(n)]
    adj = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                w = random.randint(1, max_w)
                mat[i][j] = mat[j][i] = w
                adj[i].append((j, w))
                adj[j].append((i, w))
    return mat, adj


def benchmark():
    n = 400
    mat, adj = _random_dense(n)
    variants = [
        ("Matrix scan O(V^2)", lambda: matrix_dijkstra(mat, 0)),
        ("Heap on matrix", lambda: heap_matrix_dijkstra(mat, 0)),
        ("Heap on adj list", lambda: heap_list_dijkstra(adj, 0, n)),
    ]
    print(f"Benchmark: Dijkstra 2 variants on dense n={n}")
    print("-" * 65)
    for name, fn in variants:
        t0 = time.perf_counter()
        for _ in range(3):
            r = fn()
        t = (time.perf_counter() - t0) * 1000 / 3
        reached = sum(1 for x in r if x < float("inf"))
        print(f"{name:<22} reached={reached}   time={t:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
