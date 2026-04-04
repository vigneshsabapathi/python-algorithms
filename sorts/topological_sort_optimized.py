"""Topological Sort — optimized and alternative implementations.

Four approaches compared:
  1. Recursive DFS post-order (original, O(V+E) time, O(V) stack space)
  2. Iterative DFS post-order — avoids Python recursion limit, same complexity
  3. Kahn's algorithm — BFS / in-degree drain, also detects cycles
  4. graphlib.TopologicalSorter — Python 3.9+ stdlib, C-backed, fastest in practice

All produce a valid topological order; the exact sequence may differ between
approaches when multiple valid orderings exist.

References:
  Kahn's algorithm: https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm
  graphlib: https://docs.python.org/3/library/graphlib.html
"""

from __future__ import annotations

from collections import deque
from graphlib import CycleError, TopologicalSorter


# ---------------------------------------------------------------------------
# Approach 1: Recursive DFS (baseline — see topological_sort.py)
# ---------------------------------------------------------------------------

def topological_sort_recursive(
    edges: dict[str, list[str]],
    vertices: list[str],
) -> list[str]:
    """Recursive DFS post-order, then reversed.

    Space: O(V) call stack.  May hit RecursionError on large graphs.

    Examples:
        >>> edges = {"a": ["c", "b"], "b": ["d", "e"], "c": [], "d": [], "e": []}
        >>> vertices = ["a", "b", "c", "d", "e"]
        >>> result = topological_sort_recursive(edges, vertices)
        >>> result.index("a") < result.index("b")
        True
        >>> result.index("b") < result.index("d")
        True
        >>> result[0]
        'a'
    """
    visited: set[str] = set()
    post_order: list[str] = []

    def dfs(v: str) -> None:
        visited.add(v)
        for neighbor in edges[v]:
            if neighbor not in visited:
                dfs(neighbor)
        post_order.append(v)

    for v in vertices:
        if v not in visited:
            dfs(v)

    return post_order[::-1]


# ---------------------------------------------------------------------------
# Approach 2: Iterative DFS post-order
# ---------------------------------------------------------------------------

def topological_sort_iterative(
    edges: dict[str, list[str]],
    vertices: list[str],
) -> list[str]:
    """Iterative DFS using an explicit stack — no recursion limit risk.

    Uses a two-pass stack entry: the first time a vertex is popped we push it
    again (as a "commit" marker) and push all unvisited neighbours.  The second
    time it is popped (all neighbours done) we append it to post_order.

    Time: O(V + E).  Space: O(V) stack.

    Examples:
        >>> edges = {"a": ["c", "b"], "b": ["d", "e"], "c": [], "d": [], "e": []}
        >>> vertices = ["a", "b", "c", "d", "e"]
        >>> result = topological_sort_iterative(edges, vertices)
        >>> result.index("a") < result.index("b")
        True
        >>> result.index("b") < result.index("d")
        True
        >>> result[0]
        'a'
    """
    visited: set[str] = set()
    post_order: list[str] = []

    for start in vertices:
        if start in visited:
            continue
        stack: list[tuple[str, bool]] = [(start, False)]
        while stack:
            v, committed = stack.pop()
            if committed:
                post_order.append(v)
                continue
            if v in visited:
                continue
            visited.add(v)
            stack.append((v, True))            # re-push as commit marker
            for neighbor in reversed(edges[v]):  # reversed to preserve DFS order
                if neighbor not in visited:
                    stack.append((neighbor, False))

    return post_order[::-1]


# ---------------------------------------------------------------------------
# Approach 3: Kahn's algorithm (BFS / in-degree drain)
# ---------------------------------------------------------------------------

def topological_sort_kahns(
    edges: dict[str, list[str]],
    vertices: list[str],
) -> list[str]:
    """Kahn's BFS algorithm — drains vertices with in-degree 0.

    Also detects cycles: raises ValueError if the graph is not a DAG.
    Produces a deterministic ordering when vertices are sorted.

    Time: O(V + E).  Space: O(V).

    Examples:
        >>> edges = {"a": ["c", "b"], "b": ["d", "e"], "c": [], "d": [], "e": []}
        >>> vertices = ["a", "b", "c", "d", "e"]
        >>> result = topological_sort_kahns(edges, vertices)
        >>> result.index("a") < result.index("b")
        True
        >>> result.index("b") < result.index("d")
        True
        >>> result[0]
        'a'

        Cycle detection:
        >>> topological_sort_kahns({"a": ["b"], "b": ["a"]}, ["a", "b"])
        Traceback (most recent call last):
            ...
        ValueError: Graph contains a cycle — topological sort is not possible.
    """
    in_degree: dict[str, int] = {v: 0 for v in vertices}
    for v in vertices:
        for neighbor in edges[v]:
            in_degree[neighbor] += 1

    # Start with all source nodes (in-degree 0), sorted for determinism
    queue: deque[str] = deque(sorted(v for v in vertices if in_degree[v] == 0))
    result: list[str] = []

    while queue:
        v = queue.popleft()
        result.append(v)
        for neighbor in edges[v]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) != len(vertices):
        raise ValueError("Graph contains a cycle — topological sort is not possible.")

    return result


# ---------------------------------------------------------------------------
# Approach 4: graphlib.TopologicalSorter (Python 3.9+ stdlib)
# ---------------------------------------------------------------------------

def topological_sort_graphlib(
    edges: dict[str, list[str]],
    vertices: list[str],  # noqa: ARG001 — unused; graphlib infers vertices from edges
) -> list[str]:
    """Python stdlib graphlib — C-backed, fastest for large graphs.

    Note: graphlib uses predecessor semantics: add_node(v, *predecessors).
    We invert the adjacency list (edges[u] = successors of u) to match.

    Raises graphlib.CycleError on cyclic input.

    Examples:
        >>> edges = {"a": ["c", "b"], "b": ["d", "e"], "c": [], "d": [], "e": []}
        >>> vertices = ["a", "b", "c", "d", "e"]
        >>> result = topological_sort_graphlib(edges, vertices)
        >>> result.index("a") < result.index("b")
        True
        >>> result.index("b") < result.index("d")
        True
        >>> result[0]
        'a'
    """
    # graphlib wants: {node: {predecessors}}
    # Our edges are: {node: [successors]} — invert
    predecessors: dict[str, set[str]] = {v: set() for v in edges}
    for u, successors in edges.items():
        for v in successors:
            predecessors.setdefault(v, set()).add(u)

    ts = TopologicalSorter(predecessors)
    return list(ts.static_order())


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    """Compare timing of all four approaches on a medium-sized DAG."""
    import timeit

    # Build a larger DAG: linear chain of 500 nodes
    n = 500
    verts = [str(i) for i in range(n)]
    edg = {str(i): [str(i + 1)] for i in range(n - 1)}
    edg[str(n - 1)] = []

    implementations = {
        "recursive DFS":        lambda: topological_sort_recursive(edg, verts),
        "iterative DFS":        lambda: topological_sort_iterative(edg, verts),
        "Kahn's (BFS)":         lambda: topological_sort_kahns(edg, verts),
        "graphlib (stdlib)":    lambda: topological_sort_graphlib(edg, verts),
    }

    print(f"\nBenchmark — topological sort on {n}-node linear chain (1000 runs)\n")
    print(f"{'Implementation':<25} {'Time (ms)':>12}")
    print("-" * 40)

    results = {}
    for name, fn in implementations.items():
        t = timeit.timeit(fn, number=1000)
        results[name] = t
        print(f"{name:<25} {t * 1000:>12.2f}")

    fastest = min(results, key=results.get)  # type: ignore[arg-type]
    baseline = results["recursive DFS"]
    print(f"\nFastest: {fastest}")
    for name, t in results.items():
        print(f"  {name:<25} {baseline/t:.2f}x relative to recursive DFS")

    # Also verify all agree on topological property for sample graph
    edges = {"a": ["c", "b"], "b": ["d", "e"], "c": [], "d": [], "e": []}
    vertices = ["a", "b", "c", "d", "e"]
    print("\nSample graph orderings:")
    print(f"  recursive DFS:     {topological_sort_recursive(edges, vertices)}")
    print(f"  iterative DFS:     {topological_sort_iterative(edges, vertices)}")
    print(f"  Kahn's (BFS):      {topological_sort_kahns(edges, vertices)}")
    print(f"  graphlib (stdlib): {topological_sort_graphlib(edges, vertices)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
    benchmark()
