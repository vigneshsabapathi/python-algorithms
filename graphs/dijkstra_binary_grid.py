"""
Dijkstra on a binary grid (0 = passable, 1 = blocked).

Finds shortest path length (number of cells, 8-directional) from source to
target in a grid. Because every edge cost is 1, BFS also works -- but this
file shows the heap-based Dijkstra formulation.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/dijkstra_binary_grid.py

>>> grid = [[0, 0, 0, 0, 1], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0],
...         [1, 0, 0, 1, 0], [0, 0, 0, 0, 0]]
>>> dijkstra_grid(grid, (0, 0), (4, 4))
6

>>> dijkstra_grid([[0, 1], [1, 0]], (0, 0), (1, 1))
2

>>> dijkstra_grid([[1]], (0, 0), (0, 0))
-1

>>> dijkstra_grid([[0, 0], [0, 0]], (0, 0), (0, 0))
1
"""

import heapq


def dijkstra_grid(grid: list, source: tuple, target: tuple) -> int:
    """Shortest path length from source to target on a binary grid.

    Returns number of cells in the path (including both ends), or -1 if no path.

    >>> dijkstra_grid([[0, 0], [0, 0]], (0, 0), (1, 1))
    2
    """
    rows, cols = len(grid), len(grid[0])
    sr, sc = source
    tr, tc = target
    if grid[sr][sc] == 1 or grid[tr][tc] == 1:
        return -1
    INF = float("inf")
    dist = [[INF] * cols for _ in range(rows)]
    dist[sr][sc] = 1
    pq = [(1, sr, sc)]
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    while pq:
        d, r, c = heapq.heappop(pq)
        if (r, c) == target:
            return d
        if d > dist[r][c]:
            continue
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                nd = d + 1
                if nd < dist[nr][nc]:
                    dist[nr][nc] = nd
                    heapq.heappush(pq, (nd, nr, nc))
    return -1


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    grid = [[0, 0, 0, 0, 1], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0],
            [1, 0, 0, 1, 0], [0, 0, 0, 0, 0]]
    print("Path length (0,0)->(4,4):", dijkstra_grid(grid, (0, 0), (4, 4)))
