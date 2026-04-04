"""Topological Sort — DFS-based recursive implementation.

Topological sort produces a linear ordering of vertices in a Directed Acyclic
Graph (DAG) such that for every directed edge u → v, vertex u appears before v
in the ordering.

This implementation uses DFS post-order: we fully explore all descendants of a
vertex before recording it.  Because DFS post-order naturally lists leaves
first and roots last we reverse the accumulated list before returning, which
gives the conventional topological order (roots / sources first).

Reference: https://en.wikipedia.org/wiki/Topological_sorting

Graph used in examples:
         a
        / \\
       b   c
      / \\
     d   e

    Edges: a → c, a → b, b → d, b → e

Examples:
    >>> edges = {"a": ["c", "b"], "b": ["d", "e"], "c": [], "d": [], "e": []}
    >>> vertices = ["a", "b", "c", "d", "e"]
    >>> result = topological_sort("a", [], [], edges, vertices)
    >>> result[0]
    'a'
    >>> result.index("a") < result.index("b")  # a before b
    True
    >>> result.index("a") < result.index("c")  # a before c
    True
    >>> result.index("b") < result.index("d")  # b before d
    True
    >>> result.index("b") < result.index("e")  # b before e
    True

    Single node:
    >>> topological_sort("x", [], [], {"x": []}, ["x"])
    ['x']

    Linear chain a → b → c:
    >>> edges2 = {"a": ["b"], "b": ["c"], "c": []}
    >>> vertices2 = ["a", "b", "c"]
    >>> res = topological_sort("a", [], [], edges2, vertices2)
    >>> res.index("a") < res.index("b") < res.index("c")
    True
"""


def _dfs(
    start: str,
    visited: list[str],
    post_order: list[str],
    edges: dict[str, list[str]],
    vertices: list[str],
) -> list[str]:
    """Internal DFS that accumulates nodes in post-order (leaves before roots)."""
    visited.append(start)
    for neighbor in edges[start]:
        if neighbor not in visited:
            _dfs(neighbor, visited, post_order, edges, vertices)
    post_order.append(start)
    # If disconnected vertices remain, continue from an unvisited one
    if len(visited) != len(vertices):
        for vertex in vertices:
            if vertex not in visited:
                _dfs(vertex, visited, post_order, edges, vertices)
    return post_order


def topological_sort(
    start: str,
    visited: list[str],
    sort: list[str],
    edges: dict[str, list[str]],
    vertices: list[str],
) -> list[str]:
    """Return vertices of a DAG in topological order (sources / roots first).

    Uses DFS post-order internally, then reverses the result so that for every
    directed edge u → v, u appears before v in the returned list.

    Args:
        start:    Starting vertex for the DFS.
        visited:  Accumulator for visited vertices (pass in an empty list).
        sort:     Unused accumulator kept for API compatibility (pass ``[]``).
        edges:    Adjacency list: vertex → list of successor vertices.
        vertices: All vertices in the graph.

    Returns:
        Vertices in topological order.

    Raises:
        KeyError: If a vertex in ``edges`` values is not a key in ``edges``.

    Examples:
        >>> edges = {"a": ["c", "b"], "b": ["d", "e"], "c": [], "d": [], "e": []}
        >>> vertices = ["a", "b", "c", "d", "e"]
        >>> result = topological_sort("a", [], [], edges, vertices)
        >>> result.index("a") < result.index("b")
        True
        >>> result.index("b") < result.index("d")
        True
    """
    post_order: list[str] = []
    _dfs(start, visited, post_order, edges, vertices)
    return post_order[::-1]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    #     a
    #    / \
    #   b   c
    #  / \
    # d   e
    edges: dict[str, list[str]] = {
        "a": ["c", "b"],
        "b": ["d", "e"],
        "c": [],
        "d": [],
        "e": [],
    }
    vertices: list[str] = ["a", "b", "c", "d", "e"]

    result = topological_sort("a", [], [], edges, vertices)
    print("Topological order:", result)
