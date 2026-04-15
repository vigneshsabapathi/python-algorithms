"""
Minimum Path Sum in Grid - Optimized Variants

Find the path from top-left to bottom-right with minimum sum,
moving only right or down.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/minimum_path_sum.py
"""

import time


# ---------- Variant 1: O(n) space (single row) ----------
def min_path_sum_1d(grid: list[list[int]]) -> int:
    """
    O(cols) space using single rolling array.

    >>> min_path_sum_1d([[1, 3, 1], [1, 5, 1], [4, 2, 1]])
    7
    >>> min_path_sum_1d([[1, 0, 5, 6, 7], [8, 9, 0, 4, 2], [4, 4, 4, 5, 1], [9, 6, 3, 1, 0], [8, 4, 3, 2, 7]])
    20
    """
    if not grid or not grid[0]:
        raise TypeError("The grid does not contain the appropriate information")

    rows, cols = len(grid), len(grid[0])
    dp = list(grid[0])
    for j in range(1, cols):
        dp[j] += dp[j - 1]

    for i in range(1, rows):
        dp[0] += grid[i][0]
        for j in range(1, cols):
            dp[j] = grid[i][j] + min(dp[j], dp[j - 1])

    return dp[-1]


# ---------- Variant 2: With path reconstruction ----------
def min_path_sum_with_path(grid: list[list[int]]) -> tuple[int, list[tuple[int, int]]]:
    """
    Returns both the minimum sum and the actual path taken.

    >>> cost, path = min_path_sum_with_path([[1, 3, 1], [1, 5, 1], [4, 2, 1]])
    >>> cost
    7
    >>> path
    [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]
    """
    if not grid or not grid[0]:
        raise TypeError("The grid does not contain the appropriate information")

    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]

    for j in range(1, cols):
        dp[0][j] = dp[0][j - 1] + grid[0][j]
    for i in range(1, rows):
        dp[i][0] = dp[i - 1][0] + grid[i][0]
    for i in range(1, rows):
        for j in range(1, cols):
            dp[i][j] = grid[i][j] + min(dp[i - 1][j], dp[i][j - 1])

    # Backtrack
    path = [(rows - 1, cols - 1)]
    i, j = rows - 1, cols - 1
    while i > 0 or j > 0:
        if i == 0:
            j -= 1
        elif j == 0:
            i -= 1
        elif dp[i - 1][j] < dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
        path.append((i, j))

    return dp[-1][-1], path[::-1]


# ---------- Variant 3: In-place modification (zero extra space) ----------
def min_path_sum_inplace(grid: list[list[int]]) -> int:
    """
    Modifies grid in-place for O(1) extra space.

    >>> min_path_sum_inplace([[1, 3, 1], [1, 5, 1], [4, 2, 1]])
    7
    """
    if not grid or not grid[0]:
        raise TypeError("The grid does not contain the appropriate information")

    rows, cols = len(grid), len(grid[0])
    for j in range(1, cols):
        grid[0][j] += grid[0][j - 1]
    for i in range(1, rows):
        grid[i][0] += grid[i - 1][0]
        for j in range(1, cols):
            grid[i][j] += min(grid[i - 1][j], grid[i][j - 1])
    return grid[-1][-1]


# ---------- Benchmark ----------
def benchmark():
    import random
    random.seed(42)
    n = 200
    grid = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]

    for name, fn in [
        ("1d_space", lambda: min_path_sum_1d([row[:] for row in grid])),
        ("with_path", lambda: min_path_sum_with_path([row[:] for row in grid])),
        ("inplace", lambda: min_path_sum_inplace([row[:] for row in grid])),
    ]:
        start = time.perf_counter()
        for _ in range(50):
            result = fn()
        elapsed = (time.perf_counter() - start) / 50 * 1000
        val = result[0] if isinstance(result, tuple) else result
        print(f"  {name:20s}: {elapsed:.3f} ms (min sum: {val})")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Minimum Path Sum Benchmark (200x200, 50 runs) ===")
    benchmark()
