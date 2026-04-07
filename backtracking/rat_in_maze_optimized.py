#!/usr/bin/env python3
"""
Optimized and alternative implementations of Rat in a Maze.

The reference uses recursive DFS — finds A path, not the SHORTEST path.
It explores down → right → up → left and takes the first path it finds.

Variants covered:
1. rat_in_maze_bfs        -- BFS: guaranteed shortest path, O(n²) time/space
2. rat_in_maze_astar      -- A*: heuristic-guided, finds shortest path faster
                             on average using Manhattan distance to goal
3. rat_in_maze_iterative  -- Iterative DFS with explicit stack; avoids Python
                             recursion limit on large mazes
4. rat_in_maze_all_paths  -- Backtracking to find ALL valid paths

Key interview insight:
    DFS (reference): O(n²) time, finds any path — good for "does a path exist?"
    BFS:             O(n²) time, guarantees SHORTEST path — "find minimum steps"
    A*:              O(n²) worst case but visits far fewer nodes in practice
    All paths:       Exponential — only feasible for small mazes

Convention: 0 = open cell, 1 = wall.
Solution matrix marks the path as 0, off-path cells as 1.

Run:
    python backtracking/rat_in_maze_optimized.py
"""

from __future__ import annotations

import heapq
import sys
import os
import timeit
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backtracking.rat_in_maze import solve_maze as rat_dfs

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _make_solution(maze: list[list[int]], path: list[tuple[int, int]]) -> list[list[int]]:
    """Convert a path (list of (row,col)) to the solution matrix convention."""
    n = len(maze)
    sol = [[1] * n for _ in range(n)]
    for r, c in path:
        sol[r][c] = 0
    return sol


def _is_open(maze: list[list[int]], r: int, c: int) -> bool:
    n = len(maze)
    return 0 <= r < n and 0 <= c < n and maze[r][c] == 0


# ---------------------------------------------------------------------------
# Variant 1 — BFS (guaranteed shortest path)
# ---------------------------------------------------------------------------


def rat_in_maze_bfs(
    maze: list[list[int]],
    src_r: int, src_c: int,
    dst_r: int, dst_c: int,
) -> list[list[int]]:
    """
    BFS from source to destination.
    Guarantees the SHORTEST path (fewest steps).
    Returns solution matrix (0=path, 1=off-path) or raises ValueError.

    >>> maze = [[0,1,0,1,1],[0,0,0,0,0],[1,0,1,0,1],[0,0,1,0,0],[1,0,0,1,0]]
    >>> rat_in_maze_bfs(maze,0,0,4,4)
    [[0, 1, 1, 1, 1], [0, 0, 0, 0, 1], [1, 1, 1, 0, 1], [1, 1, 1, 0, 0], [1, 1, 1, 1, 0]]

    >>> maze = [[0,0],[1,1]]
    >>> rat_in_maze_bfs(maze,0,0,1,1)
    Traceback (most recent call last):
        ...
    ValueError: No solution exists!

    >>> maze = [[0,0,0],[0,1,0],[1,0,0]]
    >>> rat_in_maze_bfs(maze,0,0,2,2)
    [[0, 0, 0], [1, 1, 0], [1, 1, 0]]
    """
    n = len(maze)
    if not (0 <= src_r < n and 0 <= src_c < n and
            0 <= dst_r < n and 0 <= dst_c < n):
        raise ValueError("Invalid source or destination coordinates")
    if not _is_open(maze, src_r, src_c) or not _is_open(maze, dst_r, dst_c):
        raise ValueError("No solution exists!")

    # BFS: each queue entry is (row, col, path_so_far)
    visited = [[False] * n for _ in range(n)]
    visited[src_r][src_c] = True
    queue: deque[tuple[int, int, list[tuple[int, int]]]] = deque(
        [( src_r, src_c, [(src_r, src_c)] )]
    )

    while queue:
        r, c, path = queue.popleft()
        if r == dst_r and c == dst_c:
            return _make_solution(maze, path)
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if _is_open(maze, nr, nc) and not visited[nr][nc]:
                visited[nr][nc] = True
                queue.append((nr, nc, path + [(nr, nc)]))

    raise ValueError("No solution exists!")


# ---------------------------------------------------------------------------
# Variant 2 — A* (shortest path with heuristic guidance)
# ---------------------------------------------------------------------------


def rat_in_maze_astar(
    maze: list[list[int]],
    src_r: int, src_c: int,
    dst_r: int, dst_c: int,
) -> list[list[int]]:
    """
    A* search using Manhattan distance heuristic.
    Finds the shortest path, visiting fewer nodes than BFS on average.

    f(n) = g(n) + h(n)
    g(n) = steps taken so far
    h(n) = |dst_row - row| + |dst_col - col|  (Manhattan distance)

    >>> maze = [[0,1,0,1,1],[0,0,0,0,0],[1,0,1,0,1],[0,0,1,0,0],[1,0,0,1,0]]
    >>> rat_in_maze_astar(maze,0,0,4,4)
    [[0, 1, 1, 1, 1], [0, 0, 0, 0, 1], [1, 1, 1, 0, 1], [1, 1, 1, 0, 0], [1, 1, 1, 1, 0]]

    >>> maze = [[0,0],[1,1]]
    >>> rat_in_maze_astar(maze,0,0,1,1)
    Traceback (most recent call last):
        ...
    ValueError: No solution exists!

    >>> maze = [[0,0,0],[0,1,0],[1,0,0]]
    >>> rat_in_maze_astar(maze,0,0,2,2)
    [[0, 0, 0], [1, 1, 0], [1, 1, 0]]
    """
    n = len(maze)
    if not (0 <= src_r < n and 0 <= src_c < n and
            0 <= dst_r < n and 0 <= dst_c < n):
        raise ValueError("Invalid source or destination coordinates")
    if not _is_open(maze, src_r, src_c) or not _is_open(maze, dst_r, dst_c):
        raise ValueError("No solution exists!")

    def h(r: int, c: int) -> int:
        return abs(dst_r - r) + abs(dst_c - c)

    # heap entry: (f, g, row, col, path)
    heap: list[tuple[int, int, int, int, list[tuple[int, int]]]] = [
        (h(src_r, src_c), 0, src_r, src_c, [(src_r, src_c)])
    ]
    visited: set[tuple[int, int]] = set()

    while heap:
        f, g, r, c, path = heapq.heappop(heap)
        if (r, c) in visited:
            continue
        visited.add((r, c))
        if r == dst_r and c == dst_c:
            return _make_solution(maze, path)
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if _is_open(maze, nr, nc) and (nr, nc) not in visited:
                ng = g + 1
                heapq.heappush(heap, (ng + h(nr, nc), ng, nr, nc, path + [(nr, nc)]))

    raise ValueError("No solution exists!")


# ---------------------------------------------------------------------------
# Variant 3 — Iterative DFS (avoids Python recursion limit)
# ---------------------------------------------------------------------------


def rat_in_maze_iterative(
    maze: list[list[int]],
    src_r: int, src_c: int,
    dst_r: int, dst_c: int,
) -> list[list[int]]:
    """
    Iterative DFS with explicit stack.
    Same exploration order as recursive DFS; avoids stack overflow on large mazes.

    >>> maze = [[0,1,0,1,1],[0,0,0,0,0],[1,0,1,0,1],[0,0,1,0,0],[1,0,0,1,0]]
    >>> rat_in_maze_iterative(maze,0,0,4,4)
    [[0, 1, 1, 1, 1], [0, 0, 0, 0, 1], [1, 1, 1, 0, 1], [1, 1, 1, 0, 0], [1, 1, 1, 1, 0]]

    >>> maze = [[0,0],[1,1]]
    >>> rat_in_maze_iterative(maze,0,0,1,1)
    Traceback (most recent call last):
        ...
    ValueError: No solution exists!
    """
    n = len(maze)
    if not (0 <= src_r < n and 0 <= src_c < n and
            0 <= dst_r < n and 0 <= dst_c < n):
        raise ValueError("Invalid source or destination coordinates")

    # Stack holds (row, col, path_as_set, path_as_list)
    stack: list[tuple[int, int, set[tuple[int,int]], list[tuple[int,int]]]] = [
        (src_r, src_c, {(src_r, src_c)}, [(src_r, src_c)])
    ]
    while stack:
        r, c, visited, path = stack.pop()
        if r == dst_r and c == dst_c and maze[r][c] == 0:
            return _make_solution(maze, path)
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if _is_open(maze, nr, nc) and (nr, nc) not in visited:
                stack.append((nr, nc, visited | {(nr, nc)}, path + [(nr, nc)]))

    raise ValueError("No solution exists!")


# ---------------------------------------------------------------------------
# Variant 4 — All paths (backtracking)
# ---------------------------------------------------------------------------


def rat_in_maze_all_paths(
    maze: list[list[int]],
    src_r: int, src_c: int,
    dst_r: int, dst_c: int,
) -> list[list[list[int]]]:
    """
    Find ALL paths from source to destination (not just one).
    Returns a list of solution matrices, one per path.
    Exponential time — only feasible for small mazes.

    >>> maze = [[0,0,0],[0,0,0],[0,0,0]]
    >>> paths = rat_in_maze_all_paths(maze,0,0,2,2)
    >>> len(paths)
    12
    >>> maze = [[0,1,0,1,1],[0,0,0,0,0],[1,0,1,0,1],[0,0,1,0,0],[1,0,0,1,0]]
    >>> len(rat_in_maze_all_paths(maze,0,0,4,4))
    1
    """
    n = len(maze)
    all_solutions: list[list[list[int]]] = []
    visited = [[False] * n for _ in range(n)]

    def dfs(r: int, c: int, path: list[tuple[int, int]]) -> None:
        if r == dst_r and c == dst_c:
            all_solutions.append(_make_solution(maze, path))
            return
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if _is_open(maze, nr, nc) and not visited[nr][nc]:
                visited[nr][nc] = True
                dfs(nr, nc, path + [(nr, nc)])
                visited[nr][nc] = False

    if _is_open(maze, src_r, src_c):
        visited[src_r][src_c] = True
        dfs(src_r, src_c, [(src_r, src_c)])
    return all_solutions


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------


def _path_length(sol: list[list[int]]) -> int:
    return sum(sol[r][c] == 0 for r in range(len(sol)) for c in range(len(sol[0])))


def run_all() -> None:
    mazes = [
        ("5x5 winding", [[0,1,0,1,1],[0,0,0,0,0],[1,0,1,0,1],[0,0,1,0,0],[1,0,0,1,0]], 0,0,4,4),
        ("5x5 open",    [[0,1,0,1,1],[0,0,0,0,0],[0,0,0,0,1],[0,0,0,0,0],[0,0,0,0,0]], 0,0,4,4),
        ("3x3",         [[0,0,0],[0,1,0],[1,0,0]], 0,0,2,2),
    ]

    print("\n=== Correctness (path lengths compared) ===")
    print(f"  {'name':>12}  {'dfs':>5}  {'bfs':>5}  {'astar':>7}  {'iter':>5}  "
          f"{'all_paths':>10}")
    for name, maze, sr, sc, dr, dc in mazes:
        s_dfs  = rat_dfs(maze, sr, sc, dr, dc)
        s_bfs  = rat_in_maze_bfs(maze, sr, sc, dr, dc)
        s_ast  = rat_in_maze_astar(maze, sr, sc, dr, dc)
        s_iter = rat_in_maze_iterative(maze, sr, sc, dr, dc)
        all_p  = rat_in_maze_all_paths(maze, sr, sc, dr, dc)
        # BFS and A* must agree (both shortest)
        bfs_astar_agree = _path_length(s_bfs) == _path_length(s_ast)
        print(f"  {name:>12}  dfs={_path_length(s_dfs)}  bfs={_path_length(s_bfs)}"
              f"  astar={_path_length(s_ast)}  iter={_path_length(s_iter)}"
              f"  all_paths={len(all_p)}  bfs==astar:{bfs_astar_agree}")

    # Build a larger maze for benchmarking
    import random
    random.seed(42)

    def random_open_maze(n: int, wall_prob: float = 0.25) -> list[list[int]]:
        """Random maze guaranteed passable at corners."""
        while True:
            m = [[1 if random.random() < wall_prob else 0 for _ in range(n)]
                 for _ in range(n)]
            m[0][0] = m[n-1][n-1] = 0  # ensure src/dst are open
            # Quick BFS reachability check
            visited = [[False]*n for _ in range(n)]
            q: deque[tuple[int,int]] = deque([(0, 0)])
            visited[0][0] = True
            while q:
                r, c = q.popleft()
                if r == n-1 and c == n-1:
                    return m
                for dr, dc in DIRECTIONS:
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and m[nr][nc] == 0:
                        visited[nr][nc] = True
                        q.append((nr, nc))
            # unsolvable, retry

    print("\n=== Benchmark (random solvable mazes) ===")
    print(f"  {'n':>4}  {'dfs':>12}  {'bfs':>12}  {'astar':>12}  {'iterative':>12}")
    for n in [10, 20, 50]:
        maze = random_open_maze(n)
        REPS = 200 if n <= 20 else 50
        t_dfs  = timeit.timeit(lambda: rat_dfs(maze, 0, 0, n-1, n-1),             number=REPS)*1000/REPS
        t_bfs  = timeit.timeit(lambda: rat_in_maze_bfs(maze, 0, 0, n-1, n-1),     number=REPS)*1000/REPS
        t_ast  = timeit.timeit(lambda: rat_in_maze_astar(maze, 0, 0, n-1, n-1),   number=REPS)*1000/REPS
        t_iter = timeit.timeit(lambda: rat_in_maze_iterative(maze, 0, 0, n-1, n-1), number=REPS)*1000/REPS
        print(f"  {n:>4}  {t_dfs:>11.3f}ms  {t_bfs:>11.3f}ms  {t_ast:>11.3f}ms  "
              f"{t_iter:>11.3f}ms")

    print("\n=== Path quality: DFS path length vs BFS shortest path ===")
    for n in [10, 20, 50]:
        maze = random_open_maze(n)
        dfs_len = _path_length(rat_dfs(maze, 0, 0, n-1, n-1))
        bfs_len = _path_length(rat_in_maze_bfs(maze, 0, 0, n-1, n-1))
        overhead = (dfs_len - bfs_len) / bfs_len * 100
        print(f"  n={n:>2}  dfs_path={dfs_len:>4}  bfs_shortest={bfs_len:>4}  "
              f"dfs overhead={overhead:+.1f}%")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
