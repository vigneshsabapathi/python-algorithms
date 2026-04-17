"""
Diameter of Binary Tree — Optimized Variants & Benchmark

Three approaches to computing the diameter:
  1. Naive: depth() called for every node — O(n^2)
  2. Optimized single-pass DFS — O(n), returns (height, diameter) together
  3. Iterative post-order with explicit stack — O(n), avoids recursion

Run:
    python binary_tree_diameter_of_binary_tree_optimized.py
"""

from __future__ import annotations

import timeit
from dataclasses import dataclass


@dataclass
class Node:
    data: int
    left: Node | None = None
    right: Node | None = None


def make_tree(n: int = 15) -> Node | None:
    """Build a balanced tree with n nodes (1-indexed)."""
    def _build(lo: int, hi: int) -> Node | None:
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        node = Node(mid)
        node.left = _build(lo, mid - 1)
        node.right = _build(mid + 1, hi)
        return node
    return _build(1, n)


# ─── Variant 1: Naive O(n^2) ─────────────────────────────────────────────────

def depth_v1(node: Node | None) -> int:
    if node is None:
        return 0
    return max(depth_v1(node.left), depth_v1(node.right)) + 1


def diameter_v1(root: Node | None) -> int:
    """For every node, compute left depth + right depth. O(n^2)."""
    if root is None:
        return 0
    left_depth = depth_v1(root.left)
    right_depth = depth_v1(root.right)
    through_root = left_depth + right_depth + 1
    left_diam = diameter_v1(root.left)
    right_diam = diameter_v1(root.right)
    return max(through_root, left_diam, right_diam)


# ─── Variant 2: Single-pass DFS — O(n) ───────────────────────────────────────

def diameter_v2(root: Node | None) -> int:
    """
    Returns diameter in a single DFS pass.
    Inner function returns height; diameter is tracked via closure.
    """
    max_diameter = [0]

    def dfs(node: Node | None) -> int:
        if node is None:
            return 0
        left_h = dfs(node.left)
        right_h = dfs(node.right)
        max_diameter[0] = max(max_diameter[0], left_h + right_h + 1)
        return max(left_h, right_h) + 1

    dfs(root)
    return max_diameter[0]


# ─── Variant 3: Iterative post-order with stack — O(n) ───────────────────────

def diameter_v3(root: Node | None) -> int:
    """
    Iterative post-order traversal using two stacks.
    Computes height bottom-up; tracks max diameter.
    """
    if root is None:
        return 0

    height: dict[int, int] = {}  # id(node) -> height
    max_diam = 0
    stack: list[Node] = [root]
    post_order: list[Node] = []

    # First pass: build reverse post-order
    while stack:
        node = stack.pop()
        post_order.append(node)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)

    # Second pass: process in post-order
    for node in reversed(post_order):
        lh = height.get(id(node.left), 0) if node.left else 0
        rh = height.get(id(node.right), 0) if node.right else 0
        height[id(node)] = max(lh, rh) + 1
        max_diam = max(max_diam, lh + rh + 1)

    return max_diam


# ─── Benchmark ────────────────────────────────────────────────────────────────

def benchmark() -> None:
    root = make_tree(1023)  # ~10 levels, 1023 nodes

    d1 = diameter_v1(root)
    d2 = diameter_v2(root)
    d3 = diameter_v3(root)
    print(f"Diameter results: V1={d1}, V2={d2}, V3={d3}")
    assert d1 == d2 == d3, f"Mismatch: {d1}, {d2}, {d3}"

    def run_v1() -> None:
        diameter_v1(root)

    def run_v2() -> None:
        diameter_v2(root)

    def run_v3() -> None:
        diameter_v3(root)

    n = 500
    t1 = timeit.timeit(run_v1, number=n)
    t2 = timeit.timeit(run_v2, number=n)
    t3 = timeit.timeit(run_v3, number=n)

    print(f"\nDiameter Benchmark ({n} runs, 1023-node tree):")
    print(f"  V1 Naive O(n^2):             {t1:.4f}s")
    print(f"  V2 Single-pass DFS O(n):     {t2:.4f}s")
    print(f"  V3 Iterative post-order O(n):{t3:.4f}s")


if __name__ == "__main__":
    benchmark()
