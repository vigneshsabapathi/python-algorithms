"""
Is BST Sorted?

Verify that a binary tree satisfies the Binary Search Tree property using
inorder traversal via __iter__. The is_sorted property checks that all values
in the inorder sequence are non-decreasing.

For doctests run:
    python -m doctest binary_tree_is_sorted.py -v
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Node:
    data: float
    left: Node | None = None
    right: Node | None = None

    def __iter__(self) -> Iterator[float]:
        """
        >>> root = Node(data=2.1)
        >>> list(root)
        [2.1]
        >>> root.left=Node(data=2.0)
        >>> list(root)
        [2.0, 2.1]
        >>> root.right=Node(data=2.2)
        >>> list(root)
        [2.0, 2.1, 2.2]
        """
        if self.left:
            yield from self.left
        yield self.data
        if self.right:
            yield from self.right

    @property
    def is_sorted(self) -> bool:
        """
        >>> Node(data='abc').is_sorted
        True
        >>> Node(data=2,
        ...      left=Node(data=1.999),
        ...      right=Node(data=3)).is_sorted
        True
        >>> Node(data=0,
        ...      left=Node(data=0),
        ...      right=Node(data=0)).is_sorted
        True
        >>> Node(data=0,
        ...      left=Node(data=-11),
        ...      right=Node(data=3)).is_sorted
        True
        >>> Node(data=5,
        ...      left=Node(data=1),
        ...      right=Node(data=4, left=Node(data=3))).is_sorted
        False
        >>> Node(data='a',
        ...      left=Node(data=1),
        ...      right=Node(data=4, left=Node(data=3))).is_sorted
        Traceback (most recent call last):
            ...
        TypeError: '<' not supported between instances of 'str' and 'int'
        >>> Node(data=2,
        ...      left=Node([]),
        ...      right=Node(data=4, left=Node(data=3))).is_sorted
        Traceback (most recent call last):
            ...
        TypeError: '<' not supported between instances of 'int' and 'list'
        """
        if self.left and (self.data < self.left.data or not self.left.is_sorted):
            return False
        return not (
            self.right and (self.data > self.right.data or not self.right.is_sorted)
        )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    tree = Node(data=2.1, left=Node(data=2.0), right=Node(data=2.2))
    print(f"Tree {list(tree)} is sorted: {tree.is_sorted = }.")
    assert tree.right
    tree.right.data = 2.0
    print(f"Tree {list(tree)} is sorted: {tree.is_sorted = }.")
    tree.right.data = 2.1
    print(f"Tree {list(tree)} is sorted: {tree.is_sorted = }.")
