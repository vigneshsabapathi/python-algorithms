"""
Basic Graph Operations and Representations.

Fundamental graph data structures and traversals: adjacency list, adjacency matrix,
edge list, BFS, DFS, topological sort, and cycle detection.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/basic_graphs.py

>>> g = AdjacencyListGraph()
>>> g.add_edge(0, 1)
>>> g.add_edge(0, 2)
>>> g.add_edge(1, 3)
>>> g.add_edge(2, 3)
>>> g.bfs(0)
[0, 1, 2, 3]
>>> g.dfs(0)
[0, 1, 3, 2]
"""

from collections import defaultdict, deque


class AdjacencyListGraph:
    """
    Graph using adjacency list representation.

    >>> g = AdjacencyListGraph(directed=True)
    >>> g.add_edge(0, 1)
    >>> g.add_edge(1, 2)
    >>> g.add_edge(0, 2)
    >>> g.bfs(0)
    [0, 1, 2]
    >>> g.has_edge(0, 1)
    True
    >>> g.has_edge(1, 0)
    False
    """

    def __init__(self, directed: bool = False) -> None:
        self.graph: dict[int, list[int]] = defaultdict(list)
        self.directed = directed

    def add_edge(self, u: int, v: int) -> None:
        self.graph[u].append(v)
        if not self.directed:
            self.graph[v].append(u)
        # Ensure nodes exist
        if v not in self.graph:
            self.graph[v] = []

    def has_edge(self, u: int, v: int) -> bool:
        return v in self.graph.get(u, [])

    def bfs(self, start: int) -> list[int]:
        """
        Breadth-first search traversal.

        >>> g = AdjacencyListGraph()
        >>> for u, v in [(0,1),(0,2),(1,3)]: g.add_edge(u, v)
        >>> g.bfs(0)
        [0, 1, 2, 3]
        """
        visited = {start}
        queue = deque([start])
        order = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in sorted(self.graph[node]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return order

    def dfs(self, start: int) -> list[int]:
        """
        Depth-first search traversal (iterative).

        >>> g = AdjacencyListGraph()
        >>> for u, v in [(0,1),(0,2),(1,3)]: g.add_edge(u, v)
        >>> g.dfs(0)
        [0, 1, 3, 2]
        """
        visited: set[int] = set()
        stack = [start]
        order = []
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                order.append(node)
                for neighbor in sorted(self.graph[node], reverse=True):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return order

    def topological_sort(self) -> list[int]:
        """
        Topological sort using Kahn's algorithm (directed graphs only).

        >>> g = AdjacencyListGraph(directed=True)
        >>> for u, v in [(5,2),(5,0),(4,0),(4,1),(2,3),(3,1)]: g.add_edge(u, v)
        >>> g.topological_sort()
        [4, 5, 0, 2, 3, 1]
        """
        in_degree: dict[int, int] = defaultdict(int)
        for node in self.graph:
            if node not in in_degree:
                in_degree[node] = 0
            for neighbor in self.graph[node]:
                in_degree[neighbor] = in_degree.get(neighbor, 0) + 1

        queue = deque(sorted(n for n in in_degree if in_degree[n] == 0))
        order = []

        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in sorted(self.graph[node]):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return order

    def has_cycle(self) -> bool:
        """
        Detect cycle using DFS coloring.

        >>> g = AdjacencyListGraph(directed=True)
        >>> g.add_edge(0, 1)
        >>> g.add_edge(1, 2)
        >>> g.has_cycle()
        False
        >>> g.add_edge(2, 0)
        >>> g.has_cycle()
        True
        """
        WHITE, GRAY, BLACK = 0, 1, 2
        color: dict[int, int] = {n: WHITE for n in self.graph}

        def dfs(u: int) -> bool:
            color[u] = GRAY
            for v in self.graph[u]:
                if color.get(v, WHITE) == GRAY:
                    return True
                if color.get(v, WHITE) == WHITE and dfs(v):
                    return True
            color[u] = BLACK
            return False

        return any(color[n] == WHITE and dfs(n) for n in self.graph)


class AdjacencyMatrixGraph:
    """
    Graph using adjacency matrix.

    >>> g = AdjacencyMatrixGraph(4)
    >>> g.add_edge(0, 1)
    >>> g.add_edge(1, 2)
    >>> g.has_edge(0, 1)
    True
    >>> g.has_edge(0, 2)
    False
    >>> g.degree(1)
    2
    """

    def __init__(self, num_vertices: int, directed: bool = False) -> None:
        self.n = num_vertices
        self.directed = directed
        self.matrix = [[0] * num_vertices for _ in range(num_vertices)]

    def add_edge(self, u: int, v: int, weight: int = 1) -> None:
        self.matrix[u][v] = weight
        if not self.directed:
            self.matrix[v][u] = weight

    def has_edge(self, u: int, v: int) -> bool:
        return self.matrix[u][v] != 0

    def degree(self, u: int) -> int:
        return sum(1 for v in range(self.n) if self.matrix[u][v] != 0)

    def neighbors(self, u: int) -> list[int]:
        return [v for v in range(self.n) if self.matrix[u][v] != 0]


class EdgeListGraph:
    """
    Graph using edge list representation.

    >>> g = EdgeListGraph()
    >>> g.add_edge(0, 1, 5)
    >>> g.add_edge(1, 2, 3)
    >>> g.edges
    [(0, 1, 5), (1, 2, 3)]
    >>> g.vertices()
    {0, 1, 2}
    """

    def __init__(self) -> None:
        self.edges: list[tuple[int, int, int]] = []

    def add_edge(self, u: int, v: int, weight: int = 1) -> None:
        self.edges.append((u, v, weight))

    def vertices(self) -> set[int]:
        verts: set[int] = set()
        for u, v, _ in self.edges:
            verts.add(u)
            verts.add(v)
        return verts


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # Demo
    g = AdjacencyListGraph()
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
    for u, v in edges:
        g.add_edge(u, v)

    print(f"BFS from 0: {g.bfs(0)}")
    print(f"DFS from 0: {g.dfs(0)}")

    dg = AdjacencyListGraph(directed=True)
    for u, v in [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]:
        dg.add_edge(u, v)
    print(f"Topological sort: {dg.topological_sort()}")
    print(f"Has cycle: {dg.has_cycle()}")
