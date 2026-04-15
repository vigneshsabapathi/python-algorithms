"""
Dijkstra's Shortest Path Algorithm.

Classic single-source shortest path for non-negative edge weights. Uses a
priority queue (heap) to always extract the nearest unfinalised node.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/dijkstra.py

>>> g = {'A': [('B', 1), ('C', 4)], 'B': [('C', 2), ('D', 5)],
...      'C': [('D', 1)], 'D': []}
>>> dist = dijkstra(g, 'A')
>>> dist['D']
4
>>> dist['C']
3

>>> dijkstra({0: []}, 0)
{0: 0}
"""

import heapq


def dijkstra(graph: dict, source) -> dict:
    """Return shortest distance from source to every reachable node.

    >>> dijkstra({0: [(1, 3)], 1: []}, 0)
    {0: 0, 1: 3}
    """
    dist = {source: 0}
    pq = [(0, source)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    g = {'A': [('B', 1), ('C', 4)], 'B': [('C', 2), ('D', 5)],
         'C': [('D', 1)], 'D': []}
    print("Distances from A:", dijkstra(g, 'A'))
