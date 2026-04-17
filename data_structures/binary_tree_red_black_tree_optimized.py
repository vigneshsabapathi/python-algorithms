"""
Optimized variants for Red-Black Tree / Self-Balancing BST.

Variants:
1. RedBlackTree  — Original red-black tree (from main file)
2. AVLTree       — AVL tree: stricter balancing, faster reads
3. SortedList    — Python sortedcontainers SortedList (fallback to bisect)
"""

from __future__ import annotations

import timeit


# --- Variant 2: AVL Tree ---
class AVLNode:
    def __init__(self, key: int) -> None:
        self.key = key
        self.left: AVLNode | None = None
        self.right: AVLNode | None = None
        self.height: int = 1


class AVLTree:
    """
    AVL Tree — self-balancing BST with height difference <= 1.
    Insert/Delete/Search: O(log n)
    """

    def _height(self, node: AVLNode | None) -> int:
        return node.height if node else 0

    def _balance(self, node: AVLNode | None) -> int:
        return self._height(node.left) - self._height(node.right) if node else 0

    def _update_height(self, node: AVLNode) -> None:
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _rotate_right(self, z: AVLNode) -> AVLNode:
        y = z.left
        assert y is not None
        t3 = y.right
        y.right = z
        z.left = t3
        self._update_height(z)
        self._update_height(y)
        return y

    def _rotate_left(self, z: AVLNode) -> AVLNode:
        y = z.right
        assert y is not None
        t2 = y.left
        y.left = z
        z.right = t2
        self._update_height(z)
        self._update_height(y)
        return y

    def _rebalance(self, node: AVLNode) -> AVLNode:
        self._update_height(node)
        bf = self._balance(node)
        if bf > 1:
            if self._balance(node.left) < 0:
                node.left = self._rotate_left(node.left)  # type: ignore[arg-type]
            return self._rotate_right(node)
        if bf < -1:
            if self._balance(node.right) > 0:
                node.right = self._rotate_right(node.right)  # type: ignore[arg-type]
            return self._rotate_left(node)
        return node

    def insert(self, root: AVLNode | None, key: int) -> AVLNode:
        if root is None:
            return AVLNode(key)
        if key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        return self._rebalance(root)

    def search(self, root: AVLNode | None, key: int) -> bool:
        if root is None:
            return False
        if key == root.key:
            return True
        elif key < root.key:
            return self.search(root.left, key)
        else:
            return self.search(root.right, key)


# --- Variant 3: Sorted list using bisect (stdlib fallback) ---
import bisect


class BisectSortedList:
    """
    Sorted list using bisect — simple and fast for moderate sizes.
    Insert: O(n), Search: O(log n), Delete: O(n)
    """

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
    import sys
    sys.setrecursionlimit(10000)

    try:
        from data_structures.binary_tree_red_black_tree import RedBlackTree  # type: ignore
    except ModuleNotFoundError:
        from binary_tree_red_black_tree import RedBlackTree  # type: ignore[no-redef]

    vals = list(range(1, 501))
    queries = [100, 200, 300, 400, 500, 1]

    def bench_rb():
        tree = RedBlackTree(-1)
        for v in vals:
            tree = tree.insert(v)
        for q in queries:
            q in tree

    avl = AVLTree()

    def bench_avl():
        root = None
        for v in vals:
            root = avl.insert(root, v)
        for q in queries:
            avl.search(root, q)

    def bench_bisect():
        sl = BisectSortedList()
        for v in vals:
            sl.insert(v)
        for q in queries:
            sl.search(q)

    t1 = timeit.timeit(bench_rb, number=20)
    t2 = timeit.timeit(bench_avl, number=20)
    t3 = timeit.timeit(bench_bisect, number=20)

    print("Benchmark (20 runs, 500 inserts + 6 searches):")
    print(f"  Variant 1 (Red-Black Tree):  {t1:.4f}s")
    print(f"  Variant 2 (AVL Tree):        {t2:.4f}s")
    print(f"  Variant 3 (Bisect list):     {t3:.4f}s")
    print("  Note: Bisect is fastest for small n; RBT/AVL scale to O(log n).")


if __name__ == "__main__":
    benchmark()
