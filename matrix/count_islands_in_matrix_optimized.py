#!/usr/bin/env python3
"""
Optimized and alternative implementations of Count Islands in Matrix.

The reference uses recursive DFS with 8-directional connectivity (diagonals
included). It uses a class-based approach with O(m*n) time and space.

Three alternatives:
  bfs_iterative  -- BFS with deque, avoids recursion stack overflow on large grids
  union_find     -- Disjoint Set Union for O(m*n * alpha(m*n)) ~ O(m*n)
  iterative_dfs  -- Explicit stack DFS, no recursion

All three handle 8-directional connectivity (including diagonals).

Run:
    python matrix/count_islands_in_matrix_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matrix.count_islands_in_matrix import Matrix as ReferenceMatrix


# ---------------------------------------------------------------------------
# Variant 1 -- BFS iterative: avoids recursion depth issues
# ---------------------------------------------------------------------------

def count_islands_bfs(grid: list[list[int]]) -> int:
    """
    Count islands using iterative BFS with 8-directional connectivity.

    >>> count_islands_bfs([[1, 1, 0], [0, 1, 0], [0, 0, 1]])
    1
    >>> count_islands_bfs([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    0
    >>> count_islands_bfs([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    1
    >>> count_islands_bfs([[1, 0, 1], [0, 0, 0], [1, 0, 1]])
    4
    >>> count_islands_bfs([])
    0
    """
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                  (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1 and not visited[i][j]:
                queue = deque([(i, j)])
                visited[i][j] = True
                while queue:
                    r, c = queue.popleft()
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and grid[nr][nc] == 1:
                            visited[nr][nc] = True
                            queue.append((nr, nc))
                count += 1
    return count


# ---------------------------------------------------------------------------
# Variant 2 -- Union-Find (Disjoint Set Union)
# ---------------------------------------------------------------------------

def count_islands_union_find(grid: list[list[int]]) -> int:
    """
    Count islands using Union-Find with path compression and union by rank.

    >>> count_islands_union_find([[1, 1, 0], [0, 1, 0], [0, 0, 1]])
    1
    >>> count_islands_union_find([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    0
    >>> count_islands_union_find([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    1
    >>> count_islands_union_find([[1, 0, 1], [0, 0, 0], [1, 0, 1]])
    4
    >>> count_islands_union_find([])
    0
    """
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    parent = list(range(rows * cols))
    rank = [0] * (rows * cols)

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: int, y: int) -> None:
        rx, ry = find(x), find(y)
        if rx == ry:
            return
        if rank[rx] < rank[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        if rank[rx] == rank[ry]:
            rank[rx] += 1

    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                  (0, 1), (1, -1), (1, 0), (1, 1)]

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                for dr, dc in directions:
                    ni, nj = i + dr, j + dc
                    if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == 1:
                        union(i * cols + j, ni * cols + nj)

    # Count unique roots among land cells
    roots = set()
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                roots.add(find(i * cols + j))
    return len(roots)


# ---------------------------------------------------------------------------
# Variant 3 -- Iterative DFS with explicit stack
# ---------------------------------------------------------------------------

def count_islands_iterative_dfs(grid: list[list[int]]) -> int:
    """
    Count islands using iterative DFS (explicit stack) with 8-directional connectivity.

    >>> count_islands_iterative_dfs([[1, 1, 0], [0, 1, 0], [0, 0, 1]])
    1
    >>> count_islands_iterative_dfs([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    0
    >>> count_islands_iterative_dfs([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    1
    >>> count_islands_iterative_dfs([[1, 0, 1], [0, 0, 0], [1, 0, 1]])
    4
    >>> count_islands_iterative_dfs([])
    0
    """
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                  (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1 and not visited[i][j]:
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    r, c = stack.pop()
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and grid[nr][nc] == 1:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                count += 1
    return count


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    import random
    random.seed(42)
    size = 50
    grid = [[random.choice([0, 1]) for _ in range(size)] for _ in range(size)]

    number = 1_000
    print(f"Benchmark ({number} runs on {size}x{size} random grid):\n")

    def ref_run() -> int:
        m = ReferenceMatrix(size, size, [row[:] for row in grid])
        return m.count_islands()

    funcs = [
        ("reference (recursive DFS class)", ref_run),
        ("bfs_iterative", lambda: count_islands_bfs(grid)),
        ("union_find", lambda: count_islands_union_find(grid)),
        ("iterative_dfs", lambda: count_islands_iterative_dfs(grid)),
    ]

    for name, func in funcs:
        t = timeit.timeit(func, number=number)
        print(f"  {name:40s} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
