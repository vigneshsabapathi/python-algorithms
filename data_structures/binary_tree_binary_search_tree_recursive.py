"""
Binary Search Tree — Recursive Implementation

A clean recursive BST with put, search, remove, traversals, min/max operations.

For doctests run:
    python -m doctest binary_tree_binary_search_tree_recursive.py -v
"""

from __future__ import annotations

import unittest
from collections.abc import Iterator


class Node:
    def __init__(self, label: int, parent: Node | None) -> None:
        self.label = label
        self.parent = parent
        self.left: Node | None = None
        self.right: Node | None = None


class BinarySearchTree:
    def __init__(self) -> None:
        self.root: Node | None = None

    def empty(self) -> None:
        """
        Empties the tree

        >>> t = BinarySearchTree()
        >>> assert t.root is None
        >>> t.put(8)
        >>> assert t.root is not None
        """
        self.root = None

    def is_empty(self) -> bool:
        """
        Checks if the tree is empty

        >>> t = BinarySearchTree()
        >>> t.is_empty()
        True
        >>> t.put(8)
        >>> t.is_empty()
        False
        """
        return self.root is None

    def put(self, label: int) -> None:
        """
        Put a new node in the tree

        >>> t = BinarySearchTree()
        >>> t.put(8)
        >>> assert t.root.parent is None
        >>> assert t.root.label == 8

        >>> t.put(10)
        >>> assert t.root.right.parent == t.root
        >>> assert t.root.right.label == 10

        >>> t.put(3)
        >>> assert t.root.left.parent == t.root
        >>> assert t.root.left.label == 3
        """
        self.root = self._put(self.root, label)

    def _put(self, node: Node | None, label: int, parent: Node | None = None) -> Node:
        if node is None:
            node = Node(label, parent)
        elif label < node.label:
            node.left = self._put(node.left, label, node)
        elif label > node.label:
            node.right = self._put(node.right, label, node)
        else:
            msg = f"Node with label {label} already exists"
            raise ValueError(msg)

        return node

    def search(self, label: int) -> Node:
        """
        Searches a node in the tree

        >>> t = BinarySearchTree()
        >>> t.put(8)
        >>> t.put(10)
        >>> node = t.search(8)
        >>> assert node.label == 8

        >>> node = t.search(3)
        Traceback (most recent call last):
            ...
        ValueError: Node with label 3 does not exist
        """
        return self._search(self.root, label)

    def _search(self, node: Node | None, label: int) -> Node:
        if node is None:
            msg = f"Node with label {label} does not exist"
            raise ValueError(msg)
        elif label < node.label:
            node = self._search(node.left, label)
        elif label > node.label:
            node = self._search(node.right, label)

        return node

    def remove(self, label: int) -> None:
        """
        Removes a node in the tree

        >>> t = BinarySearchTree()
        >>> t.put(8)
        >>> t.put(10)
        >>> t.remove(8)
        >>> assert t.root.label == 10

        >>> t.remove(3)
        Traceback (most recent call last):
            ...
        ValueError: Node with label 3 does not exist
        """
        node = self.search(label)
        if node.right and node.left:
            lowest_node = self._get_lowest_node(node.right)
            lowest_node.left = node.left
            lowest_node.right = node.right
            node.left.parent = lowest_node
            if node.right:
                node.right.parent = lowest_node
            self._reassign_nodes(node, lowest_node)
        elif not node.right and node.left:
            self._reassign_nodes(node, node.left)
        elif node.right and not node.left:
            self._reassign_nodes(node, node.right)
        else:
            self._reassign_nodes(node, None)

    def _reassign_nodes(self, node: Node, new_children: Node | None) -> None:
        if new_children:
            new_children.parent = node.parent

        if node.parent:
            if node.parent.right == node:
                node.parent.right = new_children
            else:
                node.parent.left = new_children
        else:
            self.root = new_children

    def _get_lowest_node(self, node: Node) -> Node:
        if node.left:
            lowest_node = self._get_lowest_node(node.left)
        else:
            lowest_node = node
            self._reassign_nodes(node, node.right)

        return lowest_node

    def exists(self, label: int) -> bool:
        """
        Checks if a node exists in the tree

        >>> t = BinarySearchTree()
        >>> t.put(8)
        >>> t.put(10)
        >>> t.exists(8)
        True

        >>> t.exists(3)
        False
        """
        try:
            self.search(label)
            return True
        except ValueError:
            return False

    def get_max_label(self) -> int:
        """
        Gets the max label inserted in the tree

        >>> t = BinarySearchTree()
        >>> t.get_max_label()
        Traceback (most recent call last):
            ...
        ValueError: Binary search tree is empty

        >>> t.put(8)
        >>> t.put(10)
        >>> t.get_max_label()
        10
        """
        if self.root is None:
            raise ValueError("Binary search tree is empty")

        node = self.root
        while node.right is not None:
            node = node.right

        return node.label

    def get_min_label(self) -> int:
        """
        Gets the min label inserted in the tree

        >>> t = BinarySearchTree()
        >>> t.get_min_label()
        Traceback (most recent call last):
            ...
        ValueError: Binary search tree is empty

        >>> t.put(8)
        >>> t.put(10)
        >>> t.get_min_label()
        8
        """
        if self.root is None:
            raise ValueError("Binary search tree is empty")

        node = self.root
        while node.left is not None:
            node = node.left

        return node.label

    def inorder_traversal(self) -> Iterator[Node]:
        """
        Return the inorder traversal of the tree

        >>> t = BinarySearchTree()
        >>> [i.label for i in t.inorder_traversal()]
        []

        >>> t.put(8)
        >>> t.put(10)
        >>> t.put(9)
        >>> [i.label for i in t.inorder_traversal()]
        [8, 9, 10]
        """
        return self._inorder_traversal(self.root)

    def _inorder_traversal(self, node: Node | None) -> Iterator[Node]:
        if node is not None:
            yield from self._inorder_traversal(node.left)
            yield node
            yield from self._inorder_traversal(node.right)

    def preorder_traversal(self) -> Iterator[Node]:
        """
        Return the preorder traversal of the tree

        >>> t = BinarySearchTree()
        >>> [i.label for i in t.preorder_traversal()]
        []

        >>> t.put(8)
        >>> t.put(10)
        >>> t.put(9)
        >>> [i.label for i in t.preorder_traversal()]
        [8, 10, 9]
        """
        return self._preorder_traversal(self.root)

    def _preorder_traversal(self, node: Node | None) -> Iterator[Node]:
        if node is not None:
            yield node
            yield from self._preorder_traversal(node.left)
            yield from self._preorder_traversal(node.right)


class BinarySearchTreeTest(unittest.TestCase):
    @staticmethod
    def _get_binary_search_tree() -> BinarySearchTree:
        r"""
              8
             / \
            3   10
           / \    \
          1   6    14
             / \   /
            4   7 13
             \
              5
        """
        t = BinarySearchTree()
        t.put(8)
        t.put(3)
        t.put(6)
        t.put(1)
        t.put(10)
        t.put(14)
        t.put(13)
        t.put(4)
        t.put(7)
        t.put(5)

        return t

    def test_put(self) -> None:
        t = BinarySearchTree()
        assert t.is_empty()

        t.put(8)
        assert t.root is not None
        assert t.root.parent is None
        assert t.root.label == 8

        t.put(10)
        assert t.root.right is not None
        assert t.root.right.parent == t.root
        assert t.root.right.label == 10

        t.put(3)
        assert t.root.left is not None
        assert t.root.left.parent == t.root
        assert t.root.left.label == 3

    def test_search(self) -> None:
        t = self._get_binary_search_tree()
        node = t.search(6)
        assert node.label == 6

    def test_remove(self) -> None:
        t = self._get_binary_search_tree()
        t.remove(13)
        assert t.root is not None
        assert t.root.right is not None
        assert t.root.right.right is not None
        assert t.root.right.right.right is None

    def test_empty(self) -> None:
        t = self._get_binary_search_tree()
        t.empty()
        assert t.root is None

    def test_exists(self) -> None:
        t = self._get_binary_search_tree()
        assert t.exists(6)
        assert not t.exists(-1)

    def test_get_max_label(self) -> None:
        t = self._get_binary_search_tree()
        assert t.get_max_label() == 14

    def test_get_min_label(self) -> None:
        t = self._get_binary_search_tree()
        assert t.get_min_label() == 1

    def test_inorder_traversal(self) -> None:
        t = self._get_binary_search_tree()
        labels = [i.label for i in t.inorder_traversal()]
        assert labels == [1, 3, 4, 5, 6, 7, 8, 10, 13, 14]

    def test_preorder_traversal(self) -> None:
        t = self._get_binary_search_tree()
        labels = [i.label for i in t.preorder_traversal()]
        assert labels == [8, 3, 1, 6, 4, 5, 7, 10, 14, 13]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
