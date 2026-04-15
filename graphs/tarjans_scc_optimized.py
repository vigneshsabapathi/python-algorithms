"""
Tarjan's SCC Algorithm - Optimized Variants

Single-pass DFS algorithm for finding strongly connected components using
index and lowlink values. O(V + E) time complexity.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/tarjans_scc.py
"""

import time
from collections import deque


# ---------- Variant 1: Fully iterative (no recursion limit) ----------
def tarjan_iterative(graph: list[list[int]]) -> list[list[int]]:
    """
    Iterative Tarjan's SCC to handle large graphs without recursion depth issues.

    >>> tarjan_iterative([[2, 3, 4], [2, 3, 4], [0, 1, 3], [0, 1, 2], [1]])
    [[4, 3, 1, 2, 0]]
    >>> sorted([sorted(c) for c in tarjan_iterative([[], [], [], []])])
    [[0], [1], [2], [3]]
    """
    n = len(graph)
    index_of = [-1] * n
    lowlink = [-1] * n
    on_stack = [False] * n
    stack = []
    components = []
    counter = [0]

    for start in range(n):
        if index_of[start] != -1:
            continue

        call_stack = [(start, 0)]
        index_of[start] = lowlink[start] = counter[0]
        counter[0] += 1
        stack.append(start)
        on_stack[start] = True

        while call_stack:
            v, idx = call_stack[-1]
            if idx < len(graph[v]):
                call_stack[-1] = (v, idx + 1)
                w = graph[v][idx]
                if index_of[w] == -1:
                    index_of[w] = lowlink[w] = counter[0]
                    counter[0] += 1
                    stack.append(w)
                    on_stack[w] = True
                    call_stack.append((w, 0))
                elif on_stack[w]:
                    lowlink[v] = min(lowlink[v], lowlink[w])
            else:
                if lowlink[v] == index_of[v]:
                    component = []
                    while True:
                        w = stack.pop()
                        on_stack[w] = False
                        component.append(w)
                        if w == v:
                            break
                    components.append(component)

                call_stack.pop()
                if call_stack:
                    parent = call_stack[-1][0]
                    lowlink[parent] = min(lowlink[parent], lowlink[v])

    return components


# ---------- Variant 2: Returns both SCCs and condensation DAG ----------
def tarjan_with_dag(graph: list[list[int]]) -> tuple[list[list[int]], list[list[int]]]:
    """
    Tarjan's returning SCCs and the condensation DAG.

    >>> sccs, dag = tarjan_with_dag([[1], [2], [0, 3], []])
    >>> len(sccs) >= 2
    True
    """
    sccs = tarjan_iterative(graph)
    n = len(graph)
    comp_id = [0] * n
    for i, scc in enumerate(sccs):
        for v in scc:
            comp_id[v] = i

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


# ---------- Variant 3: Dict-based for labeled graphs ----------
def tarjan_dict(graph: dict[str, list[str]]) -> list[list[str]]:
    """
    Tarjan's SCC for dictionary-based graphs with string labels.

    >>> sorted([sorted(c) for c in tarjan_dict({'a': ['b'], 'b': ['c'], 'c': ['a'], 'd': []})])
    [['a', 'b', 'c'], ['d']]
    """
    index_of = {}
    lowlink = {}
    on_stack = set()
    stack = []
    components = []
    counter = [0]

    for start in graph:
        if start in index_of:
            continue

        call_stack = [(start, 0)]
        index_of[start] = lowlink[start] = counter[0]
        counter[0] += 1
        stack.append(start)
        on_stack.add(start)

        while call_stack:
            v, idx = call_stack[-1]
            neighbors = graph.get(v, [])
            if idx < len(neighbors):
                call_stack[-1] = (v, idx + 1)
                w = neighbors[idx]
                if w not in index_of:
                    index_of[w] = lowlink[w] = counter[0]
                    counter[0] += 1
                    stack.append(w)
                    on_stack.add(w)
                    call_stack.append((w, 0))
                elif w in on_stack:
                    lowlink[v] = min(lowlink[v], lowlink[w])
            else:
                if lowlink[v] == index_of[v]:
                    component = []
                    while True:
                        w = stack.pop()
                        on_stack.discard(w)
                        component.append(w)
                        if w == v:
                            break
                    components.append(component)

                call_stack.pop()
                if call_stack:
                    parent = call_stack[-1][0]
                    lowlink[parent] = min(lowlink[parent], lowlink[v])

    return components


# ---------- Benchmark ----------
def benchmark():
    import random
    random.seed(42)
    n = 2000
    graph = [[] for _ in range(n)]
    for i in range(n):
        for _ in range(3):
            j = random.randint(0, n - 1)
            if j != i:
                graph[i].append(j)

    for name, fn in [
        ("iterative", lambda: tarjan_iterative(graph)),
        ("with_dag", lambda: tarjan_with_dag(graph)),
    ]:
        start = time.perf_counter()
        for _ in range(20):
            fn()
        elapsed = (time.perf_counter() - start) / 20 * 1000
        result = fn()
        scc_count = len(result) if isinstance(result, list) else len(result[0])
        print(f"  {name:20s}: {elapsed:.3f} ms ({scc_count} SCCs)")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Tarjan's SCC Benchmark (2000 nodes, 20 runs) ===")
    benchmark()
