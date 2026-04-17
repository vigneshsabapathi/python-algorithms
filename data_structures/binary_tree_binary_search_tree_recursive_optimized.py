"""
BST Recursive — Optimized Variants & Benchmark

Three BST traversal/search strategies:
  1. Recursive DFS (original style)
  2. Iterative search with stack-based traversal
  3. Generator-based inorder (lazy)

Run:
    python binary_tree_binary_search_tree_recursive_optimized.py
"""

from __future__ import annotations

import timeit
from collections.abc import Generator
from dataclasses import dataclass


@dataclass
class Node:
    label: int
    left: Node | None = None
    right: Node | None = None


def build_tree(values: list[int]) -> Node | None:
    """Insert values into a BST iteratively and return root."""
    root: Node | None = None

    def _insert(root: Node | None, label: int) -> Node:
        if root is None:
            return Node(label)
        if label < root.label:
            root.left = _insert(root.left, label)
        elif label > root.label:
            root.right = _insert(root.right, label)
        return root

    for v in values:
        root = _insert(root, v)
    return root


# ─── Variant 1: Recursive inorder ────────────────────────────────────────────

def inorder_recursive(node: Node | None) -> list[int]:
    if node is None:
        return []
    return inorder_recursive(node.left) + [node.label] + inorder_recursive(node.right)


def search_recursive(node: Node | None, label: int) -> Node | None:
    if node is None or node.label == label:
        return node
    if label < node.label:
        return search_recursive(node.left, label)
    return search_recursive(node.right, label)


# ─── Variant 2: Iterative inorder with explicit stack ─────────────────────────

def inorder_iterative(node: Node | None) -> list[int]:
    result: list[int] = []
    stack: list[Node] = []
    current = node
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        result.append(current.label)
        current = current.right
    return result


def search_iterative(node: Node | None, label: int) -> Node | None:
    while node:
        if label == node.label:
            return node
        node = node.left if label < node.label else node.right
    return None


# ─── Variant 3: Generator-based inorder (lazy, memory-efficient) ─────────────

def inorder_generator(node: Node | None) -> Generator[int, None, None]:
    if node:
        yield from inorder_generator(node.left)
        yield node.label
        yield from inorder_generator(node.right)


# ─── Benchmark ────────────────────────────────────────────────────────────────

def benchmark() -> None:
    import random

    keys = list(range(300))
    random.shuffle(keys)
    root = build_tree(keys)
    search_targets = keys[:50]

    def run_v1() -> None:
        inorder_recursive(root)
        for k in search_targets:
            search_recursive(root, k)

    def run_v2() -> None:
        inorder_iterative(root)
        for k in search_targets:
            search_iterative(root, k)

    def run_v3() -> None:
        list(inorder_generator(root))
        for k in search_targets:
            search_iterative(root, k)

    n = 1000
    t1 = timeit.timeit(run_v1, number=n)
    t2 = timeit.timeit(run_v2, number=n)
    t3 = timeit.timeit(run_v3, number=n)

    print(f"BST Traversal Benchmark ({n} runs, 300-node tree, 50 searches):")
    print(f"  V1 Recursive inorder + search:  {t1:.4f}s")
    print(f"  V2 Iterative inorder + search:  {t2:.4f}s")
    print(f"  V3 Generator inorder + search:  {t3:.4f}s")

    # Correctness
    small_root = build_tree([5, 3, 7, 1, 4])
    assert inorder_recursive(small_root) == inorder_iterative(small_root) == list(inorder_generator(small_root))
    print("\nAll traversals produce identical inorder results: OK")


if __name__ == "__main__":
    benchmark()
