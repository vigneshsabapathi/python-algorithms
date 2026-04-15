"""
Kruskal's MST Algorithm - Optimized Variants

Finds MST by sorting edges by weight and greedily adding edges that don't form cycles.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/minimum_spanning_tree_kruskal.py
"""

import time


# ---------- Variant 1: Union-Find with path compression + union by rank ----------
def kruskal_optimized(n: int, edges: list[tuple[int, int, int]]) -> tuple[list[tuple[int, int, int]], int]:
    """
    Kruskal's with optimized Union-Find. Returns MST edges and total weight.

    >>> edges, weight = kruskal_optimized(4, [(0, 1, 3), (1, 2, 5), (2, 3, 1)])
    >>> weight
    9
    >>> edges
    [(2, 3, 1), (0, 1, 3), (1, 2, 5)]
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

    sorted_edges = sorted(edges, key=lambda e: e[2])
    mst = []
    total = 0

    for u, v, w in sorted_edges:
        if union(u, v):
            mst.append((u, v, w))
            total += w
            if len(mst) == n - 1:
                break

    return mst, total


# ---------- Variant 2: Returns MST as adjacency list ----------
def kruskal_adj_list(n: int, edges: list[tuple[int, int, int]]) -> dict[int, list[tuple[int, int]]]:
    """
    Kruskal's returning MST as adjacency list with weights.

    >>> mst = kruskal_adj_list(3, [(0, 1, 2), (1, 2, 3), (0, 2, 5)])
    >>> sorted(mst[0])
    [(1, 2)]
    """
    mst_edges, _ = kruskal_optimized(n, edges)
    adj = {i: [] for i in range(n)}
    for u, v, w in mst_edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj


# ---------- Variant 3: Counting sort for integer weights ----------
def kruskal_counting_sort(n: int, edges: list[tuple[int, int, int]], max_weight: int) -> list[tuple[int, int, int]]:
    """
    Kruskal's with counting sort for O(E + W) sorting when weights are small integers.

    >>> kruskal_counting_sort(4, [(0, 1, 3), (1, 2, 5), (2, 3, 1), (0, 2, 1)], 5)
    [(2, 3, 1), (0, 2, 1), (0, 1, 3)]
    """
    buckets = [[] for _ in range(max_weight + 1)]
    for edge in edges:
        buckets[edge[2]].append(edge)

    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    mst = []
    for w in range(max_weight + 1):
        for u, v, weight in buckets[w]:
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[ru] = rv
                mst.append((u, v, weight))
                if len(mst) == n - 1:
                    return mst
    return mst


# ---------- Benchmark ----------
def benchmark():
    import random
    random.seed(42)
    n = 1000
    edges = []
    for i in range(n - 1):
        edges.append((i, i + 1, random.randint(1, 100)))
    for _ in range(n * 2):
        u, v = random.randint(0, n - 1), random.randint(0, n - 1)
        if u != v:
            edges.append((u, v, random.randint(1, 100)))

    for name, fn in [
        ("optimized_uf", lambda: kruskal_optimized(n, edges)),
        ("counting_sort", lambda: kruskal_counting_sort(n, edges, 100)),
    ]:
        start = time.perf_counter()
        for _ in range(50):
            fn()
        elapsed = (time.perf_counter() - start) / 50 * 1000
        print(f"  {name:20s}: {elapsed:.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Kruskal MST Benchmark (1000 nodes, 50 runs) ===")
    benchmark()
