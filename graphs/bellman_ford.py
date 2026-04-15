"""
Bellman-Ford Algorithm for single-source shortest paths.

Handles negative weight edges and detects negative cycles.
Relaxes all edges V-1 times, then checks for negative cycles.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/bellman_ford.py

>>> edges = [(0,1,4), (0,2,5), (1,2,-3), (2,3,3), (3,1,1)]
>>> bellman_ford(4, edges, 0)
{0: 0, 1: 4, 2: 1, 3: 4}

>>> bellman_ford(4, edges, 1)
{0: inf, 1: 0, 2: -3, 3: 0}

>>> neg_cycle_edges = [(0,1,1), (1,2,-1), (2,0,-1)]
>>> bellman_ford(3, neg_cycle_edges, 0)
Traceback (most recent call last):
    ...
ValueError: Graph contains a negative-weight cycle
"""

from math import inf


def bellman_ford(
    num_vertices: int,
    edges: list[tuple[int, int, float]],
    source: int,
) -> dict[int, float]:
    """
    Bellman-Ford single-source shortest paths.

    Args:
        num_vertices: number of vertices (0-indexed)
        edges: list of (u, v, weight) tuples
        source: starting vertex

    Returns:
        dict mapping vertex to shortest distance from source

    Raises:
        ValueError: if negative-weight cycle is reachable from source

    >>> bellman_ford(3, [(0,1,1),(1,2,2)], 0)
    {0: 0, 1: 1, 2: 3}
    """
    dist = {i: inf for i in range(num_vertices)}
    dist[source] = 0

    # Relax all edges V-1 times
    for _ in range(num_vertices - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break  # Early termination

    # Check for negative cycles
    for u, v, w in edges:
        if dist[u] != inf and dist[u] + w < dist[v]:
            raise ValueError("Graph contains a negative-weight cycle")

    return dist


def bellman_ford_with_path(
    num_vertices: int,
    edges: list[tuple[int, int, float]],
    source: int,
    target: int,
) -> tuple[list[int], float]:
    """
    Bellman-Ford with path reconstruction.

    >>> bellman_ford_with_path(4, [(0,1,1),(1,2,2),(0,2,5),(2,3,1)], 0, 3)
    ([0, 1, 2, 3], 4)

    >>> bellman_ford_with_path(3, [(0,1,1),(1,2,2)], 0, 2)
    ([0, 1, 2], 3)
    """
    dist = {i: inf for i in range(num_vertices)}
    parent: dict[int, int | None] = {i: None for i in range(num_vertices)}
    dist[source] = 0

    for _ in range(num_vertices - 1):
        for u, v, w in edges:
            if dist[u] != inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u

    for u, v, w in edges:
        if dist[u] != inf and dist[u] + w < dist[v]:
            raise ValueError("Graph contains a negative-weight cycle")

    if dist[target] == inf:
        return [], inf

    path = []
    current: int | None = target
    while current is not None:
        path.append(current)
        current = parent[current]
    return path[::-1], dist[target]


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    edges = [
        (0, 1, -1), (0, 2, 4),
        (1, 2, 3), (1, 3, 2), (1, 4, 2),
        (3, 2, 5), (3, 1, 1),
        (4, 3, -3),
    ]
    dist = bellman_ford(5, edges, 0)
    print(f"Distances from vertex 0: {dist}")

    path, cost = bellman_ford_with_path(5, edges, 0, 4)
    print(f"Path 0->4: {path}, cost: {cost}")
