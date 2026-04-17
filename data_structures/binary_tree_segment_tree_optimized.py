"""
Optimized variants for Segment Tree.

Variants:
1. RecursiveSegTree   — Standard recursive (from main file), range max
2. IterativeSegTree   — Non-recursive (Fenwick-style indexing), generic combiner
3. SparseSegTree      — Sparse / implicit segment tree (useful for huge ranges)
"""

from __future__ import annotations

import math
import timeit
from collections.abc import Callable
from typing import Any


# --- Variant 1: Recursive max segment tree ---
class RecursiveSegTree:
    def __init__(self, a: list[int]) -> None:
        self.n = len(a)
        self.st = [0] * (4 * self.n)
        if self.n:
            self._build(1, 0, self.n - 1, a)

    def _build(self, idx: int, l: int, r: int, a: list[int]) -> None:
        if l == r:
            self.st[idx] = a[l]
            return
        m = (l + r) // 2
        self._build(2 * idx, l, m, a)
        self._build(2 * idx + 1, m + 1, r, a)
        self.st[idx] = max(self.st[2 * idx], self.st[2 * idx + 1])

    def query(self, l: int, r: int) -> int:
        return self._query(1, 0, self.n - 1, l, r)

    def _query(self, idx: int, lo: int, hi: int, l: int, r: int) -> int | float:
        if hi < l or lo > r:
            return -math.inf
        if lo >= l and hi <= r:
            return self.st[idx]
        m = (lo + hi) // 2
        return max(self._query(2 * idx, lo, m, l, r), self._query(2 * idx + 1, m + 1, hi, l, r))

    def update(self, pos: int, val: int) -> None:
        self._update(1, 0, self.n - 1, pos, val)

    def _update(self, idx: int, lo: int, hi: int, pos: int, val: int) -> None:
        if lo == hi:
            self.st[idx] = val
            return
        m = (lo + hi) // 2
        if pos <= m:
            self._update(2 * idx, lo, m, pos, val)
        else:
            self._update(2 * idx + 1, m + 1, hi, pos, val)
        self.st[idx] = max(self.st[2 * idx], self.st[2 * idx + 1])


# --- Variant 2: Iterative segment tree (generic combiner) ---
class IterativeSegTree:
    def __init__(self, arr: list, fn: Callable[[Any, Any], Any]) -> None:
        self.n = len(arr)
        self.fn = fn
        self.st: list = [None] * self.n + list(arr)
        for i in range(self.n - 1, 0, -1):
            self.st[i] = fn(self.st[2 * i], self.st[2 * i + 1])

    def update(self, pos: int, val: Any) -> None:
        pos += self.n
        self.st[pos] = val
        while pos > 1:
            pos //= 2
            self.st[pos] = self.fn(self.st[2 * pos], self.st[2 * pos + 1])

    def query(self, left: int, right: int) -> Any:
        """Inclusive [left, right] range query."""
        left += self.n
        right += self.n
        res = None
        while left <= right:
            if left % 2 == 1:
                res = self.st[left] if res is None else self.fn(res, self.st[left])
                left += 1
            if right % 2 == 0:
                res = self.st[right] if res is None else self.fn(res, self.st[right])
                right -= 1
            left //= 2
            right //= 2
        return res


# --- Variant 3: Sparse (implicit) segment tree, good for huge index ranges ---
class SparseSegTreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self) -> None:
        self.val: int = 0
        self.left: SparseSegTreeNode | None = None
        self.right: SparseSegTreeNode | None = None


class SparseSegTree:
    """
    Segment tree that only creates nodes when needed.
    Suitable for very large index ranges where most positions are 0.
    """

    def __init__(self, lo: int, hi: int) -> None:
        self.lo = lo
        self.hi = hi
        self.root = SparseSegTreeNode()

    def update(self, pos: int, val: int) -> None:
        self._update(self.root, self.lo, self.hi, pos, val)

    def _update(self, node: SparseSegTreeNode, lo: int, hi: int, pos: int, val: int) -> None:
        if lo == hi:
            node.val = val
            return
        mid = (lo + hi) // 2
        if pos <= mid:
            if node.left is None:
                node.left = SparseSegTreeNode()
            self._update(node.left, lo, mid, pos, val)
        else:
            if node.right is None:
                node.right = SparseSegTreeNode()
            self._update(node.right, mid + 1, hi, pos, val)
        left_val = node.left.val if node.left else 0
        right_val = node.right.val if node.right else 0
        node.val = max(left_val, right_val)

    def query(self, l: int, r: int) -> int:
        return self._query(self.root, self.lo, self.hi, l, r)

    def _query(self, node: SparseSegTreeNode | None, lo: int, hi: int, l: int, r: int) -> int:
        if node is None or hi < l or lo > r:
            return 0
        if lo >= l and hi <= r:
            return node.val
        mid = (lo + hi) // 2
        return max(
            self._query(node.left, lo, mid, l, r),
            self._query(node.right, mid + 1, hi, l, r),
        )


def benchmark() -> None:
    import timeit

    A = list(range(1, 1001))
    N = 1000

    def bench_v1():
        st = RecursiveSegTree(A)
        for i in range(0, N, 50):
            st.query(i, min(i + 49, N - 1))
        for i in range(0, N, 100):
            st.update(i, i * 2)

    def bench_v2():
        st = IterativeSegTree(A, max)
        for i in range(0, N, 50):
            st.query(i, min(i + 49, N - 1))
        for i in range(0, N, 100):
            st.update(i, i * 2)

    def bench_v3():
        st = SparseSegTree(0, 10**9)
        for i in range(0, N, 10):
            st.update(i * 1000, i)
        for i in range(0, N, 50):
            st.query(i * 1000, (i + 49) * 1000)

    t1 = timeit.timeit(bench_v1, number=100)
    t2 = timeit.timeit(bench_v2, number=100)
    t3 = timeit.timeit(bench_v3, number=100)

    print("Benchmark (100 runs, N=1000):")
    print(f"  Variant 1 (Recursive Seg):   {t1:.4f}s")
    print(f"  Variant 2 (Iterative Seg):   {t2:.4f}s")
    print(f"  Variant 3 (Sparse Seg):      {t3:.4f}s")
    print("  Iterative is fastest; Sparse shines for huge sparse ranges.")


if __name__ == "__main__":
    benchmark()
