r"""
Different Views of a Binary Tree

Given the root of a binary tree, return:
  1. Right side view  — rightmost node at each level
  2. Left side view   — leftmost node at each level
  3. Top side view    — first visible node per horizontal distance (BFS)
  4. Bottom side view — last visible node per horizontal distance (BFS)

For doctests run:
    python -m doctest binary_tree_diff_views_of_binary_tree.py -v
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass


@dataclass
class TreeNode:
    val: int
    left: TreeNode | None = None
    right: TreeNode | None = None


def make_tree() -> TreeNode:
    """
    >>> make_tree().val
    3
    """
    return TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))


def binary_tree_right_side_view(root: TreeNode | None) -> list[int]:
    r"""
    Function returns the right side view of binary tree.

       3       <-  3
     / \
    9   20    <-  20
       /  \
      15   7  <-  7

    >>> binary_tree_right_side_view(make_tree())
    [3, 20, 7]
    >>> binary_tree_right_side_view(None)
    []
    """

    def depth_first_search(
        root: TreeNode | None, depth: int, right_view: list[int]
    ) -> None:
        if not root:
            return

        if depth == len(right_view):
            right_view.append(root.val)

        depth_first_search(root.right, depth + 1, right_view)
        depth_first_search(root.left, depth + 1, right_view)

    right_view: list = []
    if not root:
        return right_view

    depth_first_search(root, 0, right_view)
    return right_view


def binary_tree_left_side_view(root: TreeNode | None) -> list[int]:
    r"""
    Function returns the left side view of binary tree.

    3  ->    3
            / \
    9  ->  9   20
              /  \
    15 ->    15   7

    >>> binary_tree_left_side_view(make_tree())
    [3, 9, 15]
    >>> binary_tree_left_side_view(None)
    []
    """

    def depth_first_search(
        root: TreeNode | None, depth: int, left_view: list[int]
    ) -> None:
        if not root:
            return

        if depth == len(left_view):
            left_view.append(root.val)

        depth_first_search(root.left, depth + 1, left_view)
        depth_first_search(root.right, depth + 1, left_view)

    left_view: list = []
    if not root:
        return left_view

    depth_first_search(root, 0, left_view)
    return left_view


def binary_tree_top_side_view(root: TreeNode | None) -> list[int]:
    r"""
    Function returns the top side view of binary tree.

    9 3 20 7
    v v v  v

      3
     / \
    9   20
       /  \
      15   7

    >>> binary_tree_top_side_view(make_tree())
    [9, 3, 20, 7]
    >>> binary_tree_top_side_view(None)
    []
    """

    def breadth_first_search(root: TreeNode, top_view: list[int]) -> None:
        queue = [(root, 0)]
        lookup: dict = defaultdict(list)

        while queue:
            first = queue.pop(0)
            node, hd = first

            lookup[hd].append(node.val)

            if node.left:
                queue.append((node.left, hd - 1))
            if node.right:
                queue.append((node.right, hd + 1))

        for pair in sorted(lookup.items(), key=lambda each: each[0]):
            top_view.append(pair[1][0])

    top_view: list = []
    if not root:
        return top_view

    breadth_first_search(root, top_view)
    return top_view


def binary_tree_bottom_side_view(root: TreeNode | None) -> list[int]:
    r"""
    Function returns the bottom side view of binary tree

      3
     / \
    9   20
       /  \
      15   7
    ^  ^  ^  ^
    9 15 20  7

    >>> binary_tree_bottom_side_view(make_tree())
    [9, 15, 20, 7]
    >>> binary_tree_bottom_side_view(None)
    []
    """

    def breadth_first_search(root: TreeNode, bottom_view: list[int]) -> None:
        queue = [(root, 0)]
        lookup: dict = defaultdict(list)

        while queue:
            first = queue.pop(0)
            node, hd = first
            lookup[hd].append(node.val)

            if node.left:
                queue.append((node.left, hd - 1))
            if node.right:
                queue.append((node.right, hd + 1))

        for pair in sorted(lookup.items(), key=lambda each: each[0]):
            bottom_view.append(pair[1][-1])

    bottom_view: list = []
    if not root:
        return bottom_view

    breadth_first_search(root, bottom_view)
    return bottom_view


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    tree = make_tree()
    print("Right view:", binary_tree_right_side_view(tree))
    print("Left view:", binary_tree_left_side_view(tree))
    print("Top view:", binary_tree_top_side_view(tree))
    print("Bottom view:", binary_tree_bottom_side_view(tree))
