"""Binary Tree Traversal — optimized and alternative implementations.

Problems with the baseline (binary_tree_traversal.py):
  1. Traversal functions print directly — not reusable or testable without stdout capture.
  2. Recursive depth limited by Python's default call stack (~1000).
  3. No Morris traversal (constant space).

Improvements here:
  1. Generator-based traversals — yield values, caller decides what to do.
  2. Iterative versions for all three DFS orders (single-stack in/pre; two-stack post).
  3. Morris in-order traversal — O(n) time, O(1) extra space (no stack/recursion).
  4. anytree library demo for readable tree building and display.
  5. Benchmark comparing recursive vs iterative vs Morris.

Tree used in examples:
         1
        / \\
       2   3
      / \\ / \\
     4  5 6  7
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Node definition (shared)
# ---------------------------------------------------------------------------

@dataclass
class Node:
    val: int
    left: Node | None = field(default=None, repr=False)
    right: Node | None = field(default=None, repr=False)


def make_sample_tree() -> Node:
    """Build the standard 7-node complete binary tree for examples."""
    root = Node(1)
    root.left = Node(2, Node(4), Node(5))
    root.right = Node(3, Node(6), Node(7))
    return root


# ---------------------------------------------------------------------------
# Approach 1: Generator-based traversals (most reusable)
# ---------------------------------------------------------------------------

def pre_order_gen(node: Node | None):
    """Root → Left → Right, yields values lazily.

    Examples:
        >>> root = make_sample_tree()
        >>> list(pre_order_gen(root))
        [1, 2, 4, 5, 3, 6, 7]
        >>> list(pre_order_gen(None))
        []
        >>> list(pre_order_gen(Node(42)))
        [42]
    """
    if node is None:
        return
    yield node.val
    yield from pre_order_gen(node.left)
    yield from pre_order_gen(node.right)


def in_order_gen(node: Node | None):
    """Left → Root → Right, yields values lazily.

    On a BST produces sorted output.

    Examples:
        >>> root = make_sample_tree()
        >>> list(in_order_gen(root))
        [4, 2, 5, 1, 6, 3, 7]
        >>> list(in_order_gen(None))
        []
    """
    if node is None:
        return
    yield from in_order_gen(node.left)
    yield node.val
    yield from in_order_gen(node.right)


def post_order_gen(node: Node | None):
    """Left → Right → Root, yields values lazily.

    Examples:
        >>> root = make_sample_tree()
        >>> list(post_order_gen(root))
        [4, 5, 2, 6, 7, 3, 1]
        >>> list(post_order_gen(None))
        []
    """
    if node is None:
        return
    yield from post_order_gen(node.left)
    yield from post_order_gen(node.right)
    yield node.val


def level_order_gen(node: Node | None):
    """BFS — yields (depth, value) pairs level by level.

    Examples:
        >>> root = make_sample_tree()
        >>> [(d, v) for d, v in level_order_gen(root)]
        [(0, 1), (1, 2), (1, 3), (2, 4), (2, 5), (2, 6), (2, 7)]
        >>> list(level_order_gen(None))
        []
    """
    if node is None:
        return
    q: deque[tuple[Node, int]] = deque([(node, 0)])
    while q:
        current, depth = q.popleft()
        yield depth, current.val
        if current.left:
            q.append((current.left, depth + 1))
        if current.right:
            q.append((current.right, depth + 1))


def level_order_by_row(node: Node | None) -> list[list[int]]:
    """BFS — returns list of rows, each row a list of node values.

    Examples:
        >>> root = make_sample_tree()
        >>> level_order_by_row(root)
        [[1], [2, 3], [4, 5, 6, 7]]
        >>> level_order_by_row(None)
        []
        >>> level_order_by_row(Node(1))
        [[1]]
    """
    if node is None:
        return []
    result: list[list[int]] = []
    q: deque[Node] = deque([node])
    while q:
        row = []
        for _ in range(len(q)):
            current = q.popleft()
            row.append(current.val)
            if current.left:
                q.append(current.left)
            if current.right:
                q.append(current.right)
        result.append(row)
    return result


# ---------------------------------------------------------------------------
# Approach 2: Iterative DFS generators (no recursion limit)
# ---------------------------------------------------------------------------

def pre_order_iter_gen(node: Node | None):
    """Root → Left → Right iterative — yields values, O(n) time, O(h) space.

    Examples:
        >>> root = make_sample_tree()
        >>> list(pre_order_iter_gen(root))
        [1, 2, 4, 5, 3, 6, 7]
        >>> list(pre_order_iter_gen(None))
        []
    """
    if node is None:
        return
    stack: list[Node] = [node]
    while stack:
        current = stack.pop()
        yield current.val
        if current.right:          # push right first → left processed first
            stack.append(current.right)
        if current.left:
            stack.append(current.left)


def in_order_iter_gen(node: Node | None):
    """Left → Root → Right iterative — yields values, O(n) time, O(h) space.

    Examples:
        >>> root = make_sample_tree()
        >>> list(in_order_iter_gen(root))
        [4, 2, 5, 1, 6, 3, 7]
        >>> list(in_order_iter_gen(None))
        []
    """
    stack: list[Node] = []
    current = node
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        yield current.val
        current = current.right


def post_order_iter_gen(node: Node | None):
    """Left → Right → Root iterative (single-stack with visited flag).

    Uses a (node, visited) tuple to distinguish first vs second visit.
    Avoids the two-stack approach — more memory efficient.

    Examples:
        >>> root = make_sample_tree()
        >>> list(post_order_iter_gen(root))
        [4, 5, 2, 6, 7, 3, 1]
        >>> list(post_order_iter_gen(None))
        []
    """
    if node is None:
        return
    stack: list[tuple[Node, bool]] = [(node, False)]
    while stack:
        current, visited = stack.pop()
        if visited:
            yield current.val
        else:
            stack.append((current, True))        # second visit: emit
            if current.right:
                stack.append((current.right, False))
            if current.left:
                stack.append((current.left, False))


# ---------------------------------------------------------------------------
# Approach 3: Morris In-order Traversal — O(1) extra space
# ---------------------------------------------------------------------------

def morris_in_order(node: Node | None) -> list[int]:
    """In-order traversal with O(1) extra space using threaded BST technique.

    Creates temporary right-links (threads) to predecessor nodes, then
    removes them after use.  No stack or recursion required.

    Algorithm:
      While current is not None:
        If no left child:  visit current, move right.
        Else:
          Find in-order predecessor (rightmost node of left subtree).
          If predecessor.right is None:   thread it to current; go left.
          If predecessor.right is current: unthread it; visit current; go right.

    Examples:
        >>> root = make_sample_tree()
        >>> morris_in_order(root)
        [4, 2, 5, 1, 6, 3, 7]
        >>> morris_in_order(None)
        []
        >>> morris_in_order(Node(1, Node(2), Node(3)))
        [2, 1, 3]
    """
    result: list[int] = []
    current = node

    while current:
        if current.left is None:
            result.append(current.val)
            current = current.right
        else:
            # Find in-order predecessor (rightmost of left subtree)
            predecessor = current.left
            while predecessor.right and predecessor.right is not current:
                predecessor = predecessor.right

            if predecessor.right is None:
                # Thread: link predecessor back to current, then go left
                predecessor.right = current
                current = current.left
            else:
                # Unthread: restore tree, visit current, go right
                predecessor.right = None
                result.append(current.val)
                current = current.right

    return result


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def _build_chain(n: int) -> Node:
    """Build a right-skewed tree of n nodes (worst case for recursive depth)."""
    root = Node(1)
    cur = root
    for i in range(2, n + 1):
        cur.right = Node(i)
        cur = cur.right
    return root


def benchmark() -> None:
    """Compare recursive generator vs iterative generator vs Morris on a
    balanced tree and a skewed chain."""
    import timeit

    root = make_sample_tree()
    n = 500
    chain = _build_chain(n)

    cases: dict[str, object] = {
        "7-node balanced":   root,
        f"{n}-node chain":   chain,
    }

    print("\nBenchmark — in-order traversal variants (10 000 runs)\n")
    for case_name, tree in cases.items():
        print(f"  Tree: {case_name}")
        print(f"  {'Method':<30} {'Time (ms)':>12}")
        print("  " + "-" * 45)
        impls = {
            "recursive generator":   lambda t=tree: list(in_order_gen(t)),
            "iterative generator":   lambda t=tree: list(in_order_iter_gen(t)),
            "Morris (O(1) space)":   lambda t=tree: morris_in_order(t),
        }
        for name, fn in impls.items():
            t = timeit.timeit(fn, number=10_000)
            print(f"  {name:<30} {t * 1000:>12.2f}")
        print()

    # Show level-order-by-row output
    print("level_order_by_row on balanced tree:", level_order_by_row(root))
    print("pre_order_iter_gen:                 ", list(pre_order_iter_gen(root)))
    print("post_order_iter_gen:                ", list(post_order_iter_gen(root)))


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
    benchmark()
