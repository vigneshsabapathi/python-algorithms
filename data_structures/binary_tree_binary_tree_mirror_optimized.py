"""
Binary Tree Mirror — Optimized Variants & Benchmark

Three mirroring strategies:
  1. Recursive dict-based (original)
  2. Iterative BFS-based dict mirror
  3. In-place Node swap (linked-node tree)

Run:
    python binary_tree_binary_tree_mirror_optimized.py
"""

from __future__ import annotations

import timeit
from collections import deque
from dataclasses import dataclass


# ─── Variant 1: Recursive dict-based mirror ───────────────────────────────────

def mirror_recursive(tree: dict, root: int = 1) -> dict:
    result = dict(tree)

    def _mirror(r: int) -> None:
        if r not in result:
            return
        left, right = result[r]
        result[r] = [right, left]
        if left:
            _mirror(left)
        if right:
            _mirror(right)

    _mirror(root)
    return result


# ─── Variant 2: Iterative BFS dict-based mirror ───────────────────────────────

def mirror_iterative_bfs(tree: dict, root: int = 1) -> dict:
    result = dict(tree)
    queue: deque[int] = deque([root])
    while queue:
        node = queue.popleft()
        if node not in result:
            continue
        left, right = result[node]
        result[node] = [right, left]
        if left:
            queue.append(left)
        if right:
            queue.append(right)
    return result


# ─── Variant 3: Linked-node in-place mirror ───────────────────────────────────

@dataclass
class TreeNode:
    val: int
    left: TreeNode | None = None
    right: TreeNode | None = None


def mirror_inplace(root: TreeNode | None) -> TreeNode | None:
    """Mirror by swapping left/right pointers in-place."""
    if root is None:
        return None
    root.left, root.right = mirror_inplace(root.right), mirror_inplace(root.left)
    return root


def dict_to_tree(tree: dict, node: int) -> TreeNode | None:
    if not node or node not in tree:
        return None
    left_id, right_id = tree[node]
    n = TreeNode(node)
    n.left = dict_to_tree(tree, left_id)
    n.right = dict_to_tree(tree, right_id)
    return n


def tree_to_dict(root: TreeNode | None) -> dict:
    result: dict = {}
    if root is None:
        return result
    queue: deque[TreeNode] = deque([root])
    while queue:
        node = queue.popleft()
        left_val = node.left.val if node.left else 0
        right_val = node.right.val if node.right else 0
        result[node.val] = [left_val, right_val]
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result


# ─── Benchmark ────────────────────────────────────────────────────────────────

def benchmark() -> None:
    sample = {1: [2, 3], 2: [4, 5], 3: [6, 7], 7: [8, 9]}

    def run_v1() -> None:
        mirror_recursive(sample, 1)

    def run_v2() -> None:
        mirror_iterative_bfs(sample, 1)

    def run_v3() -> None:
        tree = dict_to_tree(sample, 1)
        mirror_inplace(tree)

    n = 50000
    t1 = timeit.timeit(run_v1, number=n)
    t2 = timeit.timeit(run_v2, number=n)
    t3 = timeit.timeit(run_v3, number=n)

    print(f"Mirror Benchmark ({n} runs):")
    print(f"  V1 Recursive dict mirror:    {t1:.4f}s")
    print(f"  V2 Iterative BFS dict:       {t2:.4f}s")
    print(f"  V3 Linked-node in-place:     {t3:.4f}s")

    # Correctness
    r1 = mirror_recursive(sample, 1)
    r2 = mirror_iterative_bfs(sample, 1)
    assert r1 == r2, f"Mismatch: {r1} vs {r2}"
    print("\nV1 == V2 result: OK")
    print(f"Mirrored: {r1}")


if __name__ == "__main__":
    benchmark()
