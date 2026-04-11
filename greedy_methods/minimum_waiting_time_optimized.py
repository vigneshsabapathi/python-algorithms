#!/usr/bin/env python3
"""
Optimized and alternative implementations of Minimum Waiting Time.

The reference sorts ascending and computes sum(duration * remaining_queries).

Variants covered:
1. multiply_remaining  -- duration * (n-1-i) for each sorted position (reference)
2. prefix_sum          -- running prefix sum approach
3. sort_descending     -- prove why descending is worst (for comparison)
4. one_liner           -- compact generator expression

Key interview insight:
    Sorting shortest-first is provably optimal by exchange argument: if two
    adjacent queries are out of order (longer before shorter), swapping them
    reduces total wait. This generalizes to: sorted ascending = optimal.

Run:
    python greedy_methods/minimum_waiting_time_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from greedy_methods.minimum_waiting_time import minimum_waiting_time as reference


# ---------------------------------------------------------------------------
# Variant 1 — multiply by remaining count (reference)
# ---------------------------------------------------------------------------

def multiply_remaining(queries: list[int]) -> int:
    """
    Sort ascending, each query at index i makes (n-1-i) others wait.

    >>> multiply_remaining([3, 2, 1, 2, 6])
    17
    >>> multiply_remaining([1, 2, 3])
    4
    >>> multiply_remaining([5])
    0
    >>> multiply_remaining([])
    0
    """
    sorted_q = sorted(queries)
    n = len(sorted_q)
    return sum(d * (n - 1 - i) for i, d in enumerate(sorted_q))


# ---------------------------------------------------------------------------
# Variant 2 — prefix sum: total wait = sum of prefix sums
# ---------------------------------------------------------------------------

def prefix_sum(queries: list[int]) -> int:
    """
    Sort ascending. Each query waits for the sum of all previous queries.
    Total wait = sum of all prefix sums (excluding last element's prefix).

    >>> prefix_sum([3, 2, 1, 2, 6])
    17
    >>> prefix_sum([1, 2, 3])
    4
    >>> prefix_sum([5])
    0
    >>> prefix_sum([])
    0
    """
    sorted_q = sorted(queries)
    total_wait = 0
    running_sum = 0
    for i in range(len(sorted_q) - 1):
        running_sum += sorted_q[i]
        total_wait += running_sum
    return total_wait


# ---------------------------------------------------------------------------
# Variant 3 — descending sort (worst case, for comparison)
# ---------------------------------------------------------------------------

def sort_descending(queries: list[int]) -> int:
    """
    Sort DESCENDING — gives MAXIMUM waiting time. Useful to show
    the contrast with optimal (ascending).

    >>> sort_descending([3, 2, 1, 2, 6])
    39
    >>> sort_descending([1, 2, 3])
    8
    >>> sort_descending([5])
    0
    """
    sorted_q = sorted(queries, reverse=True)
    n = len(sorted_q)
    return sum(d * (n - 1 - i) for i, d in enumerate(sorted_q))


# ---------------------------------------------------------------------------
# Variant 4 — one-liner generator expression
# ---------------------------------------------------------------------------

def one_liner(queries: list[int]) -> int:
    """
    Compact one-liner using sorted + enumerate + generator.

    >>> one_liner([3, 2, 1, 2, 6])
    17
    >>> one_liner([1, 2, 3])
    4
    >>> one_liner([5])
    0
    >>> one_liner([])
    0
    """
    s = sorted(queries)
    return sum(d * (len(s) - 1 - i) for i, d in enumerate(s))


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([3, 2, 1, 2, 6], 17),
    ([1, 2, 3], 4),
    ([5], 0),
    ([], 0),
    ([1, 1, 1, 1], 6),
    ([5, 1], 1),
    ([10, 20, 30, 40], 100),
]

IMPLS = [
    ("reference",           reference),
    ("multiply_remaining",  multiply_remaining),
    ("prefix_sum",          prefix_sum),
    ("one_liner",           one_liner),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for queries, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(queries)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] queries={str(queries):<22} expected={expected}")

    # Show best vs worst
    print("\n=== Best vs Worst Ordering ===")
    for queries in [[3, 2, 1, 2, 6], [10, 20, 30, 40]]:
        best = multiply_remaining(queries)
        worst = sort_descending(queries)
        print(f"  queries={queries}  best={best}  worst={worst}  ratio={worst/best if best else 'inf':.2f}x")

    import random
    random.seed(42)
    big = [random.randint(1, 100) for _ in range(10_000)]

    REPS = 5_000
    print(f"\n=== Benchmark (10k queries): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(big), number=REPS) * 1000 / REPS
        print(f"  {name:<22} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
