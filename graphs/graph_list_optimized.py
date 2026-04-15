"""
Graph List (Adjacency List with chaining) - Optimized Variants

Simple adjacency list graph with directed/undirected support and method chaining.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/graph_list.py
"""

import time
from collections import defaultdict
from pprint import pformat


# ---------- Variant 1: Chainable with set-based adjacency ----------
class GraphChainSet:
    """
    Chainable graph API with set-based adjacency for O(1) lookups.

    >>> g = GraphChainSet(directed=False)
    >>> g.add_edge(0, 1).add_edge(1, 2)
    {0: {1}, 1: {0, 2}, 2: {1}}
    >>> g.has_edge(0, 1)
    True
    """

    def __init__(self, directed: bool = True):
        self.adj: dict[int, set[int]] = defaultdict(set)
        self.directed = directed

    def add_edge(self, u, v):
        self.adj[u].add(v)
        if u not in self.adj:
            self.adj[u] = set()
        if self.directed:
            if v not in self.adj:
                self.adj[v] = set()
        else:
            self.adj[v].add(u)
        return self

    def has_edge(self, u, v) -> bool:
        return v in self.adj.get(u, set())

    def __repr__(self):
        return pformat(dict(self.adj))


# ---------- Variant 2: Edge-list based construction ----------
class GraphFromEdges:
    """
    Build graph from edge list in one shot.

    >>> g = GraphFromEdges([(0, 1), (1, 2), (2, 0)], directed=True)
    >>> sorted(g.adj.keys())
    [0, 1, 2]
    >>> 1 in g.adj[0]
    True
    """

    def __init__(self, edges: list[tuple], directed: bool = True):
        self.adj: dict = defaultdict(list)
        self.directed = directed
        for u, v in edges:
            self.adj[u].append(v)
            if not directed:
                self.adj[v].append(u)
            elif v not in self.adj:
                self.adj[v] = []


# ---------- Variant 3: Weighted adjacency list ----------
class WeightedGraphList:
    """
    Adjacency list with edge weights.

    >>> g = WeightedGraphList(directed=False)
    >>> g.add_edge('A', 'B', 5).add_edge('B', 'C', 3)
    WeightedGraphList(3 vertices)
    >>> g.weight('A', 'B')
    5
    """

    def __init__(self, directed: bool = True):
        self.adj: dict = defaultdict(dict)
        self.directed = directed

    def add_edge(self, u, v, weight=1):
        self.adj[u][v] = weight
        if not self.directed:
            self.adj[v][u] = weight
        else:
            if v not in self.adj:
                self.adj[v] = {}
        return self

    def weight(self, u, v):
        return self.adj[u].get(v, float('inf'))

    def __repr__(self):
        return f"WeightedGraphList({len(self.adj)} vertices)"


# ---------- Benchmark ----------
def benchmark():
    n = 1000
    edges = [(i, (i + 1) % n) for i in range(n)]

    for name, build_fn in [
        ("chain_set", lambda: GraphChainSet(False)),
        ("from_edges", lambda: None),
        ("weighted", lambda: WeightedGraphList(False)),
    ]:
        start = time.perf_counter()
        for _ in range(100):
            if name == "from_edges":
                GraphFromEdges(edges, directed=False)
            else:
                g = build_fn()
                for u, v in edges:
                    g.add_edge(u, v)
        elapsed = (time.perf_counter() - start) / 100 * 1000
        print(f"  {name:20s}: {elapsed:.3f} ms ({n} edges)")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Graph List Benchmark (1000 edges, 100 runs) ===")
    benchmark()
