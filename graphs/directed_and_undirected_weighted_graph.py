"""
Directed and Undirected Weighted Graph classes with DFS, BFS, shortest path,
cycle detection, and topological sort.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/directed_and_undirected_(weighted)_graph.py

>>> dg = DirectedGraph()
>>> for u, v, w in [(1, 2, 3), (2, 3, 4), (3, 1, 5)]:
...     dg.add_edge(u, v, w)
>>> dg.has_cycle()
True
>>> dg.shortest_path(1, 3)
7

>>> ug = UndirectedGraph()
>>> for u, v, w in [(1, 2, 3), (2, 3, 4), (1, 3, 10)]:
...     ug.add_edge(u, v, w)
>>> ug.shortest_path(1, 3)
7
>>> ug.connected_components() == [{1, 2, 3}]
True
"""

import heapq
from collections import defaultdict, deque


class DirectedGraph:
    """Directed weighted graph.

    >>> g = DirectedGraph(); g.add_edge(1, 2, 5); g.shortest_path(1, 2)
    5
    """

    def __init__(self) -> None:
        self.adj: dict = defaultdict(list)
        self.nodes: set = set()

    def add_edge(self, u, v, w=1) -> None:
        self.adj[u].append((v, w))
        self.nodes.update([u, v])

    def bfs(self, start) -> list:
        visited, order = {start}, [start]
        q = deque([start])
        while q:
            u = q.popleft()
            for v, _ in self.adj[u]:
                if v not in visited:
                    visited.add(v)
                    order.append(v)
                    q.append(v)
        return order

    def dfs(self, start) -> list:
        visited, order = set(), []

        def go(u):
            visited.add(u)
            order.append(u)
            for v, _ in self.adj[u]:
                if v not in visited:
                    go(v)

        go(start)
        return order

    def shortest_path(self, src, dst) -> float:
        if src == dst:
            return 0
        dist = {src: 0}
        pq = [(0, src)]
        while pq:
            d, u = heapq.heappop(pq)
            if u == dst:
                return d
            if d > dist[u]:
                continue
            for v, w in self.adj[u]:
                nd = d + w
                if nd < dist.get(v, float("inf")):
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
        return float("inf")

    def has_cycle(self) -> bool:
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {n: WHITE for n in self.nodes}

        def dfs(u):
            color[u] = GRAY
            for v, _ in self.adj[u]:
                if color[v] == GRAY:
                    return True
                if color[v] == WHITE and dfs(v):
                    return True
            color[u] = BLACK
            return False

        for n in self.nodes:
            if color[n] == WHITE and dfs(n):
                return True
        return False

    def topological_sort(self) -> list:
        if self.has_cycle():
            raise ValueError("Graph has a cycle")
        indeg = defaultdict(int)
        for n in self.nodes:
            indeg[n]
        for u in self.adj:
            for v, _ in self.adj[u]:
                indeg[v] += 1
        q = deque([n for n in self.nodes if indeg[n] == 0])
        out = []
        while q:
            u = q.popleft()
            out.append(u)
            for v, _ in self.adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return out


class UndirectedGraph:
    """Undirected weighted graph (implemented via two directed edges).

    >>> g = UndirectedGraph(); g.add_edge(1, 2, 5); g.shortest_path(2, 1)
    5
    """

    def __init__(self) -> None:
        self.adj: dict = defaultdict(list)
        self.nodes: set = set()

    def add_edge(self, u, v, w=1) -> None:
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))
        self.nodes.update([u, v])

    def shortest_path(self, src, dst) -> float:
        if src == dst:
            return 0
        dist = {src: 0}
        pq = [(0, src)]
        while pq:
            d, u = heapq.heappop(pq)
            if u == dst:
                return d
            if d > dist[u]:
                continue
            for v, w in self.adj[u]:
                nd = d + w
                if nd < dist.get(v, float("inf")):
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
        return float("inf")

    def connected_components(self) -> list:
        visited: set = set()
        comps = []
        for s in self.nodes:
            if s in visited:
                continue
            comp = set()
            stack = [s]
            visited.add(s)
            while stack:
                u = stack.pop()
                comp.add(u)
                for v, _ in self.adj[u]:
                    if v not in visited:
                        visited.add(v)
                        stack.append(v)
            comps.append(comp)
        return comps


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    dg = DirectedGraph()
    for u, v, w in [(1, 2, 3), (2, 3, 4), (3, 1, 5)]:
        dg.add_edge(u, v, w)
    print("Directed cycle?", dg.has_cycle())
    print("Directed SP 1->3:", dg.shortest_path(1, 3))

    ug = UndirectedGraph()
    for u, v, w in [(1, 2, 3), (2, 3, 4), (1, 3, 10)]:
        ug.add_edge(u, v, w)
    print("Undirected SP 1->3:", ug.shortest_path(1, 3))
    print("Undirected components:", ug.connected_components())
