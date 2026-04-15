"""
Edmonds-Karp for Multiple Sources and Sinks.

Adds a super-source S* connected to every real source with infinite capacity
and a super-sink T* connected from every real sink with infinite capacity,
then runs Edmonds-Karp (BFS-based Ford-Fulkerson) from S* to T*.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/edmonds_karp_multiple_source_and_sink.py

>>> flow = FlowNetwork(4)
>>> for u, v, c in [(0, 2, 3), (1, 2, 5), (2, 3, 6)]:
...     flow.add_edge(u, v, c)
>>> flow.max_flow([0, 1], [3])
6

>>> f2 = FlowNetwork(3)
>>> f2.add_edge(0, 1, 10); f2.add_edge(1, 2, 5)
>>> f2.max_flow([0], [2])
5
"""

from collections import defaultdict, deque


class FlowNetwork:
    """Flow network with multi-source / multi-sink Edmonds-Karp.

    >>> f = FlowNetwork(2); f.add_edge(0, 1, 4); f.max_flow([0], [1])
    4
    """

    INF = float("inf")

    def __init__(self, n: int) -> None:
        self.n = n
        self.cap: dict = defaultdict(lambda: defaultdict(int))

    def add_edge(self, u: int, v: int, c: int) -> None:
        self.cap[u][v] += c

    def _bfs(self, s: int, t: int, cap) -> dict:
        parent = {s: None}
        q = deque([s])
        while q and t not in parent:
            u = q.popleft()
            for v, c in cap[u].items():
                if v not in parent and c > 0:
                    parent[v] = u
                    q.append(v)
        return parent

    def max_flow(self, sources: list, sinks: list) -> int:
        # Build working residual with super-source/super-sink
        cap: dict = defaultdict(lambda: defaultdict(int))
        for u, nb in self.cap.items():
            for v, c in nb.items():
                cap[u][v] += c
        S, T = self.n, self.n + 1
        for s in sources:
            cap[S][s] = self.INF
        for t in sinks:
            cap[t][T] = self.INF
        flow = 0
        while True:
            parent = self._bfs(S, T, cap)
            if T not in parent:
                return flow
            # Bottleneck
            pf = self.INF
            v = T
            while parent[v] is not None:
                pf = min(pf, cap[parent[v]][v])
                v = parent[v]
            # Augment
            v = T
            while parent[v] is not None:
                cap[parent[v]][v] -= pf
                cap[v][parent[v]] += pf
                v = parent[v]
            flow += pf


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    f = FlowNetwork(4)
    for u, v, c in [(0, 2, 3), (1, 2, 5), (2, 3, 6)]:
        f.add_edge(u, v, c)
    print("Max flow with sources [0,1] -> sinks [3]:", f.max_flow([0, 1], [3]))
