"""
Graph Adjacency Matrix - Optimized Variants

Unweighted graph using adjacency matrix representation with O(1) edge operations.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/graph_adjacency_matrix.py
"""

import time


# ---------- Variant 1: NumPy-based matrix (vectorized operations) ----------
def create_numpy_graph(n: int):
    """
    Create a graph backed by a NumPy array for fast batch operations.

    >>> import numpy as np
    >>> mat = create_numpy_graph(3)
    >>> mat.shape
    (3, 3)
    """
    import numpy as np
    return np.zeros((n, n), dtype=int)


def add_edge_numpy(matrix, u: int, v: int, directed: bool = True):
    """
    >>> import numpy as np
    >>> m = create_numpy_graph(3)
    >>> add_edge_numpy(m, 0, 1, directed=False)
    >>> m[0][1] == 1 and m[1][0] == 1
    True
    """
    matrix[u][v] = 1
    if not directed:
        matrix[v][u] = 1


# ---------- Variant 2: Bitset-based matrix (memory efficient) ----------
class GraphBitMatrix:
    """
    Graph using integer bitsets for ultra-compact adjacency matrix.

    >>> g = GraphBitMatrix(4)
    >>> g.add_edge(0, 1)
    >>> g.has_edge(0, 1)
    True
    >>> g.has_edge(1, 0)
    False
    >>> g.add_edge(1, 0)
    >>> g.has_edge(1, 0)
    True
    """

    def __init__(self, n: int):
        self.n = n
        self.rows = [0] * n  # each row is an integer bitmask

    def add_edge(self, u: int, v: int):
        self.rows[u] |= (1 << v)

    def remove_edge(self, u: int, v: int):
        self.rows[u] &= ~(1 << v)

    def has_edge(self, u: int, v: int) -> bool:
        return bool(self.rows[u] & (1 << v))

    def neighbors(self, u: int) -> list[int]:
        result = []
        bits = self.rows[u]
        v = 0
        while bits:
            if bits & 1:
                result.append(v)
            bits >>= 1
            v += 1
        return result


# ---------- Variant 3: Dict-indexed matrix (supports non-integer vertices) ----------
class GraphDictMatrix:
    """
    Adjacency matrix with dict-based vertex indexing.

    >>> g = GraphDictMatrix(directed=False)
    >>> g.add_vertex('A')
    >>> g.add_vertex('B')
    >>> g.add_edge('A', 'B')
    >>> g.has_edge('A', 'B')
    True
    >>> g.has_edge('B', 'A')
    True
    """

    def __init__(self, directed: bool = True):
        self.vertex_to_idx: dict = {}
        self.matrix: list[list[int]] = []
        self.directed = directed

    def add_vertex(self, v):
        if v in self.vertex_to_idx:
            return
        idx = len(self.matrix)
        self.vertex_to_idx[v] = idx
        for row in self.matrix:
            row.append(0)
        self.matrix.append([0] * (idx + 1))

    def add_edge(self, u, v):
        i, j = self.vertex_to_idx[u], self.vertex_to_idx[v]
        self.matrix[i][j] = 1
        if not self.directed:
            self.matrix[j][i] = 1

    def has_edge(self, u, v) -> bool:
        i, j = self.vertex_to_idx[u], self.vertex_to_idx[v]
        return self.matrix[i][j] == 1


# ---------- Benchmark ----------
def benchmark():
    n = 300
    edges = [(i, (i + 1) % n) for i in range(n)]

    # Bitset
    start = time.perf_counter()
    for _ in range(100):
        g = GraphBitMatrix(n)
        for u, v in edges:
            g.add_edge(u, v)
        for u, v in edges:
            g.has_edge(u, v)
    elapsed = (time.perf_counter() - start) / 100 * 1000
    print(f"  {'bitset_matrix':20s}: {elapsed:.3f} ms")

    # Dict matrix
    start = time.perf_counter()
    for _ in range(100):
        g = GraphDictMatrix()
        for i in range(n):
            g.add_vertex(i)
        for u, v in edges:
            g.add_edge(u, v)
        for u, v in edges:
            g.has_edge(u, v)
    elapsed = (time.perf_counter() - start) / 100 * 1000
    print(f"  {'dict_matrix':20s}: {elapsed:.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Graph Adjacency Matrix Benchmark (300 nodes, 100 runs) ===")
    benchmark()
