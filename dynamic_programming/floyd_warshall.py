"""
Floyd-Warshall Algorithm — All-pairs shortest paths.

Given a weighted directed graph, find the shortest distances between
every pair of vertices. Uses dynamic programming with O(V^3) time
and O(V^2) space.

Works with negative edge weights (but not negative cycles).

>>> g = Graph(3)
>>> g.add_edge(0, 1, 1)
>>> g.add_edge(1, 2, 2)
>>> g.floyd_warshall()
>>> g.show_min(0, 2)
3
>>> g.show_min(2, 0)
inf
"""

import math


class Graph:
    """
    Weighted directed graph with Floyd-Warshall shortest paths.

    >>> g = Graph(3)
    >>> g.add_edge(0, 1, 5)
    >>> g.dp[0][1]
    5
    """

    def __init__(self, n: int = 0) -> None:
        self.n = n
        self.w = [[math.inf for _ in range(n)] for _ in range(n)]
        self.dp = [[math.inf for _ in range(n)] for _ in range(n)]

    def add_edge(self, u: int, v: int, w: float) -> None:
        """
        Add a directed edge from u to v with weight w.

        >>> g = Graph(3)
        >>> g.add_edge(0, 1, 5)
        >>> g.dp[0][1]
        5
        """
        self.dp[u][v] = w

    def floyd_warshall(self) -> None:
        """
        Compute shortest paths between all pairs of nodes.

        >>> g = Graph(3)
        >>> g.add_edge(0, 1, 1)
        >>> g.add_edge(1, 2, 2)
        >>> g.floyd_warshall()
        >>> g.show_min(0, 2)
        3
        >>> g.show_min(2, 0)
        inf
        """
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    self.dp[i][j] = min(self.dp[i][j], self.dp[i][k] + self.dp[k][j])

    def show_min(self, u: int, v: int) -> float:
        """
        Return the shortest distance from u to v.

        >>> g = Graph(3)
        >>> g.add_edge(0, 1, 3)
        >>> g.add_edge(1, 2, 4)
        >>> g.floyd_warshall()
        >>> g.show_min(0, 2)
        7
        >>> g.show_min(1, 0)
        inf
        """
        return self.dp[u][v]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    graph = Graph(5)
    graph.add_edge(0, 2, 9)
    graph.add_edge(0, 4, 10)
    graph.add_edge(1, 3, 5)
    graph.add_edge(2, 3, 7)
    graph.add_edge(3, 0, 10)
    graph.add_edge(3, 1, 2)
    graph.add_edge(3, 2, 1)
    graph.add_edge(3, 4, 6)
    graph.add_edge(4, 1, 3)
    graph.add_edge(4, 2, 4)
    graph.add_edge(4, 3, 9)
    graph.floyd_warshall()

    print(f"  Shortest 1->4: {graph.show_min(1, 4)}")
    print(f"  Shortest 0->3: {graph.show_min(0, 3)}")
    print(f"  Shortest 4->0: {graph.show_min(4, 0)}")
