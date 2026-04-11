#!/usr/bin/env python3
"""
Optimized and alternative implementations of Fractional Cover Problem.

The reference uses greedy selection by cost-effectiveness ratio.

Variants covered:
1. greedy_ratio     -- pick most cost-effective set (reference)
2. greedy_largest   -- pick set covering most uncovered elements
3. weighted_greedy  -- weighted cost-effectiveness with tie-breaking
4. sorted_precomp   -- precompute ratios, sort once, re-evaluate

Key interview insight:
    Greedy set cover gives O(ln n) approximation to the NP-hard minimum
    set cover problem. This is the best polynomial-time guarantee unless P=NP.

Run:
    python greedy_methods/fractional_cover_problem_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from greedy_methods.fractional_cover_problem import fractional_cover as reference


# ---------------------------------------------------------------------------
# Variant 1 — greedy by cost/coverage ratio (reference)
# ---------------------------------------------------------------------------

def greedy_ratio(
    universe: set[int], subsets: list[set[int]], costs: list[float]
) -> float:
    """
    Pick the set with lowest cost per newly covered element.

    >>> greedy_ratio({1,2,3,4,5}, [{1,2,3},{2,4},{3,4,5}], [5,10,3])
    8.0
    >>> greedy_ratio({1,2,3}, [{1,2},{2,3},{1,3}], [1,1,1])
    2.0
    >>> greedy_ratio(set(), [], [])
    0.0
    """
    uncovered = set(universe)
    total_cost = 0.0
    while uncovered:
        best_idx, best_ratio = -1, float("inf")
        for i, (s, c) in enumerate(zip(subsets, costs)):
            covered = s & uncovered
            if covered:
                ratio = c / len(covered)
                if ratio < best_ratio:
                    best_ratio = ratio
                    best_idx = i
        if best_idx == -1:
            break
        uncovered -= subsets[best_idx]
        total_cost += costs[best_idx]
    return total_cost


# ---------------------------------------------------------------------------
# Variant 2 — greedy by largest coverage (ignore cost)
# ---------------------------------------------------------------------------

def greedy_largest(
    universe: set[int], subsets: list[set[int]], costs: list[float]
) -> float:
    """
    Always pick the set that covers the most uncovered elements.
    Ignores cost — useful when all sets have equal cost.

    >>> greedy_largest({1,2,3,4,5}, [{1,2,3},{2,4},{3,4,5}], [5,10,3])
    8.0
    >>> greedy_largest(set(), [], [])
    0.0
    """
    uncovered = set(universe)
    total_cost = 0.0
    while uncovered:
        best_idx, best_count = -1, 0
        for i, s in enumerate(subsets):
            count = len(s & uncovered)
            if count > best_count:
                best_count = count
                best_idx = i
        if best_idx == -1:
            break
        uncovered -= subsets[best_idx]
        total_cost += costs[best_idx]
    return total_cost


# ---------------------------------------------------------------------------
# Variant 3 — weighted greedy with tie-breaking by set size
# ---------------------------------------------------------------------------

def weighted_greedy(
    universe: set[int], subsets: list[set[int]], costs: list[float]
) -> float:
    """
    Cost-effectiveness ratio with tie-breaking: prefer larger sets.

    >>> weighted_greedy({1,2,3,4,5}, [{1,2,3},{2,4},{3,4,5}], [5,10,3])
    8.0
    >>> weighted_greedy({1,2,3}, [{1,2},{2,3},{1,3}], [1,1,1])
    2.0
    """
    uncovered = set(universe)
    total_cost = 0.0
    while uncovered:
        best_idx = -1
        best_key = (float("inf"), 0)  # (ratio, -coverage)
        for i, (s, c) in enumerate(zip(subsets, costs)):
            covered = s & uncovered
            if covered:
                key = (c / len(covered), -len(covered))
                if key < best_key:
                    best_key = key
                    best_idx = i
        if best_idx == -1:
            break
        uncovered -= subsets[best_idx]
        total_cost += costs[best_idx]
    return total_cost


# ---------------------------------------------------------------------------
# Variant 4 — sorted precompute: sort by ratio, re-evaluate
# ---------------------------------------------------------------------------

def sorted_precomp(
    universe: set[int], subsets: list[set[int]], costs: list[float]
) -> float:
    """
    Precompute initial ratios, sort, then re-evaluate on each pick.

    >>> sorted_precomp({1,2,3,4,5}, [{1,2,3},{2,4},{3,4,5}], [5,10,3])
    8.0
    >>> sorted_precomp(set(), [], [])
    0.0
    """
    uncovered = set(universe)
    total_cost = 0.0
    # Initial sort by cost/|set| ratio
    indices = sorted(
        range(len(subsets)),
        key=lambda i: costs[i] / len(subsets[i]) if subsets[i] else float("inf"),
    )
    used = set()
    while uncovered:
        best_idx = -1
        best_ratio = float("inf")
        for i in indices:
            if i in used:
                continue
            covered = subsets[i] & uncovered
            if covered:
                ratio = costs[i] / len(covered)
                if ratio < best_ratio:
                    best_ratio = ratio
                    best_idx = i
        if best_idx == -1:
            break
        used.add(best_idx)
        uncovered -= subsets[best_idx]
        total_cost += costs[best_idx]
    return total_cost


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ({1, 2, 3, 4, 5}, [{1, 2, 3}, {2, 4}, {3, 4, 5}], [5, 10, 3]),
    ({1, 2, 3}, [{1, 2}, {2, 3}, {1, 3}], [1, 1, 1]),
    ({1}, [{1}], [7]),
    (set(), [], []),
]

EXPECTED_REF = [8.0, 2.0, 7.0, 0.0]

IMPLS = [
    ("reference",       reference),
    ("greedy_ratio",    greedy_ratio),
    ("greedy_largest",  greedy_largest),
    ("weighted_greedy", weighted_greedy),
    ("sorted_precomp",  sorted_precomp),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for (u, s, c), exp in zip(TEST_CASES, EXPECTED_REF):
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(u, s, c)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ref_ok = all(v == exp for v in results.values() if name in ("reference", "greedy_ratio"))
        tag = "OK" if results["reference"] == exp else "FAIL"
        print(f"  [{tag}] universe={u}  ref_expected={exp}  results={results}")

    # Benchmark with larger input
    import random
    random.seed(42)
    big_universe = set(range(100))
    big_subsets = [set(random.sample(range(100), random.randint(5, 20))) for _ in range(50)]
    big_costs = [random.uniform(1, 10) for _ in range(50)]

    REPS = 5_000
    print(f"\n=== Benchmark (100 elements, 50 sets): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: fn(big_universe, big_subsets, big_costs), number=REPS
        ) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
