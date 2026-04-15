"""
Articulation Points (Cut Vertices) in an undirected graph.

An articulation point is a vertex whose removal disconnects the graph.
Uses Tarjan's algorithm with DFS, tracking discovery time and low values.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/articulation_points.py

>>> graph = {0: [1, 2], 1: [0, 2], 2: [0, 1, 3], 3: [2, 4], 4: [3]}
>>> sorted(find_articulation_points(graph))
[2, 3]

>>> graph2 = {0: [1], 1: [0, 2], 2: [1]}
>>> find_articulation_points(graph2)
[1]

>>> find_articulation_points({0: [1], 1: [0]})
[]
"""


def find_articulation_points(graph: dict[int, list[int]]) -> list[int]:
    """
    Find all articulation points using Tarjan's algorithm.

    Args:
        graph: adjacency list representation of undirected graph

    Returns:
        List of articulation point vertices

    >>> find_articulation_points({0: [1, 2], 1: [0, 2], 2: [0, 1]})
    []
    >>> find_articulation_points({0: [1], 1: [0, 2, 3], 2: [1], 3: [1]})
    [1]
    """
    n = len(graph)
    if n == 0:
        return []

    visited: set[int] = set()
    disc: dict[int, int] = {}
    low: dict[int, int] = {}
    parent: dict[int, int | None] = {}
    ap: set[int] = set()
    timer = [0]

    def dfs(u: int) -> None:
        visited.add(u)
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        children = 0

        for v in graph[u]:
            if v not in visited:
                children += 1
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])

                # u is root and has 2+ children
                if parent[u] is None and children > 1:
                    ap.add(u)
                # u is not root and low[v] >= disc[u]
                if parent[u] is not None and low[v] >= disc[u]:
                    ap.add(u)
            elif v != parent.get(u):
                low[u] = min(low[u], disc[v])

    for node in graph:
        if node not in visited:
            parent[node] = None
            dfs(node)

    return sorted(ap)


def find_bridges(graph: dict[int, list[int]]) -> list[tuple[int, int]]:
    """
    Find all bridges (cut edges) using similar Tarjan approach.

    >>> graph = {0: [1, 2], 1: [0, 2], 2: [0, 1, 3], 3: [2]}
    >>> find_bridges(graph)
    [(2, 3)]

    >>> find_bridges({0: [1, 2], 1: [0, 2], 2: [0, 1]})
    []
    """
    visited: set[int] = set()
    disc: dict[int, int] = {}
    low: dict[int, int] = {}
    parent: dict[int, int | None] = {}
    bridges: list[tuple[int, int]] = []
    timer = [0]

    def dfs(u: int) -> None:
        visited.add(u)
        disc[u] = low[u] = timer[0]
        timer[0] += 1

        for v in graph[u]:
            if v not in visited:
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append((min(u, v), max(u, v)))
            elif v != parent.get(u):
                low[u] = min(low[u], disc[v])

    for node in graph:
        if node not in visited:
            parent[node] = None
            dfs(node)

    return sorted(bridges)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    graph = {
        0: [1, 2],
        1: [0, 2],
        2: [0, 1, 3, 5],
        3: [2, 4],
        4: [3],
        5: [2, 6, 8],
        6: [5, 7],
        7: [6, 8],
        8: [5, 7],
    }
    print(f"Graph: {graph}")
    print(f"Articulation points: {find_articulation_points(graph)}")
    print(f"Bridges: {find_bridges(graph)}")
