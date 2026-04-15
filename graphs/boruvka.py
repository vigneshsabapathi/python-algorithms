"""
Boruvka's Algorithm for Minimum Spanning Tree.

Each component finds its cheapest outgoing edge simultaneously, then merges.
Repeats until one component remains. Naturally parallelizable.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/boruvka.py

>>> edges = [(0,1,10), (0,2,6), (0,3,5), (1,3,15), (2,3,4)]
>>> mst_edges, total = boruvka(4, edges)
>>> total
19
>>> len(mst_edges)
3

>>> boruvka(1, [])
([], 0)
"""


class UnionFind:
    """
    Disjoint Set Union with path compression and union by rank.

    >>> uf = UnionFind(5)
    >>> uf.union(0, 1)
    True
    >>> uf.find(0) == uf.find(1)
    True
    >>> uf.union(0, 1)
    False
    """

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path compression
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.components -= 1
        return True


def boruvka(
    num_vertices: int,
    edges: list[tuple[int, int, float]],
) -> tuple[list[tuple[int, int, float]], float]:
    """
    Boruvka's MST algorithm.

    Args:
        num_vertices: number of vertices
        edges: list of (u, v, weight) tuples

    Returns:
        (mst_edges, total_weight)

    >>> boruvka(4, [(0,1,1),(1,2,2),(2,3,3),(0,3,4)])
    ([(0, 1, 1), (1, 2, 2), (2, 3, 3)], 6)
    """
    if num_vertices <= 1:
        return [], 0

    uf = UnionFind(num_vertices)
    mst_edges: list[tuple[int, int, float]] = []
    total_weight = 0

    while uf.components > 1:
        # Find cheapest edge for each component
        cheapest: dict[int, tuple[float, int, int]] = {}

        for u, v, w in edges:
            ru, rv = uf.find(u), uf.find(v)
            if ru == rv:
                continue
            if ru not in cheapest or w < cheapest[ru][0]:
                cheapest[ru] = (w, u, v)
            if rv not in cheapest or w < cheapest[rv][0]:
                cheapest[rv] = (w, u, v)

        if not cheapest:
            break  # Disconnected graph

        added = False
        for _, (w, u, v) in cheapest.items():
            if uf.union(u, v):
                mst_edges.append((u, v, w))
                total_weight += w
                added = True

        if not added:
            break

    mst_edges.sort(key=lambda e: e[2])
    return mst_edges, total_weight


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    edges = [
        (0, 1, 10), (0, 2, 6), (0, 3, 5),
        (1, 3, 15), (2, 3, 4),
    ]
    mst, weight = boruvka(4, edges)
    print(f"MST edges: {mst}")
    print(f"Total weight: {weight}")
