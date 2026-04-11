"""
Ford-Fulkerson Algorithm for Maximum Flow Problem.

Uses BFS to find augmenting paths (Edmonds-Karp variant), guaranteeing
polynomial time complexity O(V * E^2).

Reference: https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm

Steps:
    1. Start with initial flow as 0.
    2. While there exists an augmenting path from source to sink:
        a. Find the minimum residual capacity along the path (bottleneck).
        b. Update residual capacities of forward and backward edges.
        c. Add the bottleneck to the total flow.

>>> ford_fulkerson(
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
23
"""

from collections import deque


def breadth_first_search(
    graph: list[list[int]], source: int, sink: int, parents: list[int]
) -> bool:
    """
    BFS on the residual graph to find an augmenting path from source to sink.

    Fills *parents* so the caller can reconstruct the path.
    Returns True if sink is reachable from source.

    >>> g = [
    ...     [0, 16, 13, 0, 0, 0],
    ...     [0, 0, 10, 12, 0, 0],
    ...     [0, 4, 0, 0, 14, 0],
    ...     [0, 0, 9, 0, 0, 20],
    ...     [0, 0, 0, 7, 0, 4],
    ...     [0, 0, 0, 0, 0, 0],
    ... ]
    >>> breadth_first_search(g, 0, 5, [-1] * 6)
    True
    >>> breadth_first_search(g, 5, 0, [-1] * 6)
    False
    """
    n = len(graph)
    visited = [False] * n
    queue: deque[int] = deque([source])
    visited[source] = True

    while queue:
        u = queue.popleft()
        for v in range(n):
            if not visited[v] and graph[u][v] > 0:
                queue.append(v)
                visited[v] = True
                parents[v] = u
                if v == sink:
                    return True
    return visited[sink]


def ford_fulkerson(graph: list[list[int]], source: int, sink: int) -> int:
    """
    Return the maximum flow from *source* to *sink* using the
    Edmonds-Karp (BFS-based Ford-Fulkerson) algorithm.

    CAUTION: This function mutates *graph* (the residual graph is built
    in-place).  Pass a deep copy if you need the original.

    Args:
        graph:  Adjacency matrix where graph[u][v] is the capacity of edge u->v.
        source: Index of the source node.
        sink:   Index of the sink node.

    Returns:
        The maximum flow value.

    >>> ford_fulkerson(
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
    23

    >>> ford_fulkerson([[0, 10, 0], [0, 0, 10], [0, 0, 0]], 0, 2)
    10

    >>> ford_fulkerson([[0, 0], [0, 0]], 0, 1)
    0

    >>> ford_fulkerson(
    ...     [
    ...         [0, 10, 10, 0],
    ...         [0, 0, 0, 10],
    ...         [0, 0, 0, 10],
    ...         [0, 0, 0, 0],
    ...     ],
    ...     0,
    ...     3,
    ... )
    20
    """
    parent = [-1] * len(graph)
    max_flow = 0

    while breadth_first_search(graph, source, sink, parent):
        # Find bottleneck along the path
        path_flow = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, graph[u][v])
            v = u

        # Update residual capacities
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = u

        max_flow += path_flow
        parent = [-1] * len(graph)

    return max_flow


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
    print(f"Max flow (CLRS example): {ford_fulkerson(demo_graph, source=0, sink=5)}")
