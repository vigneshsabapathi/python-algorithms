"""
Dinic's Maximum Flow Algorithm.

Dinic builds a layered graph via BFS, then repeatedly finds blocking flows
via DFS. On unit-capacity networks, runs in O(E sqrt(V)); on general networks
O(V^2 * E).

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/dinic.py

>>> d = Dinic(6)
>>> for u, v, c in [(0, 1, 10), (0, 2, 10), (1, 2, 2), (1, 3, 4),
...                  (1, 4, 8), (2, 4, 9), (3, 5, 10), (4, 3, 6), (4, 5, 10)]:
...     d.add_edge(u, v, c)
>>> d.max_flow(0, 5)
19

>>> d2 = Dinic(2); d2.add_edge(0, 1, 7)
>>> d2.max_flow(0, 1)
7
"""

from collections import deque


class Dinic:
    """Max-flow solver using Dinic's algorithm.

    >>> d = Dinic(3); d.add_edge(0, 1, 1); d.add_edge(1, 2, 1); d.max_flow(0, 2)
    1
    """

    def __init__(self, n: int) -> None:
        self.n = n
        self.graph: list = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, cap: int) -> None:
        self.graph[u].append([v, cap, len(self.graph[v])])
        self.graph[v].append([u, 0, len(self.graph[u]) - 1])

    def _bfs(self, s: int, t: int) -> bool:
        self.level = [-1] * self.n
        self.level[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v, cap, _ in self.graph[u]:
                if cap > 0 and self.level[v] < 0:
                    self.level[v] = self.level[u] + 1
                    q.append(v)
        return self.level[t] >= 0

    def _dfs(self, u: int, t: int, pushed: int) -> int:
        if u == t or pushed == 0:
            return pushed
        while self.iter_[u] < len(self.graph[u]):
            v, cap, rev = self.graph[u][self.iter_[u]]
            if cap > 0 and self.level[v] == self.level[u] + 1:
                d = self._dfs(v, t, min(pushed, cap))
                if d > 0:
                    self.graph[u][self.iter_[u]][1] -= d
                    self.graph[v][rev][1] += d
                    return d
            self.iter_[u] += 1
        return 0

    def max_flow(self, s: int, t: int) -> int:
        flow = 0
        while self._bfs(s, t):
            self.iter_ = [0] * self.n
            while True:
                f = self._dfs(s, t, float("inf"))
                if f == 0:
                    break
                flow += f
        return flow


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    d = Dinic(6)
    for u, v, c in [(0, 1, 10), (0, 2, 10), (1, 2, 2), (1, 3, 4),
                    (1, 4, 8), (2, 4, 9), (3, 5, 10), (4, 3, 6), (4, 5, 10)]:
        d.add_edge(u, v, c)
    print("Max flow 0 -> 5:", d.max_flow(0, 5))
