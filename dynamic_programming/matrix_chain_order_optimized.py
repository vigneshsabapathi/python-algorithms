#!/usr/bin/env python3
"""
Optimized and alternative implementations of Matrix Chain Order.

This variant returns BOTH the cost matrix and the split matrix
(enabling reconstruction of the optimal parenthesization),
unlike matrix_chain_multiplication which only returns the min cost.

Three variants:
  bottom_up_tables   — iterative DP, returns (cost, split) tables (reference)
  top_down_tables    — recursive with memo, fills both tables
  reconstruct_parens — walks split matrix to build parenthesization string

Run:
    python dynamic_programming/matrix_chain_order_optimized.py
"""

from __future__ import annotations

import os
import random
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.matrix_chain_order import (
    matrix_chain_order as ref_order,
    print_optimal_solution as ref_print,
)


# ---------------------------------------------------------------------------
# Variant 1 — bottom_up_tables (reference)
# ---------------------------------------------------------------------------

def bottom_up_tables(
    arr: list[int],
) -> tuple[list[list[int]], list[list[int]]]:
    """
    >>> m, s = bottom_up_tables([10, 30, 5])
    >>> m[1][2]
    1500
    """
    return ref_order(arr)


# ---------------------------------------------------------------------------
# Variant 2 — top_down_tables (memoized recursion)
# ---------------------------------------------------------------------------

def top_down_tables(
    arr: list[int],
) -> tuple[list[list[int]], list[list[int]]]:
    """
    >>> m, s = top_down_tables([10, 30, 5])
    >>> m[1][2]
    1500
    """
    n = len(arr)
    INF = sys.maxsize
    cost = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]

    def solve(i: int, j: int) -> int:
        if i >= j:
            return 0
        if cost[i][j] != 0:
            return cost[i][j]
        best = INF
        best_k = i
        for k in range(i, j):
            c = solve(i, k) + solve(k + 1, j) + arr[i - 1] * arr[k] * arr[j]
            if c < best:
                best = c
                best_k = k
        cost[i][j] = best
        split[i][j] = best_k
        return best

    solve(1, n - 1)
    return cost, split


# ---------------------------------------------------------------------------
# Variant 3 — reconstruct_parens (walk the split matrix)
# ---------------------------------------------------------------------------

def reconstruct_parens(arr: list[int]) -> str:
    """
    >>> reconstruct_parens([30, 35, 15, 5, 10, 20, 25])
    '( ( A1 ( A2 A3 ) ) ( ( A4 A5 ) A6 ) )'
    """
    _, split = ref_order(arr)
    return ref_print(split, 1, len(arr) - 1)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def _bench() -> None:
    random.seed(0)
    arr = [random.randint(5, 50) for _ in range(25)]
    n_runs = 20

    print(f"Benchmark on chain of {len(arr) - 1} matrices, {n_runs} runs:\n")
    for name, fn in [
        ("bottom_up_tables", bottom_up_tables),
        ("top_down_tables ", top_down_tables),
    ]:
        t = timeit.timeit(lambda f=fn: f(arr), number=n_runs) / n_runs
        print(f"  {name}: {t * 1000:8.3f} ms / call")

    print("\nOptimal parenthesization for [30,35,15,5,10,20,25]:")
    print(" ", reconstruct_parens([30, 35, 15, 5, 10, 20, 25]))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.\n")
    _bench()
