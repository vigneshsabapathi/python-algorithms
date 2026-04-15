"""
Bidirectional A* Search Algorithm.

Runs A* from both source and target simultaneously, meeting in the middle.
Uses consistent heuristic for correctness.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/bidirectional_a_star.py

>>> graph = {
...     "A": [("B", 1), ("C", 4)],
...     "B": [("A", 1), ("C", 2), ("D", 5)],
...     "C": [("A", 4), ("B", 2), ("D", 1)],
...     "D": [("B", 5), ("C", 1)],
... }
>>> h = {"A": 5, "B": 3, "C": 1, "D": 0}
>>> h_rev = {"A": 0, "B": 2, "C": 3, "D": 5}
>>> bidirectional_a_star(graph, "A", "D", h, h_rev)
(['A', 'B', 'C', 'D'], 4)
"""

import heapq
from math import inf


def bidirectional_a_star(
    graph: dict[str, list[tuple[str, float]]],
    source: str,
    target: str,
    heuristic_f: dict[str, float],
    heuristic_b: dict[str, float],
) -> tuple[list[str], float]:
    """
    Bidirectional A* search.

    Args:
        graph: undirected graph as adjacency list
        source: start node
        target: end node
        heuristic_f: heuristic for forward search (estimates cost to target)
        heuristic_b: heuristic for backward search (estimates cost to source)

    Returns:
        (path, cost) tuple

    >>> g = {"X": [("Y", 2), ("Z", 5)], "Y": [("X", 2), ("Z", 1)], "Z": [("X", 5), ("Y", 1)]}
    >>> bidirectional_a_star(g, "X", "Z", {"X": 3, "Y": 1, "Z": 0}, {"X": 0, "Y": 1, "Z": 3})
    (['X', 'Y', 'Z'], 3)
    """
    if source == target:
        return [source], 0

    dist_f: dict[str, float] = {source: 0}
    dist_b: dict[str, float] = {target: 0}
    parent_f: dict[str, str | None] = {source: None}
    parent_b: dict[str, str | None] = {target: None}

    pq_f = [(heuristic_f.get(source, 0), source)]
    pq_b = [(heuristic_b.get(target, 0), target)]
    settled_f: set[str] = set()
    settled_b: set[str] = set()

    best_dist = inf
    meeting_node = ""

    while pq_f or pq_b:
        # Expand forward
        if pq_f:
            f_val, u = heapq.heappop(pq_f)
            if u in settled_f:
                pass
            else:
                settled_f.add(u)
                if u in settled_b:
                    candidate = dist_f[u] + dist_b[u]
                    if candidate < best_dist:
                        best_dist = candidate
                        meeting_node = u
                else:
                    for v, w in graph.get(u, []):
                        new_g = dist_f[u] + w
                        if new_g < dist_f.get(v, inf):
                            dist_f[v] = new_g
                            parent_f[v] = u
                            heapq.heappush(pq_f, (new_g + heuristic_f.get(v, 0), v))
                        if v in dist_b:
                            candidate = dist_f.get(v, inf) + dist_b[v]
                            if candidate < best_dist:
                                best_dist = candidate
                                meeting_node = v

        # Expand backward
        if pq_b:
            f_val, u = heapq.heappop(pq_b)
            if u in settled_b:
                pass
            else:
                settled_b.add(u)
                if u in settled_f:
                    candidate = dist_f[u] + dist_b[u]
                    if candidate < best_dist:
                        best_dist = candidate
                        meeting_node = u
                else:
                    for v, w in graph.get(u, []):
                        new_g = dist_b[u] + w
                        if new_g < dist_b.get(v, inf):
                            dist_b[v] = new_g
                            parent_b[v] = u
                            heapq.heappush(pq_b, (new_g + heuristic_b.get(v, 0), v))
                        if v in dist_f:
                            candidate = dist_f[v] + dist_b.get(v, inf)
                            if candidate < best_dist:
                                best_dist = candidate
                                meeting_node = v

        # Termination: both frontiers have f-values >= best known path
        min_f = pq_f[0][0] if pq_f else inf
        min_b = pq_b[0][0] if pq_b else inf
        if min(min_f, min_b) >= best_dist:
            break

    if not meeting_node:
        return [], inf

    # Reconstruct path
    path_f: list[str] = []
    node: str | None = meeting_node
    while node is not None:
        path_f.append(node)
        node = parent_f.get(node)
    path_f.reverse()

    path_b: list[str] = []
    node = parent_b.get(meeting_node)
    while node is not None:
        path_b.append(node)
        node = parent_b.get(node)

    return path_f + path_b, best_dist


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    graph = {
        "A": [("B", 1), ("C", 4)],
        "B": [("A", 1), ("C", 2), ("D", 5)],
        "C": [("A", 4), ("B", 2), ("D", 1)],
        "D": [("B", 5), ("C", 1)],
    }
    h_f = {"A": 5, "B": 3, "C": 1, "D": 0}
    h_b = {"A": 0, "B": 2, "C": 3, "D": 5}
    path, cost = bidirectional_a_star(graph, "A", "D", h_f, h_b)
    print(f"Bidirectional A* path: {path}, cost: {cost}")
