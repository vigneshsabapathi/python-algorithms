"""
Dijkstra Algorithm - PriorityQueue object variant.

Same algorithm as dijkstra.py but built around an explicit PriorityQueue class
that demonstrates decrease-key semantics. Useful for showing interviewers
the classical formulation from CLRS.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/dijkstra_algorithm.py

>>> g = Graph(5)
>>> g.add_edge(0, 1, 4)
>>> g.add_edge(0, 2, 1)
>>> g.add_edge(2, 1, 2)
>>> g.add_edge(1, 3, 1)
>>> g.add_edge(2, 3, 5)
>>> g.add_edge(3, 4, 3)
>>> g.dijkstra(0)
[0, 3, 1, 4, 7]

>>> Graph(1).dijkstra(0)
[0]
"""

import heapq


class PriorityQueue:
    """Heap-backed priority queue with lazy deletion.

    >>> pq = PriorityQueue(); pq.push(1, 'a'); pq.pop()
    'a'
    """

    def __init__(self) -> None:
        self.heap: list = []
        self.entry: dict = {}
        self.counter = 0

    def push(self, priority, item) -> None:
        self.counter += 1
        entry = [priority, self.counter, item, False]
        self.entry[item] = entry
        heapq.heappush(self.heap, entry)

    def pop(self):
        while self.heap:
            _, _, item, removed = heapq.heappop(self.heap)
            if not removed:
                return item
        raise KeyError("pop from empty queue")

    def decrease(self, item, new_priority) -> None:
        if item in self.entry:
            self.entry[item][3] = True
        self.push(new_priority, item)

    def __bool__(self) -> bool:
        return any(not e[3] for e in self.heap)


class Graph:
    """Directed weighted graph with Dijkstra.

    >>> g = Graph(2); g.add_edge(0, 1, 3); g.dijkstra(0)
    [0, 3]
    """

    def __init__(self, n: int) -> None:
        self.n = n
        self.adj: list = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, w: int) -> None:
        self.adj[u].append((v, w))

    def dijkstra(self, source: int) -> list:
        INF = float("inf")
        dist = [INF] * self.n
        dist[source] = 0
        pq = PriorityQueue()
        pq.push(0, source)
        while pq:
            u = pq.pop()
            for v, w in self.adj[u]:
                nd = dist[u] + w
                if nd < dist[v]:
                    dist[v] = nd
                    pq.decrease(v, nd)
        return [d if d != INF else -1 for d in dist]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    g = Graph(5)
    for u, v, w in [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3)]:
        g.add_edge(u, v, w)
    print("Distances from 0:", g.dijkstra(0))
