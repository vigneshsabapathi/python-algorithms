#!/usr/bin/env python3
"""
Optimized and alternative implementations of Tabu Search for TSP.

Variants covered:
1. tabu_search_2opt      -- Tabu search with 2-opt moves instead of 1-1 swap.
                            2-opt is the standard TSP neighborhood: reverse a
                            sub-segment of the tour. Produces much better solutions.
2. nearest_neighbor_tsp  -- Greedy nearest-neighbor heuristic (no TS).
                            Fast O(n^2) baseline; what the original uses as initial
                            solution but never improves standalone.
3. networkx_tsp          -- networkx.approximation.christofides / greedy_tsp.
                            Production-quality 1.5x approximation guarantee.

Design notes vs reference implementation:
- Reference stores graph as dict[node -> list[list[node, str_dist]]].
  This file uses dict[node -> dict[node -> int]] (adjacency dict) — O(1) lookup
  instead of O(n) list scan per edge.
- Reference reads the graph file for start node every call — this file separates
  graph parsing from algorithm logic cleanly.

Run:
    python searches/tabu_search_optimized.py
"""

from __future__ import annotations

import copy
import itertools
import math
import random
import sys
import os
import timeit
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ---------------------------------------------------------------------------
# Graph helpers
# ---------------------------------------------------------------------------

Graph = dict[str, dict[str, int]]  # adjacency dict: graph[u][v] = distance


def load_graph(path: str) -> tuple[Graph, str]:
    """
    Load a symmetric TSP graph from a whitespace-delimited file.
    Returns (graph, start_node) where start_node is the first node seen.
    """
    graph: Graph = {}
    start_node: str | None = None

    with open(path) as f:
        for line in f:
            parts = line.split()
            if len(parts) < 3:
                continue
            u, v, d = parts[0], parts[1], int(parts[2])
            if start_node is None:
                start_node = u
            graph.setdefault(u, {})[v] = d
            graph.setdefault(v, {})[u] = d

    assert start_node is not None
    return graph, start_node


def tour_distance(tour: list[str], graph: Graph) -> int:
    """Return total distance of a tour (last node loops back to first)."""
    return sum(graph[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))


def nearest_neighbor_tour(graph: Graph, start: str) -> list[str]:
    """
    Greedy nearest-neighbor: always go to the closest unvisited city.
    O(n^2). Same strategy as generate_first_solution in the reference.
    Returns a closed tour: [start, ..., start].
    """
    unvisited = set(graph) - {start}
    tour = [start]
    current = start
    while unvisited:
        nearest = min(unvisited, key=lambda v: graph[current][v])
        tour.append(nearest)
        unvisited.remove(nearest)
        current = nearest
    tour.append(start)
    return tour


# ---------------------------------------------------------------------------
# Variant 1 — Tabu search with 2-opt neighborhood
# ---------------------------------------------------------------------------


def tabu_search_2opt(
    graph: Graph,
    start: str,
    iters: int = 100,
    tabu_size: int = 10,
    seed: int | None = 42,
) -> tuple[list[str], int]:
    """
    Tabu search using 2-opt moves.

    2-opt neighborhood: for each pair (i, j) with i < j, reverse the sub-tour
    between positions i+1 and j. This eliminates crossing edges and is the
    standard TSP improvement move.

    Tabu list stores (i, j) index pairs of recent moves to prevent cycling.

    Args:
        graph: adjacency dict.
        start: starting city.
        iters: number of tabu search iterations.
        tabu_size: max number of moves kept in the tabu list.
        seed: random seed (not used — 2-opt is deterministic here).

    Returns:
        (best_tour, best_distance)
    """
    # Initial solution via nearest neighbor
    current_tour = nearest_neighbor_tour(graph, start)
    best_tour = current_tour[:]
    best_dist = tour_distance(best_tour, graph)

    tabu_list: list[tuple[int, int]] = []

    for _ in range(iters):
        cities = current_tour[1:-1]  # exclude start/end sentinel
        n = len(cities)
        best_neighbor: list[str] | None = None
        best_neighbor_dist = math.inf
        best_move: tuple[int, int] | None = None

        # Generate all 2-opt neighbors
        for i in range(n - 1):
            for j in range(i + 1, n):
                move = (i, j)
                # Build 2-opt neighbor: reverse segment [i+1 .. j]
                new_cities = cities[:i] + cities[i:j + 1][::-1] + cities[j + 1:]
                new_tour = [start] + new_cities + [start]
                new_dist = tour_distance(new_tour, graph)

                # Accept if not tabu, or tabu but beats best_dist (aspiration)
                if move not in tabu_list or new_dist < best_dist:
                    if new_dist < best_neighbor_dist:
                        best_neighbor_dist = new_dist
                        best_neighbor = new_tour
                        best_move = move

        if best_neighbor is None:
            break

        current_tour = best_neighbor
        tabu_list.append(best_move)  # type: ignore[arg-type]
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        if best_neighbor_dist < best_dist:
            best_dist = best_neighbor_dist
            best_tour = best_neighbor[:]

    return best_tour, best_dist


# ---------------------------------------------------------------------------
# Variant 2 — networkx greedy TSP + Christofides
# ---------------------------------------------------------------------------


def networkx_tsp(
    graph: Graph,
    method: str = "christofides",
) -> tuple[list[str], int]:
    """
    Use networkx.approximation for TSP.

    Methods:
        'christofides' — 1.5x approximation guarantee (requires networkx >= 2.6).
                         Best general-purpose approximation for metric TSP.
        'greedy'       — greedy_tsp; fast O(n^2 log n), no guarantee.
        'sa'           — simulated_annealing_tsp; best quality, slowest.

    Returns:
        (tour, distance)
    """
    import networkx as nx
    from networkx.algorithms import approximation as approx

    G = nx.Graph()
    for u, neighbors in graph.items():
        for v, d in neighbors.items():
            G.add_edge(u, v, weight=d)

    nodes = list(graph.keys())
    start = nodes[0]

    if method == "christofides":
        cycle = approx.christofides(G, weight="weight")
    elif method == "greedy":
        cycle = approx.greedy_tsp(G, weight="weight", source=start)
    elif method == "sa":
        cycle = approx.simulated_annealing_tsp(G, "greedy", weight="weight",
                                                source=start, seed=42)
    else:
        raise ValueError(f"Unknown method: {method}")

    dist = sum(graph[cycle[i]][cycle[i + 1]] for i in range(len(cycle) - 1))
    return cycle, dist


# ---------------------------------------------------------------------------
# Brute-force optimal (for small n only — reference/verification)
# ---------------------------------------------------------------------------


def brute_force_tsp(graph: Graph, start: str) -> tuple[list[str], int]:
    """
    Brute-force TSP: try all permutations.
    O(n!) — only feasible for n <= 10.
    Used to verify that other methods find the true optimum.
    """
    other_cities = [c for c in graph if c != start]
    best_dist = math.inf
    best_tour: list[str] = []

    for perm in itertools.permutations(other_cities):
        tour = [start] + list(perm) + [start]
        d = tour_distance(tour, graph)
        if d < best_dist:
            best_dist = d
            best_tour = tour

    return best_tour, int(best_dist)


# ---------------------------------------------------------------------------
# Run all
# ---------------------------------------------------------------------------


def run_all(data_file: str = "searches/tabudata2.txt") -> None:
    graph, start = load_graph(data_file)
    nodes = list(graph.keys())
    n = len(nodes)
    print(f"\nGraph: {n} cities, start='{start}'")
    print(f"Cities: {nodes}")

    # --- Brute force optimal (ground truth) --------------------------------
    opt_tour, opt_dist = brute_force_tsp(graph, start)
    print(f"\nBrute-force optimal:     dist={opt_dist}  tour={opt_tour}")

    # --- Reference tabu search (1-1 swap) ----------------------------------
    from searches.tabu_search import (
        generate_neighbours,
        generate_first_solution,
        tabu_search,
    )
    neighbours = generate_neighbours(data_file)
    first_sol, first_dist = generate_first_solution(data_file, neighbours)
    ref_tour, ref_dist = tabu_search(first_sol, first_dist, neighbours, iters=10, size=5)
    print(f"Reference TS (1-1 swap): dist={ref_dist}  tour={ref_tour}")

    # --- 2-opt tabu search -------------------------------------------------
    ts2_tour, ts2_dist = tabu_search_2opt(graph, start, iters=50, tabu_size=10)
    print(f"TS 2-opt:                dist={ts2_dist}  tour={ts2_tour}")

    # --- networkx ----------------------------------------------------------
    try:
        nx_chr_tour, nx_chr_dist = networkx_tsp(graph, method="christofides")
        print(f"networkx christofides:   dist={nx_chr_dist}  tour={nx_chr_tour}")

        nx_sa_tour, nx_sa_dist = networkx_tsp(graph, method="sa")
        print(f"networkx SA-TSP:         dist={nx_sa_dist}  tour={nx_sa_tour}")
    except ImportError:
        print("networkx not installed -- skipping")

    # --- Benchmark ---------------------------------------------------------
    REPS = 200
    print(f"\n=== Benchmark ({REPS} runs each) ===")

    t1 = timeit.timeit(
        lambda: tabu_search(
            *generate_first_solution(data_file, neighbours),
            neighbours, 10, 5
        ),
        number=REPS,
    )
    print(f"  Reference TS (1-1 swap):  {t1*1000/REPS:7.3f} ms/run")

    t2 = timeit.timeit(
        lambda: tabu_search_2opt(graph, start, iters=50, tabu_size=10),
        number=REPS,
    )
    print(f"  TS 2-opt (50 iters):      {t2*1000/REPS:7.3f} ms/run")

    try:
        import networkx  # noqa: F401
        t3 = timeit.timeit(
            lambda: networkx_tsp(graph, method="christofides"),
            number=REPS,
        )
        print(f"  networkx christofides:    {t3*1000/REPS:7.3f} ms/run")

        t4 = timeit.timeit(
            lambda: networkx_tsp(graph, method="greedy"),
            number=REPS,
        )
        print(f"  networkx greedy_tsp:      {t4*1000/REPS:7.3f} ms/run")
    except ImportError:
        print("  networkx not installed -- skipping benchmark")


if __name__ == "__main__":
    run_all()
