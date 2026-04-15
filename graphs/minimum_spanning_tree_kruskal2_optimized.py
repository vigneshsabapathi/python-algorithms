"""
Kruskal's MST (Version 2 - OOP) - Optimized Variants

Object-oriented Kruskal's with DisjointSetTree for cycle detection.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/minimum_spanning_tree_kruskal2.py
"""

import time


# ---------- Variant 1: Flat Union-Find (no OOP overhead) ----------
def kruskal_flat(connections: dict, start_node=None) -> dict:
    """
    Flat dictionary-based Kruskal's without class overhead.

    >>> g = {'A': {'B': 1, 'C': 10}, 'B': {'A': 1, 'C': 2, 'D': 100}, 'C': {'A': 10, 'B': 2, 'D': 1}, 'D': {'B': 100, 'C': 1}}
    >>> mst = kruskal_flat(g)
    >>> 'D' not in mst.get('B', {}) or mst['B']['D'] != 100
    True
    """
    # Extract edges
    edges = []
    seen = set()
    for u in connections:
        for v, w in connections[u].items():
            if (u, v) not in seen and (v, u) not in seen:
                edges.append((w, u, v))
                seen.add((u, v))
    edges.sort()

    parent = {}
    rank = {}

    def find(x):
        if x not in parent:
            parent[x] = x
            rank[x] = 0
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1
        return True

    result = {}
    for w, u, v in edges:
        if union(u, v):
            result.setdefault(u, {})[v] = w
            result.setdefault(v, {})[u] = w

    return result


# ---------- Variant 2: Returns total MST weight ----------
def kruskal_weight(connections: dict) -> int:
    """
    Returns just the total MST weight.

    >>> g = {'A': {'B': 1, 'C': 10}, 'B': {'A': 1, 'C': 2}, 'C': {'A': 10, 'B': 2}}
    >>> kruskal_weight(g)
    3
    """
    edges = []
    seen = set()
    for u in connections:
        for v, w in connections[u].items():
            if (u, v) not in seen and (v, u) not in seen:
                edges.append((w, u, v))
                seen.add((u, v))
    edges.sort()

    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = 0
    count = 0
    n = len(connections)
    for w, u, v in edges:
        if find(u) != find(v):
            parent[find(u)] = find(v)
            total += w
            count += 1
            if count == n - 1:
                break
    return total


# ---------- Variant 3: Generic type support with edge list ----------
def kruskal_generic(vertices: list, edges: list[tuple]) -> list[tuple]:
    """
    Kruskal's with any hashable vertex type.

    >>> kruskal_generic(['A', 'B', 'C'], [('A', 'B', 1), ('B', 'C', 2), ('A', 'C', 10)])
    [('A', 'B', 1), ('B', 'C', 2)]
    """
    parent = {v: v for v in vertices}
    rank = {v: 0 for v in vertices}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1
        return True

    sorted_edges = sorted(edges, key=lambda e: e[2])
    mst = []
    for u, v, w in sorted_edges:
        if union(u, v):
            mst.append((u, v, w))
            if len(mst) == len(vertices) - 1:
                break
    return mst


# ---------- Benchmark ----------
def benchmark():
    import random
    random.seed(42)
    n = 500
    nodes = [str(i) for i in range(n)]
    connections = {node: {} for node in nodes}
    for i in range(n - 1):
        w = random.randint(1, 1000)
        connections[str(i)][str(i + 1)] = w
        connections[str(i + 1)][str(i)] = w
    for _ in range(n):
        u, v = str(random.randint(0, n - 1)), str(random.randint(0, n - 1))
        if u != v:
            w = random.randint(1, 1000)
            connections[u][v] = w
            connections[v][u] = w

    for name, fn in [
        ("flat_dict", lambda: kruskal_flat(connections)),
        ("weight_only", lambda: kruskal_weight(connections)),
    ]:
        start = time.perf_counter()
        for _ in range(30):
            fn()
        elapsed = (time.perf_counter() - start) / 30 * 1000
        print(f"  {name:20s}: {elapsed:.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Kruskal2 MST Benchmark (500 nodes, 30 runs) ===")
    benchmark()
