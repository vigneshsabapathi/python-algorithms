"""
Depth-First Search - Class-based variant.

Wraps DFS in a Graph class. Demonstrates the same algorithm with OO packaging.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/depth_first_search_2.py

>>> g = Graph()
>>> for u, v in [(0, 1), (0, 9), (1, 8), (9, 8)]:
...     g.add_edge(u, v)
>>> g.dfs(0)
[0, 1, 8, 9]

>>> Graph().dfs(0)
[0]
"""

from collections import defaultdict


class Graph:
    """Undirected graph with DFS traversal.

    >>> g = Graph(); g.add_edge(1, 2); g.dfs(1)
    [1, 2]
    """

    def __init__(self) -> None:
        self.adj: dict = defaultdict(list)

    def add_edge(self, u, v) -> None:
        self.adj[u].append(v)
        self.adj[v].append(u)

    def dfs(self, start) -> list:
        visited = set()
        order: list = []

        def go(u):
            visited.add(u)
            order.append(u)
            for nb in sorted(self.adj[u]):
                if nb not in visited:
                    go(nb)

        go(start)
        return order


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    g = Graph()
    for u, v in [(0, 1), (0, 9), (1, 8), (9, 8)]:
        g.add_edge(u, v)
    print("DFS from 0:", g.dfs(0))
