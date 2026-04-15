"""
Dijkstra Alternate - Functional adjacency-list implementation.

An alternate idiomatic Python formulation of Dijkstra using tuples in a heap.
Mirrors the style seen in many LeetCode templates.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/dijkstra_alternate.py

>>> g = {'s': {'a': 2, 'b': 1},
...      'a': {'s': 3, 'b': 4, 'c': 8},
...      'b': {'s': 4, 'a': 2, 'd': 2},
...      'c': {'a': 2, 'd': 7, 't': 4},
...      'd': {'b': 1, 'c': 11, 't': 5},
...      't': {'c': 3, 'd': 5}}
>>> dijkstra_alt(g, 's', 't')
8

>>> dijkstra_alt({'a': {}}, 'a', 'a')
0

>>> dijkstra_alt({'a': {'b': 1}, 'b': {}}, 'a', 'z')
-1
"""

import heapq


def dijkstra_alt(graph: dict, start, end) -> int:
    """Shortest distance from start to end, or -1 if unreachable.

    >>> dijkstra_alt({'a': {'b': 3}, 'b': {}}, 'a', 'b')
    3
    """
    if start == end:
        return 0
    pq = [(0, start)]
    visited = set()
    while pq:
        cost, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        if u == end:
            return cost
        for v, w in graph.get(u, {}).items():
            if v not in visited:
                heapq.heappush(pq, (cost + w, v))
    return -1


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    g = {'s': {'a': 2, 'b': 1},
         'a': {'s': 3, 'b': 4, 'c': 8},
         'b': {'s': 4, 'a': 2, 'd': 2},
         'c': {'a': 2, 'd': 7, 't': 4},
         'd': {'b': 1, 'c': 11, 't': 5},
         't': {'c': 3, 'd': 5}}
    print("Shortest s -> t:", dijkstra_alt(g, 's', 't'))
