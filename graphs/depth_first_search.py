"""
Depth-First Search (DFS) on a graph.

DFS explores as far as possible along each branch before backtracking. It uses
a stack (implicit via recursion, or explicit). Good for path existence, cycle
detection, topological sort, and connected components.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/depth_first_search.py

>>> g = {'A': ['B', 'C'], 'B': ['D', 'E'], 'C': ['F'], 'D': [], 'E': ['F'], 'F': []}
>>> dfs_recursive(g, 'A')
['A', 'B', 'D', 'E', 'F', 'C']

>>> dfs_iterative({0: [1], 1: [0, 2], 2: [1]}, 0)
[0, 1, 2]

>>> dfs_recursive({}, 'X')
['X']
"""


def dfs_recursive(graph: dict, start, visited: set | None = None, order: list | None = None) -> list:
    """Recursive DFS.

    >>> dfs_recursive({1: [2], 2: []}, 1)
    [1, 2]
    """
    if visited is None:
        visited = set()
    if order is None:
        order = []
    visited.add(start)
    order.append(start)
    for nb in graph.get(start, []):
        if nb not in visited:
            dfs_recursive(graph, nb, visited, order)
    return order


def dfs_iterative(graph: dict, start) -> list:
    """Iterative DFS using a stack. Produces same order as recursive when neighbors are reversed.

    >>> dfs_iterative({1: [2], 2: []}, 1)
    [1, 2]
    """
    visited = {start}
    order = [start]
    stack = [iter(graph.get(start, []))]
    path = [start]
    while stack:
        try:
            nb = next(stack[-1])
            if nb not in visited:
                visited.add(nb)
                order.append(nb)
                path.append(nb)
                stack.append(iter(graph.get(nb, [])))
        except StopIteration:
            stack.pop()
            path.pop()
    return order


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    g = {'A': ['B', 'C'], 'B': ['D', 'E'], 'C': ['F'], 'D': [], 'E': ['F'], 'F': []}
    print("DFS recursive from A:", dfs_recursive(g, 'A'))
    print("DFS iterative from A:", dfs_iterative(g, 'A'))
