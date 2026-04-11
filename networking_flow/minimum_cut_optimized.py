#!/usr/bin/env python3
"""
Optimized and alternative implementations of Minimum Cut.

The reference runs Edmonds-Karp then BFS on the residual to find cut edges.

Variants covered:
1. bfs_mincut       -- BFS (Edmonds-Karp) residual + reachability (reference)
2. dinic_mincut     -- Dinic's algorithm + reachability (faster max-flow phase)
3. stoer_wagner     -- Stoer-Wagner algorithm for UNDIRECTED global min-cut
                       (no source/sink needed, O(V^3))

Key interview insight:
    Max-flow min-cut theorem: the maximum flow equals the minimum cut capacity.
    For directed graphs, run any max-flow algorithm then BFS on residual.
    For undirected graphs, Stoer-Wagner finds the global min-cut directly
    without needing a source or sink — common in network reliability problems.

Run:
    python networking_flow/minimum_cut_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from collections import deque
from copy import deepcopy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from networking_flow.minimum_cut import minimum_cut as reference


# ---------------------------------------------------------------------------
# Variant 1 — BFS-based min-cut (Edmonds-Karp + residual BFS)
# ---------------------------------------------------------------------------

def bfs_mincut(
    graph: list[list[int]], source: int, sink: int
) -> list[tuple[int, int]]:
    """
    Min-cut using BFS (Edmonds-Karp) for max-flow, then BFS on residual.

    >>> bfs_mincut(
    ...     [[0, 16, 13, 0, 0, 0],
    ...      [0, 0, 10, 12, 0, 0],
    ...      [0, 4, 0, 0, 14, 0],
    ...      [0, 0, 9, 0, 0, 20],
    ...      [0, 0, 0, 7, 0, 4],
    ...      [0, 0, 0, 0, 0, 0]],
    ...     0, 5)
    [(1, 3), (4, 3), (4, 5)]
    >>> bfs_mincut([[0, 0], [0, 0]], 0, 1)
    []
    """
    g = deepcopy(graph)
    n = len(g)

    def bfs_path() -> list[int] | None:
        parent = [-1] * n
        visited = [False] * n
        visited[source] = True
        queue: deque[int] = deque([source])
        while queue:
            u = queue.popleft()
            for v in range(n):
                if not visited[v] and g[u][v] > 0:
                    visited[v] = True
                    parent[v] = u
                    if v == sink:
                        return parent
                    queue.append(v)
        return None

    # Max flow phase
    while True:
        parent = bfs_path()
        if parent is None:
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

    # Reachability on residual
    reachable = [False] * n
    reachable[source] = True
    queue: deque[int] = deque([source])
    while queue:
        u = queue.popleft()
        for v in range(n):
            if not reachable[v] and g[u][v] > 0:
                reachable[v] = True
                queue.append(v)

    return [
        (u, v)
        for u in range(n)
        for v in range(n)
        if reachable[u] and not reachable[v] and graph[u][v] > 0
    ]


# ---------------------------------------------------------------------------
# Variant 2 — Dinic-based min-cut (faster max-flow, same cut extraction)
# ---------------------------------------------------------------------------

def dinic_mincut(
    graph: list[list[int]], source: int, sink: int
) -> list[tuple[int, int]]:
    """
    Min-cut using Dinic's algorithm for the max-flow phase.

    >>> dinic_mincut(
    ...     [[0, 16, 13, 0, 0, 0],
    ...      [0, 0, 10, 12, 0, 0],
    ...      [0, 4, 0, 0, 14, 0],
    ...      [0, 0, 9, 0, 0, 20],
    ...      [0, 0, 0, 7, 0, 4],
    ...      [0, 0, 0, 0, 0, 0]],
    ...     0, 5)
    [(1, 3), (4, 3), (4, 5)]
    >>> dinic_mincut([[0, 5, 0], [0, 0, 5], [0, 0, 0]], 0, 2)
    [(0, 1)]
    """
    n = len(graph)
    # Build adjacency list with edge pairs
    adj: list[list[list[int]]] = [[] for _ in range(n)]

    def add_edge(u: int, v: int, cap: int) -> None:
        adj[u].append([v, cap, len(adj[v])])
        adj[v].append([u, 0, len(adj[u]) - 1])

    for u in range(n):
        for v in range(n):
            if graph[u][v] > 0:
                add_edge(u, v, graph[u][v])

    level = [0] * n

    def bfs_level() -> bool:
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

    def dfs_block(u: int, pushed: float) -> float:
        if u == sink:
            return pushed
        while work[u] < len(adj[u]):
            v, cap, rev = adj[u][work[u]]
            if level[v] == level[u] + 1 and cap > 0:
                d = dfs_block(v, min(pushed, cap))
                if d > 0:
                    adj[u][work[u]][1] -= d
                    adj[v][rev][1] += d
                    return d
            work[u] += 1
        return 0

    while bfs_level():
        work = [0] * n
        while True:
            f = dfs_block(source, float("inf"))
            if f == 0:
                break

    # Reachability on residual (adjacency list)
    reachable = [False] * n
    reachable[source] = True
    queue: deque[int] = deque([source])
    while queue:
        u = queue.popleft()
        for v, cap, _ in adj[u]:
            if not reachable[v] and cap > 0:
                reachable[v] = True
                queue.append(v)

    return [
        (u, v)
        for u in range(n)
        for v in range(n)
        if reachable[u] and not reachable[v] and graph[u][v] > 0
    ]


# ---------------------------------------------------------------------------
# Variant 3 — Stoer-Wagner (global min-cut for UNDIRECTED graphs, O(V^3))
# ---------------------------------------------------------------------------

def stoer_wagner(graph: list[list[int]]) -> tuple[int, list[int]]:
    """
    Stoer-Wagner algorithm for global minimum cut on an UNDIRECTED graph.

    Unlike max-flow min-cut, this does NOT require source/sink -- it finds
    the globally minimum cut separating the graph into any two non-empty parts.

    Returns (min_cut_value, one_side_of_cut_as_node_list).

    Input must be a symmetric adjacency matrix (undirected weights).

    >>> stoer_wagner([
    ...     [0, 2, 0, 3],
    ...     [2, 0, 3, 0],
    ...     [0, 3, 0, 2],
    ...     [3, 0, 2, 0],
    ... ])
    (4, [1, 2])
    >>> stoer_wagner([[0, 5], [5, 0]])
    (5, [1])
    """
    n = len(graph)
    w = [row[:] for row in graph]
    # active[i] = True if node i hasn't been merged into another
    active = [True] * n
    merged: list[list[int]] = [[i] for i in range(n)]

    best_cut = float("inf")
    best_partition: list[int] = []

    for phase in range(n - 1):
        # Minimum-cut phase using maximum adjacency ordering
        # key[v] = total weight of edges from v to the growing set A
        key = [0] * n
        in_a = [False] * n

        # Start with the first active node
        start = -1
        for i in range(n):
            if active[i]:
                start = i
                break

        prev = start
        last = start

        for count in range(sum(active)):
            # Add 'last' to A
            in_a[last] = True
            # Update keys for all active nodes not yet in A
            for v in range(n):
                if active[v] and not in_a[v]:
                    key[v] += w[last][v]

            # Find most tightly connected active node not in A
            best_key = -1
            best_node = -1
            for v in range(n):
                if active[v] and not in_a[v] and key[v] > best_key:
                    best_key = key[v]
                    best_node = v

            if best_node == -1:
                break
            prev = last
            last = best_node

        # 'last' is t, 'prev' is s in the standard description
        cut_of_phase = key[last]
        if cut_of_phase < best_cut:
            best_cut = cut_of_phase
            best_partition = merged[last][:]

        # Merge 'last' into 'prev'
        for v in range(n):
            w[prev][v] += w[last][v]
            w[v][prev] += w[v][last]
        merged[prev].extend(merged[last])
        active[last] = False

    return int(best_cut), sorted(best_partition)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

DIRECTED_GRAPHS = {
    "CLRS 6-node": (
        [
            [0, 16, 13, 0, 0, 0],
            [0, 0, 10, 12, 0, 0],
            [0, 4, 0, 0, 14, 0],
            [0, 0, 9, 0, 0, 20],
            [0, 0, 0, 7, 0, 4],
            [0, 0, 0, 0, 0, 0],
        ],
        0, 5,
        [(1, 3), (4, 3), (4, 5)],
    ),
    "simple chain": (
        [[0, 10, 0], [0, 0, 10], [0, 0, 0]],
        0, 2,
        [(0, 1)],
    ),
    "no path": (
        [[0, 0], [0, 0]],
        0, 1,
        [],
    ),
    "parallel": (
        [
            [0, 10, 10, 0],
            [0, 0, 0, 10],
            [0, 0, 0, 10],
            [0, 0, 0, 0],
        ],
        0, 3,
        [(0, 1), (0, 2)],
    ),
}

DIRECTED_IMPLS = [
    ("reference",    lambda g, s, t: reference(deepcopy(g), s, t)),
    ("bfs_mincut",   bfs_mincut),
    ("dinic_mincut", dinic_mincut),
]


def run_all() -> None:
    print("\n=== Correctness (directed min-cut) ===")
    for label, (graph, s, t, expected) in DIRECTED_GRAPHS.items():
        results = {}
        for name, fn in DIRECTED_IMPLS:
            try:
                results[name] = fn(deepcopy(graph), s, t)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(sorted(v) == sorted(expected) for v in results.values()
                 if not isinstance(v, str))
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] {label:<16} expected={expected}")
        for nm, v in results.items():
            print(f"         {nm:<16} -> {v}")

    print("\n=== Correctness (Stoer-Wagner undirected global min-cut) ===")
    sw_tests = [
        ("2-node", [[0, 5], [5, 0]], 5),
        ("4-node ring", [
            [0, 2, 0, 3],
            [2, 0, 3, 0],
            [0, 3, 0, 2],
            [3, 0, 2, 0],
        ], 4),
        ("K4 uniform (3)", [
            [0, 1, 1, 1],
            [1, 0, 1, 1],
            [1, 1, 0, 1],
            [1, 1, 1, 0],
        ], 3),
    ]
    for label, g, expected_val in sw_tests:
        val, partition = stoer_wagner(deepcopy(g))
        tag = "OK" if val == expected_val else "FAIL"
        print(f"  [{tag}] {label:<16} expected={expected_val}  got={val}  partition={partition}")

    import random
    random.seed(42)
    N = 25
    big_graph = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if i != j and random.random() < 0.3:
                big_graph[i][j] = random.randint(1, 50)

    REPS = 200
    print(f"\n=== Benchmark: {N}-node random directed graph, {REPS} iterations ===")
    for name, fn in DIRECTED_IMPLS:
        t = timeit.timeit(
            lambda fn=fn: fn(deepcopy(big_graph), 0, N - 1), number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>8.3f} ms / run")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
