"""
Graph Adjacency List - Optimized Variants

Robust unweighted graph data structure using adjacency lists. Supports
directed and undirected graphs with generic vertex types.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/graph_adjacency_list.py
"""

import time
from collections import defaultdict


# ---------- Variant 1: DefaultDict-based (simpler, auto-creates vertices) ----------
class GraphDefaultDict:
    """
    Graph using defaultdict for automatic vertex creation.

    >>> g = GraphDefaultDict(directed=False)
    >>> g.add_edge(0, 1)
    >>> g.add_edge(1, 2)
    >>> g.has_edge(0, 1)
    True
    >>> g.has_edge(2, 1)
    True
    >>> g.remove_edge(0, 1)
    >>> g.has_edge(0, 1)
    False
    """

    def __init__(self, directed: bool = True):
        self.adj: dict[int, set[int]] = defaultdict(set)
        self.directed = directed

    def add_edge(self, u, v):
        self.adj[u].add(v)
        self.adj[v]  # ensure vertex exists
        if not self.directed:
            self.adj[v].add(u)

    def remove_edge(self, u, v):
        self.adj[u].discard(v)
        if not self.directed:
            self.adj[v].discard(u)

    def has_edge(self, u, v) -> bool:
        return v in self.adj[u]

    def vertices(self) -> list:
        return list(self.adj.keys())

    def neighbors(self, u) -> set:
        return self.adj[u]


# ---------- Variant 2: Set-based adjacency (O(1) edge lookups) ----------
class GraphSetAdjacency:
    """
    Graph using sets for O(1) edge membership checks.

    >>> g = GraphSetAdjacency()
    >>> g.add_vertex('A')
    >>> g.add_vertex('B')
    >>> g.add_edge('A', 'B')
    >>> g.has_edge('A', 'B')
    True
    >>> g.remove_vertex('B')
    >>> g.has_vertex('B')
    False
    """

    def __init__(self, directed: bool = True):
        self.adj: dict = {}
        self.directed = directed

    def add_vertex(self, v):
        if v not in self.adj:
            self.adj[v] = set()

    def add_edge(self, u, v):
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].add(v)
        if not self.directed:
            self.adj[v].add(u)

    def remove_vertex(self, v):
        if v in self.adj:
            del self.adj[v]
            for neighbors in self.adj.values():
                neighbors.discard(v)

    def remove_edge(self, u, v):
        if u in self.adj:
            self.adj[u].discard(v)
        if not self.directed and v in self.adj:
            self.adj[v].discard(u)

    def has_vertex(self, v) -> bool:
        return v in self.adj

    def has_edge(self, u, v) -> bool:
        return u in self.adj and v in self.adj[u]


# ---------- Variant 3: Compact list-based with validation ----------
class GraphListAdjacency:
    """
    List-based adjacency with full validation (mirrors original).

    >>> g = GraphListAdjacency(directed=False)
    >>> g.add_vertex(1)
    >>> g.add_vertex(2)
    >>> g.add_edge(1, 2)
    >>> 2 in g.adj_list[1]
    True
    >>> 1 in g.adj_list[2]
    True
    """

    def __init__(self, directed: bool = True):
        self.adj_list: dict = {}
        self.directed = directed

    def add_vertex(self, v):
        if v in self.adj_list:
            raise ValueError(f"{v} already in graph")
        self.adj_list[v] = []

    def add_edge(self, u, v):
        if u not in self.adj_list or v not in self.adj_list:
            raise ValueError(f"Vertex {u} or {v} not in graph")
        self.adj_list[u].append(v)
        if not self.directed:
            self.adj_list[v].append(u)

    def remove_vertex(self, v):
        if v not in self.adj_list:
            raise ValueError(f"{v} not in graph")
        del self.adj_list[v]
        for neighbors in self.adj_list.values():
            while v in neighbors:
                neighbors.remove(v)

    def has_edge(self, u, v) -> bool:
        return u in self.adj_list and v in self.adj_list[u]


# ---------- Benchmark ----------
def benchmark():
    n = 500
    edges = [(i, i + 1) for i in range(n - 1)] + [(0, n - 1)]

    for name, GraphClass in [
        ("defaultdict_set", GraphDefaultDict),
        ("set_adjacency", GraphSetAdjacency),
        ("list_adjacency", GraphListAdjacency),
    ]:
        start = time.perf_counter()
        for _ in range(50):
            g = GraphClass(directed=False)
            if name == "list_adjacency":
                for i in range(n):
                    g.add_vertex(i)
            for u, v in edges:
                g.add_edge(u, v)
            # Check all edges
            for u, v in edges:
                g.has_edge(u, v)
        elapsed = (time.perf_counter() - start) / 50 * 1000
        print(f"  {name:20s}: {elapsed:.3f} ms ({n} vertices, {len(edges)} edges)")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Graph Adjacency List Benchmark (500 nodes, 50 runs) ===")
    benchmark()
