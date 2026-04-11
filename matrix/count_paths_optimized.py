#!/usr/bin/env python3
"""
Optimized and alternative implementations of Count Paths in Matrix.

The reference uses recursive DFS with 4-directional backtracking. This counts
ALL distinct paths (not just shortest), visiting each cell at most once per path.
Time complexity is exponential in the worst case.

Three alternatives:
  dp_right_down    -- DP for right+down only paths (LeetCode 62/63), O(m*n)
  dp_right_down_obstacles -- DP with obstacles (LeetCode 63), O(m*n)
  memoized_dfs     -- Same 4-dir backtracking but with bitmask memoization

Note: The reference allows 4-directional movement (up/down/left/right), which
is fundamentally different from right+down only. The DP variants solve the
more common interview version (right+down only).

Run:
    python matrix/count_paths_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matrix.count_paths import depth_first_search as reference


# ---------------------------------------------------------------------------
# Variant 1 -- DP right+down only (no obstacles), LeetCode 62
# ---------------------------------------------------------------------------

def count_paths_dp(rows: int, cols: int) -> int:
    """
    Count unique paths from top-left to bottom-right moving only right or down.
    Classic DP: dp[i][j] = dp[i-1][j] + dp[i][j-1].

    >>> count_paths_dp(3, 7)
    28
    >>> count_paths_dp(3, 2)
    3
    >>> count_paths_dp(1, 1)
    1
    >>> count_paths_dp(2, 2)
    2
    >>> count_paths_dp(3, 3)
    6
    """
    dp = [1] * cols
    for _ in range(1, rows):
        for j in range(1, cols):
            dp[j] += dp[j - 1]
    return dp[-1]


# ---------------------------------------------------------------------------
# Variant 2 -- DP right+down with obstacles, LeetCode 63
# ---------------------------------------------------------------------------

def count_paths_dp_obstacles(grid: list[list[int]]) -> int:
    """
    Count unique paths in a grid with obstacles (1=blocked), moving only right/down.
    O(m*n) time, O(n) space.

    >>> count_paths_dp_obstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    2
    >>> count_paths_dp_obstacles([[0, 1], [0, 0]])
    1
    >>> count_paths_dp_obstacles([[1, 0]])
    0
    >>> count_paths_dp_obstacles([[0]])
    1
    >>> count_paths_dp_obstacles([[0, 0], [0, 0]])
    2
    """
    if not grid or grid[0][0] == 1:
        return 0
    rows, cols = len(grid), len(grid[0])
    dp = [0] * cols
    dp[0] = 1

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                dp[j] = 0
            elif j > 0:
                dp[j] += dp[j - 1]
    return dp[-1]


# ---------------------------------------------------------------------------
# Variant 3 -- Combinatorial formula (right+down only, no obstacles)
# ---------------------------------------------------------------------------

def count_paths_combinatorial(rows: int, cols: int) -> int:
    """
    Use combinatorics: C(m+n-2, m-1) where m=rows, n=cols.
    We need (m-1) down moves and (n-1) right moves, total (m+n-2) moves.
    O(min(m,n)) time.

    >>> count_paths_combinatorial(3, 7)
    28
    >>> count_paths_combinatorial(3, 2)
    3
    >>> count_paths_combinatorial(1, 1)
    1
    >>> count_paths_combinatorial(2, 2)
    2
    >>> count_paths_combinatorial(3, 3)
    6
    """
    from math import comb
    return comb(rows + cols - 2, rows - 1)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    # For reference (4-dir), use a small grid since it's exponential
    grid_4dir = [[0, 0, 0, 0], [1, 1, 0, 0], [0, 0, 0, 1], [0, 1, 0, 0]]
    # For DP variants, can use larger grids
    grid_dp = [[0] * 10 for _ in range(10)]

    number = 10_000
    print(f"Benchmark:\n")

    funcs = [
        ("reference 4-dir DFS (4x4)", lambda: reference(grid_4dir, 0, 0, set()), 10_000),
        ("dp_right_down (10x10)", lambda: count_paths_dp(10, 10), 100_000),
        ("dp_obstacles (10x10)", lambda: count_paths_dp_obstacles(grid_dp), 100_000),
        ("combinatorial (10x10)", lambda: count_paths_combinatorial(10, 10), 100_000),
    ]

    for name, func, n in funcs:
        t = timeit.timeit(func, number=n)
        print(f"  {name:40s} {t:.4f}s ({n} runs)")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
