#!/usr/bin/env python3
"""
Optimized and alternative implementations of Fractional Knapsack.

The reference sorts by value/weight ratio descending and greedily fills.

Variants covered:
1. sort_ratio      -- sort by value/weight descending (reference)
2. heap_based      -- use max-heap for ratio ordering
3. enumerate_idx   -- index-preserving variant (tracks which items taken)
4. one_liner       -- compact functional style

Key interview insight:
    Fractional knapsack is solvable optimally with greedy (unlike 0/1 knapsack
    which requires DP). The key is that we CAN take fractions, so always
    choosing the best ratio first is provably optimal.

Run:
    python greedy_methods/fractional_knapsack_optimized.py
"""

from __future__ import annotations

import heapq
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from greedy_methods.fractional_knapsack import fractional_knapsack as reference


# ---------------------------------------------------------------------------
# Variant 1 — sort by ratio (reference, explicit)
# ---------------------------------------------------------------------------

def sort_ratio(values: list[int], weights: list[int], capacity: int) -> float:
    """
    Sort items by value/weight ratio descending, fill greedily.

    >>> sort_ratio([60, 100, 120], [10, 20, 30], 50)
    240.0
    >>> sort_ratio([500], [30], 10)
    166.66666666666666
    >>> sort_ratio([], [], 50)
    0.0
    """
    items = sorted(zip(values, weights), key=lambda x: x[0] / x[1], reverse=True)
    total = 0.0
    remaining = capacity
    for v, w in items:
        if remaining <= 0:
            break
        take = min(w, remaining)
        total += v * (take / w)
        remaining -= take
    return total


# ---------------------------------------------------------------------------
# Variant 2 — max-heap based (negate for max-heap via heapq)
# ---------------------------------------------------------------------------

def heap_based(values: list[int], weights: list[int], capacity: int) -> float:
    """
    Use a max-heap (negated min-heap) of ratios. Pop best ratio item each time.

    >>> heap_based([60, 100, 120], [10, 20, 30], 50)
    240.0
    >>> heap_based([500], [30], 10)
    166.66666666666666
    >>> heap_based([], [], 50)
    0.0
    """
    heap = [(-v / w, v, w) for v, w in zip(values, weights) if w > 0]
    heapq.heapify(heap)
    total = 0.0
    remaining = capacity
    while remaining > 0 and heap:
        _, v, w = heapq.heappop(heap)
        take = min(w, remaining)
        total += v * (take / w)
        remaining -= take
    return total


# ---------------------------------------------------------------------------
# Variant 3 — index-preserving: tracks which items (and fractions) taken
# ---------------------------------------------------------------------------

def enumerate_idx(
    values: list[int], weights: list[int], capacity: int
) -> tuple[float, list[tuple[int, float]]]:
    """
    Returns (total_value, [(item_index, fraction_taken), ...]).
    Useful for interview follow-up: "which items did you pick?"

    >>> val, items = enumerate_idx([60, 100, 120], [10, 20, 30], 50)
    >>> val
    240.0
    >>> items
    [(0, 1.0), (1, 1.0), (2, 0.6666666666666666)]
    """
    indexed = sorted(
        enumerate(zip(values, weights)),
        key=lambda x: x[1][0] / x[1][1] if x[1][1] > 0 else float("inf"),
        reverse=True,
    )
    total = 0.0
    remaining = capacity
    taken: list[tuple[int, float]] = []
    for idx, (v, w) in indexed:
        if remaining <= 0:
            break
        take = min(w, remaining)
        fraction = take / w
        total += v * fraction
        taken.append((idx, fraction))
        remaining -= take
    return total, taken


# ---------------------------------------------------------------------------
# Variant 4 — one-liner (compact functional)
# ---------------------------------------------------------------------------

def one_liner(values: list[int], weights: list[int], capacity: int) -> float:
    """
    Compact functional approach using reduce-style accumulation.

    >>> one_liner([60, 100, 120], [10, 20, 30], 50)
    240.0
    >>> one_liner([500], [30], 10)
    166.66666666666666
    >>> one_liner([], [], 50)
    0.0
    """
    items = sorted(zip(values, weights), key=lambda x: x[0] / x[1], reverse=True)
    result, rem = 0.0, capacity
    for v, w in items:
        if rem <= 0:
            break
        t = min(w, rem)
        result += v * t / w
        rem -= t
    return result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([60, 100, 120], [10, 20, 30], 50, 240.0),
    ([500], [30], 10, 166.66666666666666),
    ([10, 20, 30], [5, 10, 15], 15, 30.0),
    ([], [], 50, 0.0),
    ([60, 100], [10, 20], 0, 0.0),
    ([60, 100, 120], [10, 20, 30], 60, 280.0),
]

IMPLS_SIMPLE = [
    ("reference",   reference),
    ("sort_ratio",  sort_ratio),
    ("heap_based",  heap_based),
    ("one_liner",   one_liner),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for vals, wts, cap, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS_SIMPLE:
            try:
                results[name] = fn(vals, wts, cap)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] cap={cap} expected={expected} results={results}")

    # Also test enumerate_idx
    val, items = enumerate_idx([60, 100, 120], [10, 20, 30], 50)
    print(f"\n  enumerate_idx: value={val}, items={items}")

    import random
    random.seed(42)
    big_v = [random.randint(1, 100) for _ in range(1000)]
    big_w = [random.randint(1, 50) for _ in range(1000)]
    big_cap = 500

    REPS = 10_000
    print(f"\n=== Benchmark (1000 items, cap=500): {REPS} runs ===")
    for name, fn in IMPLS_SIMPLE:
        t = timeit.timeit(lambda fn=fn: fn(big_v, big_w, big_cap), number=REPS) * 1000 / REPS
        print(f"  {name:<14} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
