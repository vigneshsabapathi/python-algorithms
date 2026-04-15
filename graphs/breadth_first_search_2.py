"""
Breadth-First Search - Class-based with explicit adjacency list.

This variant wraps BFS in a Graph class with add_edge/print_bfs.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/breadth_first_search_2.py

>>> g = Graph()
>>> for u, v in [(0, 1), (0, 2), (1, 2), (2, 0), (2, 3), (3, 3)]:
...     g.add_edge(u, v)
>>> g.bfs(2)
[2, 0, 3, 1]

>>> Graph().bfs(0)
[]
"""

from collections import defaultdict, deque


class Graph:
    """Directed graph using adjacency list.

    >>> g = Graph()
    >>> g.add_edge(1, 2)
    >>> g.bfs(1)
    [1, 2]
    """

    def __init__(self) -> None:
        self.adj: dict = defaultdict(list)

    def add_edge(self, u, v) -> None:
        self.adj[u].append(v)

    def bfs(self, start) -> list:
        if start not in self.adj and not any(start in vs for vs in self.adj.values()):
            return []
        visited = {start}
        order = []
        q = deque([start])
        while q:
            node = q.popleft()
            order.append(node)
            for nb in self.adj[node]:
                if nb not in visited:
                    visited.add(nb)
                    q.append(nb)
        return order


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    g = Graph()
    for u, v in [(0, 1), (0, 2), (1, 2), (2, 0), (2, 3), (3, 3)]:
        g.add_edge(u, v)
    print("BFS from 2:", g.bfs(2))
