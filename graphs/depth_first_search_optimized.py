"""
DFS - Optimized Variants with Benchmarks.

Variant 1: Recursive DFS
Variant 2: Iterative DFS (stack of nodes)
Variant 3: Iterative DFS (stack of iterators) - true recursion order

>>> dfs_recurse({0: [1, 2], 1: [], 2: []}, 0)
[0, 1, 2]
>>> dfs_stack({0: [1, 2], 1: [], 2: []}, 0)
[0, 2, 1]
>>> dfs_iter_tree({0: [1, 2], 1: [], 2: []}, 0)
[0, 1, 2]
"""

import sys
import time
import random
from collections import defaultdict


def dfs_recurse(graph, start):
    """Classic recursive DFS.

    >>> dfs_recurse({1: [2]}, 1)
    [1, 2]
    """
    out, seen = [], set()

    def go(u):
        seen.add(u)
        out.append(u)
        for v in graph.get(u, []):
            if v not in seen:
                go(v)

    go(start)
    return out


def dfs_stack(graph, start):
    """Iterative DFS with a plain node stack (order differs -- neighbours pushed then popped).

    >>> dfs_stack({1: [2]}, 1)
    [1, 2]
    """
    out, seen, stack = [], set(), [start]
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        out.append(u)
        for v in graph.get(u, []):
            if v not in seen:
                stack.append(v)
    return out


def dfs_iter_tree(graph, start):
    """Iterative DFS using iterators -- preserves recursive call order.

    >>> dfs_iter_tree({1: [2, 3], 2: [], 3: []}, 1)
    [1, 2, 3]
    """
    out, seen = [start], {start}
    stack = [iter(graph.get(start, []))]
    while stack:
        try:
            v = next(stack[-1])
            if v not in seen:
                seen.add(v)
                out.append(v)
                stack.append(iter(graph.get(v, [])))
        except StopIteration:
            stack.pop()
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
        ("Recursive DFS", dfs_recurse),
        ("Stack DFS", dfs_stack),
        ("Iter-tree DFS", dfs_iter_tree),
    ]
    print(f"Benchmark: DFS on n={n}")
    print("-" * 65)
    for name, fn in variants:
        t0 = time.perf_counter()
        for _ in range(5):
            r = fn(g, 0)
        t = (time.perf_counter() - t0) * 1000 / 5
        print(f"{name:<18} visited={len(r)}   time={t:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
