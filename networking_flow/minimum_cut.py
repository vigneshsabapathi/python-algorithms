"""
Minimum Cut via Ford-Fulkerson (Max-Flow Min-Cut Theorem).

The min-cut of a flow network is the smallest total capacity of edges
whose removal disconnects the source from the sink.  By the max-flow
min-cut theorem, the value of the maximum flow equals the capacity of
the minimum cut.

Algorithm:
    1. Run Ford-Fulkerson (BFS / Edmonds-Karp) to compute max flow and
       the residual graph.
    2. BFS from the source on the residual graph to find all nodes
       reachable from the source (the S-side of the cut).
    3. Any original edge (u, v) where u is reachable and v is NOT
       reachable is a min-cut edge.

Reference: https://en.wikipedia.org/wiki/Minimum_cut

>>> minimum_cut(
...     [
...         [0, 16, 13, 0, 0, 0],
...         [0, 0, 10, 12, 0, 0],
...         [0, 4, 0, 0, 14, 0],
...         [0, 0, 9, 0, 0, 20],
...         [0, 0, 0, 7, 0, 4],
...         [0, 0, 0, 0, 0, 0],
...     ],
...     source=0,
...     sink=5,
... )
[(1, 3), (4, 3), (4, 5)]
"""

from collections import deque


def _bfs(graph: list[list[int]], source: int, sink: int, parent: list[int]) -> bool:
    """BFS on residual graph; returns True if sink is reachable from source."""
    n = len(graph)
    visited = [False] * n
    visited[source] = True
    queue: deque[int] = deque([source])

    while queue:
        u = queue.popleft()
        for v in range(n):
            if not visited[v] and graph[u][v] > 0:
                visited[v] = True
                parent[v] = u
                queue.append(v)

    return visited[sink]


def _bfs_reachable(graph: list[list[int]], source: int) -> list[bool]:
    """Return a boolean list of nodes reachable from source in the residual graph."""
    n = len(graph)
    visited = [False] * n
    visited[source] = True
    queue: deque[int] = deque([source])

    while queue:
        u = queue.popleft()
        for v in range(n):
            if not visited[v] and graph[u][v] > 0:
                visited[v] = True
                queue.append(v)

    return visited


def minimum_cut(
    graph: list[list[int]], source: int, sink: int
) -> list[tuple[int, int]]:
    """
    Return the list of edges forming the minimum cut of the flow network.

    Each edge is a tuple (u, v) where u is on the source side and v is
    on the sink side of the cut.

    CAUTION: Mutates *graph* (builds residual in place).

    Args:
        graph:  Adjacency matrix where graph[u][v] is the capacity of edge u->v.
        source: Index of the source node.
        sink:   Index of the sink node.

    Returns:
        List of (u, v) tuples forming the minimum cut.

    >>> minimum_cut(
    ...     [
    ...         [0, 16, 13, 0, 0, 0],
    ...         [0, 0, 10, 12, 0, 0],
    ...         [0, 4, 0, 0, 14, 0],
    ...         [0, 0, 9, 0, 0, 20],
    ...         [0, 0, 0, 7, 0, 4],
    ...         [0, 0, 0, 0, 0, 0],
    ...     ],
    ...     source=0,
    ...     sink=5,
    ... )
    [(1, 3), (4, 3), (4, 5)]

    >>> minimum_cut([[0, 10, 0], [0, 0, 10], [0, 0, 0]], 0, 2)
    [(0, 1)]

    >>> minimum_cut([[0, 0], [0, 0]], 0, 1)
    []

    >>> minimum_cut(
    ...     [
    ...         [0, 10, 10, 0],
    ...         [0, 0, 0, 10],
    ...         [0, 0, 0, 10],
    ...         [0, 0, 0, 0],
    ...     ],
    ...     0,
    ...     3,
    ... )
    [(0, 1), (0, 2)]
    """
    n = len(graph)
    original = [row[:] for row in graph]  # save original capacities

    # Step 1: Run Ford-Fulkerson (Edmonds-Karp) to exhaustion
    parent = [-1] * n
    while _bfs(graph, source, sink, parent):
        # Find bottleneck
        path_flow = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, graph[u][v])
            v = u

        # Update residual graph
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = u

        parent = [-1] * n

    # Step 2: BFS on residual graph from source
    reachable = _bfs_reachable(graph, source)

    # Step 3: Find cut edges — original edges from reachable to non-reachable
    cut_edges: list[tuple[int, int]] = []
    for u in range(n):
        for v in range(n):
            if reachable[u] and not reachable[v] and original[u][v] > 0:
                cut_edges.append((u, v))

    return cut_edges


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    demo_graph = [
        [0, 16, 13, 0, 0, 0],
        [0, 0, 10, 12, 0, 0],
        [0, 4, 0, 0, 14, 0],
        [0, 0, 9, 0, 0, 20],
        [0, 0, 0, 7, 0, 4],
        [0, 0, 0, 0, 0, 0],
    ]
    cut = minimum_cut(demo_graph, source=0, sink=5)
    print(f"Min-cut edges: {cut}")
    print(f"Min-cut capacity: {sum([ [0,16,13,0,0,0],[0,0,10,12,0,0],[0,4,0,0,14,0],[0,0,9,0,0,20],[0,0,0,7,0,4],[0,0,0,0,0,0] ][u][v] for u, v in cut)}")
