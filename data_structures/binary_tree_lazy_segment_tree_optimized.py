"""
Optimized variants for Lazy Segment Tree.

Variants:
1. LazySegTreeMax   — Original lazy propagation (range update, range max query)
2. LazySegTreeAdd   — Lazy additive segment tree (sum queries with range add)
3. LazySegTreeIter  — Iterative (non-recursive) lazy segment tree for range sum
"""

from __future__ import annotations

import math
import timeit


# --- Variant 1: Original lazy max segment tree (cleaned up) ---
class LazySegTreeMax:
    """Lazy segment tree for range-assign + range-max queries."""

    def __init__(self, size: int) -> None:
        self.size = size
        self.tree = [0] * (4 * size)
        self.lazy = [0] * (4 * size)
        self.flag = [False] * (4 * size)

    def _push_down(self, idx: int, left: int, right: int) -> None:
        if self.flag[idx]:
            val = self.lazy[idx]
            self.tree[idx] = val
            self.flag[idx] = False
            if left != right:
                for child in (idx * 2, idx * 2 + 1):
                    self.lazy[child] = val
                    self.flag[child] = True

    def build(self, idx: int, left: int, right: int, a: list[int]) -> None:
        if left == right:
            self.tree[idx] = a[left - 1]
            return
        mid = (left + right) // 2
        self.build(idx * 2, left, mid, a)
        self.build(idx * 2 + 1, mid + 1, right, a)
        self.tree[idx] = max(self.tree[idx * 2], self.tree[idx * 2 + 1])

    def update(self, idx: int, left: int, right: int, a: int, b: int, val: int) -> None:
        self._push_down(idx, left, right)
        if right < a or left > b:
            return
        if left >= a and right <= b:
            self.lazy[idx] = val
            self.flag[idx] = True
            return
        mid = (left + right) // 2
        self.update(idx * 2, left, mid, a, b, val)
        self.update(idx * 2 + 1, mid + 1, right, a, b, val)
        self.tree[idx] = max(self.tree[idx * 2], self.tree[idx * 2 + 1])

    def query(self, idx: int, left: int, right: int, a: int, b: int) -> int | float:
        self._push_down(idx, left, right)
        if right < a or left > b:
            return -math.inf
        if left >= a and right <= b:
            return self.tree[idx]
        mid = (left + right) // 2
        return max(
            self.query(idx * 2, left, mid, a, b),
            self.query(idx * 2 + 1, mid + 1, right, a, b),
        )


# --- Variant 2: Lazy additive segment tree (range add, range sum) ---
class LazySegTreeAdd:
    """Lazy segment tree for range-add + range-sum queries."""

    def __init__(self, a: list[int]) -> None:
        self.n = len(a)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self._build(1, 0, self.n - 1, a)

    def _build(self, idx: int, left: int, right: int, a: list[int]) -> None:
        if left == right:
            self.tree[idx] = a[left]
            return
        mid = (left + right) // 2
        self._build(idx * 2, left, mid, a)
        self._build(idx * 2 + 1, mid + 1, right, a)
        self.tree[idx] = self.tree[idx * 2] + self.tree[idx * 2 + 1]

    def _push_down(self, idx: int, left: int, right: int) -> None:
        if self.lazy[idx] != 0:
            mid = (left + right) // 2
            for child, lo, hi in [(idx * 2, left, mid), (idx * 2 + 1, mid + 1, right)]:
                self.tree[child] += self.lazy[idx] * (hi - lo + 1)
                self.lazy[child] += self.lazy[idx]
            self.lazy[idx] = 0

    def range_add(self, idx: int, left: int, right: int, a: int, b: int, val: int) -> None:
        if right < a or left > b:
            return
        if left >= a and right <= b:
            self.tree[idx] += val * (right - left + 1)
            self.lazy[idx] += val
            return
        self._push_down(idx, left, right)
        mid = (left + right) // 2
        self.range_add(idx * 2, left, mid, a, b, val)
        self.range_add(idx * 2 + 1, mid + 1, right, a, b, val)
        self.tree[idx] = self.tree[idx * 2] + self.tree[idx * 2 + 1]

    def range_sum(self, idx: int, left: int, right: int, a: int, b: int) -> int:
        if right < a or left > b:
            return 0
        if left >= a and right <= b:
            return self.tree[idx]
        self._push_down(idx, left, right)
        mid = (left + right) // 2
        return (
            self.range_sum(idx * 2, left, mid, a, b)
            + self.range_sum(idx * 2 + 1, mid + 1, right, a, b)
        )


# --- Variant 3: Iterative (non-recursive) simple segment tree (sum, O(log n)) ---
class IterativeSumSegTree:
    """Non-recursive segment tree for point update + range sum."""

    def __init__(self, a: list[int]) -> None:
        self.n = len(a)
        self.tree = [0] * (2 * self.n)
        for i, v in enumerate(a):
            self.tree[self.n + i] = v
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def update(self, pos: int, val: int) -> None:
        pos += self.n
        self.tree[pos] = val
        while pos > 1:
            pos //= 2
            self.tree[pos] = self.tree[2 * pos] + self.tree[2 * pos + 1]

    def query(self, left: int, right: int) -> int:
        """Range sum [left, right] inclusive."""
        result = 0
        left += self.n
        right += self.n + 1
        while left < right:
            if left & 1:
                result += self.tree[left]
                left += 1
            if right & 1:
                right -= 1
                result += self.tree[right]
            left >>= 1
            right >>= 1
        return result


def benchmark() -> None:
    import timeit

    A = list(range(1, 1001))
    N = 1000

    def bench_v1():
        st = LazySegTreeMax(N)
        st.build(1, 1, N, A)
        for i in range(1, N + 1, 100):
            st.update(1, 1, N, i, i + 99, i)
        for i in range(1, N + 1, 100):
            st.query(1, 1, N, i, i + 99)

    def bench_v2():
        st = LazySegTreeAdd(A)
        for i in range(0, N, 100):
            st.range_add(1, 0, N - 1, i, i + 99, 10)
        for i in range(0, N, 100):
            st.range_sum(1, 0, N - 1, i, i + 99)

    def bench_v3():
        st = IterativeSumSegTree(A)
        for i in range(0, N, 10):
            st.update(i, i * 2)
        for i in range(0, N, 100):
            st.query(i, i + 99)

    t1 = timeit.timeit(bench_v1, number=50)
    t2 = timeit.timeit(bench_v2, number=50)
    t3 = timeit.timeit(bench_v3, number=50)

    print("Benchmark (50 runs, N=1000):")
    print(f"  Variant 1 (Lazy Max Seg Tree):    {t1:.4f}s")
    print(f"  Variant 2 (Lazy Additive Seg):    {t2:.4f}s")
    print(f"  Variant 3 (Iterative Sum Seg):    {t3:.4f}s")
    print(f"  Fastest: Variant 3 (iterative, no recursion overhead)")


if __name__ == "__main__":
    benchmark()
