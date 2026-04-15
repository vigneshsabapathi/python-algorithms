"""
Check Cycle - Detect a cycle in a directed graph.

Uses DFS with three colors (WHITE/GRAY/BLACK) or an in-stack flag to find a
back edge, which indicates a cycle.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/check_cycle.py

>>> has_cycle({0: [1], 1: [2], 2: [0]})
True
>>> has_cycle({0: [1], 1: [2], 2: []})
False
>>> has_cycle({})
False
>>> has_cycle({0: [0]})
True
"""


def has_cycle(graph: dict) -> bool:
    """Return True iff directed graph contains a cycle.

    >>> has_cycle({1: [2], 2: [3], 3: []})
    False
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in graph}
    # Also include neighbors not listed as keys
    for neighbors in list(graph.values()):
        for n in neighbors:
            color.setdefault(n, WHITE)

    def dfs(u: int) -> bool:
        color[u] = GRAY
        for v in graph.get(u, []):
            if color[v] == GRAY:
                return True
            if color[v] == WHITE and dfs(v):
                return True
        color[u] = BLACK
        return False

    for node in list(color):
        if color[node] == WHITE and dfs(node):
            return True
    return False


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Has cycle A->B->C->A?", has_cycle({0: [1], 1: [2], 2: [0]}))
    print("Has cycle A->B->C?", has_cycle({0: [1], 1: [2], 2: []}))
    print("Self-loop?", has_cycle({0: [0]}))
