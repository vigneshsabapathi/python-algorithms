"""
Karger's Min-Cut Algorithm - Optimized Variants

Randomized algorithm for finding the minimum cut in an undirected graph by
randomly contracting edges until only 2 super-nodes remain.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/karger.py
"""

import random
import time
import math


# ---------- Variant 1: Repeated trials for high probability ----------
def karger_min_cut(graph: dict[str, list[str]], trials: int | None = None) -> set[tuple[str, str]]:
    """
    Run Karger's algorithm multiple times and return the smallest cut found.
    Default trials: n^2 * ln(n) for high probability of finding min cut.

    >>> random.seed(42)
    >>> g = {'0': ['1'], '1': ['0']}
    >>> karger_min_cut(g)
    {('0', '1')}
    """
    n = len(graph)
    if trials is None:
        trials = max(1, int(n * n * math.log(n + 1)))

    best_cut = None
    for _ in range(trials):
        cut = _single_karger(graph)
        if best_cut is None or len(cut) < len(best_cut):
            best_cut = cut
    return best_cut


def _single_karger(graph: dict[str, list[str]]) -> set[tuple[str, str]]:
    contracted = {node: {node} for node in graph}
    g = {node: graph[node][:] for node in graph}

    while len(g) > 2:
        u = random.choice(list(g.keys()))
        v = random.choice(g[u])
        uv = u + v
        uv_neighbors = list(set(g[u] + g[v]))
        if u in uv_neighbors:
            uv_neighbors.remove(u)
        if v in uv_neighbors:
            uv_neighbors.remove(v)
        g[uv] = uv_neighbors
        contracted[uv] = contracted[u] | contracted[v]

        del g[u]
        del g[v]
        for nbr in uv_neighbors:
            g[nbr] = [uv if x in (u, v) else x for x in g[nbr] if x not in (u, v) or True]
            g[nbr] = [uv if x == u or x == v else x for x in g[nbr]]

    groups = [contracted[node] for node in g]
    return {
        (node, nbr)
        for node in groups[0]
        for nbr in graph.get(node, [])
        if nbr in groups[1]
    }


# ---------- Variant 2: Union-Find based contraction ----------
def karger_union_find(n: int, edges: list[tuple[int, int]]) -> int:
    """
    Karger's using Union-Find for efficient contraction. Returns cut size.

    >>> random.seed(42)
    >>> karger_union_find(4, [(0, 1), (0, 2), (1, 2), (2, 3)])
    1
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

    best = len(edges)
    trials = max(1, n * n)
    for _ in range(trials):
        parent[:] = range(n)
        rank[:] = [0] * n
        components = n
        shuffled = edges[:]
        random.shuffle(shuffled)

        for u, v in shuffled:
            if components <= 2:
                break
            if find(u) != find(v):
                union(u, v)
                components -= 1

        cut = sum(1 for u, v in edges if find(u) != find(v))
        best = min(best, cut)
    return best


# ---------- Variant 3: Karger-Stein (recursive contraction) ----------
def karger_stein(graph: dict[str, list[str]]) -> set[tuple[str, str]]:
    """
    Karger-Stein algorithm: recursively contract to sqrt(n) then brute-force.
    Better probability than basic Karger.

    >>> random.seed(42)
    >>> g = {'0': ['1'], '1': ['0']}
    >>> karger_stein(g)
    {('0', '1')}
    """
    n = len(graph)
    if n <= 6:
        return karger_min_cut(graph, trials=max(10, n * n))

    # Contract to ceil(n/sqrt(2)) + 1
    target = int(n / math.sqrt(2)) + 1
    cut1 = _contract_to(graph, target)
    cut2 = _contract_to(graph, target)
    return cut1 if len(cut1) <= len(cut2) else cut2


def _contract_to(graph, target):
    contracted = {node: {node} for node in graph}
    g = {node: graph[node][:] for node in graph}
    while len(g) > target:
        u = random.choice(list(g.keys()))
        if not g[u]:
            continue
        v = random.choice(g[u])
        uv = u + v
        uv_neighbors = [x for x in set(g[u] + g[v]) if x not in (u, v)]
        g[uv] = uv_neighbors
        contracted[uv] = contracted[u] | contracted[v]
        del g[u], g[v]
        for nbr in uv_neighbors:
            g[nbr] = [uv if x in (u, v) else x for x in g[nbr]]
    if len(g) > 2:
        return _single_karger(g) if len(g) > 2 else set()
    groups = [contracted[node] for node in g]
    if len(groups) < 2:
        return set()
    return {
        (node, nbr)
        for node in groups[0]
        for nbr in graph.get(node, [])
        if nbr in groups[1]
    }


# ---------- Benchmark ----------
def benchmark():
    random.seed(42)
    graph = {
        str(i): [str(j) for j in range(10) if j != i and random.random() < 0.4]
        for i in range(10)
    }
    # Make undirected
    for u in list(graph):
        for v in graph[u]:
            if u not in graph[v]:
                graph[v].append(u)

    for name, fn in [
        ("basic_karger", lambda: karger_min_cut(graph, trials=50)),
        ("karger_stein", lambda: karger_stein(graph)),
    ]:
        start = time.perf_counter()
        for _ in range(10):
            result = fn()
        elapsed = (time.perf_counter() - start) / 10 * 1000
        print(f"  {name:20s}: {elapsed:.3f} ms (cut size: {len(result)})")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Karger's Min-Cut Benchmark (10 nodes, 10 runs) ===")
    benchmark()
