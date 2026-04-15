"""
Kosaraju's SCC Algorithm - Optimized Variants

Finds strongly connected components by running DFS twice: once on the original
graph to get finish order, then on the reversed graph in reverse finish order.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/scc_kosaraju.py
"""

import time
from collections import deque


# ---------- Variant 1: Iterative DFS (no recursion limit) ----------
def kosaraju_iterative(graph: list[list[int]]) -> list[list[int]]:
    """
    Kosaraju's with iterative DFS to avoid stack overflow on large graphs.

    >>> kosaraju_iterative([[1], [2], [0, 3], [4], [5], [3]])
    [[0, 2, 1], [3, 5, 4]]
    """
    n = len(graph)
    # Build reverse graph
    rev = [[] for _ in range(n)]
    for u in range(n):
        for v in graph[u]:
            rev[v].append(u)

    # First pass: iterative DFS to get finish order
    visited = [False] * n
    order = []
    for start in range(n):
        if visited[start]:
            continue
        stack = [(start, 0)]
        visited[start] = True
        while stack:
            u, idx = stack[-1]
            if idx < len(graph[u]):
                stack[-1] = (u, idx + 1)
                v = graph[u][idx]
                if not visited[v]:
                    visited[v] = True
                    stack.append((v, 0))
            else:
                stack.pop()
                order.append(u)

    # Second pass: iterative DFS on reversed graph
    visited = [False] * n
    sccs = []
    for start in reversed(order):
        if visited[start]:
            continue
        component = []
        stack = [start]
        visited[start] = True
        while stack:
            u = stack.pop()
            component.append(u)
            for v in rev[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append(v)
        sccs.append(component)

    return sccs


# ---------- Variant 2: Dict-based (supports any hashable vertex) ----------
def kosaraju_dict(graph: dict[str, list[str]]) -> list[list[str]]:
    """
    Kosaraju's with dictionary graph for string/any-type vertices.

    >>> kosaraju_dict({'a': ['b'], 'b': ['c'], 'c': ['a'], 'd': []})
    [['d'], ['a', 'c', 'b']]
    """
    rev = {v: [] for v in graph}
    for u in graph:
        for v in graph[u]:
            rev[v].append(u)

    visited = set()
    order = []

    def dfs1(u):
        stack = [(u, 0)]
        visited.add(u)
        while stack:
            node, idx = stack[-1]
            neighbors = graph[node]
            if idx < len(neighbors):
                stack[-1] = (node, idx + 1)
                v = neighbors[idx]
                if v not in visited:
                    visited.add(v)
                    stack.append((v, 0))
            else:
                stack.pop()
                order.append(node)

    for v in graph:
        if v not in visited:
            dfs1(v)

    visited = set()
    sccs = []
    for start in reversed(order):
        if start in visited:
            continue
        component = []
        stack = [start]
        visited.add(start)
        while stack:
            u = stack.pop()
            component.append(u)
            for v in rev[u]:
                if v not in visited:
                    visited.add(v)
                    stack.append(v)
        sccs.append(component)

    return sccs


# ---------- Variant 3: Returns condensation DAG ----------
def kosaraju_condensation(graph: list[list[int]]) -> tuple[list[list[int]], list[list[int]]]:
    """
    Returns SCCs and the condensation DAG (DAG of SCCs).

    >>> sccs, dag = kosaraju_condensation([[1], [2], [0, 3], [4], [5], [3]])
    >>> len(sccs)
    2
    >>> len(dag)
    2
    """
    sccs = kosaraju_iterative(graph)
    n = len(graph)

    # Map each vertex to its SCC index
    comp_id = [0] * n
    for i, scc in enumerate(sccs):
        for v in scc:
            comp_id[v] = i

    # Build condensation DAG
    k = len(sccs)
    dag = [[] for _ in range(k)]
    seen = set()
    for u in range(n):
        for v in graph[u]:
            cu, cv = comp_id[u], comp_id[v]
            if cu != cv and (cu, cv) not in seen:
                seen.add((cu, cv))
                dag[cu].append(cv)

    return sccs, dag


# ---------- Benchmark ----------
def benchmark():
    import random
    random.seed(42)
    n = 1000
    graph = [[] for _ in range(n)]
    for i in range(n):
        for _ in range(3):
            j = random.randint(0, n - 1)
            if j != i:
                graph[i].append(j)

    for name, fn in [
        ("iterative", lambda: kosaraju_iterative(graph)),
        ("condensation", lambda: kosaraju_condensation(graph)),
    ]:
        start = time.perf_counter()
        for _ in range(30):
            fn()
        elapsed = (time.perf_counter() - start) / 30 * 1000
        result = fn()
        scc_count = len(result) if isinstance(result, list) else len(result[0])
        print(f"  {name:20s}: {elapsed:.3f} ms ({scc_count} SCCs)")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Kosaraju SCC Benchmark (1000 nodes, 30 runs) ===")
    benchmark()
