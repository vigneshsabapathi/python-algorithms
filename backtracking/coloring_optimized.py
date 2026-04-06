#!/usr/bin/env python3
"""
Optimized and alternative implementations of Graph Coloring (m-coloring problem).

Variants covered:
1. color_adjacency_set    -- uses adjacency sets instead of the full adjacency matrix
                             row scan; O(degree) validity check instead of O(n).
2. color_networkx         -- networkx greedy_color / DSatur for production use;
                             finds a valid coloring with few colors automatically.
3. chromatic_number       -- finds the minimum number of colors needed (chromatic
                             number) by trying m=1,2,... until a coloring succeeds.
4. color_iterative        -- iterative backtracking with an explicit stack instead
                             of recursion; avoids Python stack-depth issues on large
                             graphs.

Key insight for interviews:
    The reference O(m^n) worst case is unavoidable for exact m-coloring.
    DSatur (networkx) heuristic is the practical choice for large graphs.
    The chromatic number problem (minimum m) is NP-hard.

Run:
    python backtracking/coloring_optimized.py
"""

from __future__ import annotations

import timeit
from collections import defaultdict


# ---------------------------------------------------------------------------
# Graph representations
# ---------------------------------------------------------------------------

AdjMatrix = list[list[int]]  # 0/1 adjacency matrix (reference)
AdjSet = dict[int, set[int]]  # adjacency set (optimized)


def matrix_to_adjset(graph: AdjMatrix) -> AdjSet:
    """Convert 0/1 adjacency matrix to adjacency set dict."""
    return {i: {j for j, v in enumerate(row) if v} for i, row in enumerate(graph)}


# ---------------------------------------------------------------------------
# Variant 1 — adjacency-set backtracking (O(degree) constraint check)
# ---------------------------------------------------------------------------


def color_adjacency_set(adj: AdjSet, max_colors: int) -> list[int]:
    """
    Graph coloring using adjacency sets for O(degree) constraint checks
    instead of the reference's O(n) row scan.

    For sparse graphs (most real graphs) this is significantly faster.
    For dense graphs (degree ~ n) it's equivalent.

    Args:
        adj: adjacency set dict {vertex: set of neighbours}.
        max_colors: maximum number of colors allowed.

    Returns:
        List of color assignments (0-indexed), or [] if impossible.

    >>> adj = {0:{1}, 1:{0,2,4}, 2:{1,3}, 3:{1,2}, 4:{1}}
    >>> result = color_adjacency_set(adj, 3)
    >>> len(result) == 5 and result[1] != result[0] and result[1] != result[2]
    True
    >>> color_adjacency_set({0:{1},1:{0}}, 1)
    []
    >>> color_adjacency_set({0:{1},1:{0}}, 2)
    [0, 1]
    >>> color_adjacency_set({}, 2)
    []
    """
    n = len(adj)
    if n == 0:
        return []
    coloring = [-1] * n

    def _backtrack(v: int) -> bool:
        if v == n:
            return True
        neighbor_colors = {coloring[u] for u in adj[v] if coloring[u] != -1}
        for c in range(max_colors):
            if c not in neighbor_colors:
                coloring[v] = c
                if _backtrack(v + 1):
                    return True
                coloring[v] = -1
        return False

    return coloring if _backtrack(0) else []


# ---------------------------------------------------------------------------
# Variant 2 — networkx greedy coloring (production heuristic)
# ---------------------------------------------------------------------------


def color_networkx(
    graph: AdjMatrix, strategy: str = "DSATUR"
) -> tuple[int, list[int]]:
    """
    Greedy graph coloring via networkx.

    Strategies:
        'DSATUR'     -- Saturation Degree: at each step color the vertex with
                        the most distinctly-colored neighbours. Best quality.
        'largest_first' -- color vertices in decreasing degree order.
        'smallest_last' -- order by smallest degree last; best for planar graphs.
        'random_sequential' -- random order.

    Note: networkx greedy coloring is a heuristic — it finds a valid coloring
    but NOT necessarily with the minimum number of colors (chromatic number).

    Returns:
        (num_colors_used, coloring_list)

    >>> matrix = [[0,1,0,0,0],[1,0,1,0,1],[0,1,0,1,0],[0,1,1,0,0],[0,1,0,0,0]]
    >>> num_colors, coloring = color_networkx(matrix)
    >>> num_colors <= 3 and len(coloring) == 5
    True
    """
    import networkx as nx

    G = nx.Graph()
    n = len(graph)
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j]:
                G.add_edge(i, j)

    color_map = nx.coloring.greedy_color(G, strategy=strategy)
    coloring = [color_map[i] for i in range(n)]
    return max(coloring) + 1 if coloring else 0, coloring


# ---------------------------------------------------------------------------
# Variant 3 — find chromatic number (minimum colors needed)
# ---------------------------------------------------------------------------


def chromatic_number(graph: AdjMatrix) -> tuple[int, list[int]]:
    """
    Find the chromatic number — the minimum number of colors needed.
    Tries m = 1, 2, ... until a valid coloring is found.

    NP-hard in general; this brute-force is feasible only for small graphs (n<=20).

    Returns:
        (chromatic_number, coloring)

    >>> graph = [[0,1,0,0,0],[1,0,1,0,1],[0,1,0,1,0],[0,1,1,0,0],[0,1,0,0,0]]
    >>> chi, col = chromatic_number(graph)
    >>> chi
    3
    >>> graph_k3 = [[0,1,1],[1,0,1],[1,1,0]]
    >>> chromatic_number(graph_k3)[0]
    3
    >>> chromatic_number([[0,1],[1,0]])[0]
    2
    >>> chromatic_number([[0]])[0]
    1
    """
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from backtracking.coloring import color as ref_color

    for m in range(1, len(graph) + 1):
        result = ref_color(graph, m)
        if result:
            return m, result
    return len(graph), list(range(len(graph)))  # worst case: each vertex its own color


# ---------------------------------------------------------------------------
# Variant 4 — iterative backtracking (avoids Python recursion limit)
# ---------------------------------------------------------------------------


def color_iterative(graph: AdjMatrix, max_colors: int) -> list[int]:
    """
    Iterative backtracking using an explicit stack.
    Avoids Python's recursion limit (~1000) for large graphs.

    Algorithm:
    - Stack holds (vertex_index, color_to_try).
    - If a vertex can't be colored with any remaining color, pop back
      and try the next color for the previous vertex.

    >>> graph = [[0,1,0,0,0],[1,0,1,0,1],[0,1,0,1,0],[0,1,1,0,0],[0,1,0,0,0]]
    >>> result = color_iterative(graph, 3)
    >>> len(result) == 5 and all(c >= 0 for c in result)
    True
    >>> color_iterative([[0,1],[1,0]], 1)
    []
    >>> color_iterative([[0,1],[1,0]], 2)
    [0, 1]
    >>> color_iterative([], 2)
    []
    """
    n = len(graph)
    if n == 0:
        return []

    coloring = [-1] * n  # -1 = uncolored; start each vertex at "try color 0"
    v = 0

    while 0 <= v < n:
        # Find the next valid color for vertex v, starting just after the current one
        next_color = coloring[v] + 1
        placed = False
        while next_color < max_colors:
            if not any(graph[v][u] == 1 and coloring[u] == next_color for u in range(n)):
                coloring[v] = next_color
                v += 1      # advance to next vertex
                placed = True
                break
            next_color += 1

        if not placed:
            coloring[v] = -1    # reset: no valid color found — backtrack
            v -= 1

    return coloring if v == n else []


# ---------------------------------------------------------------------------
# Benchmark + correctness
# ---------------------------------------------------------------------------


def run_all() -> None:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from backtracking.coloring import color as ref_color

    # Test graphs
    g5 = [[0,1,0,0,0],[1,0,1,0,1],[0,1,0,1,0],[0,1,1,0,0],[0,1,0,0,0]]
    k4 = [[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]]   # complete graph, needs 4 colors
    petersen = [  # Petersen graph, chromatic number = 3
        [0,1,0,0,1,1,0,0,0,0],
        [1,0,1,0,0,0,1,0,0,0],
        [0,1,0,1,0,0,0,1,0,0],
        [0,0,1,0,1,0,0,0,1,0],
        [1,0,0,1,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,1,1,0],
        [0,1,0,0,0,0,0,0,1,1],
        [0,0,1,0,0,1,0,0,0,1],
        [0,0,0,1,0,1,1,0,0,0],
        [0,0,0,0,1,0,1,1,0,0],
    ]

    print("\n=== Correctness check ===")
    for name, graph, m in [
        ("5-node, m=3", g5, 3),
        ("5-node, m=2 (impossible)", g5, 2),
        ("K4, m=4", k4, 4),
        ("K4, m=3 (impossible)", k4, 3),
        ("Petersen, m=3", petersen, 3),
    ]:
        ref = ref_color(graph, m)
        adj = matrix_to_adjset(graph)
        r_adj = color_adjacency_set(adj, m)
        r_ite = color_iterative(graph, m)
        # verify validity: no two adjacent vertices share a color
        def is_valid(g, col):
            if not col:
                return True
            n = len(g)
            return all(
                not (g[i][j] and col[i] == col[j])
                for i in range(n) for j in range(i+1, n)
            )
        ref_ok = bool(ref) == bool(r_adj) == bool(r_ite)
        validity = (not ref or is_valid(graph, ref)) and (not r_ite or is_valid(graph, r_ite))
        print(f"  {name:30}  ref={str(ref or []):20}  ite={str(r_ite or []):20}  "
              f"{'OK' if ref_ok and validity else 'MISMATCH'}")

    print("\n=== Chromatic number ===")
    for name, graph in [("5-node", g5), ("K4", k4), ("Petersen", petersen)]:
        chi, col = chromatic_number(graph)
        print(f"  {name:12}  chromatic_number={chi}  coloring={col}")

    try:
        print("\n=== networkx DSatur ===")
        for name, graph in [("5-node", g5), ("K4", k4), ("Petersen", petersen)]:
            num_c, col = color_networkx(graph, strategy="DSATUR")
            print(f"  {name:12}  colors_used={num_c}  coloring={col}")
    except ImportError:
        print("  networkx not installed -- skipping")

    REPS = 2000
    print(f"\n=== Benchmark ({REPS} runs, 5-node graph, m=3) ===")
    adj5 = matrix_to_adjset(g5)

    t1 = timeit.timeit(lambda: ref_color(g5, 3), number=REPS) * 1000 / REPS
    print(f"  reference (adj matrix):   {t1:.4f} ms/run")

    t2 = timeit.timeit(lambda: color_adjacency_set(adj5, 3), number=REPS) * 1000 / REPS
    print(f"  adjacency set:            {t2:.4f} ms/run")

    t3 = timeit.timeit(lambda: color_iterative(g5, 3), number=REPS) * 1000 / REPS
    print(f"  iterative backtrack:      {t3:.4f} ms/run")

    REPS2 = 500
    print(f"\n=== Benchmark ({REPS2} runs, Petersen graph, m=3) ===")
    adj_p = matrix_to_adjset(petersen)

    t4 = timeit.timeit(lambda: ref_color(petersen, 3), number=REPS2) * 1000 / REPS2
    print(f"  reference (adj matrix):   {t4:.4f} ms/run")

    t5 = timeit.timeit(lambda: color_adjacency_set(adj_p, 3), number=REPS2) * 1000 / REPS2
    print(f"  adjacency set:            {t5:.4f} ms/run")

    t6 = timeit.timeit(lambda: color_iterative(petersen, 3), number=REPS2) * 1000 / REPS2
    print(f"  iterative backtrack:      {t6:.4f} ms/run")

    try:
        import networkx  # noqa: F401
        t7 = timeit.timeit(lambda: color_networkx(petersen, "DSATUR"), number=REPS2) * 1000 / REPS2
        print(f"  networkx DSatur:          {t7:.4f} ms/run")
    except ImportError:
        pass


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
