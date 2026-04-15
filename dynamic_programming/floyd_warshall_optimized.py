#!/usr/bin/env python3
"""
Optimized and alternative implementations of Floyd-Warshall.

Three variants:
  class_based     — OOP with Graph class (reference)
  functional      — pure function operating on adjacency matrix
  with_path       — tracks predecessor matrix for path reconstruction

Run:
    python dynamic_programming/floyd_warshall_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.floyd_warshall import Graph


# ---------------------------------------------------------------------------
# Variant 1 — class_based (same as reference)
# ---------------------------------------------------------------------------

def class_based(n: int, edges: list[tuple[int, int, float]]) -> list[list[float]]:
    """
    >>> class_based(3, [(0, 1, 1), (1, 2, 2)])
    [[inf, 1, 3], [inf, inf, 2], [inf, inf, inf]]
    """
    g = Graph(n)
    for u, v, w in edges:
        g.add_edge(u, v, w)
    g.floyd_warshall()
    return g.dp


# ---------------------------------------------------------------------------
# Variant 2 — functional: Pure function with adjacency matrix
# ---------------------------------------------------------------------------

def functional(n: int, edges: list[tuple[int, int, float]]) -> list[list[float]]:
    """
    >>> functional(3, [(0, 1, 1), (1, 2, 2)])
    [[inf, 1, 3], [inf, inf, 2], [inf, inf, inf]]
    """
    dist = [[math.inf] * n for _ in range(n)]
    for u, v, w in edges:
        dist[u][v] = w

    for k in range(n):
        for i in range(n):
            if dist[i][k] == math.inf:
                continue
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


# ---------------------------------------------------------------------------
# Variant 3 — with_path: Path reconstruction
# ---------------------------------------------------------------------------

def with_path(
    n: int, edges: list[tuple[int, int, float]]
) -> tuple[list[list[float]], list[list[int | None]]]:
    """
    Returns (dist, next_node) where next_node[i][j] is the next hop from i toward j.

    >>> d, p = with_path(3, [(0, 1, 1), (1, 2, 2)])
    >>> d[0][2]
    3
    >>> p[0][2]
    1
    """
    dist = [[math.inf] * n for _ in range(n)]
    nxt: list[list[int | None]] = [[None] * n for _ in range(n)]

    for u, v, w in edges:
        dist[u][v] = w
        nxt[u][v] = v

    for k in range(n):
        for i in range(n):
            if dist[i][k] == math.inf:
                continue
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]

    return dist, nxt


def reconstruct_path(nxt: list[list[int | None]], u: int, v: int) -> list[int]:
    """Reconstruct shortest path from u to v using next-hop matrix."""
    if nxt[u][v] is None:
        return []
    path = [u]
    while u != v:
        u = nxt[u][v]  # type: ignore
        path.append(u)
    return path


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

EDGES_5 = [
    (0, 2, 9), (0, 4, 10), (1, 3, 5), (2, 3, 7), (3, 0, 10),
    (3, 1, 2), (3, 2, 1), (3, 4, 6), (4, 1, 3), (4, 2, 4), (4, 3, 9),
]

IMPLS = [
    ("class_based", class_based),
    ("functional", functional),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    ref = class_based(5, EDGES_5)
    func = functional(5, EDGES_5)
    ok = all(
        ref[i][j] == func[i][j]
        for i in range(5) for j in range(5)
    )
    print(f"  [{'OK' if ok else 'FAIL'}] class_based == functional for 5-node graph")

    dist, nxt = with_path(5, EDGES_5)
    print(f"  Shortest 0->3: {dist[0][3]}")
    print(f"  Path 0->3: {reconstruct_path(nxt, 0, 3)}")
    print(f"  Shortest 1->4: {dist[1][4]}")
    print(f"  Path 1->4: {reconstruct_path(nxt, 1, 4)}")

    REPS = 10_000
    print(f"\n=== Benchmark (5 nodes): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(5, EDGES_5), number=REPS) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
