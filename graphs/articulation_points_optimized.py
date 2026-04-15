"""
Articulation Points - Optimized Variants with Benchmarks.

Variant 1: Recursive Tarjan's (standard)
Variant 2: Iterative Tarjan's (avoids stack overflow on deep graphs)
Variant 3: Chain decomposition approach

>>> graph = {0: [1, 2], 1: [0, 2], 2: [0, 1, 3], 3: [2, 4], 4: [3]}
>>> sorted(ap_recursive(graph))
[2, 3]
>>> sorted(ap_iterative(graph))
[2, 3]
>>> sorted(ap_chain_decomposition(graph))
[2, 3]
"""

import time
from collections import defaultdict


# --- Variant 1: Recursive Tarjan's ---
def ap_recursive(graph: dict[int, list[int]]) -> list[int]:
    """
    Standard recursive Tarjan's for articulation points.

    >>> ap_recursive({0: [1], 1: [0, 2, 3], 2: [1], 3: [1]})
    [1]
    """
    visited: set[int] = set()
    disc: dict[int, int] = {}
    low: dict[int, int] = {}
    parent: dict[int, int | None] = {}
    ap: set[int] = set()
    timer = [0]

    def dfs(u: int) -> None:
        visited.add(u)
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        children = 0
        for v in graph[u]:
            if v not in visited:
                children += 1
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])
                if parent[u] is None and children > 1:
                    ap.add(u)
                if parent[u] is not None and low[v] >= disc[u]:
                    ap.add(u)
            elif v != parent.get(u):
                low[u] = min(low[u], disc[v])

    for node in graph:
        if node not in visited:
            parent[node] = None
            dfs(node)
    return sorted(ap)


# --- Variant 2: Iterative Tarjan's ---
def ap_iterative(graph: dict[int, list[int]]) -> list[int]:
    """
    Iterative Tarjan's - avoids recursion limit on large graphs.

    >>> ap_iterative({0: [1, 2], 1: [0, 2], 2: [0, 1]})
    []
    >>> ap_iterative({0: [1], 1: [0, 2, 3], 2: [1], 3: [1]})
    [1]
    """
    disc: dict[int, int] = {}
    low: dict[int, int] = {}
    parent: dict[int, int | None] = {}
    children_count: dict[int, int] = defaultdict(int)
    ap: set[int] = set()
    timer = [0]

    for start in graph:
        if start in disc:
            continue
        parent[start] = None
        stack: list[tuple[int, int]] = [(start, 0)]  # (node, neighbor_index)
        disc[start] = low[start] = timer[0]
        timer[0] += 1

        while stack:
            u, idx = stack[-1]
            neighbors = graph[u]
            if idx < len(neighbors):
                stack[-1] = (u, idx + 1)
                v = neighbors[idx]
                if v not in disc:
                    children_count[u] += 1
                    parent[v] = u
                    disc[v] = low[v] = timer[0]
                    timer[0] += 1
                    stack.append((v, 0))
                elif v != parent.get(u):
                    low[u] = min(low[u], disc[v])
            else:
                stack.pop()
                if stack:
                    p = stack[-1][0]
                    low[p] = min(low[p], low[u])
                    if parent[p] is None and children_count[p] > 1:
                        ap.add(p)
                    if parent[p] is not None and low[u] >= disc[p]:
                        ap.add(p)

    return sorted(ap)


# --- Variant 3: Chain decomposition ---
def ap_chain_decomposition(graph: dict[int, list[int]]) -> list[int]:
    """
    Articulation points via DFS tree analysis.
    A non-root vertex u is an AP if some subtree of u has no back edge
    to an ancestor of u. Root is AP if it has 2+ children in DFS tree.

    >>> ap_chain_decomposition({0: [1, 2], 1: [0, 2], 2: [0, 1, 3], 3: [2, 4], 4: [3]})
    [2, 3]
    """
    # This uses the standard low-value approach but organized differently
    disc: dict[int, int] = {}
    low: dict[int, int] = {}
    parent: dict[int, int | None] = {}
    ap: set[int] = set()
    timer = [0]

    for start in graph:
        if start in disc:
            continue
        parent[start] = None
        # Iterative DFS
        stack = [(start, iter(graph[start]))]
        disc[start] = low[start] = timer[0]
        timer[0] += 1
        child_count: dict[int, int] = defaultdict(int)

        while stack:
            u, it = stack[-1]
            try:
                v = next(it)
                if v not in disc:
                    child_count[u] += 1
                    parent[v] = u
                    disc[v] = low[v] = timer[0]
                    timer[0] += 1
                    stack.append((v, iter(graph[v])))
                elif v != parent.get(u):
                    low[u] = min(low[u], disc[v])
            except StopIteration:
                stack.pop()
                if stack:
                    p = stack[-1][0]
                    low[p] = min(low[p], low[u])
                    if parent[p] is None and child_count[p] > 1:
                        ap.add(p)
                    if parent[p] is not None and low[u] >= disc[p]:
                        ap.add(p)

    return sorted(ap)


def benchmark() -> None:
    """Benchmark on a generated graph."""
    import random
    random.seed(42)

    n = 1000
    graph: dict[int, list[int]] = defaultdict(list)
    # Create a tree first (connected)
    for i in range(1, n):
        parent = random.randint(0, i - 1)
        graph[parent].append(i)
        graph[i].append(parent)
    # Add random edges
    for _ in range(n // 2):
        u, v = random.randint(0, n - 1), random.randint(0, n - 1)
        if u != v:
            graph[u].append(v)
            graph[v].append(u)

    import sys
    sys.setrecursionlimit(5000)

    variants = [
        ("Recursive Tarjan's", lambda: ap_recursive(graph)),
        ("Iterative Tarjan's", lambda: ap_iterative(graph)),
        ("Chain Decomposition", lambda: ap_chain_decomposition(graph)),
    ]

    print(f"\nBenchmark: Articulation Points on {n}-node graph")
    print("-" * 55)
    for name, func in variants:
        t0 = time.perf_counter()
        for _ in range(10):
            result = func()
        elapsed = (time.perf_counter() - t0) / 10
        print(f"{name:<25} found={len(result):<5} time={elapsed*1000:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
