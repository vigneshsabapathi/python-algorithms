"""
Binary Tree Traversals — Optimized Variants & Benchmark

Three traversal implementation styles:
  1. Recursive generators (original)
  2. Iterative with explicit stack (avoids recursion limit)
  3. Morris traversal — O(1) space inorder (no stack or recursion)

Run:
    python binary_tree_binary_tree_traversals_optimized.py
"""

from __future__ import annotations

import timeit
from collections import deque
from dataclasses import dataclass


@dataclass
class Node:
    data: int
    left: Node | None = None
    right: Node | None = None


def make_balanced_tree(n: int = 127) -> Node | None:
    """Build a balanced BST from [1..n] for consistent benchmarking."""

    def _build(lo: int, hi: int) -> Node | None:
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        node = Node(mid)
        node.left = _build(lo, mid - 1)
        node.right = _build(mid + 1, hi)
        return node

    return _build(1, n)


# ─── Variant 1: Recursive generator ──────────────────────────────────────────

def inorder_recursive(root: Node | None) -> list[int]:
    result: list[int] = []

    def _inner(node: Node | None) -> None:
        if not node:
            return
        _inner(node.left)
        result.append(node.data)
        _inner(node.right)

    _inner(root)
    return result


def preorder_recursive(root: Node | None) -> list[int]:
    if not root:
        return []
    return [root.data] + preorder_recursive(root.left) + preorder_recursive(root.right)


def postorder_recursive(root: Node | None) -> list[int]:
    if not root:
        return []
    return postorder_recursive(root.left) + postorder_recursive(root.right) + [root.data]


# ─── Variant 2: Iterative traversals ─────────────────────────────────────────

def inorder_iterative(root: Node | None) -> list[int]:
    result: list[int] = []
    stack: list[Node] = []
    current = root
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        result.append(current.data)
        current = current.right
    return result


def preorder_iterative(root: Node | None) -> list[int]:
    if not root:
        return []
    result: list[int] = []
    stack: list[Node] = [root]
    while stack:
        node = stack.pop()
        result.append(node.data)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return result


def level_order_iterative(root: Node | None) -> list[int]:
    if not root:
        return []
    result: list[int] = []
    queue: deque[Node] = deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.data)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result


# ─── Variant 3: Morris inorder — O(1) space ──────────────────────────────────

def inorder_morris(root: Node | None) -> list[int]:
    """
    Morris traversal: inorder without recursion or stack.
    Uses temporary threads (right pointer modifications) to navigate back.
    Time: O(n), Space: O(1).
    """
    result: list[int] = []
    current = root

    while current:
        if current.left is None:
            result.append(current.data)
            current = current.right
        else:
            # Find inorder predecessor
            pre = current.left
            while pre.right and pre.right is not current:
                pre = pre.right

            if pre.right is None:
                # Thread: make current the right child of its predecessor
                pre.right = current
                current = current.left
            else:
                # Unthread: restore tree
                pre.right = None
                result.append(current.data)
                current = current.right

    return result


# ─── Benchmark ────────────────────────────────────────────────────────────────

def benchmark() -> None:
    root = make_balanced_tree(255)

    # Correctness check
    r1 = inorder_recursive(root)
    r2 = inorder_iterative(root)
    r3 = inorder_morris(root)
    assert r1 == r2 == r3, "Inorder traversals differ!"
    print(f"All inorder traversals match (n=255 nodes). First 5: {r1[:5]}, Last 5: {r1[-5:]}")

    def run_v1() -> None:
        inorder_recursive(root)
        preorder_recursive(root)
        postorder_recursive(root)

    def run_v2() -> None:
        inorder_iterative(root)
        preorder_iterative(root)
        level_order_iterative(root)

    def run_v3() -> None:
        inorder_morris(root)
        preorder_iterative(root)
        level_order_iterative(root)

    n = 2000
    t1 = timeit.timeit(run_v1, number=n)
    t2 = timeit.timeit(run_v2, number=n)
    t3 = timeit.timeit(run_v3, number=n)

    print(f"\nTraversal Benchmark ({n} runs, 255-node balanced tree):")
    print(f"  V1 Recursive (inorder+pre+post):  {t1:.4f}s")
    print(f"  V2 Iterative (inorder+pre+level): {t2:.4f}s")
    print(f"  V3 Morris inorder + iterative:    {t3:.4f}s")


if __name__ == "__main__":
    benchmark()
