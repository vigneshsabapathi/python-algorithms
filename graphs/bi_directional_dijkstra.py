"""
Bidirectional Dijkstra's Algorithm.

Runs Dijkstra from both source and target simultaneously.
Terminates when the two search frontiers meet, providing significant speedup.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/bi_directional_dijkstra.py

>>> graph = {
...     0: [(1, 1), (2, 4)],
...     1: [(0, 1), (2, 2), (3, 5)],
...     2: [(0, 4), (1, 2), (3, 1)],
...     3: [(1, 5), (2, 1)],
... }
>>> bidirectional_dijkstra(graph, 0, 3)
([0, 1, 2, 3], 4)

>>> bidirectional_dijkstra(graph, 0, 0)
([0], 0)

>>> bidirectional_dijkstra({0: [], 1: []}, 0, 1)
([], inf)
"""

import heapq
from math import inf


def bidirectional_dijkstra(
    graph: dict[int, list[tuple[int, float]]],
    source: int,
    target: int,
) -> tuple[list[int], float]:
    """
    Bidirectional Dijkstra's shortest path.

    Args:
        graph: adjacency list with (neighbor, weight) tuples (undirected)
        source: start node
        target: end node

    Returns:
        (path, distance) tuple

    >>> g = {0: [(1, 2)], 1: [(0, 2), (2, 3)], 2: [(1, 3)]}
    >>> bidirectional_dijkstra(g, 0, 2)
    ([0, 1, 2], 5)
    """
    if source == target:
        return [source], 0

    # Forward search from source
    dist_f: dict[int, float] = {source: 0}
    parent_f: dict[int, int | None] = {source: None}
    pq_f: list[tuple[float, int]] = [(0, source)]

    # Backward search from target
    dist_b: dict[int, float] = {target: 0}
    parent_b: dict[int, int | None] = {target: None}
    pq_b: list[tuple[float, int]] = [(0, target)]

    visited_f: set[int] = set()
    visited_b: set[int] = set()

    best_dist = inf
    meeting_node = -1

    while pq_f or pq_b:
        # Check termination
        min_f = pq_f[0][0] if pq_f else inf
        min_b = pq_b[0][0] if pq_b else inf
        if min_f + min_b >= best_dist:
            break

        # Expand forward
        if pq_f and (not pq_b or min_f <= min_b):
            d, u = heapq.heappop(pq_f)
            if u in visited_f:
                continue
            visited_f.add(u)
            for v, w in graph.get(u, []):
                new_dist = d + w
                if new_dist < dist_f.get(v, inf):
                    dist_f[v] = new_dist
                    parent_f[v] = u
                    heapq.heappush(pq_f, (new_dist, v))
                # Check if meets backward
                if v in dist_b:
                    candidate = dist_f.get(v, inf) + dist_b[v]
                    if candidate < best_dist:
                        best_dist = candidate
                        meeting_node = v
        else:
            # Expand backward
            d, u = heapq.heappop(pq_b)
            if u in visited_b:
                continue
            visited_b.add(u)
            for v, w in graph.get(u, []):
                new_dist = d + w
                if new_dist < dist_b.get(v, inf):
                    dist_b[v] = new_dist
                    parent_b[v] = u
                    heapq.heappush(pq_b, (new_dist, v))
                if v in dist_f:
                    candidate = dist_f[v] + dist_b.get(v, inf)
                    if candidate < best_dist:
                        best_dist = candidate
                        meeting_node = v

    if meeting_node == -1:
        return [], inf

    # Reconstruct path
    path_f = []
    node: int | None = meeting_node
    while node is not None:
        path_f.append(node)
        node = parent_f.get(node)
    path_f.reverse()

    path_b = []
    node = parent_b.get(meeting_node)
    while node is not None:
        path_b.append(node)
        node = parent_b.get(node)

    return path_f + path_b, best_dist


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    graph = {
        0: [(1, 7), (2, 9), (5, 14)],
        1: [(0, 7), (2, 10), (3, 15)],
        2: [(0, 9), (1, 10), (3, 11), (5, 2)],
        3: [(1, 15), (2, 11), (4, 6)],
        4: [(3, 6), (5, 9)],
        5: [(0, 14), (2, 2), (4, 9)],
    }
    path, dist = bidirectional_dijkstra(graph, 0, 4)
    print(f"Path 0->4: {path}, distance: {dist}")
