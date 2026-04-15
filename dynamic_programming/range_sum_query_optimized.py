#!/usr/bin/env python3
"""
Optimized and alternative implementations of Range Sum Query.

Variants covered:
1. RangeSumBIT        -- Binary Indexed Tree (Fenwick) — supports updates
2. RangeSumSegTree    -- Segment Tree — supports updates + range queries
3. RangeSumSparse     -- Sparse Table for static range queries

Run:
    python dynamic_programming/range_sum_query_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.range_sum_query import RangeSumQuery as Reference


# ---------------------------------------------------------------------------
# Variant 1 — Binary Indexed Tree (Fenwick Tree)
# ---------------------------------------------------------------------------

class RangeSumBIT:
    """
    Range Sum using a Binary Indexed Tree. Supports point updates in O(log n).

    >>> bit = RangeSumBIT([-2, 0, 3, -5, 2, -1])
    >>> bit.sum_range(0, 2)
    1
    >>> bit.sum_range(2, 5)
    -1
    >>> bit.sum_range(0, 5)
    -3
    """

    def __init__(self, nums: list[int]) -> None:
        self.n = len(nums)
        self.tree = [0] * (self.n + 1)
        for i, v in enumerate(nums):
            self._update(i + 1, v)

    def _update(self, i: int, delta: int) -> None:
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)

    def _prefix(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

    def sum_range(self, left: int, right: int) -> int:
        return self._prefix(right + 1) - self._prefix(left)


# ---------------------------------------------------------------------------
# Variant 2 — Segment Tree
# ---------------------------------------------------------------------------

class RangeSumSegTree:
    """
    Range Sum using a Segment Tree.

    >>> st = RangeSumSegTree([-2, 0, 3, -5, 2, -1])
    >>> st.sum_range(0, 2)
    1
    >>> st.sum_range(2, 5)
    -1
    >>> st.sum_range(0, 5)
    -3
    """

    def __init__(self, nums: list[int]) -> None:
        self.n = len(nums)
        self.tree = [0] * (4 * self.n)
        if self.n > 0:
            self._build(nums, 1, 0, self.n - 1)

    def _build(self, nums: list[int], node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = nums[start]
        else:
            mid = (start + end) // 2
            self._build(nums, 2 * node, start, mid)
            self._build(nums, 2 * node + 1, mid + 1, end)
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def _query(self, node: int, start: int, end: int, l: int, r: int) -> int:
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return (self._query(2 * node, start, mid, l, r) +
                self._query(2 * node + 1, mid + 1, end, l, r))

    def sum_range(self, left: int, right: int) -> int:
        return self._query(1, 0, self.n - 1, left, right)


# ---------------------------------------------------------------------------
# Variant 3 — Sparse Table (static, O(1) query for idempotent ops)
# ---------------------------------------------------------------------------

class RangeSumSparse:
    """
    Prefix-sum approach identical to reference but using itertools.accumulate.

    >>> sp = RangeSumSparse([-2, 0, 3, -5, 2, -1])
    >>> sp.sum_range(0, 2)
    1
    >>> sp.sum_range(2, 5)
    -1
    >>> sp.sum_range(0, 5)
    -3
    """

    def __init__(self, nums: list[int]) -> None:
        from itertools import accumulate
        self.prefix = [0] + list(accumulate(nums))

    def sum_range(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

NUMS = [-2, 0, 3, -5, 2, -1]
TEST_CASES = [(0, 2, 1), (2, 5, -1), (0, 5, -3)]


def run_all() -> None:
    impls = [
        ("reference", Reference(NUMS)),
        ("BIT", RangeSumBIT(NUMS)),
        ("seg_tree", RangeSumSegTree(NUMS)),
        ("sparse", RangeSumSparse(NUMS)),
    ]

    print("\n=== Correctness ===")
    for left, right, expected in TEST_CASES:
        results = {name: obj.sum_range(left, right) for name, obj in impls}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] sum_range({left}, {right})  expected={expected}  " +
              "  ".join(f"{n}={v}" for n, v in results.items()))

    REPS = 100_000
    import random
    random.seed(42)
    bench_nums = [random.randint(-100, 100) for _ in range(1000)]
    queries = [(random.randint(0, 499), random.randint(500, 999)) for _ in range(10)]

    print(f"\n=== Benchmark: {REPS} runs, len=1000, 10 queries ===")
    for name, cls in [("reference", Reference), ("BIT", RangeSumBIT),
                       ("seg_tree", RangeSumSegTree), ("sparse", RangeSumSparse)]:
        obj = cls(bench_nums)
        t = timeit.timeit(
            lambda obj=obj: [obj.sum_range(l, r) for l, r in queries],
            number=REPS
        ) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms / 10 queries")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
