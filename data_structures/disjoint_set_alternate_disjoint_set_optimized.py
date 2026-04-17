"""
Optimized variants of Alternate Disjoint Set (array-based).

Three implementations comparing path compression strategies and
union heuristics.

Benchmarks using timeit.
"""

import timeit


# Variant 1: Original — union by rank with recursive path compression
class DisjointSetRankRecursive:
    """
    Union by rank with recursive path compression.

    >>> ds = DisjointSetRankRecursive([1, 1, 1, 1])
    >>> ds.merge(0, 1)
    True
    >>> ds.merge(2, 3)
    True
    >>> ds.get_parent(0) == ds.get_parent(1)
    True
    >>> ds.get_parent(0) == ds.get_parent(2)
    False
    """

    def __init__(self, set_counts: list) -> None:
        self.set_counts = list(set_counts)
        self.max_set = max(set_counts)
        n = len(set_counts)
        self.ranks = [1] * n
        self.parents = list(range(n))

    def get_parent(self, disj_set: int) -> int:
        if self.parents[disj_set] == disj_set:
            return disj_set
        self.parents[disj_set] = self.get_parent(self.parents[disj_set])
        return self.parents[disj_set]

    def merge(self, src: int, dst: int) -> bool:
        sp, dp = self.get_parent(src), self.get_parent(dst)
        if sp == dp:
            return False
        if self.ranks[dp] >= self.ranks[sp]:
            self.set_counts[dp] += self.set_counts[sp]
            self.set_counts[sp] = 0
            self.parents[sp] = dp
            if self.ranks[dp] == self.ranks[sp]:
                self.ranks[dp] += 1
            joined = self.set_counts[dp]
        else:
            self.set_counts[sp] += self.set_counts[dp]
            self.set_counts[dp] = 0
            self.parents[dp] = sp
            joined = self.set_counts[sp]
        self.max_set = max(self.max_set, joined)
        return True


# Variant 2: Union by size with iterative path compression
class DisjointSetSizeIterative:
    """
    Union by size with iterative (two-pass) path compression.

    >>> ds = DisjointSetSizeIterative([1, 1, 1, 1])
    >>> ds.merge(0, 1)
    True
    >>> ds.merge(2, 3)
    True
    >>> ds.get_parent(0) == ds.get_parent(1)
    True
    """

    def __init__(self, set_counts: list) -> None:
        self.set_counts = list(set_counts)
        n = len(set_counts)
        self.sizes = list(set_counts)
        self.parents = list(range(n))

    def get_parent(self, x: int) -> int:
        root = x
        while self.parents[root] != root:
            root = self.parents[root]
        while self.parents[x] != root:
            self.parents[x], x = root, self.parents[x]
        return root

    def merge(self, src: int, dst: int) -> bool:
        sp, dp = self.get_parent(src), self.get_parent(dst)
        if sp == dp:
            return False
        if self.sizes[sp] < self.sizes[dp]:
            sp, dp = dp, sp
        self.parents[dp] = sp
        self.sizes[sp] += self.sizes[dp]
        self.set_counts[sp] += self.set_counts[dp]
        self.set_counts[dp] = 0
        return True


# Variant 3: Weighted quick union (no path compression, simple)
class DisjointSetWeightedQuick:
    """
    Weighted quick union without path compression (baseline).

    >>> ds = DisjointSetWeightedQuick(4)
    >>> ds.merge(0, 1)
    True
    >>> ds.merge(2, 3)
    True
    >>> ds.find(0) == ds.find(1)
    True
    >>> ds.find(0) == ds.find(2)
    False
    """

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.weight = [1] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def merge(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.weight[rx] < self.weight[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        self.weight[rx] += self.weight[ry]
        return True


def benchmark():
    n = 500
    counts = [1] * n
    pairs = [(i, i + 1) for i in range(0, n - 2, 2)]
    runs = 500

    def run_rank():
        ds = DisjointSetRankRecursive(counts)
        for a, b in pairs:
            ds.merge(a, b)

    def run_size():
        ds = DisjointSetSizeIterative(counts)
        for a, b in pairs:
            ds.merge(a, b)

    def run_weighted():
        ds = DisjointSetWeightedQuick(n)
        for a, b in pairs:
            ds.merge(a, b)

    t1 = timeit.timeit(run_rank, number=runs)
    t2 = timeit.timeit(run_size, number=runs)
    t3 = timeit.timeit(run_weighted, number=runs)

    print(f"rank+recursive_compress:  {t1:.4f}s for {runs} runs")
    print(f"size+iterative_compress:  {t2:.4f}s for {runs} runs")
    print(f"weighted_quick_union:     {t3:.4f}s for {runs} runs")


if __name__ == "__main__":
    benchmark()
