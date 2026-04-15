"""
Even Tree (HackerRank) - Maximum edges removable so every remaining
component has an even number of vertices.

Observation: root the tree at any node. For each subtree, if its size is even,
the edge connecting it to the parent can be removed. Answer = count of
subtrees (excluding the root) with even size.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/even_tree.py

>>> adj = {1: [2, 3], 2: [1, 6], 3: [1, 4], 4: [3, 5, 8], 5: [4],
...        6: [2, 7], 7: [6], 8: [4, 9, 10], 9: [8], 10: [8]}
>>> even_tree(adj, root=1)
2

>>> even_tree({1: [2], 2: [1]}, root=1)
0

>>> even_tree({1: []}, root=1)
0
"""


def even_tree(adj: dict, root: int = 1) -> int:
    """Return max number of edges to cut so every subtree has even size.

    >>> even_tree({1: [2, 3], 2: [1], 3: [1]}, 1)
    0
    """
    n = len(adj)
    if n % 2 == 1:
        # Total must be even for any valid removal; if odd, answer is 0
        return 0
    size: dict = {}
    removable = 0
    # Iterative DFS to avoid recursion limits on very deep trees
    order = []
    parent = {root: None}
    stack = [root]
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if v != parent[u]:
                parent[v] = u
                stack.append(v)
    # Post-order: process leaves first
    for u in reversed(order):
        s = 1
        for v in adj[u]:
            if v != parent[u]:
                s += size[v]
        size[u] = s
        if u != root and s % 2 == 0:
            removable += 1
    return removable


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    adj = {1: [2, 3], 2: [1, 6], 3: [1, 4], 4: [3, 5, 8], 5: [4],
           6: [2, 7], 7: [6], 8: [4, 9, 10], 9: [8], 10: [8]}
    print("Even tree removable edges:", even_tree(adj, 1))
