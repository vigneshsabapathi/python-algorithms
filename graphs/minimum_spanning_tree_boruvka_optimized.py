"""
Boruvka's MST Algorithm - Optimized Variants

Boruvka's finds MST by repeatedly adding the cheapest edge from each component
to another component. Requires distinct weights.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/minimum_spanning_tree_boruvka.py
"""

import time


# ---------- Variant 1: Union-Find based Boruvka (clean implementation) ----------
def boruvka_union_find(n: int, edges: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    """
    Boruvka's MST using Union-Find with path compression and union by rank.

    >>> boruvka_union_find(4, [(0, 1, 1), (0, 2, 2), (2, 3, 3), (1, 3, 4)])
    [(0, 1, 1), (0, 2, 2), (2, 3, 3)]
    """
    parent = list(range(n))
    rank = [0] * n

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

    mst = []
    components = n

    while components > 1:
        cheapest = [-1] * n
        for i, (u, v, w) in enumerate(edges):
            ru, rv = find(u), find(v)
            if ru != rv:
                if cheapest[ru] == -1 or edges[cheapest[ru]][2] > w:
                    cheapest[ru] = i
                if cheapest[rv] == -1 or edges[cheapest[rv]][2] > w:
                    cheapest[rv] = i

        for i in range(n):
            if cheapest[i] != -1:
                u, v, w = edges[cheapest[i]]
                if find(u) != find(v):
                    union(u, v)
                    mst.append((u, v, w))
                    components -= 1

    return mst


# ---------- Variant 2: Edge-list based with sorting ----------
def boruvka_sorted(n: int, edges: list[tuple[int, int, int]]) -> tuple[list[tuple[int, int, int]], int]:
    """
    Boruvka's returning MST edges and total weight.

    >>> edges, weight = boruvka_sorted(4, [(0, 1, 1), (0, 2, 2), (2, 3, 3), (1, 3, 4)])
    >>> weight
    6
    """
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        parent[ra] = rb
        return True

    sorted_edges = sorted(edges, key=lambda e: e[2])
    mst = []
    total = 0
    components = n

    while components > 1:
        cheapest = {}
        for u, v, w in sorted_edges:
            ru, rv = find(u), find(v)
            if ru != rv:
                if ru not in cheapest or cheapest[ru][2] > w:
                    cheapest[ru] = (u, v, w)
                if rv not in cheapest or cheapest[rv][2] > w:
                    cheapest[rv] = (u, v, w)

        if not cheapest:
            break

        for u, v, w in cheapest.values():
            if union(u, v):
                mst.append((u, v, w))
                total += w
                components -= 1

    return mst, total


# ---------- Variant 3: Adjacency list based ----------
def boruvka_adj_list(graph: dict[int, dict[int, int]]) -> list[tuple[int, int, int]]:
    """
    Boruvka's with adjacency list input.

    >>> g = {0: {1: 1, 2: 2}, 1: {0: 1, 3: 4}, 2: {0: 2, 3: 3}, 3: {1: 4, 2: 3}}
    >>> boruvka_adj_list(g)
    [(0, 1, 1), (0, 2, 2), (2, 3, 3)]
    """
    vertices = list(graph.keys())
    edges = []
    seen = set()
    for u in graph:
        for v, w in graph[u].items():
            if (min(u, v), max(u, v)) not in seen:
                seen.add((min(u, v), max(u, v)))
                edges.append((u, v, w))

    n = max(vertices) + 1
    return boruvka_union_find(n, edges)


# ---------- Benchmark ----------
def benchmark():
    import random
    random.seed(42)
    n = 500
    edges = []
    for i in range(n - 1):
        edges.append((i, i + 1, random.randint(1, 1000)))
    for _ in range(n):
        u, v = random.randint(0, n - 1), random.randint(0, n - 1)
        if u != v:
            edges.append((u, v, random.randint(1, 1000)))

    for name, fn in [
        ("union_find", lambda: boruvka_union_find(n, edges)),
        ("sorted_edges", lambda: boruvka_sorted(n, edges)),
    ]:
        start = time.perf_counter()
        for _ in range(20):
            fn()
        elapsed = (time.perf_counter() - start) / 20 * 1000
        print(f"  {name:20s}: {elapsed:.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Boruvka MST Benchmark (500 nodes, 20 runs) ===")
    benchmark()
