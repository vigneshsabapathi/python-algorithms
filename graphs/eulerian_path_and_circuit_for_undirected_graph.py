"""
Eulerian Path and Circuit detection (undirected graph).

- Eulerian **circuit**: visits every edge exactly once and returns to start.
  Exists iff graph is connected and every vertex has even degree.
- Eulerian **path**: visits every edge exactly once (doesn't need to return).
  Exists iff graph is connected and exactly 0 or 2 vertices have odd degree.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/eulerian_path_and_circuit_for_undirected_graph.py

>>> check({0: [1, 2], 1: [0, 2], 2: [0, 1, 3, 4], 3: [2, 4], 4: [2, 3]})
'Eulerian Circuit'
>>> check({0: [1], 1: [0, 2], 2: [1]})
'Eulerian Path'
>>> check({0: [1, 2], 1: [0, 2], 2: [0, 1], 3: [4], 4: [3]})
'Not Eulerian'
>>> check({})
'Not Eulerian'
"""


def _is_connected(graph: dict) -> bool:
    non_iso = [v for v in graph if graph[v]]
    if not non_iso:
        return True
    visited, stack = {non_iso[0]}, [non_iso[0]]
    while stack:
        u = stack.pop()
        for v in graph[u]:
            if v not in visited:
                visited.add(v)
                stack.append(v)
    return all(v in visited for v in non_iso)


def check(graph: dict) -> str:
    """Return one of: 'Eulerian Circuit', 'Eulerian Path', 'Not Eulerian'.

    >>> check({0: [1, 1], 1: [0, 0]})
    'Eulerian Circuit'
    """
    if not graph:
        return "Not Eulerian"
    if not _is_connected(graph):
        return "Not Eulerian"
    odd = sum(1 for v in graph if len(graph[v]) % 2 == 1)
    if odd == 0:
        return "Eulerian Circuit"
    if odd == 2:
        return "Eulerian Path"
    return "Not Eulerian"


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    g1 = {0: [1, 2], 1: [0, 2], 2: [0, 1, 3, 4], 3: [2, 4], 4: [2, 3]}
    g2 = {0: [1], 1: [0, 2], 2: [1]}
    g3 = {0: [1, 2], 1: [0, 2], 2: [0, 1], 3: [4], 4: [3]}
    for name, g in [("Circuit", g1), ("Path", g2), ("Disconnected", g3)]:
        print(f"{name}: {check(g)}")
