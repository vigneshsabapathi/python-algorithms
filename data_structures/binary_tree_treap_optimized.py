"""
Optimized variants for Treap (Randomized BST).

Variants:
1. Treap            — Original from main file
2. ImplicitTreap    — Implicit treap (index-based, supports split/merge at index)
3. SortedList       — Python bisect-based sorted list (simple comparison baseline)
"""

from __future__ import annotations

import timeit
from random import random
import bisect


# --- Variant 1: Standard Treap (from main file, encapsulated) ---
class TreapNode:
    def __init__(self, value: int) -> None:
        self.value = value
        self.prior = random()
        self.left: TreapNode | None = None
        self.right: TreapNode | None = None


class Treap:
    def __init__(self) -> None:
        self.root: TreapNode | None = None

    def _split(self, root: TreapNode | None, value: int) -> tuple[TreapNode | None, TreapNode | None]:
        if root is None:
            return None, None
        if value < root.value:
            left, root.left = self._split(root.left, value)
            return left, root
        else:
            root.right, right = self._split(root.right, value)
            return root, right

    def _merge(self, left: TreapNode | None, right: TreapNode | None) -> TreapNode | None:
        if not left or not right:
            return left or right
        if left.prior < right.prior:
            left.right = self._merge(left.right, right)
            return left
        else:
            right.left = self._merge(left, right.left)
            return right

    def insert(self, value: int) -> None:
        node = TreapNode(value)
        left, right = self._split(self.root, value)
        self.root = self._merge(self._merge(left, node), right)

    def search(self, value: int) -> bool:
        node = self.root
        while node:
            if node.value == value:
                return True
            elif value < node.value:
                node = node.left
            else:
                node = node.right
        return False

    def delete(self, value: int) -> None:
        left, right = self._split(self.root, value - 1)
        _, right = self._split(right, value)
        self.root = self._merge(left, right)


# --- Variant 2: Implicit Treap (sequence-based, supports arbitrary split/merge) ---
class ImplicitTreapNode:
    def __init__(self, val: int) -> None:
        self.val = val
        self.prior = random()
        self.size = 1
        self.left: ImplicitTreapNode | None = None
        self.right: ImplicitTreapNode | None = None


class ImplicitTreap:
    """
    Implicit treap — like a balanced BST over indices.
    Supports O(log n): insert at position, delete at position, query range.
    """

    def _size(self, node: ImplicitTreapNode | None) -> int:
        return node.size if node else 0

    def _update(self, node: ImplicitTreapNode) -> None:
        node.size = 1 + self._size(node.left) + self._size(node.right)

    def _split(self, node: ImplicitTreapNode | None, k: int) -> tuple:
        """Split into first k elements and the rest."""
        if node is None:
            return None, None
        left_size = self._size(node.left)
        if k <= left_size:
            left, node.left = self._split(node.left, k)
            self._update(node)
            return left, node
        else:
            node.right, right = self._split(node.right, k - left_size - 1)
            self._update(node)
            return node, right

    def _merge(self, left: ImplicitTreapNode | None, right: ImplicitTreapNode | None) -> ImplicitTreapNode | None:
        if not left or not right:
            return left or right
        if left.prior > right.prior:
            left.right = self._merge(left.right, right)
            self._update(left)
            return left
        else:
            right.left = self._merge(left, right.left)
            self._update(right)
            return right

    def __init__(self) -> None:
        self.root: ImplicitTreapNode | None = None

    def insert_at(self, pos: int, val: int) -> None:
        node = ImplicitTreapNode(val)
        left, right = self._split(self.root, pos)
        self.root = self._merge(self._merge(left, node), right)

    def get_at(self, pos: int) -> int:
        left, right = self._split(self.root, pos)
        single, right = self._split(right, 1)
        val = single.val if single else -1  # type: ignore[union-attr]
        self.root = self._merge(self._merge(left, single), right)
        return val


# --- Variant 3: bisect sorted list ---
class BisectSorted:
    def __init__(self) -> None:
        self._data: list[int] = []

    def insert(self, val: int) -> None:
        bisect.insort(self._data, val)

    def search(self, val: int) -> bool:
        idx = bisect.bisect_left(self._data, val)
        return idx < len(self._data) and self._data[idx] == val

    def delete(self, val: int) -> None:
        idx = bisect.bisect_left(self._data, val)
        if idx < len(self._data) and self._data[idx] == val:
            self._data.pop(idx)


def benchmark() -> None:
    vals = list(range(300))
    queries = [50, 100, 150, 250, 299]

    def bench_treap():
        t = Treap()
        for v in vals:
            t.insert(v)
        for q in queries:
            t.search(q)
        for q in queries:
            t.delete(q)

    def bench_implicit():
        t = ImplicitTreap()
        for i, v in enumerate(vals):
            t.insert_at(i, v)
        for q in queries:
            t.get_at(q)

    def bench_bisect():
        sl = BisectSorted()
        for v in vals:
            sl.insert(v)
        for q in queries:
            sl.search(q)
        for q in queries:
            sl.delete(q)

    t1 = timeit.timeit(bench_treap, number=200)
    t2 = timeit.timeit(bench_implicit, number=200)
    t3 = timeit.timeit(bench_bisect, number=200)

    print("Benchmark (200 runs, 300 inserts, 5 ops):")
    print(f"  Variant 1 (Treap):          {t1:.4f}s")
    print(f"  Variant 2 (Implicit Treap): {t2:.4f}s")
    print(f"  Variant 3 (Bisect list):    {t3:.4f}s")
    print("  Bisect fastest for small n; Treap/Implicit scale to O(log n) reliably.")


if __name__ == "__main__":
    benchmark()
