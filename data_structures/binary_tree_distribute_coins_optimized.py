"""
Distribute Coins — Optimized Variants & Benchmark

Three implementations of the coin distribution problem:
  1. Original recursive with NamedTuple result
  2. Streamlined recursive returning (moves, excess) tuple directly
  3. Iterative post-order using explicit stack

Run:
    python binary_tree_distribute_coins_optimized.py
"""

from __future__ import annotations

import timeit
from dataclasses import dataclass
from typing import NamedTuple


@dataclass
class TreeNode:
    data: int
    left: TreeNode | None = None
    right: TreeNode | None = None


# ─── Variant 1: Original with NamedTuple ─────────────────────────────────────

class CoinsDistribResult(NamedTuple):
    moves: int
    excess: int


def distribute_v1(root: TreeNode | None) -> int:
    if root is None:
        return 0

    def get_distrib(node: TreeNode | None) -> CoinsDistribResult:
        if node is None:
            return CoinsDistribResult(0, 1)
        lm, le = get_distrib(node.left)
        rm, re = get_distrib(node.right)
        coins_to_left = 1 - le
        coins_to_right = 1 - re
        moves = lm + rm + abs(coins_to_left) + abs(coins_to_right)
        excess = node.data - coins_to_left - coins_to_right
        return CoinsDistribResult(moves, excess)

    return get_distrib(root)[0]


# ─── Variant 2: Streamlined tuple returns (avoids NamedTuple overhead) ────────

def distribute_v2(root: TreeNode | None) -> int:
    """Faster: return plain tuple (moves, excess) without NamedTuple."""
    if root is None:
        return 0

    def dfs(node: TreeNode | None) -> tuple[int, int]:
        if node is None:
            return 0, 1
        lm, le = dfs(node.left)
        rm, re = dfs(node.right)
        cl = 1 - le
        cr = 1 - re
        return lm + rm + abs(cl) + abs(cr), node.data - cl - cr

    return dfs(root)[0]


# ─── Variant 3: Iterative post-order with stack ───────────────────────────────

def distribute_v3(root: TreeNode | None) -> int:
    """Iterative post-order using explicit stack — avoids recursion limit."""
    if root is None:
        return 0

    # Build post-order sequence
    stack: list[TreeNode] = [root]
    post_order: list[TreeNode] = []
    while stack:
        node = stack.pop()
        post_order.append(node)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)

    total_moves = 0
    excess: dict[int, int] = {}  # id(node) -> excess coins

    for node in reversed(post_order):
        le = excess.get(id(node.left), 1) if node.left else 1
        re = excess.get(id(node.right), 1) if node.right else 1
        cl = 1 - le
        cr = 1 - re
        total_moves += abs(cl) + abs(cr)
        excess[id(node)] = node.data - cl - cr

    return total_moves


# ─── Benchmark ────────────────────────────────────────────────────────────────

def make_tree(depth: int) -> TreeNode:
    """Build a perfect binary tree of given depth with alternating coins."""

    def _build(d: int, coin: int) -> TreeNode:
        if d == 0:
            return TreeNode(coin)
        node = TreeNode(0)
        node.left = _build(d - 1, coin)
        node.right = _build(d - 1, 0)
        return node

    # Build a valid tree: total coins == nodes
    total = 2 ** (depth + 1) - 1
    # Simple: give all coins to root, rest are 0
    root = TreeNode(total)

    def _fill(node: TreeNode, d: int) -> None:
        if d == 0:
            return
        node.left = TreeNode(0)
        node.right = TreeNode(0)
        _fill(node.left, d - 1)
        _fill(node.right, d - 1)

    _fill(root, depth)
    return root


def benchmark() -> None:
    root = make_tree(6)  # 127 nodes

    d1 = distribute_v1(root)
    d2 = distribute_v2(root)
    d3 = distribute_v3(root)
    print(f"Results: V1={d1}, V2={d2}, V3={d3}")
    assert d1 == d2 == d3

    def run_v1() -> None:
        distribute_v1(root)

    def run_v2() -> None:
        distribute_v2(root)

    def run_v3() -> None:
        distribute_v3(root)

    n = 10000
    t1 = timeit.timeit(run_v1, number=n)
    t2 = timeit.timeit(run_v2, number=n)
    t3 = timeit.timeit(run_v3, number=n)

    print(f"\nDistribute Coins Benchmark ({n} runs, 127-node tree):")
    print(f"  V1 NamedTuple result:    {t1:.4f}s")
    print(f"  V2 Plain tuple result:   {t2:.4f}s")
    print(f"  V3 Iterative post-order: {t3:.4f}s")


if __name__ == "__main__":
    benchmark()
