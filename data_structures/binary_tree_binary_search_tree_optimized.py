"""
Binary Search Tree — Optimized Variants & Benchmark

Three BST implementations compared:
  1. Linked-node BST (original dataclass approach)
  2. Array-based BST (heap-like index layout)
  3. SortedList (bisect module) — O(log n) search, O(n) insert

Run:
    python binary_tree_binary_search_tree_optimized.py
"""

from __future__ import annotations

import timeit
from dataclasses import dataclass, field


# ─── Variant 1: Linked-Node BST ──────────────────────────────────────────────

@dataclass
class NodeV1:
    value: int
    left: NodeV1 | None = None
    right: NodeV1 | None = None


class BSTV1:
    """Standard linked-node BST."""

    def __init__(self) -> None:
        self.root: NodeV1 | None = None

    def insert(self, value: int) -> None:
        if not self.root:
            self.root = NodeV1(value)
            return
        node = self.root
        while True:
            if value < node.value:
                if node.left is None:
                    node.left = NodeV1(value)
                    return
                node = node.left
            elif value > node.value:
                if node.right is None:
                    node.right = NodeV1(value)
                    return
                node = node.right
            else:
                return

    def search(self, value: int) -> bool:
        node = self.root
        while node:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False

    def inorder(self) -> list[int]:
        result: list[int] = []

        def _inorder(n: NodeV1 | None) -> None:
            if n:
                _inorder(n.left)
                result.append(n.value)
                _inorder(n.right)

        _inorder(self.root)
        return result


# ─── Variant 2: Array-based BST ──────────────────────────────────────────────

class BSTV2:
    """
    Array-indexed BST.
    Node at index i has children at 2i+1 (left) and 2i+2 (right).
    Supports small trees without pointer overhead.
    Lookup: O(log n) average.
    """

    def __init__(self, capacity: int = 2047) -> None:
        self._tree: list[int | None] = [None] * capacity

    def insert(self, value: int) -> None:
        i = 0
        while i < len(self._tree):
            if self._tree[i] is None:
                self._tree[i] = value
                return
            elif value < self._tree[i]:  # type: ignore[operator]
                i = 2 * i + 1
            elif value > self._tree[i]:  # type: ignore[operator]
                i = 2 * i + 2
            else:
                return  # duplicate
        raise OverflowError("BST array capacity exceeded")

    def search(self, value: int) -> bool:
        i = 0
        while i < len(self._tree) and self._tree[i] is not None:
            if value == self._tree[i]:
                return True
            elif value < self._tree[i]:  # type: ignore[operator]
                i = 2 * i + 1
            else:
                i = 2 * i + 2
        return False


# ─── Variant 3: SortedList (bisect) — baseline ───────────────────────────────

class BSTV3:
    """
    SortedList backed by Python's bisect module.
    O(log n) search, O(n) insert due to list shifting.
    Acts as a BST replacement for read-heavy workloads on small datasets.
    """

    def __init__(self) -> None:
        import bisect

        self._data: list[int] = []
        self._bisect = bisect

    def insert(self, value: int) -> None:
        self._bisect.insort(self._data, value)

    def search(self, value: int) -> bool:
        idx = self._bisect.bisect_left(self._data, value)
        return idx < len(self._data) and self._data[idx] == value

    def inorder(self) -> list[int]:
        return list(self._data)


# ─── Benchmark ────────────────────────────────────────────────────────────────

def benchmark() -> None:
    import random

    # Use sorted insertion for array BST (worst case for linked BST, predictable for array)
    keys = list(range(1, 64))  # 63 keys fit perfectly in 7-level BST
    random.shuffle(keys)
    search_keys = keys[:20]

    def run_v1() -> None:
        t = BSTV1()
        for k in keys:
            t.insert(k)
        for k in search_keys:
            t.search(k)

    def run_v2() -> None:
        t = BSTV2(capacity=8191)  # 13 levels, handles up to 8191 nodes
        for k in keys:
            t.insert(k)
        for k in search_keys:
            t.search(k)

    def run_v3() -> None:
        t = BSTV3()
        for k in keys:
            t.insert(k)
        for k in search_keys:
            t.search(k)

    n = 500
    t1 = timeit.timeit(run_v1, number=n)
    t2 = timeit.timeit(run_v2, number=n)
    t3 = timeit.timeit(run_v3, number=n)

    print(f"BST Variant Benchmark ({n} runs, {len(keys)} inserts + {len(search_keys)} searches):")
    print(f"  V1 Linked-node BST:    {t1:.4f}s")
    print(f"  V2 Array-indexed BST:  {t2:.4f}s")
    print(f"  V3 SortedList bisect:  {t3:.4f}s")

    # Correctness check
    t1_tree = BSTV1()
    for k in [5, 3, 7, 1]: t1_tree.insert(k)
    print(f"\nV1 inorder: {t1_tree.inorder()}")
    assert t1_tree.search(3)
    assert not t1_tree.search(99)
    print("All correctness checks passed.")


if __name__ == "__main__":
    benchmark()
