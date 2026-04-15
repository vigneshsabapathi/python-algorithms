"""
Strongly Connected Components - Optimized Variants

Finds SCCs using Kosaraju's method: topology sort + reverse DFS.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/strongly_connected_components.py
"""

import time


# ---------- Variant 1: Iterative topology sort + iterative reverse DFS ----------
def scc_iterative(graph: dict[int, list[int]]) -> list[list[int]]:
    """
    Fully iterative SCC finder (no recursion depth limits).

    >>> scc_iterative({0: [2, 3], 1: [0], 2: [1], 3: [4], 4: []})
    [[0, 1, 2], [3], [4]]
    >>> scc_iterative({0: [1, 2, 3], 1: [2], 2: [0], 3: [4], 4: [5], 5: [3]})
    [[0, 2, 1], [3, 5, 4]]
    """
    n = len(graph)
    rev = {i: [] for i in range(n)}
    for u, neighbors in graph.items():
        for v in neighbors:
            rev[v].append(u)

    # Iterative topology sort
    visited = [False] * n
    order = []
    for start in range(n):
        if visited[start]:
            continue
        stack = [(start, 0)]
        visited[start] = True
        while stack:
            u, idx = stack[-1]
            neighbors = graph.get(u, [])
            if idx < len(neighbors):
                stack[-1] = (u, idx + 1)
                v = neighbors[idx]
                if not visited[v]:
                    visited[v] = True
                    stack.append((v, 0))
            else:
                stack.pop()
                order.append(u)

    # Iterative component finding on reverse graph
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


# ---------- Variant 2: Returns component membership map ----------
def scc_membership(graph: dict[int, list[int]]) -> dict[int, int]:
    """
    Returns a dict mapping each vertex to its SCC index.

    >>> scc_membership({0: [2, 3], 1: [0], 2: [1], 3: [4], 4: []})
    {0: 0, 1: 0, 2: 0, 3: 1, 4: 2}
    """
    sccs = scc_iterative(graph)
    membership = {}
    for i, scc in enumerate(sccs):
        for v in scc:
            membership[v] = i
    return membership


# ---------- Variant 3: Tarjan-based SCC (single DFS pass) ----------
def scc_tarjan(graph: dict[int, list[int]]) -> list[list[int]]:
    """
    Tarjan's SCC algorithm (single DFS pass, iterative).

    >>> sorted([sorted(c) for c in scc_tarjan({0: [2, 3], 1: [0], 2: [1], 3: [4], 4: []})])
    [[0, 1, 2], [3], [4]]
    """
    n = len(graph)
    index_counter = [0]
    stack = []
    on_stack = [False] * n
    index = [-1] * n
    lowlink = [-1] * n
    sccs = []

    def strongconnect(v):
        call_stack = [(v, 0)]
        index[v] = lowlink[v] = index_counter[0]
        index_counter[0] += 1
        stack.append(v)
        on_stack[v] = True

        while call_stack:
            u, idx = call_stack[-1]
            neighbors = graph.get(u, [])
            if idx < len(neighbors):
                call_stack[-1] = (u, idx + 1)
                w = neighbors[idx]
                if index[w] == -1:
                    index[w] = lowlink[w] = index_counter[0]
                    index_counter[0] += 1
                    stack.append(w)
                    on_stack[w] = True
                    call_stack.append((w, 0))
                elif on_stack[w]:
                    lowlink[u] = min(lowlink[u], index[w])
            else:
                if lowlink[u] == index[u]:
                    component = []
                    while True:
                        w = stack.pop()
                        on_stack[w] = False
                        component.append(w)
                        if w == u:
                            break
                    sccs.append(component)
                call_stack.pop()
                if call_stack:
                    parent = call_stack[-1][0]
                    lowlink[parent] = min(lowlink[parent], lowlink[u])

    for v in range(n):
        if index[v] == -1:
            strongconnect(v)

    return sccs


# ---------- Benchmark ----------
def benchmark():
    import random
    random.seed(42)
    n = 1000
    graph = {i: [] for i in range(n)}
    for i in range(n):
        for _ in range(3):
            j = random.randint(0, n - 1)
            if j != i:
                graph[i].append(j)

    for name, fn in [
        ("iterative_kosaraju", scc_iterative),
        ("tarjan_iterative", scc_tarjan),
    ]:
        start = time.perf_counter()
        for _ in range(30):
            fn(graph)
        elapsed = (time.perf_counter() - start) / 30 * 1000
        result = fn(graph)
        print(f"  {name:20s}: {elapsed:.3f} ms ({len(result)} SCCs)")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== SCC Benchmark (1000 nodes, 30 runs) ===")
    benchmark()
