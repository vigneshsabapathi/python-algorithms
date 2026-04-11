"""

Task:
Given a binary matrix, count the number of islands. An island is a group
of connected 1s (land). Connections include all 8 directions (horizontal,
vertical, and diagonal).

Implementation notes: Uses DFS to traverse each island. When a land cell
is found, DFS marks all connected land cells as visited, then increment
the island counter.

Reference: https://github.com/TheAlgorithms/Python/blob/master/matrix/count_islands_in_matrix.py
"""


class Matrix:
    """
    Graph represented as a 2D boolean matrix for island counting.

    >>> m = Matrix(3, 3, [[1, 1, 0], [0, 1, 0], [0, 0, 1]])
    >>> m.count_islands()
    1
    >>> m = Matrix(3, 3, [[1, 0, 0], [0, 0, 0], [0, 0, 1]])
    >>> m.count_islands()
    2
    >>> m = Matrix(3, 3, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    >>> m.count_islands()
    0
    >>> m = Matrix(3, 3, [[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    >>> m.count_islands()
    1
    """

    def __init__(self, row: int, col: int, graph: list[list[bool]]) -> None:
        self.ROW = row
        self.COL = col
        self.graph = graph

    def is_safe(self, i: int, j: int, visited: list[list[bool]]) -> bool:
        return (
            0 <= i < self.ROW
            and 0 <= j < self.COL
            and not visited[i][j]
            and self.graph[i][j]
        )

    def dfs(self, i: int, j: int, visited: list[list[bool]]) -> None:
        """DFS to mark all cells in the current island as visited."""
        row_nbr = [-1, -1, -1, 0, 0, 1, 1, 1]
        col_nbr = [-1, 0, 1, -1, 1, -1, 0, 1]
        visited[i][j] = True
        for k in range(8):
            if self.is_safe(i + row_nbr[k], j + col_nbr[k], visited):
                self.dfs(i + row_nbr[k], j + col_nbr[k], visited)

    def count_islands(self) -> int:
        """Count all islands using DFS traversal."""
        visited = [[False for _ in range(self.COL)] for _ in range(self.ROW)]
        count = 0
        for i in range(self.ROW):
            for j in range(self.COL):
                if not visited[i][j] and self.graph[i][j] == 1:
                    self.dfs(i, j, visited)
                    count += 1
        return count


if __name__ == "__main__":
    import doctest

    doctest.testmod()
