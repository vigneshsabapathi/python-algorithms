# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/minimum_cost_path.py


def minimum_cost_path(grid: list[list[int]]) -> int:
    """
    Find minimum cost path from top-left to bottom-right in a grid.
    Can only move right or down.

    >>> minimum_cost_path([[1, 3, 1], [1, 5, 1], [4, 2, 1]])
    7
    >>> minimum_cost_path([[1, 2, 3], [4, 5, 6]])
    12
    >>> minimum_cost_path([[1]])
    1
    >>> minimum_cost_path([[1, 2], [1, 1]])
    3
    """
    if not grid or not grid[0]:
        return 0

    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = grid[0][0]

    for i in range(1, m):
        dp[i][0] = dp[i - 1][0] + grid[i][0]
    for j in range(1, n):
        dp[0][j] = dp[0][j - 1] + grid[0][j]

    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = grid[i][j] + min(dp[i - 1][j], dp[i][j - 1])

    return dp[m - 1][n - 1]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        ([[1, 3, 1], [1, 5, 1], [4, 2, 1]], 7),
        ([[1, 2, 3], [4, 5, 6]], 12),
        ([[1]], 1),
        ([[1, 2], [1, 1]], 3),
    ]
    for grid, expected in cases:
        result = minimum_cost_path(grid)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] minimum_cost_path({grid}) = {result}  (expected {expected})")
