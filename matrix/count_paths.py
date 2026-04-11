"""

Task:
Given a grid with obstacles (1 = blocked, 0 = open), count the number
of distinct paths from top-left to bottom-right. Movement is allowed
in all 4 directions (up, down, left, right) with backtracking.

Implementation notes: Uses recursive DFS with backtracking. A visited set
prevents revisiting cells. Moves in all 4 directions, not just right/down.

Reference: https://github.com/TheAlgorithms/Python/blob/master/matrix/count_paths.py
"""


def depth_first_search(grid: list[list[int]], row: int, col: int, visit: set) -> int:
    """
    Recursive backtracking DFS to count distinct paths from (row, col)
    to the bottom-right corner of the grid.

    0 = accessible, 1 = blocked.

    >>> grid = [[0, 0, 0, 0], [1, 1, 0, 0], [0, 0, 0, 1], [0, 1, 0, 0]]
    >>> depth_first_search(grid, 0, 0, set())
    2

    >>> grid = [[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0]]
    >>> depth_first_search(grid, 0, 0, set())
    2

    >>> grid = [[0, 1], [1, 0]]
    >>> depth_first_search(grid, 0, 0, set())
    0

    >>> grid = [[0]]
    >>> depth_first_search(grid, 0, 0, set())
    1
    """
    row_length, col_length = len(grid), len(grid[0])
    if (
        min(row, col) < 0
        or row == row_length
        or col == col_length
        or (row, col) in visit
        or grid[row][col] == 1
    ):
        return 0
    if row == row_length - 1 and col == col_length - 1:
        return 1

    visit.add((row, col))

    count = 0
    count += depth_first_search(grid, row + 1, col, visit)
    count += depth_first_search(grid, row - 1, col, visit)
    count += depth_first_search(grid, row, col + 1, visit)
    count += depth_first_search(grid, row, col - 1, visit)

    visit.remove((row, col))
    return count


if __name__ == "__main__":
    import doctest

    doctest.testmod()
