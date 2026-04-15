"""
Dijkstra 2 - Adjacency matrix variant with path reconstruction.

Uses an O(V^2) scan instead of a heap -- optimal for dense graphs.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/dijkstra_2.py

>>> INF = float('inf')
>>> graph = [
...     [0,   7,   9,   INF, INF, 14],
...     [7,   0,   10,  15,  INF, INF],
...     [9,   10,  0,   11,  INF, 2],
...     [INF, 15,  11,  0,   6,   INF],
...     [INF, INF, INF, 6,   0,   9],
...     [14,  INF, 2,   INF, 9,   0],
... ]
>>> dist, prev = dijkstra_matrix(graph, 0)
>>> dist
[0, 7, 9, 20, 20, 11]
>>> reconstruct_path(prev, 0, 4)
[0, 2, 5, 4]
"""


def dijkstra_matrix(matrix: list, source: int) -> tuple:
    """Adjacency matrix Dijkstra. Returns (dist, prev).

    >>> dijkstra_matrix([[0, 1], [1, 0]], 0)[0]
    [0, 1]
    """
    n = len(matrix)
    INF = float("inf")
    dist = [INF] * n
    prev = [None] * n
    visited = [False] * n
    dist[source] = 0
    for _ in range(n):
        u = -1
        best = INF
        for i in range(n):
            if not visited[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u == -1:
            break
        visited[u] = True
        for v in range(n):
            w = matrix[u][v]
            if w == INF or w == 0 and u != v:
                continue
            if not visited[v] and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
    return dist, prev


def reconstruct_path(prev: list, source: int, target: int) -> list:
    """Reconstruct path from source to target using prev array.

    >>> reconstruct_path([None, 0], 0, 1)
    [0, 1]
    """
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        if cur == source:
            break
        cur = prev[cur]
    path.reverse()
    return path if path and path[0] == source else []


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    INF = float('inf')
    g = [
        [0, 7, 9, INF, INF, 14],
        [7, 0, 10, 15, INF, INF],
        [9, 10, 0, 11, INF, 2],
        [INF, 15, 11, 0, 6, INF],
        [INF, INF, INF, 6, 0, 9],
        [14, INF, 2, INF, 9, 0],
    ]
    d, p = dijkstra_matrix(g, 0)
    print("Distances:", d)
    print("Path 0->4:", reconstruct_path(p, 0, 4))
