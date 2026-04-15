"""
Boruvka's MST - Optimized Variants with Benchmarks.

Variant 1: Standard Boruvka's with Union-Find
Variant 2: Kruskal's (for comparison)
Variant 3: Prim's (for comparison)

>>> edges = [(0,1,10), (0,2,6), (0,3,5), (1,3,15), (2,3,4)]
>>> boruvka_standard(4, edges)
19
>>> kruskal(4, edges)
19
>>> prim(4, edges)
19
"""

import heapq
import time
from collections import defaultdict


class UF:
    def __init__(self, n):
        self.p = list(range(n))
        self.r = [0]*n
        self.c = n
    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]; x = self.p[x]
        return x
    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry: return False
        if self.r[rx] < self.r[ry]: rx, ry = ry, rx
        self.p[ry] = rx
        if self.r[rx] == self.r[ry]: self.r[rx] += 1
        self.c -= 1; return True


def boruvka_standard(n, edges):
    """Standard Boruvka's.

    >>> boruvka_standard(3, [(0,1,1),(1,2,2),(0,2,3)])
    3
    """
    uf = UF(n)
    total = 0
    while uf.c > 1:
        cheapest = {}
        for u, v, w in edges:
            ru, rv = uf.find(u), uf.find(v)
            if ru == rv: continue
            if ru not in cheapest or w < cheapest[ru][0]:
                cheapest[ru] = (w, u, v)
            if rv not in cheapest or w < cheapest[rv][0]:
                cheapest[rv] = (w, u, v)
        if not cheapest: break
        for _, (w, u, v) in cheapest.items():
            if uf.union(u, v): total += w
    return total


def kruskal(n, edges):
    """Kruskal's MST for comparison.

    >>> kruskal(3, [(0,1,1),(1,2,2),(0,2,3)])
    3
    """
    uf = UF(n)
    total = 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if uf.union(u, v): total += w
        if uf.c == 1: break
    return total


def prim(n, edges):
    """Prim's MST for comparison.

    >>> prim(3, [(0,1,1),(1,2,2),(0,2,3)])
    3
    """
    adj = defaultdict(list)
    for u, v, w in edges:
        adj[u].append((w, v))
        adj[v].append((w, u))
    visited = [False]*n
    visited[0] = True
    heap = list(adj[0])
    heapq.heapify(heap)
    total = 0
    count = 1
    while heap and count < n:
        w, u = heapq.heappop(heap)
        if visited[u]: continue
        visited[u] = True; total += w; count += 1
        for ww, v in adj[u]:
            if not visited[v]: heapq.heappush(heap, (ww, v))
    return total


def benchmark():
    import random
    random.seed(42)
    n = 5000
    edges = []
    for i in range(1, n):
        j = random.randint(0, i-1)
        edges.append((j, i, random.randint(1, 100)))
    for _ in range(n*3):
        u, v = random.randint(0, n-1), random.randint(0, n-1)
        if u != v: edges.append((u, v, random.randint(1, 100)))

    variants = [
        ("Boruvka's", lambda: boruvka_standard(n, edges)),
        ("Kruskal's", lambda: kruskal(n, edges)),
        ("Prim's", lambda: prim(n, edges)),
    ]
    print(f"\nBenchmark: MST on {n}-node, {len(edges)}-edge graph")
    print("-" * 50)
    for name, func in variants:
        t0 = time.perf_counter()
        for _ in range(3):
            result = func()
        elapsed = (time.perf_counter() - t0) / 3
        print(f"{name:<15} MST={result:<8} time={elapsed*1000:.1f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
