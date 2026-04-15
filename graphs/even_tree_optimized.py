"""
Even Tree - Optimized Variants with Benchmarks.

Variant 1: Iterative DFS (two-pass)
Variant 2: Recursive DFS (classic post-order)
Variant 3: Topological-like leaf peeling

>>> iter_even_tree({1: [2, 3], 2: [1, 4], 3: [1], 4: [2]}, 1)
1
>>> rec_even_tree({1: [2, 3], 2: [1, 4], 3: [1], 4: [2]}, 1)
1
>>> peel_even_tree({1: [2, 3], 2: [1, 4], 3: [1], 4: [2]}, 1)
1
"""

import sys
import time
import random
from collections import defaultdict, deque


def iter_even_tree(adj, root):
    """Iterative DFS post-order.

    >>> iter_even_tree({1: [2], 2: [1]}, 1)
    0
    """
    parent = {root: None}
    order = []
    st = [root]
    while st:
        u = st.pop()
        order.append(u)
        for v in adj[u]:
            if v != parent[u]:
                parent[v] = u
                st.append(v)
    size = {}
    removed = 0
    for u in reversed(order):
        s = 1
        for v in adj[u]:
            if v != parent[u]:
                s += size[v]
        size[u] = s
        if u != root and s % 2 == 0:
            removed += 1
    return removed


def rec_even_tree(adj, root):
    """Recursive post-order.

    >>> rec_even_tree({1: [2], 2: [1]}, 1)
    0
    """
    sys.setrecursionlimit(20000)
    removed = [0]

    def dfs(u, p):
        s = 1
        for v in adj[u]:
            if v != p:
                s += dfs(v, u)
        if p is not None and s % 2 == 0:
            removed[0] += 1
        return s

    dfs(root, None)
    return removed[0]


def peel_even_tree(adj, root):
    """Leaf peeling - repeatedly remove leaves with even subtree sizes.

    >>> peel_even_tree({1: [2], 2: [1]}, 1)
    0
    """
    # Build parent via BFS
    parent = {root: None}
    q = deque([root])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            if v != parent[u]:
                parent[v] = u
                q.append(v)
    size = defaultdict(int)
    for u in order:
        size[u] = 1
    removed = 0
    for u in reversed(order):
        if parent[u] is not None:
            size[parent[u]] += size[u]
            if size[u] % 2 == 0:
                removed += 1
    return removed


def _random_tree(n):
    random.seed(0)
    adj = defaultdict(list)
    for v in range(2, n + 1):
        u = random.randint(1, v - 1)
        adj[u].append(v)
        adj[v].append(u)
    return dict(adj)


def benchmark():
    n = 5000
    adj = _random_tree(n)
    # Ensure every node present
    for i in range(1, n + 1):
        adj.setdefault(i, [])
    variants = [
        ("Iterative DFS", iter_even_tree),
        ("Recursive DFS", rec_even_tree),
        ("Leaf peel", peel_even_tree),
    ]
    print(f"Benchmark: Even tree on n={n}")
    print("-" * 65)
    for name, fn in variants:
        t0 = time.perf_counter()
        for _ in range(3):
            r = fn(adj, 1)
        dt = (time.perf_counter() - t0) * 1000 / 3
        print(f"{name:<18} removable={r}   time={dt:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
