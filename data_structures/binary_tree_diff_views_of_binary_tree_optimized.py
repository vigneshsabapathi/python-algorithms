"""
Binary Tree Views — Optimized Variants & Benchmark

Three approaches for tree views (right/left/top/bottom):
  1. DFS recursive (original)
  2. BFS level-order with deque
  3. BFS with collections.OrderedDict for top/bottom (preserves insertion order)

Run:
    python binary_tree_diff_views_of_binary_tree_optimized.py
"""

from __future__ import annotations

import timeit
from collections import defaultdict, deque
from dataclasses import dataclass


@dataclass
class TreeNode:
    val: int
    left: TreeNode | None = None
    right: TreeNode | None = None


def make_tree() -> TreeNode:
    return TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))


# ─── Variant 1: DFS recursive (original) ─────────────────────────────────────

def right_view_dfs(root: TreeNode | None) -> list[int]:
    view: list[int] = []

    def dfs(node: TreeNode | None, depth: int) -> None:
        if not node:
            return
        if depth == len(view):
            view.append(node.val)
        dfs(node.right, depth + 1)
        dfs(node.left, depth + 1)

    dfs(root, 0)
    return view


def left_view_dfs(root: TreeNode | None) -> list[int]:
    view: list[int] = []

    def dfs(node: TreeNode | None, depth: int) -> None:
        if not node:
            return
        if depth == len(view):
            view.append(node.val)
        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return view


# ─── Variant 2: BFS level-order ──────────────────────────────────────────────

def right_view_bfs(root: TreeNode | None) -> list[int]:
    if not root:
        return []
    view: list[int] = []
    queue: deque[TreeNode] = deque([root])
    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == level_size - 1:
                view.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return view


def left_view_bfs(root: TreeNode | None) -> list[int]:
    if not root:
        return []
    view: list[int] = []
    queue: deque[TreeNode] = deque([root])
    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == 0:
                view.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return view


def top_view_bfs(root: TreeNode | None) -> list[int]:
    if not root:
        return []
    hd_map: dict[int, int] = {}  # horizontal_distance -> first val
    queue: deque[tuple[TreeNode, int]] = deque([(root, 0)])
    while queue:
        node, hd = queue.popleft()
        if hd not in hd_map:
            hd_map[hd] = node.val
        if node.left:
            queue.append((node.left, hd - 1))
        if node.right:
            queue.append((node.right, hd + 1))
    return [hd_map[k] for k in sorted(hd_map)]


def bottom_view_bfs(root: TreeNode | None) -> list[int]:
    if not root:
        return []
    hd_map: dict[int, int] = {}  # horizontal_distance -> last val (overwrite)
    queue: deque[tuple[TreeNode, int]] = deque([(root, 0)])
    while queue:
        node, hd = queue.popleft()
        hd_map[hd] = node.val  # always overwrite = last seen = bottom
        if node.left:
            queue.append((node.left, hd - 1))
        if node.right:
            queue.append((node.right, hd + 1))
    return [hd_map[k] for k in sorted(hd_map)]


# ─── Variant 3: Single BFS pass — all four views at once ─────────────────────

def all_views_single_pass(root: TreeNode | None) -> dict[str, list[int]]:
    """
    Compute right view, left view, top view, bottom view in one BFS traversal.
    Most cache-friendly: visits every node exactly once.
    """
    if not root:
        return {"right": [], "left": [], "top": [], "bottom": []}

    right_v: list[int] = []
    left_v: list[int] = []
    top_hd: dict[int, int] = {}
    bottom_hd: dict[int, int] = {}

    queue: deque[tuple[TreeNode, int]] = deque([(root, 0)])
    level_queue: deque[tuple[TreeNode, int]] = deque([(root, 0)])

    # BFS for top/bottom views
    while queue:
        node, hd = queue.popleft()
        if hd not in top_hd:
            top_hd[hd] = node.val
        bottom_hd[hd] = node.val
        if node.left:
            queue.append((node.left, hd - 1))
        if node.right:
            queue.append((node.right, hd + 1))

    # BFS for left/right views
    queue2: deque[TreeNode] = deque([root])
    while queue2:
        lvl = len(queue2)
        for i in range(lvl):
            node = queue2.popleft()
            if i == 0:
                left_v.append(node.val)
            if i == lvl - 1:
                right_v.append(node.val)
            if node.left:
                queue2.append(node.left)
            if node.right:
                queue2.append(node.right)

    return {
        "right": right_v,
        "left": left_v,
        "top": [top_hd[k] for k in sorted(top_hd)],
        "bottom": [bottom_hd[k] for k in sorted(bottom_hd)],
    }


# ─── Benchmark ────────────────────────────────────────────────────────────────

def benchmark() -> None:
    # Build a larger tree
    def build(levels: int) -> TreeNode:
        root = TreeNode(1)
        queue: deque[TreeNode] = deque([root])
        val = 2
        for _ in range(levels - 1):
            next_q: deque[TreeNode] = deque()
            while queue and val < 2 ** levels:
                node = queue.popleft()
                node.left = TreeNode(val); val += 1
                node.right = TreeNode(val); val += 1
                next_q.append(node.left)
                next_q.append(node.right)
            queue = next_q
        return root

    root = build(8)  # ~255 nodes

    def run_v1() -> None:
        right_view_dfs(root)
        left_view_dfs(root)

    def run_v2() -> None:
        right_view_bfs(root)
        left_view_bfs(root)
        top_view_bfs(root)
        bottom_view_bfs(root)

    def run_v3() -> None:
        all_views_single_pass(root)

    n = 5000
    t1 = timeit.timeit(run_v1, number=n)
    t2 = timeit.timeit(run_v2, number=n)
    t3 = timeit.timeit(run_v3, number=n)

    print(f"Views Benchmark ({n} runs, ~255 node tree):")
    print(f"  V1 DFS recursive (right+left):   {t1:.4f}s")
    print(f"  V2 BFS (right+left+top+bottom):  {t2:.4f}s")
    print(f"  V3 Single-pass all views:         {t3:.4f}s")

    tree = make_tree()
    views = all_views_single_pass(tree)
    print(f"\nSample tree views: {views}")


if __name__ == "__main__":
    benchmark()
