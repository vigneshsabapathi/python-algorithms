"""
Optimized variants of Disjoint Set (Union-Find).

Three implementations:
1. Node-based with path compression + union by rank (original)
2. Array-based with path compression + union by rank
3. Array-based with path splitting (Tarjan's optimization)

Benchmarks using timeit.
"""

import timeit


# Variant 1: Node-based (original style)
class NodeDisjointSet:
    """
    Node-based disjoint set with union by rank and path compression.

    >>> ds = NodeDisjointSet(5)
    >>> ds.union(0, 1)
    True
    >>> ds.union(1, 2)
    True
    >>> ds.find(0) == ds.find(2)
    True
    >>> ds.find(3) == ds.find(4)
    False
    >>> ds.union(3, 4)
    True
    >>> ds.find(3) == ds.find(4)
    True
    """

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


# Variant 2: Array-based with path compression + size tracking
class SizeDisjointSet:
    """
    Array-based disjoint set with union by size.

    >>> ds = SizeDisjointSet(5)
    >>> ds.union(0, 1)
    True
    >>> ds.union(1, 2)
    True
    >>> ds.find(0) == ds.find(2)
    True
    >>> ds.union(0, 2)
    False
    """

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:  # path compression
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.size[rx] < self.size[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        self.size[rx] += self.size[ry]
        return True


# Variant 3: Path splitting (Tarjan) — avoids recursion
class PathSplitDisjointSet:
    """
    Array-based disjoint set with path splitting (Tarjan's optimization).
    Path splitting makes every node on the path point to its grandparent.

    >>> ds = PathSplitDisjointSet(5)
    >>> ds.union(0, 1)
    True
    >>> ds.union(1, 2)
    True
    >>> ds.find(0) == ds.find(2)
    True
    """

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x], x = self.parent[self.parent[x]], self.parent[x]
        return x

    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


def benchmark():
    n = 1000
    pairs = [(i, i + 1) for i in range(0, n - 1, 2)]
    runs = 500

    def run_node():
        ds = NodeDisjointSet(n)
        for a, b in pairs:
            ds.union(a, b)
        return ds.find(0)

    def run_size():
        ds = SizeDisjointSet(n)
        for a, b in pairs:
            ds.union(a, b)
        return ds.find(0)

    def run_split():
        ds = PathSplitDisjointSet(n)
        for a, b in pairs:
            ds.union(a, b)
        return ds.find(0)

    t1 = timeit.timeit(run_node, number=runs)
    t2 = timeit.timeit(run_size, number=runs)
    t3 = timeit.timeit(run_split, number=runs)

    print(f"node-based (rank+compress):   {t1:.4f}s for {runs} runs")
    print(f"array-based (size+compress):  {t2:.4f}s for {runs} runs")
    print(f"path-splitting (Tarjan):      {t3:.4f}s for {runs} runs")


if __name__ == "__main__":
    benchmark()
