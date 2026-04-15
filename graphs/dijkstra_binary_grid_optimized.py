"""
Dijkstra Binary Grid - Optimized Variants with Benchmarks.

Variant 1: Dijkstra with heap
Variant 2: BFS (unit weights - equivalent and faster)
Variant 3: A* with Chebyshev distance heuristic (8-directional)

>>> grid = [[0, 0], [0, 0]]
>>> grid_dijkstra(grid, (0, 0), (1, 1))
2
>>> grid_bfs(grid, (0, 0), (1, 1))
2
>>> grid_astar(grid, (0, 0), (1, 1))
2
"""

import heapq
import time
import random
from collections import deque


DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def grid_dijkstra(grid, src, tgt):
    """Heap Dijkstra on grid.

    >>> grid_dijkstra([[0, 0], [0, 0]], (0, 0), (1, 1))
    2
    """
    R, C = len(grid), len(grid[0])
    sr, sc = src
    if grid[sr][sc] or grid[tgt[0]][tgt[1]]:
        return -1
    dist = [[float("inf")] * C for _ in range(R)]
    dist[sr][sc] = 1
    pq = [(1, sr, sc)]
    while pq:
        d, r, c = heapq.heappop(pq)
        if (r, c) == tgt:
            return d
        if d > dist[r][c]:
            continue
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0:
                if d + 1 < dist[nr][nc]:
                    dist[nr][nc] = d + 1
                    heapq.heappush(pq, (d + 1, nr, nc))
    return -1


def grid_bfs(grid, src, tgt):
    """Unit-weight BFS (optimal when all edges cost 1).

    >>> grid_bfs([[0, 0], [0, 0]], (0, 0), (1, 1))
    2
    """
    R, C = len(grid), len(grid[0])
    sr, sc = src
    if grid[sr][sc] or grid[tgt[0]][tgt[1]]:
        return -1
    seen = {(sr, sc)}
    q = deque([(sr, sc, 1)])
    while q:
        r, c, d = q.popleft()
        if (r, c) == tgt:
            return d
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0 and (nr, nc) not in seen:
                seen.add((nr, nc))
                q.append((nr, nc, d + 1))
    return -1


def grid_astar(grid, src, tgt):
    """A* with Chebyshev heuristic (admissible for 8-directional grid).

    >>> grid_astar([[0, 0], [0, 0]], (0, 0), (1, 1))
    2
    """
    R, C = len(grid), len(grid[0])
    sr, sc = src
    tr, tc = tgt
    if grid[sr][sc] or grid[tr][tc]:
        return -1

    def h(r, c):
        return max(abs(r - tr), abs(c - tc))

    g = [[float("inf")] * C for _ in range(R)]
    g[sr][sc] = 1
    pq = [(1 + h(sr, sc), 1, sr, sc)]
    while pq:
        f, d, r, c = heapq.heappop(pq)
        if (r, c) == tgt:
            return d
        if d > g[r][c]:
            continue
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0:
                nd = d + 1
                if nd < g[nr][nc]:
                    g[nr][nc] = nd
                    heapq.heappush(pq, (nd + h(nr, nc), nd, nr, nc))
    return -1


def _random_grid(n, p=0.2):
    random.seed(0)
    g = [[1 if random.random() < p else 0 for _ in range(n)] for _ in range(n)]
    g[0][0] = g[-1][-1] = 0
    return g


def benchmark():
    n = 60
    g = _random_grid(n)
    src, tgt = (0, 0), (n - 1, n - 1)
    variants = [
        ("Dijkstra heap", lambda: grid_dijkstra(g, src, tgt)),
        ("BFS", lambda: grid_bfs(g, src, tgt)),
        ("A* Chebyshev", lambda: grid_astar(g, src, tgt)),
    ]
    print(f"Benchmark: Shortest path in {n}x{n} binary grid")
    print("-" * 65)
    for name, fn in variants:
        t0 = time.perf_counter()
        for _ in range(5):
            r = fn()
        t = (time.perf_counter() - t0) * 1000 / 5
        print(f"{name:<18} dist={r}   time={t:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
