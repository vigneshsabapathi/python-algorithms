from __future__ import annotations

from random import random


class Node:
    """
    Treap's node
    Treap is a binary tree by value and heap by priority
    """

    def __init__(self, value: int | None = None):
        self.value = value
        self.prior = random()
        self.left: Node | None = None
        self.right: Node | None = None

    def __repr__(self) -> str:
        from pprint import pformat

        if self.left is None and self.right is None:
            return f"'{self.value}: {self.prior:.5}'"
        else:
            return pformat(
                {f"{self.value}: {self.prior:.5}": (self.left, self.right)}, indent=1
            )

    def __str__(self) -> str:
        value = str(self.value) + " "
        left = str(self.left or "")
        right = str(self.right or "")
        return value + left + right


def split(root: Node | None, value: int) -> tuple[Node | None, Node | None]:
    """
    We split current tree into 2 trees with value:

    Left tree contains all values less than split value.
    Right tree contains all values greater or equal, than split value
    """
    if root is None or root.value is None:
        return None, None
    elif value < root.value:
        left, root.left = split(root.left, value)
        return left, root
    else:
        root.right, right = split(root.right, value)
        return root, right


def merge(left: Node | None, right: Node | None) -> Node | None:
    """
    We merge 2 trees into one.
    Note: all left tree's values must be less than all right tree's
    """
    if (not left) or (not right):
        return left or right
    elif left.prior < right.prior:
        left.right = merge(left.right, right)
        return left
    else:
        right.left = merge(left, right.left)
        return right


def insert(root: Node | None, value: int) -> Node | None:
    """
    Insert element

    Split current tree with a value into left, right,
    Insert new node into the middle
    Merge left, node, right into root
    """
    node = Node(value)
    left, right = split(root, value)
    return merge(merge(left, node), right)


def erase(root: Node | None, value: int) -> Node | None:
    """
    Erase element

    Split all nodes with values less into left,
    Split all nodes with values greater into right.
    Merge left, right
    """
    left, right = split(root, value - 1)
    _, right = split(right, value)
    return merge(left, right)


def inorder(root: Node | None) -> None:
    """Just recursive print of a tree"""
    if not root:
        return
    else:
        inorder(root.left)
        print(root.value, end=",")
        inorder(root.right)


def interact_treap(root: Node | None, args: str) -> Node | None:
    """
    Commands:
    + value to add value into treap
    - value to erase all nodes with value

        >>> root = interact_treap(None, "+1")
        >>> inorder(root)
        1,
        >>> root = interact_treap(root, "+3 +5 +17 +19 +2 +16 +4 +0")
        >>> inorder(root)
        0,1,2,3,4,5,16,17,19,
        >>> root = interact_treap(root, "+4 +4 +4")
        >>> inorder(root)
        0,1,2,3,4,4,4,4,5,16,17,19,
        >>> root = interact_treap(root, "-0")
        >>> inorder(root)
        1,2,3,4,4,4,4,5,16,17,19,
        >>> root = interact_treap(root, "-4")
        >>> inorder(root)
        1,2,3,5,16,17,19,
        >>> root = interact_treap(root, "=0")
        Unknown command
    """
    for arg in args.split():
        if arg[0] == "+":
            root = insert(root, int(arg[1:]))
        elif arg[0] == "-":
            root = erase(root, int(arg[1:]))
        else:
            print("Unknown command")

    return root


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    root = None
    root = interact_treap(root, "+5 +3 +8 +1 +4 +7 +9")
    print("Inorder traversal: ", end="")
    inorder(root)
    print()
    root = interact_treap(root, "-3")
    print("After deleting 3: ", end="")
    inorder(root)
    print()
