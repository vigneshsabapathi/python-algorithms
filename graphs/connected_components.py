"""
Connected Components in an undirected graph.

Finds all maximal connected subgraphs. DFS/BFS from every unvisited node;
each traversal enumerates one component.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/connected_components.py

>>> g = {0: [1], 1: [0, 2], 2: [1], 3: [4], 4: [3], 5: []}
>>> sorted(map(sorted, connected_components(g)))
[[0, 1, 2], [3, 4], [5]]

>>> connected_components({})
[]
"""


def connected_components(graph: dict) -> list:
    """Return list of components as lists of nodes.

    >>> sorted(map(sorted, connected_components({0: [1], 1: [0]})))
    [[0, 1]]
    """
    visited: set = set()
    components = []
    for start in graph:
        if start in visited:
            continue
        stack = [start]
        visited.add(start)
        comp = []
        while stack:
            node = stack.pop()
            comp.append(node)
            for nb in graph[node]:
                if nb not in visited:
                    visited.add(nb)
                    stack.append(nb)
        components.append(comp)
    return components


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    g = {0: [1], 1: [0, 2], 2: [1], 3: [4], 4: [3], 5: []}
    print("Components:", sorted(map(sorted, connected_components(g))))
