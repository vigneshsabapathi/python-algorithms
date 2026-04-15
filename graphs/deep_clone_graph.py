"""
Deep Clone Graph (LeetCode 133).

Given a reference to a node in an undirected connected graph, return a deep
copy (clone) of the graph. Each node has an integer val and a list of neighbors.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/deep_clone_graph.py

>>> n1 = Node(1); n2 = Node(2); n3 = Node(3); n4 = Node(4)
>>> n1.neighbors = [n2, n4]
>>> n2.neighbors = [n1, n3]
>>> n3.neighbors = [n2, n4]
>>> n4.neighbors = [n1, n3]
>>> c = clone_graph(n1)
>>> c is not n1
True
>>> c.val
1
>>> sorted(nb.val for nb in c.neighbors)
[2, 4]
>>> clone_graph(None) is None
True
"""


class Node:
    """Graph node with integer value and neighbor list.

    >>> Node(5).val
    5
    """

    def __init__(self, val: int = 0, neighbors: list | None = None) -> None:
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def clone_graph(node: Node | None) -> Node | None:
    """DFS clone. Returns root of deep copy, or None.

    >>> clone_graph(None) is None
    True
    """
    if node is None:
        return None
    mapping: dict = {}

    def dfs(orig: Node) -> Node:
        if orig in mapping:
            return mapping[orig]
        copy = Node(orig.val)
        mapping[orig] = copy
        copy.neighbors = [dfs(nb) for nb in orig.neighbors]
        return copy

    return dfs(node)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    n1 = Node(1); n2 = Node(2); n3 = Node(3); n4 = Node(4)
    n1.neighbors = [n2, n4]; n2.neighbors = [n1, n3]
    n3.neighbors = [n2, n4]; n4.neighbors = [n1, n3]
    c = clone_graph(n1)
    print("Clone root val:", c.val, "-- neighbor vals:", sorted(nb.val for nb in c.neighbors))
    print("Is deep copy:", c is not n1 and c.neighbors[0] is not n2)
