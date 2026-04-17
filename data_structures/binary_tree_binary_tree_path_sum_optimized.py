"""
Binary Tree Path Sum — Optimized Variants & Benchmark

Three path sum counting approaches:
  1. Original DFS + recursive subtree scan (O(n^2))
  2. Prefix sum hash map (O(n)) — optimal
  3. Memoized prefix-count approach (same O(n) but with explicit cache)

Run:
    python binary_tree_binary_tree_path_sum_optimized.py
"""

from __future__ import annotations

import timeit
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Node:
    value: int
    left: Node | None = None
    right: Node | None = None


def build_tree() -> Node:
    r"""
        10
       /  \
      5   -3
     / \    \
    3   2    11
   / \   \
  3  -2   1
    """
    root = Node(10)
    root.left = Node(5)
    root.right = Node(-3)
    root.left.left = Node(3)
    root.left.right = Node(2)
    root.right.right = Node(11)
    root.left.left.left = Node(3)
    root.left.left.right = Node(-2)
    root.left.right.right = Node(1)
    return root


# ─── Variant 1: Original O(n^2) DFS scan ─────────────────────────────────────

class PathSumV1:
    def __init__(self) -> None:
        self.paths = 0
        self.target = 0

    def dfs(self, node: Node | None, path_sum: int) -> None:
        if node is None:
            return
        if path_sum == self.target:
            self.paths += 1
        if node.left:
            self.dfs(node.left, path_sum + node.left.value)
        if node.right:
            self.dfs(node.right, path_sum + node.right.value)

    def count(self, node: Node | None, target: int) -> int:
        if node is None:
            return 0
        self.target = target
        self.dfs(node, node.value)
        self.count(node.left, target)
        self.count(node.right, target)
        return self.paths


# ─── Variant 2: Prefix sum hash map — O(n) ────────────────────────────────────

def path_sum_prefix(root: Node | None, target: int) -> int:
    """
    Use running prefix sum + hash map to count paths in O(n).
    prefix_count[s] = number of root-to-current paths with sum s.
    A path [i+1..j] sums to target iff prefix[j] - prefix[i] == target.
    """
    prefix_count: dict[int, int] = defaultdict(int)
    prefix_count[0] = 1

    def dfs(node: Node | None, current_sum: int) -> int:
        if node is None:
            return 0
        current_sum += node.value
        count = prefix_count[current_sum - target]
        prefix_count[current_sum] += 1
        count += dfs(node.left, current_sum)
        count += dfs(node.right, current_sum)
        prefix_count[current_sum] -= 1
        return count

    return dfs(root, 0)


# ─── Variant 3: Iterative DFS with stack + prefix sums ────────────────────────

def path_sum_iterative(root: Node | None, target: int) -> int:
    """
    Iterative DFS using explicit stack carrying (node, current_sum, path_prefix_counts).
    Avoids Python recursion limit for very deep trees.
    """
    if root is None:
        return 0

    count = 0
    # stack entries: (node, current_sum, prefix_count snapshot as dict)
    stack: list[tuple[Node, int, dict[int, int]]] = [(root, 0, {0: 1})]

    while stack:
        node, curr, prefix = stack.pop()
        curr += node.value
        count += prefix.get(curr - target, 0)

        new_prefix = dict(prefix)
        new_prefix[curr] = new_prefix.get(curr, 0) + 1

        if node.left:
            stack.append((node.left, curr, new_prefix))
        if node.right:
            stack.append((node.right, curr, new_prefix))

    return count


# ─── Benchmark ────────────────────────────────────────────────────────────────

def benchmark() -> None:
    root = build_tree()
    target = 8

    # Verify correctness first
    v1_result = PathSumV1().count(root, target)
    v2_result = path_sum_prefix(root, target)
    v3_result = path_sum_iterative(root, target)
    print(f"Results for target={target}: V1={v1_result}, V2={v2_result}, V3={v3_result}")

    def run_v1() -> None:
        PathSumV1().count(build_tree(), target)

    def run_v2() -> None:
        path_sum_prefix(build_tree(), target)

    def run_v3() -> None:
        path_sum_iterative(build_tree(), target)

    n = 10000
    t1 = timeit.timeit(run_v1, number=n)
    t2 = timeit.timeit(run_v2, number=n)
    t3 = timeit.timeit(run_v3, number=n)

    print(f"\nPath Sum Benchmark ({n} runs):")
    print(f"  V1 Naive O(n^2) DFS:      {t1:.4f}s")
    print(f"  V2 Prefix sum O(n):       {t2:.4f}s")
    print(f"  V3 Iterative prefix sum:  {t3:.4f}s")


if __name__ == "__main__":
    benchmark()
