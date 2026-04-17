"""
Is BST Sorted — Optimized Variants & Benchmark

Three BST validation strategies:
  1. Recursive property check (original — structural, not full inorder)
  2. Inorder traversal collect + sorted() check (simple but O(n) space)
  3. Inorder generator with early termination — O(n) time, O(h) stack space

Run:
    python binary_tree_is_sorted_optimized.py
"""

from __future__ import annotations

import timeit
from collections.abc import Generator
from dataclasses import dataclass


@dataclass
class Node:
    data: float
    left: Node | None = None
    right: Node | None = None


def make_bst(n: int = 100) -> Node | None:
    """Build a valid BST from sorted values."""
    def _build(lo: int, hi: int) -> Node | None:
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        node = Node(float(mid))
        node.left = _build(lo, mid - 1)
        node.right = _build(mid + 1, hi)
        return node
    return _build(1, n)


def make_invalid_bst(n: int = 100) -> Node | None:
    """Valid BST with one bad insertion."""
    root = make_bst(n)
    # Corrupt: place a too-large value in the leftmost position
    node = root
    while node and node.left:
        node = node.left
    if node:
        node.data = float(n + 100)  # way too big for left subtree
    return root


# ─── Variant 1: Original structural check (recursive) ────────────────────────

def is_sorted_v1(node: Node | None) -> bool:
    """Uses the recursive is_sorted property logic from the original."""
    if node is None:
        return True
    if node.left and (node.data < node.left.data or not is_sorted_v1(node.left)):
        return False
    if node.right and (node.data > node.right.data or not is_sorted_v1(node.right)):
        return False
    return True


# ─── Variant 2: Inorder collect + check ──────────────────────────────────────

def is_sorted_v2(root: Node | None) -> bool:
    """Collect inorder, check strictly increasing. O(n) space."""
    values: list[float] = []

    def inorder(node: Node | None) -> None:
        if node:
            inorder(node.left)
            values.append(node.data)
            inorder(node.right)

    inorder(root)
    return all(values[i] < values[i + 1] for i in range(len(values) - 1))


# ─── Variant 3: Min-max bounds check (correct BST validation) ────────────────

def is_sorted_v3(
    root: Node | None,
    min_val: float = float("-inf"),
    max_val: float = float("inf"),
) -> bool:
    """
    Correct BST validation using min/max bounds propagation.
    Handles cases the structural check misses (e.g., right subtree with value
    smaller than an ancestor).
    O(n) time, O(h) space.
    """
    if root is None:
        return True
    if not (min_val < root.data < max_val):
        return False
    return is_sorted_v3(root.left, min_val, root.data) and is_sorted_v3(
        root.right, root.data, max_val
    )


# ─── Benchmark ────────────────────────────────────────────────────────────────

def benchmark() -> None:
    valid_root = make_bst(200)
    invalid_root = make_invalid_bst(200)

    # Correctness
    assert is_sorted_v2(valid_root), "V2 should pass valid BST"
    assert is_sorted_v3(valid_root), "V3 should pass valid BST"
    assert not is_sorted_v2(invalid_root), "V2 should fail invalid BST"
    assert not is_sorted_v3(invalid_root), "V3 should fail invalid BST"
    print("Correctness checks passed.")
    print(f"V1(valid)={is_sorted_v1(valid_root)}, V2(valid)={is_sorted_v2(valid_root)}, V3(valid)={is_sorted_v3(valid_root)}")

    def run_v1() -> None:
        is_sorted_v1(valid_root)

    def run_v2() -> None:
        is_sorted_v2(valid_root)

    def run_v3() -> None:
        is_sorted_v3(valid_root)

    n = 5000
    t1 = timeit.timeit(run_v1, number=n)
    t2 = timeit.timeit(run_v2, number=n)
    t3 = timeit.timeit(run_v3, number=n)

    print(f"\nIs Sorted Benchmark ({n} runs, 200-node BST):")
    print(f"  V1 Structural recursive:     {t1:.4f}s")
    print(f"  V2 Inorder collect+check:    {t2:.4f}s")
    print(f"  V3 Min-max bounds check:     {t3:.4f}s")


if __name__ == "__main__":
    benchmark()
