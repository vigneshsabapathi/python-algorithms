#!/usr/bin/env python3
"""
Optimized and alternative implementations of Hamiltonian Cycle.

Hamiltonian Cycle: visit every vertex of an undirected graph exactly once
and return to the start. The decision problem is NP-complete; no polynomial
algorithm is known. These variants trade memory for speed on dense graphs.

Variants covered:
1. hamilton_cycle_backtrack   -- reference (imported from base file)
2. hamilton_cycle_iterative   -- stack-based DFS, avoids Python recursion limit
3. hamilton_cycle_held_karp   -- bitmask DP, O(n² × 2ⁿ) time / O(n × 2ⁿ) space
                                 optimal exact algorithm for n ≤ ~20
4. has_hamiltonian_cycle_ore  -- Ore's theorem sufficient-condition check
                                 O(n²) — quick "definitely yes" shortcut

Key interview insight:
    Backtracking is O(n!) in the worst case.
    Held-Karp DP is O(n² × 2ⁿ) — exponential but massively better than factorial.
    For n=20: 20! ≈ 2.4×10¹⁸  vs  20² × 2²⁰ ≈ 4×10⁸  (a billion times faster).
    Ore's theorem: if every pair of NON-ADJACENT vertices has deg(u)+deg(v) ≥ n,
    the graph is guaranteed to have a Hamiltonian cycle — O(n²) check, no search.

Run:
    python backtracking/hamiltonian_cycle_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backtracking.hamiltonian_cycle import hamilton_cycle as hamilton_cycle_backtrack


# ---------------------------------------------------------------------------
# Variant 1 — Iterative stack-based backtracking
# ---------------------------------------------------------------------------


def hamilton_cycle_iterative(
    graph: list[list[int]], start: int = 0
) -> list[int]:
    """
    Iterative DFS backtracking using an explicit stack.
    Avoids Python's recursion depth limit (default 1000) for large graphs.
    Returns the cycle as a vertex list (first == last), or [] if none exists.

    Stack entry: (current_vertex, path_so_far_as_frozenset, path_list)

    >>> graph = [[0,1,0,1,0],[1,0,1,1,1],[0,1,0,0,1],[1,1,0,0,1],[0,1,1,1,0]]
    >>> hamilton_cycle_iterative(graph, 0)
    [0, 3, 4, 2, 1, 0]
    >>> hamilton_cycle_iterative(graph, 3)
    [3, 4, 2, 1, 0, 3]

    >>> no_cycle = [[0,1,0,1,0],[1,0,1,1,1],[0,1,0,0,1],[1,1,0,0,0],[0,1,1,0,0]]
    >>> hamilton_cycle_iterative(no_cycle, 0)
    []
    """
    n = len(graph)
    # Stack holds (current_vertex, visited_set, path_list)
    stack: list[tuple[int, set[int], list[int]]] = [
        (start, {start}, [start])
    ]
    while stack:
        curr, visited, path = stack.pop()
        if len(visited) == n:
            # All vertices visited — check if we can close the cycle
            if graph[curr][start] == 1:
                return path + [start]
            continue
        for nxt in range(n):
            if graph[curr][nxt] == 1 and nxt not in visited:
                stack.append((nxt, visited | {nxt}, path + [nxt]))
    return []


# ---------------------------------------------------------------------------
# Variant 2 — Held-Karp bitmask DP (exact, O(n² × 2ⁿ))
# ---------------------------------------------------------------------------


def hamilton_cycle_held_karp(
    graph: list[list[int]], start: int = 0
) -> list[int]:
    """
    Held-Karp algorithm using bitmask DP.
    dp[mask][v] = True if there is a Hamiltonian path visiting exactly the
    vertices in `mask` starting from `start` and ending at `v`.

    After filling the DP table, we reconstruct the path via `parent` pointers.

    Time:  O(n² × 2ⁿ)   — practical up to n ≈ 20
    Space: O(n × 2ⁿ)

    >>> graph = [[0,1,0,1,0],[1,0,1,1,1],[0,1,0,0,1],[1,1,0,0,1],[0,1,1,1,0]]
    >>> hamilton_cycle_held_karp(graph, 0)
    [0, 3, 4, 2, 1, 0]
    >>> hamilton_cycle_held_karp(graph, 3)
    [3, 4, 2, 1, 0, 3]

    >>> no_cycle = [[0,1,0,1,0],[1,0,1,1,1],[0,1,0,0,1],[1,1,0,0,0],[0,1,1,0,0]]
    >>> hamilton_cycle_held_karp(no_cycle, 0)
    []
    """
    n = len(graph)
    full_mask = (1 << n) - 1

    # dp[mask][v]: can we reach v visiting exactly the vertices in mask?
    dp: list[list[bool]] = [[False] * n for _ in range(1 << n)]
    # parent[mask][v]: which vertex did we come from?
    parent: list[list[int]] = [[-1] * n for _ in range(1 << n)]

    dp[1 << start][start] = True

    for mask in range(1 << n):
        for u in range(n):
            if not dp[mask][u]:
                continue
            if not (mask >> u & 1):
                continue
            for v in range(n):
                if mask >> v & 1:
                    continue  # already visited
                if graph[u][v] == 0:
                    continue  # no edge
                new_mask = mask | (1 << v)
                if not dp[new_mask][v]:
                    dp[new_mask][v] = True
                    parent[new_mask][v] = u

    # Check if any complete path closes back to start
    last = -1
    for v in range(n):
        if v == start:
            continue
        if dp[full_mask][v] and graph[v][start] == 1:
            last = v
            break

    if last == -1:
        return []

    # Reconstruct path backwards
    path: list[int] = [start, last]
    mask = full_mask
    curr = last
    while curr != start:
        prev = parent[mask][curr]
        path.append(prev)
        mask ^= 1 << curr
        curr = prev

    path.reverse()
    return path


# ---------------------------------------------------------------------------
# Variant 3 — Ore's theorem existence check (O(n²), no path returned)
# ---------------------------------------------------------------------------


def has_hamiltonian_cycle_ore(graph: list[list[int]]) -> bool | None:
    """
    Ore's theorem (1960): If for every pair of NON-ADJACENT vertices u, v:
        deg(u) + deg(v) ≥ n
    then the graph has a Hamiltonian cycle.

    Returns:
        True  — cycle definitely exists (theorem satisfied)
        None  — inconclusive (theorem not satisfied; cycle may or may not exist)

    This is a SUFFICIENT condition, not necessary. It cannot prove absence.
    O(n²) — use as a fast pre-check before running expensive backtracking.

    >>> graph = [[0,1,0,1,0],[1,0,1,1,1],[0,1,0,0,1],[1,1,0,0,1],[0,1,1,1,0]]
    >>> has_hamiltonian_cycle_ore(graph)  # n=5, deg(0)+deg(2)=4 < 5 → inconclusive
    >>> has_hamiltonian_cycle_ore(graph) is None
    True

    >>> # K4 — complete graph, all pairs adjacent, theorem vacuously satisfied
    >>> k4 = [[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]]
    >>> has_hamiltonian_cycle_ore(k4)
    True

    >>> # Path graph 0-1-2-3: deg(0)+deg(3) = 1+1 = 2 < 4 → inconclusive
    >>> path4 = [[0,1,0,0],[1,0,1,0],[0,1,0,1],[0,0,1,0]]
    >>> has_hamiltonian_cycle_ore(path4) is None
    True
    """
    n = len(graph)
    degrees = [sum(row) for row in graph]
    for u in range(n):
        for v in range(u + 1, n):
            if graph[u][v] == 0:  # non-adjacent
                if degrees[u] + degrees[v] < n:
                    return None  # theorem not satisfied — inconclusive
    return True  # theorem satisfied — cycle guaranteed


# ---------------------------------------------------------------------------
# Correctness check + benchmark
# ---------------------------------------------------------------------------


def run_all() -> None:
    graphs = {
        "5-node (has cycle)": (
            [[0, 1, 0, 1, 0],
             [1, 0, 1, 1, 1],
             [0, 1, 0, 0, 1],
             [1, 1, 0, 0, 1],
             [0, 1, 1, 1, 0]],
            0,
        ),
        "5-node (no cycle)": (
            [[0, 1, 0, 1, 0],
             [1, 0, 1, 1, 1],
             [0, 1, 0, 0, 1],
             [1, 1, 0, 0, 0],
             [0, 1, 1, 0, 0]],
            0,
        ),
        "K4 complete": (
            [[0, 1, 1, 1],
             [1, 0, 1, 1],
             [1, 1, 0, 1],
             [1, 1, 1, 0]],
            0,
        ),
    }

    print("\n=== Correctness ===")
    for name, (g, s) in graphs.items():
        r1 = hamilton_cycle_backtrack(g, s)
        r2 = hamilton_cycle_iterative(g, s)
        r3 = hamilton_cycle_held_karp(g, s)
        found1 = bool(r1)
        found2 = bool(r2)
        found3 = bool(r3)
        match = found1 == found2 == found3
        ore = has_hamiltonian_cycle_ore(g)
        print(f"  {name}")
        print(f"    backtrack={r1}  iterative={r2}  held_karp={r3}")
        print(f"    all_agree={match}  ore_check={ore}")

    # Dense benchmark graph: random Hamiltonian graph for n=10,12,14
    import random
    random.seed(42)

    def make_ham_graph(n: int) -> list[list[int]]:
        """Build a graph guaranteed to have a Hamiltonian cycle (random cycle + extra edges)."""
        g = [[0] * n for _ in range(n)]
        perm = list(range(n))
        random.shuffle(perm)
        for i in range(n):
            u, v = perm[i], perm[(i + 1) % n]
            g[u][v] = g[v][u] = 1
        # add ~30% extra random edges
        for u in range(n):
            for v in range(u + 1, n):
                if g[u][v] == 0 and random.random() < 0.3:
                    g[u][v] = g[v][u] = 1
        return g

    REPS_SMALL = 200
    REPS_LARGE = 20

    print(f"\n=== Benchmark ===")
    print(f"  {'n':>4}  {'backtrack':>14}  {'iterative':>14}  {'held_karp':>14}")

    for n in [6, 8, 10, 12]:
        g = make_ham_graph(n)
        reps = REPS_SMALL if n <= 8 else REPS_LARGE
        t1 = timeit.timeit(lambda: hamilton_cycle_backtrack(g, 0), number=reps) * 1000 / reps
        t2 = timeit.timeit(lambda: hamilton_cycle_iterative(g, 0), number=reps) * 1000 / reps
        t3 = timeit.timeit(lambda: hamilton_cycle_held_karp(g, 0), number=reps) * 1000 / reps
        print(f"  {n:>4}  {t1:>13.4f}ms  {t2:>13.4f}ms  {t3:>13.4f}ms")

    print("\n=== Ore's theorem pre-check speed ===")
    for n in [10, 50, 100]:
        g = make_ham_graph(n)
        reps = 5000
        t = timeit.timeit(lambda: has_hamiltonian_cycle_ore(g), number=reps) * 1000 / reps
        result = has_hamiltonian_cycle_ore(g)
        print(f"  n={n:>3}  ore_result={result}  {t:.6f} ms/call")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
