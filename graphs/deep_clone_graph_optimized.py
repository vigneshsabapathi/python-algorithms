"""
Deep Clone Graph - Optimized Variants with Benchmarks.

Variant 1: Recursive DFS
Variant 2: Iterative BFS
Variant 3: Iterative DFS (stack)

>>> n = _build_cycle(5)
>>> clone_bfs(n).val == n.val
True
"""

from collections import deque
import time


class Node:
    __slots__ = ("val", "neighbors")

    def __init__(self, val=0):
        self.val = val
        self.neighbors = []


def _build_cycle(n):
    nodes = [Node(i) for i in range(n)]
    for i in range(n):
        nodes[i].neighbors.append(nodes[(i + 1) % n])
        nodes[i].neighbors.append(nodes[(i - 1) % n])
    return nodes[0]


def clone_dfs(node):
    """Recursive DFS clone.

    >>> clone_dfs(None) is None
    True
    """
    mp = {}

    def dfs(u):
        if u in mp:
            return mp[u]
        c = Node(u.val)
        mp[u] = c
        c.neighbors = [dfs(nb) for nb in u.neighbors]
        return c

    return dfs(node) if node else None


def clone_bfs(node):
    """Iterative BFS clone.

    >>> clone_bfs(None) is None
    True
    """
    if node is None:
        return None
    mp = {node: Node(node.val)}
    q = deque([node])
    while q:
        u = q.popleft()
        for nb in u.neighbors:
            if nb not in mp:
                mp[nb] = Node(nb.val)
                q.append(nb)
            mp[u].neighbors.append(mp[nb])
    return mp[node]


def clone_dfs_iter(node):
    """Iterative DFS clone via stack.

    >>> clone_dfs_iter(None) is None
    True
    """
    if node is None:
        return None
    mp = {node: Node(node.val)}
    stack = [node]
    while stack:
        u = stack.pop()
        for nb in u.neighbors:
            if nb not in mp:
                mp[nb] = Node(nb.val)
                stack.append(nb)
            mp[u].neighbors.append(mp[nb])
    return mp[node]


def benchmark():
    root = _build_cycle(2000)
    variants = [
        ("Recursive DFS", clone_dfs),
        ("BFS", clone_bfs),
        ("Iterative DFS", clone_dfs_iter),
    ]
    print(f"Benchmark: Clone graph (cycle of 2000 nodes)")
    print("-" * 65)
    for name, fn in variants:
        t0 = time.perf_counter()
        for _ in range(5):
            c = fn(root)
        t = (time.perf_counter() - t0) * 1000 / 5
        print(f"{name:<18} root_val={c.val}   time={t:.3f}ms")


if __name__ == "__main__":
    import doctest, sys
    sys.setrecursionlimit(10000)
    doctest.testmod()
    benchmark()
