"""
Fenwick Tree — Optimized Variants & Benchmark

Three Fenwick tree implementations:
  1. Original class-based with deepcopy init
  2. Functional approach (pure functions on list)
  3. Numpy-based (for large numeric arrays)

Run:
    python binary_tree_fenwick_tree_optimized.py
"""

from __future__ import annotations

import timeit
from copy import deepcopy


# ─── Variant 1: Original class-based ─────────────────────────────────────────

class FenwickTreeV1:
    """Original implementation — class-based with deepcopy init."""

    def __init__(self, arr: list[int]) -> None:
        self.size = len(arr)
        self.tree = deepcopy(arr)
        for i in range(1, self.size):
            j = i + (i & -i)
            if j < self.size:
                self.tree[j] += self.tree[i]

    def add(self, index: int, value: int) -> None:
        if index == 0:
            self.tree[0] += value
            return
        while index < self.size:
            self.tree[index] += value
            index += index & -index

    def prefix(self, right: int) -> int:
        if right == 0:
            return 0
        result = self.tree[0]
        right -= 1
        while right > 0:
            result += self.tree[right]
            right -= right & -right
        return result

    def query(self, left: int, right: int) -> int:
        return self.prefix(right) - self.prefix(left)


# ─── Variant 2: Functional / procedural approach (no class) ──────────────────

def fenwick_build(arr: list[int]) -> list[int]:
    """Build Fenwick tree in O(n)."""
    tree = arr[:]
    n = len(tree)
    for i in range(1, n):
        j = i + (i & -i)
        if j < n:
            tree[j] += tree[i]
    return tree


def fenwick_add(tree: list[int], index: int, value: int) -> None:
    n = len(tree)
    if index == 0:
        tree[0] += value
        return
    while index < n:
        tree[index] += value
        index += index & -index


def fenwick_prefix(tree: list[int], right: int) -> int:
    if right == 0:
        return 0
    result = tree[0]
    right -= 1
    while right > 0:
        result += tree[right]
        right -= right & -right
    return result


def fenwick_query(tree: list[int], left: int, right: int) -> int:
    return fenwick_prefix(tree, right) - fenwick_prefix(tree, left)


# ─── Variant 3: Segment tree (more general, O(n) build, O(log n) query) ───────

class SegmentTree:
    """
    Segment tree for comparison — supports arbitrary aggregation.
    Build: O(n), query: O(log n), update: O(log n).
    """

    def __init__(self, arr: list[int]) -> None:
        self.n = len(arr)
        self.tree = [0] * (2 * self.n)
        # Build leaf nodes
        for i, v in enumerate(arr):
            self.tree[self.n + i] = v
        # Build internal nodes
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def update(self, index: int, value: int) -> None:
        pos = index + self.n
        self.tree[pos] = value
        while pos > 1:
            pos //= 2
            self.tree[pos] = self.tree[2 * pos] + self.tree[2 * pos + 1]

    def query(self, left: int, right: int) -> int:
        """Sum in [left, right) — half-open interval."""
        result = 0
        lo, hi = left + self.n, right + self.n
        while lo < hi:
            if lo & 1:
                result += self.tree[lo]
                lo += 1
            if hi & 1:
                hi -= 1
                result += self.tree[hi]
            lo >>= 1
            hi >>= 1
        return result


# ─── Benchmark ────────────────────────────────────────────────────────────────

def benchmark() -> None:
    import random

    n = 1024
    arr = [random.randint(0, 100) for _ in range(n)]

    # Correctness check
    ft1 = FenwickTreeV1(arr)
    ft2_tree = fenwick_build(arr)
    st = SegmentTree(arr)

    for i in range(0, n, 100):
        for j in range(i + 1, min(i + 50, n)):
            r1 = ft1.query(i, j)
            r2 = fenwick_query(ft2_tree, i, j)
            r3 = st.query(i, j)
            assert r1 == r2 == r3 == sum(arr[i:j]), f"Mismatch at [{i},{j})"

    print("All queries match brute-force sum.")

    def run_v1() -> None:
        ft = FenwickTreeV1(arr)
        for i in range(0, n, 8):
            ft.add(i, 1)
        for i in range(0, n, 8):
            ft.query(i, min(i + 4, n))

    def run_v2() -> None:
        tree = fenwick_build(arr)
        for i in range(0, n, 8):
            fenwick_add(tree, i, 1)
        for i in range(0, n, 8):
            fenwick_query(tree, i, min(i + 4, n))

    def run_v3() -> None:
        seg = SegmentTree(arr)
        for i in range(0, n, 8):
            seg.update(i, arr[i] + 1)
        for i in range(0, n, 8):
            seg.query(i, min(i + 4, n))

    runs = 500
    t1 = timeit.timeit(run_v1, number=runs)
    t2 = timeit.timeit(run_v2, number=runs)
    t3 = timeit.timeit(run_v3, number=runs)

    print(f"\nFenwick Tree Benchmark ({runs} runs, n={n}):")
    print(f"  V1 Class-based Fenwick:       {t1:.4f}s")
    print(f"  V2 Functional Fenwick:        {t2:.4f}s")
    print(f"  V3 Segment Tree (comparison): {t3:.4f}s")


if __name__ == "__main__":
    benchmark()
