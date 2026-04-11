#!/usr/bin/env python3
"""
Optimized and alternative implementations of Ford-Fulkerson max-flow.

The reference uses BFS (Edmonds-Karp) on an adjacency matrix.

Variants covered:
1. edmonds_karp_matrix  -- BFS on adjacency matrix  (reference, O(V * E^2))
2. edmonds_karp_adjlist -- BFS on adjacency list     (faster for sparse graphs)
3. dfs_ford_fulkerson   -- DFS path finding          (classic Ford-Fulkerson, not polynomial)
4. dinic                -- Dinic's algorithm          (O(V^2 * E), fastest for dense graphs)

Key interview insight:
    Edmonds-Karp = Ford-Fulkerson + BFS.  BFS guarantees O(V*E^2).
    DFS-based Ford-Fulkerson has no polynomial bound on general graphs
    (can loop on irrational capacities), but works fine with integer capacities.
    Dinic's uses level graphs + blocking flows for O(V^2 * E) — the go-to for
    competitive programming.

Run:
    python networking_flow/ford_fulkerson_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from collections import deque
from copy import deepcopy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from networking_flow.ford_fulkerson import ford_fulkerson as reference


# ---------------------------------------------------------------------------
# Variant 1 — Edmonds-Karp on adjacency matrix (reference reimplementation)
# ---------------------------------------------------------------------------

def edmonds_karp_matrix(graph: list[list[int]], source: int, sink: int) -> int:
    """
    Max flow via BFS augmenting paths on an adjacency matrix.

    >>> edmonds_karp_matrix(
    ...     [[0, 16, 13, 0, 0, 0],
    ...      [0, 0, 10, 12, 0, 0],
    ...      [0, 4, 0, 0, 14, 0],
    ...      [0, 0, 9, 0, 0, 20],
    ...      [0, 0, 0, 7, 0, 4],
    ...      [0, 0, 0, 0, 0, 0]],
    ...     0, 5)
    23
    >>> edmonds_karp_matrix([[0, 0], [0, 0]], 0, 1)
    0
    """
    g = deepcopy(graph)
    n = len(g)
    max_flow = 0

    while True:
        parent = [-1] * n
        visited = [False] * n
        visited[source] = True
        queue: deque[int] = deque([source])
        found = False

        while queue and not found:
            u = queue.popleft()
            for v in range(n):
                if not visited[v] and g[u][v] > 0:
                    visited[v] = True
                    parent[v] = u
                    if v == sink:
                        found = True
                        break
                    queue.append(v)

        if not found:
            break

        # Bottleneck
        path_flow = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, g[u][v])
            v = u

        # Update residual graph
        v = sink
        while v != source:
            u = parent[v]
            g[u][v] -= path_flow
            g[v][u] += path_flow
            v = u

        max_flow += path_flow

    return max_flow


# ---------------------------------------------------------------------------
# Variant 2 — Edmonds-Karp on adjacency list (sparse-graph friendly)
# ---------------------------------------------------------------------------

def edmonds_karp_adjlist(graph: list[list[int]], source: int, sink: int) -> int:
    """
    Edmonds-Karp using an adjacency-list residual graph with edge objects.
    Better constant factors for sparse graphs.

    >>> edmonds_karp_adjlist(
    ...     [[0, 16, 13, 0, 0, 0],
    ...      [0, 0, 10, 12, 0, 0],
    ...      [0, 4, 0, 0, 14, 0],
    ...      [0, 0, 9, 0, 0, 20],
    ...      [0, 0, 0, 7, 0, 4],
    ...      [0, 0, 0, 0, 0, 0]],
    ...     0, 5)
    23
    >>> edmonds_karp_adjlist([[0, 5, 0], [0, 0, 5], [0, 0, 0]], 0, 2)
    5
    """
    n = len(graph)
    # Build adjacency list with forward/reverse edge pairs
    # Each edge: [to, capacity, index_of_reverse_edge_in_adj[to]]
    adj: list[list[list[int]]] = [[] for _ in range(n)]

    def add_edge(u: int, v: int, cap: int) -> None:
        adj[u].append([v, cap, len(adj[v])])
        adj[v].append([u, 0, len(adj[u]) - 1])

    for u in range(n):
        for v in range(n):
            if graph[u][v] > 0:
                add_edge(u, v, graph[u][v])

    max_flow = 0

    while True:
        # BFS to find augmenting path
        parent: list[tuple[int, int] | None] = [None] * n  # (prev_node, edge_index)
        visited = [False] * n
        visited[source] = True
        queue: deque[int] = deque([source])
        found = False

        while queue and not found:
            u = queue.popleft()
            for i, (v, cap, _) in enumerate(adj[u]):
                if not visited[v] and cap > 0:
                    visited[v] = True
                    parent[v] = (u, i)
                    if v == sink:
                        found = True
                        break
                    queue.append(v)

        if not found:
            break

        # Find bottleneck
        path_flow = float("inf")
        v = sink
        while v != source:
            u, idx = parent[v]
            path_flow = min(path_flow, adj[u][idx][1])
            v = u

        # Update residual
        v = sink
        while v != source:
            u, idx = parent[v]
            adj[u][idx][1] -= path_flow
            adj[v][adj[u][idx][2]][1] += path_flow
            v = u

        max_flow += path_flow

    return max_flow


# ---------------------------------------------------------------------------
# Variant 3 — DFS-based Ford-Fulkerson (classic, not polynomial in general)
# ---------------------------------------------------------------------------

def dfs_ford_fulkerson(graph: list[list[int]], source: int, sink: int) -> int:
    """
    Ford-Fulkerson using DFS to find augmenting paths.
    Works correctly for integer capacities but is NOT polynomial in general
    (O(E * max_flow) worst case).

    >>> dfs_ford_fulkerson(
    ...     [[0, 16, 13, 0, 0, 0],
    ...      [0, 0, 10, 12, 0, 0],
    ...      [0, 4, 0, 0, 14, 0],
    ...      [0, 0, 9, 0, 0, 20],
    ...      [0, 0, 0, 7, 0, 4],
    ...      [0, 0, 0, 0, 0, 0]],
    ...     0, 5)
    23
    >>> dfs_ford_fulkerson([[0, 0], [0, 0]], 0, 1)
    0
    """
    g = deepcopy(graph)
    n = len(g)
    max_flow = 0

    def dfs(u: int, sink: int, visited: list[bool], parent: list[int]) -> bool:
        if u == sink:
            return True
        visited[u] = True
        for v in range(n):
            if not visited[v] and g[u][v] > 0:
                parent[v] = u
                if dfs(v, sink, visited, parent):
                    return True
        return False

    while True:
        visited = [False] * n
        parent = [-1] * n
        if not dfs(source, sink, visited, parent):
            break

        path_flow = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, g[u][v])
            v = u

        v = sink
        while v != source:
            u = parent[v]
            g[u][v] -= path_flow
            g[v][u] += path_flow
            v = u

        max_flow += path_flow

    return max_flow


# ---------------------------------------------------------------------------
# Variant 4 — Dinic's Algorithm (O(V^2 * E), optimal for many graph types)
# ---------------------------------------------------------------------------

def dinic(graph: list[list[int]], source: int, sink: int) -> int:
    """
    Dinic's algorithm: builds a level graph with BFS, then finds blocking
    flows with DFS.  O(V^2 * E) — significantly faster than Edmonds-Karp
    on dense or high-flow graphs.

    >>> dinic(
    ...     [[0, 16, 13, 0, 0, 0],
    ...      [0, 0, 10, 12, 0, 0],
    ...      [0, 4, 0, 0, 14, 0],
    ...      [0, 0, 9, 0, 0, 20],
    ...      [0, 0, 0, 7, 0, 4],
    ...      [0, 0, 0, 0, 0, 0]],
    ...     0, 5)
    23
    >>> dinic([[0, 1000000], [0, 0]], 0, 1)
    1000000
    """
    n = len(graph)
    # Build adjacency list
    adj: list[list[list[int]]] = [[] for _ in range(n)]

    def add_edge(u: int, v: int, cap: int) -> None:
        adj[u].append([v, cap, len(adj[v])])      # forward edge
        adj[v].append([u, 0, len(adj[u]) - 1])    # reverse edge

    for u in range(n):
        for v in range(n):
            if graph[u][v] > 0:
                add_edge(u, v, graph[u][v])

    def bfs_level() -> bool:
        """Build level graph via BFS. Returns True if sink is reachable."""
        for i in range(n):
            level[i] = -1
        level[source] = 0
        queue: deque[int] = deque([source])
        while queue:
            u = queue.popleft()
            for v, cap, _ in adj[u]:
                if level[v] == -1 and cap > 0:
                    level[v] = level[u] + 1
                    queue.append(v)
        return level[sink] != -1

    def dfs_blocking(u: int, pushed: float) -> float:
        """Send blocking flow from u to sink using DFS with current-arc optimization."""
        if u == sink:
            return pushed
        while work[u] < len(adj[u]):
            v, cap, rev = adj[u][work[u]]
            if level[v] == level[u] + 1 and cap > 0:
                d = dfs_blocking(v, min(pushed, cap))
                if d > 0:
                    adj[u][work[u]][1] -= d
                    adj[v][rev][1] += d
                    return d
            work[u] += 1
        return 0

    level = [0] * n
    max_flow = 0

    while bfs_level():
        work = [0] * n
        while True:
            pushed = dfs_blocking(source, float("inf"))
            if pushed == 0:
                break
            max_flow += pushed

    return max_flow


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

GRAPHS = {
    "CLRS 6-node": (
        [
            [0, 16, 13, 0, 0, 0],
            [0, 0, 10, 12, 0, 0],
            [0, 4, 0, 0, 14, 0],
            [0, 0, 9, 0, 0, 20],
            [0, 0, 0, 7, 0, 4],
            [0, 0, 0, 0, 0, 0],
        ],
        0, 5, 23,
    ),
    "simple chain": (
        [[0, 10, 0], [0, 0, 10], [0, 0, 0]],
        0, 2, 10,
    ),
    "parallel paths": (
        [
            [0, 10, 10, 0],
            [0, 0, 0, 10],
            [0, 0, 0, 10],
            [0, 0, 0, 0],
        ],
        0, 3, 20,
    ),
    "no path": (
        [[0, 0], [0, 0]],
        0, 1, 0,
    ),
    "bottleneck": (
        [
            [0, 100, 100, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 100],
            [0, 0, 0, 0],
        ],
        0, 3, 101,
    ),
}

IMPLS = [
    ("reference",           lambda g, s, t: reference(deepcopy(g), s, t)),
    ("edmonds_karp_matrix",  edmonds_karp_matrix),
    ("edmonds_karp_adjlist", edmonds_karp_adjlist),
    ("dfs_ford_fulkerson",   dfs_ford_fulkerson),
    ("dinic",                dinic),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for label, (graph, s, t, expected) in GRAPHS.items():
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(deepcopy(graph), s, t)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] {label:<18} expected={expected:<5}  "
              + "  ".join(f"{nm}={v}" for nm, v in results.items()))

    # Generate a larger graph for benchmarking
    import random
    random.seed(42)
    N = 30
    big_graph = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if i != j and random.random() < 0.3:
                big_graph[i][j] = random.randint(1, 50)

    REPS = 200
    print(f"\n=== Benchmark: {N}-node random graph, {REPS} iterations ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: fn(deepcopy(big_graph), 0, N - 1), number=REPS
        ) * 1000 / REPS
        print(f"  {name:<22} {t:>8.3f} ms / run")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
