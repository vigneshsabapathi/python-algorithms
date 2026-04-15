"""
DFS (class) - Optimized Variants with Benchmarks.

Variant 1: Recursive DFS (sorted neighbours)
Variant 2: Iterative stack DFS
Variant 3: DFS with post-order (useful for topo sort)

>>> dfs_sorted({0: [1, 2], 1: [], 2: []}, 0)
[0, 1, 2]
>>> dfs_post({0: [1, 2], 1: [], 2: []}, 0)
[1, 2, 0]
"""

import time
import random
import sys
from collections import defaultdict


def dfs_sorted(graph, start):
    """Recursive DFS visiting neighbours in sorted order.

    >>> dfs_sorted({0: [2, 1], 1: [], 2: []}, 0)
    [0, 1, 2]
    """
    seen, out = set(), []

    def go(u):
        seen.add(u)
        out.append(u)
        for v in sorted(graph.get(u, [])):
            if v not in seen:
                go(v)

    go(start)
    return out


def dfs_iter_stack(graph, start):
    """Iterative stack DFS.

    >>> sorted(dfs_iter_stack({0: [1, 2], 1: [0], 2: [0]}, 0))
    [0, 1, 2]
    """
    seen, out = set(), []
    stack = [start]
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        out.append(u)
        for v in sorted(graph.get(u, []), reverse=True):
            if v not in seen:
                stack.append(v)
    return out


def dfs_post(graph, start):
    """DFS returning post-order (children before parents).

    >>> dfs_post({0: [1]}, 0)
    [1, 0]
    """
    seen, out = set(), []

    def go(u):
        seen.add(u)
        for v in graph.get(u, []):
            if v not in seen:
                go(v)
        out.append(u)

    go(start)
    return out


def _random_graph(n, avg):
    random.seed(0)
    g = defaultdict(list)
    for _ in range(n * avg):
        u, v = random.randrange(n), random.randrange(n)
        if u != v:
            g[u].append(v)
            g[v].append(u)
    return g


def benchmark():
    sys.setrecursionlimit(10000)
    n = 2000
    g = _random_graph(n, 3)
    variants = [
        ("Sorted recursive", dfs_sorted),
        ("Iterative stack", dfs_iter_stack),
        ("Post-order DFS", dfs_post),
    ]
    print(f"Benchmark: DFS (class variant) on n={n}")
    print("-" * 65)
    for name, fn in variants:
        t0 = time.perf_counter()
        for _ in range(3):
            r = fn(g, 0)
        t = (time.perf_counter() - t0) * 1000 / 3
        print(f"{name:<20} visited={len(r)}   time={t:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
