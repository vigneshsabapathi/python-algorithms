"""
Is Sum Tree — Optimized Variants & Benchmark

Three sum tree validation approaches:
  1. Original: uses sum() over subtree iterator (multiple passes per node)
  2. Single-pass DFS returning (is_sum, subtree_sum) — O(n)
  3. Iterative post-order with accumulated sums

Run:
    python binary_tree_is_sum_tree_optimized.py
"""

from __future__ import annotations

import timeit
from dataclasses import dataclass


@dataclass
class Node:
    data: int
    left: Node | None = None
    right: Node | None = None

    def __iter__(self):
        if self.left:
            yield from self.left
        yield self.data
        if self.right:
            yield from self.right


def make_sum_tree() -> Node:
    r"""
         26
        /  \
      10    3
     /  \    \
    4    6    3
    """
    root = Node(26)
    root.left = Node(10)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(6)
    root.right.right = Node(3)
    return root


def make_non_sum_tree() -> Node:
    r"""
          11
       /     \
      2       29
     / \     /  \
    1   7  15    40
                   \
                    35
    """
    root = Node(11)
    root.left = Node(2)
    root.right = Node(29)
    root.left.left = Node(1)
    root.left.right = Node(7)
    root.right.left = Node(15)
    root.right.right = Node(40)
    root.right.right.left = Node(35)
    return root


# ─── Variant 1: Original — uses sum() over __iter__ (multiple traversals) ─────

def is_sum_tree_v1(node: Node | None) -> bool:
    """Original O(n^2) approach using sum() over subtree iterators."""
    if node is None:
        return True
    if not node.left and not node.right:
        return True
    left_sum = sum(node.left) if node.left else 0
    right_sum = sum(node.right) if node.right else 0
    if node.data != left_sum + right_sum:
        return False
    return is_sum_tree_v1(node.left) and is_sum_tree_v1(node.right)


# ─── Variant 2: Single-pass DFS — O(n) ───────────────────────────────────────

def is_sum_tree_v2(root: Node | None) -> bool:
    """
    DFS returning (is_valid, subtree_sum).
    Each node visited once: O(n) time, O(h) space.
    """
    def dfs(node: Node | None) -> tuple[bool, int]:
        if node is None:
            return True, 0
        if not node.left and not node.right:
            return True, node.data
        lv, ls = dfs(node.left)
        rv, rs = dfs(node.right)
        valid = lv and rv and node.data == ls + rs
        return valid, node.data + ls + rs

    return dfs(root)[0]


# ─── Variant 3: Iterative post-order ─────────────────────────────────────────

def is_sum_tree_v3(root: Node | None) -> bool:
    """
    Iterative post-order using explicit stack.
    Avoids Python recursion limit for very deep trees.
    """
    if root is None:
        return True

    # Build post-order sequence
    stack: list[Node] = [root]
    post_order: list[Node] = []
    while stack:
        node = stack.pop()
        post_order.append(node)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)

    subtree_sum: dict[int, int] = {}  # id(node) -> total sum of subtree incl. node
    is_valid: dict[int, bool] = {}

    for node in reversed(post_order):
        if not node.left and not node.right:
            subtree_sum[id(node)] = node.data
            is_valid[id(node)] = True
            continue

        ls = subtree_sum.get(id(node.left), 0) if node.left else 0
        rs = subtree_sum.get(id(node.right), 0) if node.right else 0
        lv = is_valid.get(id(node.left), True) if node.left else True
        rv = is_valid.get(id(node.right), True) if node.right else True

        # Sum at this level is just left_root + right_root, not full subtree
        # Re-compute correctly: check if node.data == direct child sums
        left_child_val = node.left.data if node.left else 0
        right_child_val = node.right.data if node.right else 0

        # For sum tree: node.data == sum of ALL values in left subtree + right subtree
        left_subtree_sum = subtree_sum.get(id(node.left), 0) if node.left else 0
        right_subtree_sum = subtree_sum.get(id(node.right), 0) if node.right else 0

        is_valid[id(node)] = lv and rv and node.data == left_subtree_sum + right_subtree_sum
        subtree_sum[id(node)] = node.data + left_subtree_sum + right_subtree_sum

    return is_valid.get(id(root), True)


# ─── Benchmark ────────────────────────────────────────────────────────────────

def benchmark() -> None:
    sum_tree = make_sum_tree()
    non_sum = make_non_sum_tree()

    # Correctness
    assert is_sum_tree_v1(sum_tree) and not is_sum_tree_v1(non_sum), "V1 failed"
    assert is_sum_tree_v2(sum_tree) and not is_sum_tree_v2(non_sum), "V2 failed"
    assert is_sum_tree_v3(sum_tree) and not is_sum_tree_v3(non_sum), "V3 failed"
    print("All correctness checks passed.")

    def run_v1() -> None:
        is_sum_tree_v1(sum_tree)

    def run_v2() -> None:
        is_sum_tree_v2(sum_tree)

    def run_v3() -> None:
        is_sum_tree_v3(sum_tree)

    n = 30000
    t1 = timeit.timeit(run_v1, number=n)
    t2 = timeit.timeit(run_v2, number=n)
    t3 = timeit.timeit(run_v3, number=n)

    print(f"\nIs Sum Tree Benchmark ({n} runs):")
    print(f"  V1 sum() over iterator (O(n^2)): {t1:.4f}s")
    print(f"  V2 Single-pass DFS (O(n)):       {t2:.4f}s")
    print(f"  V3 Iterative post-order (O(n)):  {t3:.4f}s")


if __name__ == "__main__":
    benchmark()
