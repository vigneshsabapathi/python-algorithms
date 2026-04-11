"""

Task:
Given a 2D binary grid, find the maximum area of an island. An island is
a group of 1s connected 4-directionally (horizontal/vertical). All edges
are surrounded by water (0s). Return 0 if no island exists.

Implementation notes: DFS from each unvisited land cell, counting area.
Track maximum area across all islands.

Reference: https://leetcode.com/problems/max-area-of-island/ (LeetCode 695)
Reference: https://github.com/TheAlgorithms/Python/blob/master/matrix/max_area_of_island.py
"""


def is_safe(row: int, col: int, rows: int, cols: int) -> bool:
    """
    Check if coordinate (row, col) is within grid bounds.

    >>> is_safe(0, 0, 5, 5)
    True
    >>> is_safe(-1, -1, 5, 5)
    False
    """
    return 0 <= row < rows and 0 <= col < cols


def depth_first_search(row: int, col: int, seen: set, mat: list[list[int]]) -> int:
    """
    DFS to compute island area starting from (row, col).

    >>> depth_first_search(0, 0, set(), [[0]])
    0
    >>> depth_first_search(0, 0, set(), [[1]])
    1
    """
    rows = len(mat)
    cols = len(mat[0])
    if is_safe(row, col, rows, cols) and (row, col) not in seen and mat[row][col] == 1:
        seen.add((row, col))
        return (
            1
            + depth_first_search(row + 1, col, seen, mat)
            + depth_first_search(row - 1, col, seen, mat)
            + depth_first_search(row, col + 1, seen, mat)
            + depth_first_search(row, col - 1, seen, mat)
        )
    return 0


def find_max_area(mat: list[list[int]]) -> int:
    """
    Find maximum island area in a binary grid.

    >>> find_max_area([[0,0,1,0,0,0,0,1,0,0,0,0,0],
    ...               [0,0,0,0,0,0,0,1,1,1,0,0,0],
    ...               [0,1,1,0,1,0,0,0,0,0,0,0,0],
    ...               [0,1,0,0,1,1,0,0,1,0,1,0,0],
    ...               [0,1,0,0,1,1,0,0,1,1,1,0,0],
    ...               [0,0,0,0,0,0,0,0,0,0,1,0,0],
    ...               [0,0,0,0,0,0,0,1,1,1,0,0,0],
    ...               [0,0,0,0,0,0,0,1,1,0,0,0,0]])
    6
    >>> find_max_area([[0, 0], [0, 0]])
    0
    >>> find_max_area([[1, 1], [1, 1]])
    4
    """
    seen: set = set()
    max_area = 0
    for row, line in enumerate(mat):
        for col, item in enumerate(line):
            if item == 1 and (row, col) not in seen:
                max_area = max(max_area, depth_first_search(row, col, seen, mat))
    return max_area


if __name__ == "__main__":
    import doctest

    doctest.testmod()
