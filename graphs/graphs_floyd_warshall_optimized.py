"""
Floyd-Warshall All-Pairs Shortest Path - Optimized Variants

Finds shortest distances between all pairs of vertices in a weighted directed graph.
Handles negative edge weights (but not negative cycles).

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/graphs_floyd_warshall.py
"""

import time


# ---------- Variant 1: In-place with path reconstruction ----------
def floyd_warshall_with_path(graph: list[list[float]]) -> tuple[list[list[float]], list[list[int]]]:
    """
    Floyd-Warshall returning both distance matrix and next-hop matrix for path reconstruction.

    >>> INF = float('inf')
    >>> g = [[0, 3, INF, 7], [8, 0, 2, INF], [5, INF, 0, 1], [2, INF, INF, 0]]
    >>> dist, nxt = floyd_warshall_with_path(g)
    >>> dist[0][2]
    5
    >>> dist[3][1]
    5
    """
    v = len(graph)
    dist = [row[:] for row in graph]
    nxt = [[j if graph[i][j] != float('inf') and i != j else -1 for j in range(v)] for i in range(v)]

    for k in range(v):
        for i in range(v):
            if dist[i][k] == float('inf'):
                continue
            for j in range(v):
                if dist[k][j] != float('inf') and dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]

    return dist, nxt


def reconstruct_path(nxt: list[list[int]], u: int, v: int) -> list[int]:
    """
    Reconstruct shortest path from u to v using next-hop matrix.

    >>> INF = float('inf')
    >>> g = [[0, 3, INF, 7], [8, 0, 2, INF], [5, INF, 0, 1], [2, INF, INF, 0]]
    >>> _, nxt = floyd_warshall_with_path(g)
    >>> reconstruct_path(nxt, 0, 2)
    [0, 1, 2]
    """
    if nxt[u][v] == -1:
        return []
    path = [u]
    while u != v:
        u = nxt[u][v]
        path.append(u)
    return path


# ---------- Variant 2: Negative cycle detection ----------
def floyd_warshall_detect_negative(graph: list[list[float]]) -> tuple[list[list[float]], bool]:
    """
    Floyd-Warshall with negative cycle detection.

    >>> INF = float('inf')
    >>> g = [[0, 1, INF], [INF, 0, -3], [2, INF, 0]]
    >>> dist, has_neg = floyd_warshall_detect_negative(g)
    >>> has_neg
    False
    >>> dist[0][2]
    -2
    """
    v = len(graph)
    dist = [row[:] for row in graph]

    for k in range(v):
        for i in range(v):
            if dist[i][k] == float('inf'):
                continue
            for j in range(v):
                if dist[k][j] != float('inf') and dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    has_negative_cycle = any(dist[i][i] < 0 for i in range(v))
    return dist, has_negative_cycle


# ---------- Variant 3: Space-optimized for transitive closure ----------
def transitive_closure(graph: list[list[int]]) -> list[list[bool]]:
    """
    Warshall's algorithm for transitive closure (reachability).

    >>> g = [[0, 1, 0], [0, 0, 1], [0, 0, 0]]
    >>> tc = transitive_closure(g)
    >>> tc[0][2]
    True
    >>> tc[2][0]
    False
    """
    v = len(graph)
    reach = [[graph[i][j] == 1 or i == j for j in range(v)] for i in range(v)]

    for k in range(v):
        for i in range(v):
            for j in range(v):
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])

    return reach


# ---------- Benchmark ----------
def benchmark():
    import random
    random.seed(42)
    INF = float('inf')
    n = 100
    graph = [[INF] * n for _ in range(n)]
    for i in range(n):
        graph[i][i] = 0
    for _ in range(n * 3):
        u, v = random.randint(0, n - 1), random.randint(0, n - 1)
        if u != v:
            graph[u][v] = random.randint(1, 100)

    for name, fn in [
        ("with_path", lambda: floyd_warshall_with_path(graph)),
        ("neg_detect", lambda: floyd_warshall_detect_negative(graph)),
        ("transitive_closure", lambda: transitive_closure([[1 if graph[i][j] != INF else 0 for j in range(n)] for i in range(n)])),
    ]:
        start = time.perf_counter()
        for _ in range(5):
            fn()
        elapsed = (time.perf_counter() - start) / 5 * 1000
        print(f"  {name:20s}: {elapsed:.3f} ms ({n}x{n} matrix)")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Floyd-Warshall Benchmark (100x100, 5 runs) ===")
    benchmark()
