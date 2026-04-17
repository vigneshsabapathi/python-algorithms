"""
Flatten Binary Tree to Linked List — Optimized Variants & Benchmark

Three flattening strategies:
  1. Recursive (original) — modifies tree in-place
  2. Iterative Morris-style — O(1) extra space, in-place
  3. Pre-order collect then re-link — simple two-pass approach

Run:
    python binary_tree_flatten_binarytree_to_linkedlist_optimized.py
"""

from __future__ import annotations

import timeit
from dataclasses import dataclass, field


@dataclass
class TreeNode:
    data: int
    left: TreeNode | None = None
    right: TreeNode | None = None


def make_tree() -> TreeNode:
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(5)
    root.left.left = TreeNode(3)
    root.left.right = TreeNode(4)
    root.right.right = TreeNode(6)
    return root


def copy_tree(root: TreeNode | None) -> TreeNode | None:
    if root is None:
        return None
    node = TreeNode(root.data)
    node.left = copy_tree(root.left)
    node.right = copy_tree(root.right)
    return node


def to_list(root: TreeNode | None) -> list[int]:
    result: list[int] = []
    node = root
    while node:
        result.append(node.data)
        node = node.right
    return result


# ─── Variant 1: Recursive (original) ─────────────────────────────────────────

def flatten_v1(root: TreeNode | None) -> None:
    if not root:
        return
    flatten_v1(root.left)
    right_subtree = root.right
    root.right = root.left
    root.left = None
    current = root
    while current.right:
        current = current.right
    current.right = right_subtree
    flatten_v1(right_subtree)


# ─── Variant 2: Iterative Morris-style (O(1) space) ──────────────────────────

def flatten_v2(root: TreeNode | None) -> None:
    """
    For each node with a left child:
      - Find the rightmost node of its left subtree (inorder predecessor)
      - Attach current.right to that node's right
      - Move current.left to current.right, set left = None
    O(n) time, O(1) space.
    """
    current = root
    while current:
        if current.left:
            # Find rightmost of left subtree
            rightmost = current.left
            while rightmost.right:
                rightmost = rightmost.right
            # Stitch
            rightmost.right = current.right
            current.right = current.left
            current.left = None
        current = current.right


# ─── Variant 3: Pre-order collect, then relink ────────────────────────────────

def flatten_v3(root: TreeNode | None) -> None:
    """
    Collect all nodes in preorder into a list, then relink right pointers.
    Clear and simple. O(n) time, O(n) space.
    """
    if not root:
        return
    nodes: list[TreeNode] = []
    stack: list[TreeNode] = [root]
    while stack:
        node = stack.pop()
        nodes.append(node)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    for i in range(len(nodes) - 1):
        nodes[i].left = None
        nodes[i].right = nodes[i + 1]
    nodes[-1].left = None
    nodes[-1].right = None


# ─── Benchmark ────────────────────────────────────────────────────────────────

def benchmark() -> None:
    # Correctness check
    original = make_tree()
    r1 = copy_tree(original)
    r2 = copy_tree(original)
    r3 = copy_tree(original)

    flatten_v1(r1)
    flatten_v2(r2)
    flatten_v3(r3)

    l1, l2, l3 = to_list(r1), to_list(r2), to_list(r3)
    assert l1 == l2 == l3, f"Mismatch: {l1} vs {l2} vs {l3}"
    print(f"All flatten variants produce: {l1}")

    n = 50000

    def run_v1() -> None:
        r = copy_tree(original)
        flatten_v1(r)

    def run_v2() -> None:
        r = copy_tree(original)
        flatten_v2(r)

    def run_v3() -> None:
        r = copy_tree(original)
        flatten_v3(r)

    t1 = timeit.timeit(run_v1, number=n)
    t2 = timeit.timeit(run_v2, number=n)
    t3 = timeit.timeit(run_v3, number=n)

    print(f"\nFlatten Benchmark ({n} runs):")
    print(f"  V1 Recursive:            {t1:.4f}s")
    print(f"  V2 Morris-style O(1):    {t2:.4f}s")
    print(f"  V3 Collect-relink O(n):  {t3:.4f}s")


if __name__ == "__main__":
    benchmark()
