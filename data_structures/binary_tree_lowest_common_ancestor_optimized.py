"""
Optimized variants for Lowest Common Ancestor (LCA).

Variants:
1. BinaryLiftingLCA   — Sparse table (binary lifting), O(log n) query, O(n log n) build
2. EulerTourRMQLCA    — Euler tour + RMQ (sparse table), O(1) query, O(n log n) build
3. NaiveLCA           — Simple path traversal, O(depth) query, O(1) extra space
"""

from __future__ import annotations

import math
import timeit
from collections import defaultdict


# --- Variant 1: Binary Lifting (same as main file, encapsulated in class) ---
class BinaryLiftingLCA:
    """
    LCA using binary lifting / sparse table.
    Build: O(n log n), Query: O(log n)
    """

    LOG = 18

    def __init__(self, n: int, edges: list[tuple[int, int]], root: int = 1) -> None:
        self.n = n
        self.root = root
        self.graph: dict[int, list[int]] = defaultdict(list)
        for u, v in edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
        self.depth = [-1] * (n + 1)
        self.parent = [[0] * (n + 1) for _ in range(self.LOG)]
        self._bfs()
        self._build_sparse()

    def _bfs(self) -> None:
        from collections import deque
        q: deque[int] = deque([self.root])
        self.depth[self.root] = 0
        while q:
            u = q.popleft()
            for v in self.graph[u]:
                if self.depth[v] == -1:
                    self.depth[v] = self.depth[u] + 1
                    self.parent[0][v] = u
                    q.append(v)

    def _build_sparse(self) -> None:
        for j in range(1, self.LOG):
            for i in range(1, self.n + 1):
                self.parent[j][i] = self.parent[j - 1][self.parent[j - 1][i]]

    def query(self, u: int, v: int) -> int:
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        diff = self.depth[u] - self.depth[v]
        for j in range(self.LOG):
            if (diff >> j) & 1:
                u = self.parent[j][u]
        if u == v:
            return u
        for j in range(self.LOG - 1, -1, -1):
            if self.parent[j][u] != self.parent[j][v]:
                u = self.parent[j][u]
                v = self.parent[j][v]
        return self.parent[0][u]


# --- Variant 2: Euler Tour + Sparse Table RMQ, O(1) query ---
class EulerTourRMQLCA:
    """
    LCA using Euler tour + RMQ via sparse table.
    Build: O(n log n), Query: O(1)
    """

    def __init__(self, n: int, edges: list[tuple[int, int]], root: int = 1) -> None:
        self.n = n
        self.root = root
        self.graph: dict[int, list[int]] = defaultdict(list)
        for u, v in edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
        self.euler: list[int] = []
        self.depth_arr: list[int] = []
        self.first: dict[int, int] = {}
        self.depth = [-1] * (n + 1)
        self._dfs(root, 0)
        self._build_sparse()

    def _dfs(self, u: int, d: int) -> None:
        self.depth[u] = d
        self.first[u] = len(self.euler)
        self.euler.append(u)
        self.depth_arr.append(d)
        for v in self.graph[u]:
            if self.depth[v] == -1:
                self._dfs(v, d + 1)
                self.euler.append(u)
                self.depth_arr.append(d)

    def _build_sparse(self) -> None:
        m = len(self.euler)
        LOG = max(1, m.bit_length())
        self.sparse: list[list[int]] = [[i for i in range(m)]]
        for j in range(1, LOG):
            prev = self.sparse[j - 1]
            half = 1 << (j - 1)
            curr = []
            for i in range(m):
                if i + half < m:
                    a, b = prev[i], prev[i + half]
                    curr.append(a if self.depth_arr[a] <= self.depth_arr[b] else b)
                else:
                    curr.append(prev[i])
            self.sparse.append(curr)
        self.log_table = [0] * (m + 1)
        for i in range(2, m + 1):
            self.log_table[i] = self.log_table[i // 2] + 1

    def query(self, u: int, v: int) -> int:
        l, r = self.first[u], self.first[v]
        if l > r:
            l, r = r, l
        length = r - l + 1
        k = self.log_table[length]
        a, b = self.sparse[k][l], self.sparse[k][r - (1 << k) + 1]
        return self.euler[a if self.depth_arr[a] <= self.depth_arr[b] else b]


# --- Variant 3: Naive LCA (walk up with parent pointers) ---
class NaiveLCA:
    """
    Simple LCA by walking up from both nodes using depth info.
    Build: O(n), Query: O(depth)
    """

    def __init__(self, n: int, edges: list[tuple[int, int]], root: int = 1) -> None:
        self.graph: dict[int, list[int]] = defaultdict(list)
        for u, v in edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
        self.parent: list[int] = [0] * (n + 1)
        self.depth: list[int] = [-1] * (n + 1)
        self._bfs(root)

    def _bfs(self, root: int) -> None:
        from collections import deque
        q: deque[int] = deque([root])
        self.depth[root] = 0
        while q:
            u = q.popleft()
            for v in self.graph[u]:
                if self.depth[v] == -1:
                    self.depth[v] = self.depth[u] + 1
                    self.parent[v] = u
                    q.append(v)

    def query(self, u: int, v: int) -> int:
        while self.depth[u] > self.depth[v]:
            u = self.parent[u]
        while self.depth[v] > self.depth[u]:
            v = self.parent[v]
        while u != v:
            u = self.parent[u]
            v = self.parent[v]
        return u


def benchmark() -> None:
    # Build a balanced binary tree of depth 10 (1023 nodes)
    n = 1023
    edges: list[tuple[int, int]] = []
    for i in range(1, n // 2 + 1):
        if 2 * i <= n:
            edges.append((i, 2 * i))
        if 2 * i + 1 <= n:
            edges.append((i, 2 * i + 1))

    queries = [(1, n), (n // 4, n // 2), (2, n - 1), (100, 200), (500, 600)]

    def bench_v1():
        lca = BinaryLiftingLCA(n, edges)
        for u, v in queries:
            lca.query(u, v)

    def bench_v2():
        lca = EulerTourRMQLCA(n, edges)
        for u, v in queries:
            lca.query(u, v)

    def bench_v3():
        lca = NaiveLCA(n, edges)
        for u, v in queries:
            lca.query(u, v)

    t1 = timeit.timeit(bench_v1, number=100)
    t2 = timeit.timeit(bench_v2, number=100)
    t3 = timeit.timeit(bench_v3, number=100)

    print("Benchmark (100 runs, n=1023 nodes, 5 queries):")
    print(f"  Variant 1 (Binary Lifting):  {t1:.4f}s")
    print(f"  Variant 2 (Euler+RMQ):       {t2:.4f}s")
    print(f"  Variant 3 (Naive walk-up):   {t3:.4f}s")
    print("  Note: Euler+RMQ has O(1) query but higher build constant.")


if __name__ == "__main__":
    benchmark()
