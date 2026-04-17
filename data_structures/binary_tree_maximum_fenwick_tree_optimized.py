"""
Optimized variants for Maximum Fenwick Tree (Binary Indexed Tree for range max).

Variants:
1. MaxFenwickTree    — Original O(log^2 n) query from main file
2. SumFenwickTree    — Classic sum BIT (O(log n) prefix sum)
3. SegTreeMaxFast    — Iterative segment tree for max queries (O(log n))
"""

from __future__ import annotations

import timeit


# --- Variant 1: Max Fenwick Tree (from main file) ---
class MaxFenwickTree:
    def __init__(self, size: int) -> None:
        self.size = size
        self.arr = [0] * size
        self.tree = [0] * size

    @staticmethod
    def get_next(index: int) -> int:
        return index | (index + 1)

    @staticmethod
    def get_prev(index: int) -> int:
        return (index & (index + 1)) - 1

    def update(self, index: int, value: int) -> None:
        self.arr[index] = value
        while index < self.size:
            current_left_border = self.get_prev(index) + 1
            if current_left_border == index:
                self.tree[index] = value
            else:
                self.tree[index] = max(value, current_left_border, index)
            index = self.get_next(index)

    def query(self, left: int, right: int) -> int:
        right -= 1
        result = 0
        while left <= right:
            current_left = self.get_prev(right)
            if left <= current_left:
                result = max(result, self.tree[right])
                right = current_left
            else:
                result = max(result, self.arr[right])
                right -= 1
        return result


# --- Variant 2: Classic sum Fenwick Tree ---
class SumFenwickTree:
    """
    Standard BIT for prefix sums.
    Update: O(log n), Prefix sum query: O(log n)
    """

    def __init__(self, n: int) -> None:
        self.n = n
        self.tree = [0] * (n + 1)

    def update(self, i: int, delta: int) -> None:
        """Add delta to index i (1-indexed)."""
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)

    def prefix_sum(self, i: int) -> int:
        """Sum of [1..i]."""
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

    def range_sum(self, l: int, r: int) -> int:
        """Sum of [l..r] (1-indexed)."""
        return self.prefix_sum(r) - self.prefix_sum(l - 1)


# --- Variant 3: Iterative segment tree for range max ---
class IterativeMaxSegTree:
    """Iterative segment tree: O(log n) update and range max query."""

    def __init__(self, n: int) -> None:
        self.n = n
        self.tree = [0] * (2 * n)

    def update(self, pos: int, val: int) -> None:
        pos += self.n
        self.tree[pos] = val
        while pos > 1:
            pos //= 2
            self.tree[pos] = max(self.tree[2 * pos], self.tree[2 * pos + 1])

    def query(self, left: int, right: int) -> int:
        """Max in [left, right] inclusive (0-indexed)."""
        res = 0
        left += self.n
        right += self.n
        while left <= right:
            if left % 2 == 1:
                res = max(res, self.tree[left])
                left += 1
            if right % 2 == 0:
                res = max(res, self.tree[right])
                right -= 1
            left //= 2
            right //= 2
        return res


def benchmark() -> None:
    N = 1000
    vals = list(range(1, N + 1))

    def bench_v1():
        ft = MaxFenwickTree(N)
        for i, v in enumerate(vals):
            ft.update(i, v)
        for i in range(0, N, 100):
            ft.query(i, i + 100)

    def bench_v2():
        bit = SumFenwickTree(N)
        for i, v in enumerate(vals, 1):
            bit.update(i, v)
        for i in range(1, N, 100):
            bit.range_sum(i, min(i + 99, N))

    def bench_v3():
        st = IterativeMaxSegTree(N)
        for i, v in enumerate(vals):
            st.update(i, v)
        for i in range(0, N, 100):
            st.query(i, min(i + 99, N - 1))

    t1 = timeit.timeit(bench_v1, number=200)
    t2 = timeit.timeit(bench_v2, number=200)
    t3 = timeit.timeit(bench_v3, number=200)

    print("Benchmark (200 runs, N=1000):")
    print(f"  Variant 1 (Max Fenwick Tree):       {t1:.4f}s")
    print(f"  Variant 2 (Sum Fenwick Tree):        {t2:.4f}s")
    print(f"  Variant 3 (Iterative Seg Tree Max):  {t3:.4f}s")
    print("  Iterative segment tree has cleaner O(log n) vs O(log^2 n) for max BIT.")


if __name__ == "__main__":
    benchmark()
