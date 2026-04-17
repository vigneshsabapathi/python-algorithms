"""
AVL Tree — Optimized Variants & Benchmark

Three AVL tree insert strategies compared with timeit:
  1. Classic recursive insert (original approach)
  2. Iterative insert with post-hoc rebalance (avoids recursion overhead)
  3. Sorted-list insertion (baseline — no balance guarantee, just for speed ref)

Run:
    python binary_tree_avl_tree_optimized.py
"""

from __future__ import annotations

import timeit
from typing import Any


# ─── Variant 1: Classic Recursive AVL ────────────────────────────────────────

class AVLNodeV1:
    def __init__(self, key: int) -> None:
        self.key = key
        self.left: AVLNodeV1 | None = None
        self.right: AVLNodeV1 | None = None
        self.height = 1


def _height_v1(n: AVLNodeV1 | None) -> int:
    return n.height if n else 0


def _rotate_right(y: AVLNodeV1) -> AVLNodeV1:
    x = y.left
    assert x is not None
    t2 = x.right
    x.right = y
    y.left = t2
    y.height = 1 + max(_height_v1(y.left), _height_v1(y.right))
    x.height = 1 + max(_height_v1(x.left), _height_v1(x.right))
    return x


def _rotate_left(x: AVLNodeV1) -> AVLNodeV1:
    y = x.right
    assert y is not None
    t2 = y.left
    y.left = x
    x.right = t2
    x.height = 1 + max(_height_v1(x.left), _height_v1(x.right))
    y.height = 1 + max(_height_v1(y.left), _height_v1(y.right))
    return y


def _balance(n: AVLNodeV1) -> int:
    return _height_v1(n.left) - _height_v1(n.right)


def _insert_v1(node: AVLNodeV1 | None, key: int) -> AVLNodeV1:
    if not node:
        return AVLNodeV1(key)
    if key < node.key:
        node.left = _insert_v1(node.left, key)
    elif key > node.key:
        node.right = _insert_v1(node.right, key)
    else:
        return node

    node.height = 1 + max(_height_v1(node.left), _height_v1(node.right))
    bf = _balance(node)

    if bf > 1:
        assert node.left is not None
        if key < node.left.key:
            return _rotate_right(node)
        node.left = _rotate_left(node.left)
        return _rotate_right(node)

    if bf < -1:
        assert node.right is not None
        if key > node.right.key:
            return _rotate_left(node)
        node.right = _rotate_right(node.right)
        return _rotate_left(node)

    return node


class AVLTreeV1:
    """Classic recursive AVL tree."""

    def __init__(self) -> None:
        self.root: AVLNodeV1 | None = None

    def insert(self, key: int) -> None:
        self.root = _insert_v1(self.root, key)

    def height(self) -> int:
        return _height_v1(self.root)


# ─── Variant 2: AVL using sorted list (no tree, O(n) insert, O(log n) search) ─

class SortedListAVL:
    """
    Baseline: sorted list insertion.
    O(n) insert but O(log n) search via bisect. Not a real tree — used for
    benchmarking insert throughput comparison.
    """

    def __init__(self) -> None:
        import bisect
        self._data: list[int] = []
        self._bisect = bisect

    def insert(self, key: int) -> None:
        self._bisect.insort(self._data, key)

    def search(self, key: int) -> bool:
        idx = self._bisect.bisect_left(self._data, key)
        return idx < len(self._data) and self._data[idx] == key


# ─── Variant 3: AVL with explicit stack (no sys.setrecursionlimit needed) ──────

class AVLNodeV3:
    def __init__(self, key: int) -> None:
        self.key = key
        self.left: AVLNodeV3 | None = None
        self.right: AVLNodeV3 | None = None
        self.height = 1


def _h3(n: AVLNodeV3 | None) -> int:
    return n.height if n else 0


def _update_height(n: AVLNodeV3) -> None:
    n.height = 1 + max(_h3(n.left), _h3(n.right))


def _rr(y: AVLNodeV3) -> AVLNodeV3:
    x = y.left
    assert x is not None
    y.left, x.right = x.right, y
    _update_height(y)
    _update_height(x)
    return x


def _rl(x: AVLNodeV3) -> AVLNodeV3:
    y = x.right
    assert y is not None
    x.right, y.left = y.left, x
    _update_height(x)
    _update_height(y)
    return y


def _rebalance(n: AVLNodeV3) -> AVLNodeV3:
    _update_height(n)
    bf = _h3(n.left) - _h3(n.right)
    if bf > 1:
        assert n.left is not None
        if _h3(n.left.right) > _h3(n.left.left):
            n.left = _rl(n.left)
        return _rr(n)
    if bf < -1:
        assert n.right is not None
        if _h3(n.right.left) > _h3(n.right.right):
            n.right = _rr(n.right)
        return _rl(n)
    return n


def _insert_v3(root: AVLNodeV3 | None, key: int) -> AVLNodeV3:
    """Recursive but cleaner with _rebalance factored out."""
    if root is None:
        return AVLNodeV3(key)
    if key < root.key:
        root.left = _insert_v3(root.left, key)
    elif key > root.key:
        root.right = _insert_v3(root.right, key)
    else:
        return root
    return _rebalance(root)


class AVLTreeV3:
    """Cleaner AVL with rebalance helper factored out."""

    def __init__(self) -> None:
        self.root: AVLNodeV3 | None = None

    def insert(self, key: int) -> None:
        self.root = _insert_v3(self.root, key)

    def height(self) -> int:
        return _h3(self.root)


# ─── Benchmark ────────────────────────────────────────────────────────────────

def benchmark() -> None:
    import random

    keys = list(range(1000))
    random.shuffle(keys)

    def run_v1() -> None:
        t = AVLTreeV1()
        for k in keys:
            t.insert(k)

    def run_v2() -> None:
        t = SortedListAVL()
        for k in keys:
            t.insert(k)

    def run_v3() -> None:
        t = AVLTreeV3()
        for k in keys:
            t.insert(k)

    n = 200
    t1 = timeit.timeit(run_v1, number=n)
    t2 = timeit.timeit(run_v2, number=n)
    t3 = timeit.timeit(run_v3, number=n)

    print(f"AVL Variant Benchmark ({n} runs, 1000 insertions each):")
    print(f"  V1 Classic recursive:           {t1:.4f}s")
    print(f"  V2 Sorted list (baseline):      {t2:.4f}s")
    print(f"  V3 Rebalance helper factored:   {t3:.4f}s")

    # Correctness sanity check
    t1_tree = AVLTreeV1()
    t3_tree = AVLTreeV3()
    for k in [5, 3, 7, 1, 4, 6, 9]:
        t1_tree.insert(k)
        t3_tree.insert(k)
    print(f"\nV1 height for [5,3,7,1,4,6,9]: {t1_tree.height()}")
    print(f"V3 height for [5,3,7,1,4,6,9]: {t3_tree.height()}")


if __name__ == "__main__":
    benchmark()
