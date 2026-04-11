#!/usr/bin/env python3
"""
Optimized and alternative implementations of Fractional Knapsack (Greedy).

The reference sorts items by profit/weight ratio and greedily takes the best.

Variants covered:
1. ratio_sort      -- sort by ratio descending, iterate once (reference, clean)
2. heap_topk       -- max-heap by ratio, pop items greedily (good when K << N)
3. enumerate_frac  -- sort + enumerate with remaining tracking (Pythonic)

Key interview insight:
    Fractional knapsack has a greedy O(n log n) solution because you can take
    fractions.  0/1 knapsack does NOT — it requires DP.  Interviewers love
    asking "why can't you use greedy for 0/1?"  The answer: greedy may take a
    high-ratio item that wastes capacity, missing a better combination.

Run:
    python knapsack/greedy_knapsack_optimized.py
"""

from __future__ import annotations

import heapq
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from knapsack.greedy_knapsack import calc_profit as reference


# ---------------------------------------------------------------------------
# Variant 1 — ratio sort (clean rewrite of reference)
# ---------------------------------------------------------------------------

def ratio_sort(profit: list, weight: list, max_weight: int) -> float:
    """
    Sort items by profit-to-weight ratio descending, greedily fill knapsack.

    >>> ratio_sort([60, 100, 120], [10, 20, 30], 50)
    240.0
    >>> ratio_sort([1, 2, 3], [3, 4, 5], 15)
    6.0
    >>> ratio_sort([10, 9, 8], [3, 4, 5], 25)
    27.0
    >>> ratio_sort([5, 4, 8, 6], [1, 2, 4, 5], 5)
    13.0
    """
    items = sorted(
        zip(profit, weight),
        key=lambda x: x[0] / x[1],
        reverse=True,
    )
    remaining = max_weight
    gain = 0.0
    for p, w in items:
        if remaining <= 0:
            break
        take = min(w, remaining)
        gain += (take / w) * p
        remaining -= take
    return gain


# ---------------------------------------------------------------------------
# Variant 2 — max-heap by ratio (useful when only top-K items needed)
# ---------------------------------------------------------------------------

def heap_topk(profit: list, weight: list, max_weight: int) -> float:
    """
    Use a max-heap (negated min-heap) to pop best-ratio items one at a time.

    >>> heap_topk([60, 100, 120], [10, 20, 30], 50)
    240.0
    >>> heap_topk([1, 2, 3], [3, 4, 5], 15)
    6.0
    >>> heap_topk([10, 9, 8], [3, 4, 5], 25)
    27.0
    >>> heap_topk([5, 4, 8, 6], [1, 2, 4, 5], 5)
    13.0
    """
    # Push negative ratio for max-heap behavior
    heap = [(-p / w, p, w) for p, w in zip(profit, weight)]
    heapq.heapify(heap)

    remaining = max_weight
    gain = 0.0
    while heap and remaining > 0:
        _neg_ratio, p, w = heapq.heappop(heap)
        take = min(w, remaining)
        gain += (take / w) * p
        remaining -= take
    return gain


# ---------------------------------------------------------------------------
# Variant 3 — enumerate with Pythonic remaining tracking
# ---------------------------------------------------------------------------

def enumerate_frac(profit: list, weight: list, max_weight: int) -> float:
    """
    Pythonic version using enumerate and early break.

    >>> enumerate_frac([60, 100, 120], [10, 20, 30], 50)
    240.0
    >>> enumerate_frac([1, 2, 3], [3, 4, 5], 15)
    6.0
    >>> enumerate_frac([10, 9, 8], [3, 4, 5], 25)
    27.0
    >>> enumerate_frac([5, 4, 8, 6], [1, 2, 4, 5], 5)
    13.0
    """
    n = len(profit)
    # Create index list sorted by ratio descending
    order = sorted(range(n), key=lambda i: profit[i] / weight[i], reverse=True)

    remaining = float(max_weight)
    gain = 0.0
    for i in order:
        if remaining <= 0:
            break
        fraction = min(1.0, remaining / weight[i])
        gain += fraction * profit[i]
        remaining -= fraction * weight[i]
    return gain


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([60, 100, 120], [10, 20, 30], 50, 240.0),
    ([1, 2, 3], [3, 4, 5], 15, 6.0),
    ([10, 9, 8], [3, 4, 5], 25, 27.0),
    ([5, 4, 8, 6], [1, 2, 4, 5], 5, 13.0),
    ([5, 8, 7, 1, 12, 3, 4], [2, 7, 1, 6, 4, 2, 5], 10, 28.142857142857142),
]

IMPLS = [
    ("reference",      lambda p, w, m: float(reference(p, w, m))),
    ("ratio_sort",     ratio_sort),
    ("heap_topk",      heap_topk),
    ("enumerate_frac", enumerate_frac),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for profit, weight, cap, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(profit, weight, cap)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(abs(v - expected) < 1e-9 if isinstance(v, float) else False
                 for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(
            f"  [{tag}] cap={cap:<4} expected={expected:<20}  "
            + "  ".join(f"{nm}={v}" for nm, v in results.items())
        )

    # Benchmark with larger input
    import random
    random.seed(42)
    n = 500
    profit_big = [random.randint(1, 100) for _ in range(n)]
    weight_big = [random.randint(1, 50) for _ in range(n)]
    cap_big = 1000

    REPS = 5_000
    print(f"\n=== Benchmark: {n} items, cap={cap_big}, {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: fn(profit_big, weight_big, cap_big), number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>8.4f} ms / call")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
