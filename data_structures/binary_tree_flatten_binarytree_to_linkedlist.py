"""
Flatten Binary Tree to Linked List

Given the root of a binary tree, flatten it in-place into a linked list.
The "linked list" uses the right pointers of the tree nodes, with all left
pointers set to None. The order follows preorder traversal.

For doctests run:
    python -m doctest binary_tree_flatten_binarytree_to_linkedlist.py -v
"""

from __future__ import annotations


class TreeNode:
    """
    A TreeNode has data variable and pointers to TreeNode objects
    for its left and right children.
    """

    def __init__(self, data: int) -> None:
        self.data = data
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None


def build_tree() -> TreeNode:
    """
    Build and return a sample binary tree.

    Returns:
        TreeNode: The root of the binary tree.

    Examples:
        >>> root = build_tree()
        >>> root.data
        1
        >>> root.left.data
        2
        >>> root.right.data
        5
        >>> root.left.left.data
        3
        >>> root.left.right.data
        4
        >>> root.right.right.data
        6
    """
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(5)
    root.left.left = TreeNode(3)
    root.left.right = TreeNode(4)
    root.right.right = TreeNode(6)
    return root


def flatten(root: TreeNode | None) -> None:
    """
    Flatten a binary tree into a linked list in-place, where the linked list is
    represented using the right pointers of the tree nodes.

    Args:
        root (TreeNode): The root of the binary tree to be flattened.

    Examples:
        >>> root = TreeNode(1)
        >>> root.left = TreeNode(2)
        >>> root.right = TreeNode(5)
        >>> root.left.left = TreeNode(3)
        >>> root.left.right = TreeNode(4)
        >>> root.right.right = TreeNode(6)
        >>> flatten(root)
        >>> root.data
        1
        >>> root.right.right is None
        False
        >>> root.right.right = TreeNode(3)
        >>> root.right.right.right is None
        True
    """
    if not root:
        return

    flatten(root.left)

    right_subtree = root.right

    root.right = root.left
    root.left = None

    current = root
    while current.right:
        current = current.right

    current.right = right_subtree

    flatten(right_subtree)


def display_linked_list(root: TreeNode | None) -> None:
    """
    Display the flattened linked list.

    Args:
        root (TreeNode | None): The root of the flattened linked list.

    Examples:
        >>> root = TreeNode(1)
        >>> root.right = TreeNode(2)
        >>> root.right.right = TreeNode(3)
        >>> display_linked_list(root)
        1 2 3
        >>> root = None
        >>> display_linked_list(root)

    """
    current = root
    while current:
        if current.right is None:
            print(current.data, end="")
            break
        print(current.data, end=" ")
        current = current.right


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Flattened Linked List:")
    root = build_tree()
    flatten(root)
    display_linked_list(root)
    print()
