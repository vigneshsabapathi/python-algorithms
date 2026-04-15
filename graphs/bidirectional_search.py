"""
Bidirectional Search (generic framework).

A general bidirectional search that can use BFS, DFS, or other strategies.
Here implemented with BFS as default (optimal for unweighted graphs).

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/bidirectional_search.py

>>> graph = {1: [2, 3], 2: [1, 4], 3: [1, 4], 4: [2, 3, 5], 5: [4]}
>>> path = bidirectional_search(graph, 1, 5)
>>> path[0] == 1 and path[-1] == 5
True
>>> len(path) == 4
True
"""

from collections import deque


def bidirectional_search(
    graph: dict[int, list[int]],
    source: int,
    target: int,
) -> list[int]:
    """
    Generic bidirectional BFS search returning shortest path.

    >>> bidirectional_search({1: [2], 2: [1, 3], 3: [2]}, 1, 3)
    [1, 2, 3]

    >>> bidirectional_search({1: [2], 2: [1], 3: []}, 1, 3)
    []
    """
    if source == target:
        return [source]

    # Forward and backward frontiers
    front_f = {source}
    front_b = {target}
    parent_f: dict[int, int | None] = {source: None}
    parent_b: dict[int, int | None] = {target: None}

    while front_f and front_b:
        # Expand smaller frontier (optimization)
        if len(front_f) <= len(front_b):
            new_front: set[int] = set()
            for u in front_f:
                for v in graph.get(u, []):
                    if v not in parent_f:
                        parent_f[v] = u
                        new_front.add(v)
                        if v in parent_b:
                            return _reconstruct(parent_f, parent_b, v)
            front_f = new_front
        else:
            new_front = set()
            for u in front_b:
                for v in graph.get(u, []):
                    if v not in parent_b:
                        parent_b[v] = u
                        new_front.add(v)
                        if v in parent_f:
                            return _reconstruct(parent_f, parent_b, v)
            front_b = new_front

    return []


def _reconstruct(
    parent_f: dict[int, int | None],
    parent_b: dict[int, int | None],
    meeting: int,
) -> list[int]:
    path_f: list[int] = []
    node: int | None = meeting
    while node is not None:
        path_f.append(node)
        node = parent_f.get(node)
    path_f.reverse()

    path_b: list[int] = []
    node = parent_b.get(meeting)
    while node is not None:
        path_b.append(node)
        node = parent_b.get(node)

    return path_f + path_b


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    graph = {
        1: [2, 3],
        2: [1, 4],
        3: [1, 4, 5],
        4: [2, 3, 6],
        5: [3, 6],
        6: [4, 5],
    }
    path = bidirectional_search(graph, 1, 6)
    print(f"Bidirectional search 1->6: {path}")
