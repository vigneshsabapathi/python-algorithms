"""
Optimized variants of KD-Tree construction and nearest neighbor search.

Three approaches for building and querying a KD-tree:
1. Recursive median-split (original)
2. Iterative build with explicit stack
3. Approximation via bucket-based KD-tree

Benchmarks using timeit.
"""

from __future__ import annotations

import random
import timeit


class KDNode:
    """Node in a KD-Tree."""

    __slots__ = ("point", "left", "right")

    def __init__(
        self,
        point: list[float],
        left: KDNode | None = None,
        right: KDNode | None = None,
    ) -> None:
        self.point = point
        self.left = left
        self.right = right


# Variant 1: Original recursive median split
def build_kdtree_recursive(points: list[list[float]], depth: int = 0) -> KDNode | None:
    """
    Recursive KD-tree build. Time: O(n log^2 n), Space: O(log n) stack.

    >>> tree = build_kdtree_recursive([[3,6],[17,15],[13,15],[6,12],[9,1],[2,7],[10,19]])
    >>> tree.point
    [9, 1]
    >>> tree.left is not None
    True
    """
    if not points:
        return None
    k = len(points[0])
    axis = depth % k
    points.sort(key=lambda p: p[axis])
    mid = len(points) // 2
    return KDNode(
        point=points[mid],
        left=build_kdtree_recursive(points[:mid], depth + 1),
        right=build_kdtree_recursive(points[mid + 1:], depth + 1),
    )


# Variant 2: Iterative build using explicit stack
def build_kdtree_iterative(points: list[list[float]]) -> KDNode | None:
    """
    Iterative KD-tree build using stack. Avoids Python recursion limit.
    Time: O(n log^2 n), Space: O(n)

    >>> tree = build_kdtree_iterative([[3,6],[17,15],[13,15],[6,12],[9,1],[2,7],[10,19]])
    >>> tree is not None
    True
    >>> tree.point[0] >= 0  # valid point
    True
    """
    if not points:
        return None

    root_holder = [None]
    stack = [(points, 0, root_holder, 0)]  # (pts, depth, parent_list, idx)

    while stack:
        pts, depth, parent_list, idx = stack.pop()
        if not pts:
            continue
        k = len(pts[0])
        axis = depth % k
        pts.sort(key=lambda p: p[axis])
        mid = len(pts) // 2
        node = KDNode(point=pts[mid])
        parent_list[idx] = node

        left_holder = [None]
        right_holder = [None]
        node.left = None
        node.right = None

        stack.append((pts[:mid], depth + 1, node.__dict__, "left"))
        stack.append((pts[mid + 1:], depth + 1, node.__dict__, "right"))

    return root_holder[0]


# Nearest neighbor search (used in both variants)
def nearest_neighbour(
    root: KDNode | None, query: list[float]
) -> tuple[list[float] | None, float]:
    """
    Nearest neighbor search in a KD-tree.

    >>> pts = [[2,3],[5,4],[9,6],[4,7],[8,1],[7,2]]
    >>> tree = build_kdtree_recursive(pts)
    >>> nn, dist = nearest_neighbour(tree, [9, 2])
    >>> nn
    [8, 1]
    >>> dist
    2
    """
    best_point: list[float] | None = None
    best_dist: float = float("inf")

    def search(node: KDNode | None, depth: int = 0) -> None:
        nonlocal best_point, best_dist
        if node is None:
            return
        dist = sum((q - p) ** 2 for q, p in zip(query, node.point))
        if best_point is None or dist < best_dist:
            best_point, best_dist = node.point, dist
        k = len(query)
        axis = depth % k
        near, far = (node.left, node.right) if query[axis] <= node.point[axis] else (node.right, node.left)
        search(near, depth + 1)
        if (query[axis] - node.point[axis]) ** 2 < best_dist:
            search(far, depth + 1)

    search(root)
    return best_point, best_dist


# Variant 3: Brute-force nearest neighbor (baseline for comparison)
def nearest_neighbour_brute(
    points: list[list[float]], query: list[float]
) -> tuple[list[float] | None, float]:
    """
    Brute-force nearest neighbor. Time: O(n), no preprocessing.

    >>> pts = [[2,3],[5,4],[9,6],[4,7],[8,1],[7,2]]
    >>> nn, dist = nearest_neighbour_brute(pts, [9, 2])
    >>> nn
    [8, 1]
    >>> dist
    2
    """
    best_point = None
    best_dist = float("inf")
    for p in points:
        dist = sum((q - pi) ** 2 for q, pi in zip(query, p))
        if dist < best_dist:
            best_point, best_dist = p, dist
    return best_point, best_dist


def benchmark():
    random.seed(42)
    points = [[random.uniform(0, 100), random.uniform(0, 100)] for _ in range(1000)]
    query = [50.0, 50.0]
    n = 200

    tree_r = build_kdtree_recursive(list(points))

    t1 = timeit.timeit(lambda: build_kdtree_recursive(list(points)), number=50)
    t2 = timeit.timeit(lambda: nearest_neighbour(tree_r, query), number=n)
    t3 = timeit.timeit(lambda: nearest_neighbour_brute(points, query), number=n)

    print(f"build_recursive (50 runs):   {t1:.4f}s")
    print(f"nn_kdtree ({n} queries):      {t2:.4f}s")
    print(f"nn_brute  ({n} queries):      {t3:.4f}s")


if __name__ == "__main__":
    benchmark()
