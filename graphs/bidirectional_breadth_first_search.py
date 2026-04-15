"""
Bidirectional Breadth-First Search.

BFS from both source and target simultaneously on unweighted graphs.
Terminates when frontiers meet. Reduces search space from O(b^d) to O(b^(d/2)).

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/bidirectional_breadth_first_search.py

>>> graph = {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2, 4], 4: [3]}
>>> bidirectional_bfs(graph, 0, 4)
([0, 1, 3, 4], 3)

>>> bidirectional_bfs(graph, 0, 0)
([0], 0)

>>> bidirectional_bfs({0: [], 1: []}, 0, 1)
([], -1)
"""

from collections import deque


def bidirectional_bfs(
    graph: dict[int, list[int]],
    source: int,
    target: int,
) -> tuple[list[int], int]:
    """
    Bidirectional BFS for shortest path in unweighted graph.

    Returns:
        (path, distance) or ([], -1) if unreachable

    >>> g = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2]}
    >>> bidirectional_bfs(g, 0, 3)
    ([0, 1, 2, 3], 3)
    """
    if source == target:
        return [source], 0

    parent_f: dict[int, int | None] = {source: None}
    parent_b: dict[int, int | None] = {target: None}
    queue_f = deque([source])
    queue_b = deque([target])
    visited_f = {source}
    visited_b = {target}

    while queue_f or queue_b:
        # Expand forward
        if queue_f:
            next_f: deque[int] = deque()
            while queue_f:
                u = queue_f.popleft()
                for v in graph.get(u, []):
                    if v not in visited_f:
                        visited_f.add(v)
                        parent_f[v] = u
                        next_f.append(v)
                        if v in visited_b:
                            return _build_path(parent_f, parent_b, v)
            queue_f = next_f

        # Expand backward
        if queue_b:
            next_b: deque[int] = deque()
            while queue_b:
                u = queue_b.popleft()
                for v in graph.get(u, []):
                    if v not in visited_b:
                        visited_b.add(v)
                        parent_b[v] = u
                        next_b.append(v)
                        if v in visited_f:
                            return _build_path(parent_f, parent_b, v)
            queue_b = next_b

    return [], -1


def _build_path(
    parent_f: dict[int, int | None],
    parent_b: dict[int, int | None],
    meeting: int,
) -> tuple[list[int], int]:
    path_f: list[int] = []
    node: int | None = meeting
    while node is not None:
        path_f.append(node)
        node = parent_f.get(node)
    path_f.reverse()

    node = parent_b.get(meeting)
    path_b: list[int] = []
    while node is not None:
        path_b.append(node)
        node = parent_b.get(node)

    full_path = path_f + path_b
    return full_path, len(full_path) - 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    graph = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 5],
        3: [1, 6],
        4: [1, 6],
        5: [2, 7],
        6: [3, 4, 7],
        7: [5, 6],
    }
    path, dist = bidirectional_bfs(graph, 0, 7)
    print(f"Path 0->7: {path}, distance: {dist}")
