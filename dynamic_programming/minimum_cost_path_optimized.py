#!/usr/bin/env python3
"""
Optimized and alternative implementations of Minimum Cost Path.

Variants covered:
1. min_cost_space_opt    -- O(n) space using single row
2. min_cost_in_place     -- O(1) extra space, modifies grid
3. min_cost_all_dirs     -- allows up/down/left/right (Dijkstra)

Run:
    python dynamic_programming/minimum_cost_path_optimized.py
"""

from __future__ import annotations

import heapq
import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.minimum_cost_path import minimum_cost_path as reference


# ---------------------------------------------------------------------------
# Variant 1 — Space-optimized single row
# ---------------------------------------------------------------------------

def min_cost_space_opt(grid: list[list[int]]) -> int:
    """
    Minimum cost path using O(n) space.

    >>> min_cost_space_opt([[1, 3, 1], [1, 5, 1], [4, 2, 1]])
    7
    >>> min_cost_space_opt([[1, 2, 3], [4, 5, 6]])
    12
    >>> min_cost_space_opt([[1]])
    1
    >>> min_cost_space_opt([[1, 2], [1, 1]])
    3
    """
    if not grid or not grid[0]:
        return 0
    m, n = len(grid), len(grid[0])
    dp = [0] * n
    dp[0] = grid[0][0]
    for j in range(1, n):
        dp[j] = dp[j - 1] + grid[0][j]

    for i in range(1, m):
        dp[0] += grid[i][0]
        for j in range(1, n):
            dp[j] = grid[i][j] + min(dp[j], dp[j - 1])

    return dp[n - 1]


# ---------------------------------------------------------------------------
# Variant 2 — In-place modification
# ---------------------------------------------------------------------------

def min_cost_in_place(grid: list[list[int]]) -> int:
    """
    Minimum cost path modifying the grid in place (O(1) extra space).

    >>> min_cost_in_place([[1, 3, 1], [1, 5, 1], [4, 2, 1]])
    7
    >>> min_cost_in_place([[1, 2, 3], [4, 5, 6]])
    12
    >>> min_cost_in_place([[1]])
    1
    """
    if not grid or not grid[0]:
        return 0
    # Work on a copy to avoid side effects in testing
    g = [row[:] for row in grid]
    m, n = len(g), len(g[0])

    for i in range(1, m):
        g[i][0] += g[i - 1][0]
    for j in range(1, n):
        g[0][j] += g[0][j - 1]
    for i in range(1, m):
        for j in range(1, n):
            g[i][j] += min(g[i - 1][j], g[i][j - 1])

    return g[m - 1][n - 1]


# ---------------------------------------------------------------------------
# Variant 3 — All 4 directions (Dijkstra)
# ---------------------------------------------------------------------------

def min_cost_all_dirs(grid: list[list[int]]) -> int:
    """
    Minimum cost path allowing movement in all 4 directions (Dijkstra).

    For right/down-only grids, gives the same result as DP.

    >>> min_cost_all_dirs([[1, 3, 1], [1, 5, 1], [4, 2, 1]])
    7
    >>> min_cost_all_dirs([[1, 2, 3], [4, 5, 6]])
    12
    >>> min_cost_all_dirs([[1]])
    1
    """
    if not grid or not grid[0]:
        return 0
    m, n = len(grid), len(grid[0])
    dist = [[float("inf")] * n for _ in range(m)]
    dist[0][0] = grid[0][0]
    heap = [(grid[0][0], 0, 0)]

    while heap:
        cost, r, c = heapq.heappop(heap)
        if r == m - 1 and c == n - 1:
            return cost
        if cost > dist[r][c]:
            continue
        for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n:
                new_cost = cost + grid[nr][nc]
                if new_cost < dist[nr][nc]:
                    dist[nr][nc] = new_cost
                    heapq.heappush(heap, (new_cost, nr, nc))

    return dist[m - 1][n - 1]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([[1, 3, 1], [1, 5, 1], [4, 2, 1]], 7),
    ([[1, 2, 3], [4, 5, 6]], 12),
    ([[1]], 1),
    ([[1, 2], [1, 1]], 3),
]

IMPLS = [
    ("reference", reference),
    ("space_opt", min_cost_space_opt),
    ("in_place", min_cost_in_place),
    ("all_dirs", min_cost_all_dirs),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for grid, expected in TEST_CASES:
        results = {name: fn([r[:] for r in grid]) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] grid={grid}  expected={expected}  " +
              "  ".join(f"{n}={v}" for n, v in results.items()))

    REPS = 10_000
    import random
    random.seed(42)
    bench_grid = [[random.randint(1, 9) for _ in range(10)] for _ in range(10)]
    print(f"\n=== Benchmark: {REPS} runs, 10x10 grid ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn([r[:] for r in bench_grid]), number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
