"""
Pure Python implementation of binary tree traversal algorithms.

Tree structure used in examples:
         1
        / \\
       2   3
      / \\ / \\
     4  5 6  7

Traversal orders:
  Pre-order  (root → left → right): 1,2,4,5,3,6,7
  In-order   (left → root → right): 4,2,5,1,6,3,7
  Post-order (left → right → root): 4,5,2,6,7,3,1
  Level-order (BFS by row):         1,2,3,4,5,6,7

Each traversal is provided in two flavours:
  - Recursive  (clean and readable)
  - Iterative  (explicit stack/queue, no recursion limit risk)
"""

from __future__ import annotations

import queue


class TreeNode:
    def __init__(self, data: int) -> None:
        self.data = data
        self.right: TreeNode | None = None
        self.left: TreeNode | None = None


def build_tree() -> TreeNode:
    """Interactively build a binary tree level by level (BFS order).
    Enter 'N' to stop adding children at any node.
    """
    print("\n********Press N to stop entering at any point of time********\n")
    check = input("Enter the value of the root node: ").strip().lower()
    q: queue.Queue[TreeNode] = queue.Queue()
    tree_node = TreeNode(int(check))
    q.put(tree_node)
    while not q.empty():
        node_found = q.get()
        check = input(f"Enter the left node of {node_found.data}: ").strip().lower() or "n"
        if check == "n":
            return tree_node
        left_node = TreeNode(int(check))
        node_found.left = left_node
        q.put(left_node)
        check = input(f"Enter the right node of {node_found.data}: ").strip().lower() or "n"
        if check == "n":
            return tree_node
        right_node = TreeNode(int(check))
        node_found.right = right_node
        q.put(right_node)
    raise ValueError("Something went wrong")


# ---------------------------------------------------------------------------
# Recursive traversals
# ---------------------------------------------------------------------------

def pre_order(node: TreeNode | None) -> None:
    """Root → Left → Right (recursive).

    >>> root = TreeNode(1)
    >>> root.left, root.right = TreeNode(2), TreeNode(3)
    >>> root.left.left, root.left.right = TreeNode(4), TreeNode(5)
    >>> root.right.left, root.right.right = TreeNode(6), TreeNode(7)
    >>> pre_order(root)
    1,2,4,5,3,6,7,
    """
    if not isinstance(node, TreeNode) or not node:
        return
    print(node.data, end=",")
    pre_order(node.left)
    pre_order(node.right)


def in_order(node: TreeNode | None) -> None:
    """Left → Root → Right (recursive).  On a BST gives sorted output.

    >>> root = TreeNode(1)
    >>> root.left, root.right = TreeNode(2), TreeNode(3)
    >>> root.left.left, root.left.right = TreeNode(4), TreeNode(5)
    >>> root.right.left, root.right.right = TreeNode(6), TreeNode(7)
    >>> in_order(root)
    4,2,5,1,6,3,7,
    """
    if not isinstance(node, TreeNode) or not node:
        return
    in_order(node.left)
    print(node.data, end=",")
    in_order(node.right)


def post_order(node: TreeNode | None) -> None:
    """Left → Right → Root (recursive).  Root is always last.

    >>> root = TreeNode(1)
    >>> root.left, root.right = TreeNode(2), TreeNode(3)
    >>> root.left.left, root.left.right = TreeNode(4), TreeNode(5)
    >>> root.right.left, root.right.right = TreeNode(6), TreeNode(7)
    >>> post_order(root)
    4,5,2,6,7,3,1,
    """
    if not isinstance(node, TreeNode) or not node:
        return
    post_order(node.left)
    post_order(node.right)
    print(node.data, end=",")


def level_order(node: TreeNode | None) -> None:
    """BFS — visits nodes level by level left to right.

    >>> root = TreeNode(1)
    >>> root.left, root.right = TreeNode(2), TreeNode(3)
    >>> root.left.left, root.left.right = TreeNode(4), TreeNode(5)
    >>> root.right.left, root.right.right = TreeNode(6), TreeNode(7)
    >>> level_order(root)
    1,2,3,4,5,6,7,
    """
    if not isinstance(node, TreeNode) or not node:
        return
    q: queue.Queue[TreeNode] = queue.Queue()
    q.put(node)
    while not q.empty():
        node_dequeued = q.get()
        print(node_dequeued.data, end=",")
        if node_dequeued.left:
            q.put(node_dequeued.left)
        if node_dequeued.right:
            q.put(node_dequeued.right)


def level_order_actual(node: TreeNode | None) -> None:
    """BFS — prints each depth level on its own line.

    >>> root = TreeNode(1)
    >>> root.left, root.right = TreeNode(2), TreeNode(3)
    >>> root.left.left, root.left.right = TreeNode(4), TreeNode(5)
    >>> root.right.left, root.right.right = TreeNode(6), TreeNode(7)
    >>> level_order_actual(root)
    1,
    2,3,
    4,5,6,7,
    """
    if not isinstance(node, TreeNode) or not node:
        return
    q: queue.Queue[TreeNode] = queue.Queue()
    q.put(node)
    while not q.empty():
        next_level: list[TreeNode] = []
        while not q.empty():
            node_dequeued = q.get()
            print(node_dequeued.data, end=",")
            if node_dequeued.left:
                next_level.append(node_dequeued.left)
            if node_dequeued.right:
                next_level.append(node_dequeued.right)
        print()
        for inner_node in next_level:
            q.put(inner_node)


# ---------------------------------------------------------------------------
# Iterative traversals (explicit stack — no recursion limit risk)
# ---------------------------------------------------------------------------

def pre_order_iter(node: TreeNode | None) -> None:
    """Root → Left → Right (iterative).

    Pushes right child first so left is processed first (LIFO).

    >>> root = TreeNode(1)
    >>> root.left, root.right = TreeNode(2), TreeNode(3)
    >>> root.left.left, root.left.right = TreeNode(4), TreeNode(5)
    >>> root.right.left, root.right.right = TreeNode(6), TreeNode(7)
    >>> pre_order_iter(root)
    1,2,4,5,3,6,7,
    """
    if not isinstance(node, TreeNode) or not node:
        return
    stack: list[TreeNode] = []
    n: TreeNode | None = node
    while n or stack:
        while n:
            print(n.data, end=",")
            stack.append(n)
            n = n.left
        n = stack.pop()
        n = n.right


def in_order_iter(node: TreeNode | None) -> None:
    """Left → Root → Right (iterative).

    >>> root = TreeNode(1)
    >>> root.left, root.right = TreeNode(2), TreeNode(3)
    >>> root.left.left, root.left.right = TreeNode(4), TreeNode(5)
    >>> root.right.left, root.right.right = TreeNode(6), TreeNode(7)
    >>> in_order_iter(root)
    4,2,5,1,6,3,7,
    """
    if not isinstance(node, TreeNode) or not node:
        return
    stack: list[TreeNode] = []
    n: TreeNode | None = node
    while n or stack:
        while n:
            stack.append(n)
            n = n.left
        n = stack.pop()
        print(n.data, end=",")
        n = n.right


def post_order_iter(node: TreeNode | None) -> None:
    """Left → Right → Root (iterative, two-stack method).

    Stack 1 drives a modified pre-order (root→right→left);
    stack 2 reverses that to give left→right→root.

    >>> root = TreeNode(1)
    >>> root.left, root.right = TreeNode(2), TreeNode(3)
    >>> root.left.left, root.left.right = TreeNode(4), TreeNode(5)
    >>> root.right.left, root.right.right = TreeNode(6), TreeNode(7)
    >>> post_order_iter(root)
    4,5,2,6,7,3,1,
    """
    if not isinstance(node, TreeNode) or not node:
        return
    stack1: list[TreeNode] = [node]
    stack2: list[TreeNode] = []
    while stack1:
        n = stack1.pop()
        if n.left:
            stack1.append(n.left)
        if n.right:
            stack1.append(n.right)
        stack2.append(n)
    while stack2:
        print(stack2.pop().data, end=",")


def prompt(s: str = "", width: int = 50, char: str = "*") -> str:
    if not s:
        return "\n" + width * char
    left, extra = divmod(width - len(s) - 2, 2)
    return f"{left * char} {s} {(left + extra) * char}"


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
    print(prompt("Binary Tree Traversals"))

    node = build_tree()

    for label, fn in [
        ("Pre Order (recursive)", pre_order),
        ("In Order (recursive)", in_order),
        ("Post Order (recursive)", post_order),
        ("Level Order (BFS)", level_order),
        ("Level Order by row", level_order_actual),
        ("Pre Order (iterative)", pre_order_iter),
        ("In Order (iterative)", in_order_iter),
        ("Post Order (iterative)", post_order_iter),
    ]:
        print(prompt(label))
        fn(node)
        print(prompt())
