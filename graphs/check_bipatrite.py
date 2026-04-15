"""
Check Bipartite - Test whether an undirected graph is 2-colorable.

A graph is bipartite iff it contains no odd-length cycle. Equivalently, its
vertices can be partitioned into two sets so every edge crosses the partition.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/check_bipatrite.py

>>> is_bipartite({0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]})
True
>>> is_bipartite({0: [1, 2], 1: [0, 2], 2: [0, 1]})
False
>>> is_bipartite({})
True
>>> is_bipartite({0: []})
True
"""

from collections import deque


def is_bipartite(graph: dict) -> bool:
    """Return True iff graph is bipartite (undirected adjacency list).

    >>> is_bipartite({0: [1], 1: [0]})
    True
    """
    color: dict = {}
    for src in graph:
        if src in color:
            continue
        color[src] = 0
        q = deque([src])
        while q:
            node = q.popleft()
            for nb in graph[node]:
                if nb not in color:
                    color[nb] = 1 - color[node]
                    q.append(nb)
                elif color[nb] == color[node]:
                    return False
    return True


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    g1 = {0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]}
    g2 = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
    print("Square graph bipartite?", is_bipartite(g1))
    print("Triangle bipartite?", is_bipartite(g2))
