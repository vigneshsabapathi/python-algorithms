#!/usr/bin/env python3
"""
Optimized and alternative implementations of Max Area of Island (LeetCode 695).

The reference uses recursive DFS with a set for visited tracking.
Time O(m*n), Space O(m*n).

Three alternatives:
  bfs_iterative     -- BFS with deque, avoids recursion depth issues
  iterative_dfs     -- Explicit stack DFS
  union_find        -- DSU to find largest connected component

Run:
    python matrix/max_area_of_island_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matrix.max_area_of_island import find_max_area as reference

matrix = [
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
]


# ---------------------------------------------------------------------------
# Variant 1 -- BFS iterative
# ---------------------------------------------------------------------------

def max_area_bfs(grid: list[list[int]]) -> int:
    """
    Find max island area using BFS.

    >>> max_area_bfs(matrix)
    6
    >>> max_area_bfs([[0, 0], [0, 0]])
    0
    >>> max_area_bfs([[1, 1], [1, 1]])
    4
    """
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    seen = set()
    max_area = 0

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1 and (i, j) not in seen:
                area = 0
                queue = deque([(i, j)])
                seen.add((i, j))
                while queue:
                    r, c = queue.popleft()
                    area += 1
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in seen and grid[nr][nc] == 1:
                            seen.add((nr, nc))
                            queue.append((nr, nc))
                max_area = max(max_area, area)

    return max_area


# ---------------------------------------------------------------------------
# Variant 2 -- Iterative DFS with explicit stack
# ---------------------------------------------------------------------------

def max_area_iterative_dfs(grid: list[list[int]]) -> int:
    """
    Find max island area using iterative DFS.

    >>> max_area_iterative_dfs(matrix)
    6
    >>> max_area_iterative_dfs([[0, 0], [0, 0]])
    0
    >>> max_area_iterative_dfs([[1, 1], [1, 1]])
    4
    """
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    seen = set()
    max_area = 0

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1 and (i, j) not in seen:
                area = 0
                stack = [(i, j)]
                seen.add((i, j))
                while stack:
                    r, c = stack.pop()
                    area += 1
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in seen and grid[nr][nc] == 1:
                            seen.add((nr, nc))
                            stack.append((nr, nc))
                max_area = max(max_area, area)

    return max_area


# ---------------------------------------------------------------------------
# Variant 3 -- Union-Find
# ---------------------------------------------------------------------------

def max_area_union_find(grid: list[list[int]]) -> int:
    """
    Find max island area using Union-Find (DSU).

    >>> max_area_union_find(matrix)
    6
    >>> max_area_union_find([[0, 0], [0, 0]])
    0
    >>> max_area_union_find([[1, 1], [1, 1]])
    4
    """
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    parent = list(range(rows * cols))
    rank = [0] * (rows * cols)
    size = [1] * (rows * cols)

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        if rank[ra] == rank[rb]:
            rank[ra] += 1

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                for di, dj in [(0, 1), (1, 0)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == 1:
                        union(i * cols + j, ni * cols + nj)

    max_area = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                max_area = max(max_area, size[find(i * cols + j)])

    return max_area


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    number = 10_000
    print(f"Benchmark ({number} runs on 8x13 grid):\n")

    funcs = [
        ("reference (recursive DFS)", lambda: reference(matrix)),
        ("bfs_iterative", lambda: max_area_bfs(matrix)),
        ("iterative_dfs", lambda: max_area_iterative_dfs(matrix)),
        ("union_find", lambda: max_area_union_find(matrix)),
    ]

    for name, func in funcs:
        t = timeit.timeit(func, number=number)
        print(f"  {name:30s} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
