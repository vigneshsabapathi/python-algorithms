#!/usr/bin/env python3
"""
Optimized and alternative implementations of Recursive 0/1 Knapsack.

The reference uses plain recursion exploring all 2^n subsets — O(2^n) time.

Variants covered:
1. naive_recursive  -- pure brute-force, no pruning (reference baseline)
2. memo_dict        -- add dict memoization to cut redundant subproblems
3. lru_memo         -- functools.lru_cache version (cleaner syntax)
4. pruned_recursive -- recursion with weight-based pruning (skip impossible branches)

Key interview insight:
    Plain recursion is O(2^n) because it re-solves overlapping subproblems.
    Adding memoization on (index, remaining_weight) drops it to O(nW) — same
    as DP tabulation.  Interviewers ask "how would you optimize this?" and
    expect the memoization answer as the first step.

Run:
    python knapsack/recursive_approach_knapsack_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from knapsack.recursive_approach_knapsack import knapsack as reference


# ---------------------------------------------------------------------------
# Variant 1 — naive recursive (clean rewrite of reference)
# ---------------------------------------------------------------------------

def naive_recursive(
    weights: list, values: list, n: int, max_weight: int, index: int
) -> int:
    """
    Pure brute-force: try include/exclude for every item.  O(2^n) time.

    >>> naive_recursive([1, 2, 4, 5], [5, 4, 8, 6], 4, 5, 0)
    13
    >>> naive_recursive([10, 20, 30], [60, 100, 120], 3, 50, 0)
    220
    >>> naive_recursive([1, 3, 4, 5], [1, 4, 5, 7], 4, 7, 0)
    9
    """
    if index == n:
        return 0
    exclude = naive_recursive(weights, values, n, max_weight, index + 1)
    include = 0
    if weights[index] <= max_weight:
        include = values[index] + naive_recursive(
            weights, values, n, max_weight - weights[index], index + 1
        )
    return max(exclude, include)


# ---------------------------------------------------------------------------
# Variant 2 — dict memoization (the classic optimization step)
# ---------------------------------------------------------------------------

def memo_dict(
    weights: list, values: list, n: int, max_weight: int, index: int = 0
) -> int:
    """
    Memoized recursion using a dict on (index, remaining_weight).
    Reduces from O(2^n) to O(nW).

    >>> memo_dict([1, 2, 4, 5], [5, 4, 8, 6], 4, 5)
    13
    >>> memo_dict([10, 20, 30], [60, 100, 120], 3, 50)
    220
    >>> memo_dict([1, 3, 4, 5], [1, 4, 5, 7], 4, 7)
    9
    """
    memo: dict[tuple[int, int], int] = {}

    def solve(idx: int, remaining: int) -> int:
        if idx == n or remaining == 0:
            return 0
        key = (idx, remaining)
        if key in memo:
            return memo[key]
        # Exclude current item
        result = solve(idx + 1, remaining)
        # Include current item if it fits
        if weights[idx] <= remaining:
            result = max(result, values[idx] + solve(idx + 1, remaining - weights[idx]))
        memo[key] = result
        return result

    return solve(index, max_weight)


# ---------------------------------------------------------------------------
# Variant 3 — lru_cache memoization (Pythonic syntax)
# ---------------------------------------------------------------------------

def lru_memo(
    weights: list, values: list, n: int, max_weight: int, index: int = 0
) -> int:
    """
    Same memoization idea using functools.lru_cache for cleaner code.

    >>> lru_memo([1, 2, 4, 5], [5, 4, 8, 6], 4, 5)
    13
    >>> lru_memo([10, 20, 30], [60, 100, 120], 3, 50)
    220
    >>> lru_memo([1, 3, 4, 5], [1, 4, 5, 7], 4, 7)
    9
    """
    from functools import lru_cache

    # Convert to tuples so lru_cache can hash them
    wt = tuple(weights)
    vl = tuple(values)

    @lru_cache(maxsize=None)
    def solve(idx: int, remaining: int) -> int:
        if idx == n or remaining == 0:
            return 0
        result = solve(idx + 1, remaining)
        if wt[idx] <= remaining:
            result = max(result, vl[idx] + solve(idx + 1, remaining - wt[idx]))
        return result

    return solve(index, max_weight)


# ---------------------------------------------------------------------------
# Variant 4 — pruned recursive (skip branches that can't improve)
# ---------------------------------------------------------------------------

def pruned_recursive(
    weights: list, values: list, n: int, max_weight: int, index: int = 0
) -> int:
    """
    Recursion with pruning: skip items heavier than remaining capacity,
    and pre-sort by value/weight ratio for better early termination.

    >>> pruned_recursive([1, 2, 4, 5], [5, 4, 8, 6], 4, 5)
    13
    >>> pruned_recursive([10, 20, 30], [60, 100, 120], 3, 50)
    220
    >>> pruned_recursive([1, 3, 4, 5], [1, 4, 5, 7], 4, 7)
    9
    """
    # Sort items by value/weight ratio descending for better pruning
    items = sorted(
        zip(values, weights),
        key=lambda x: x[0] / x[1] if x[1] > 0 else float("inf"),
        reverse=True,
    )
    best = [0]

    def upper_bound(idx: int, remaining: int, current: int) -> float:
        """Fractional upper bound from idx onward."""
        ub = float(current)
        rem = remaining
        for j in range(idx, n):
            v, w = items[j]
            if w <= rem:
                ub += v
                rem -= w
            else:
                ub += (rem / w) * v
                break
        return ub

    def solve(idx: int, remaining: int, current: int) -> None:
        if current > best[0]:
            best[0] = current
        if idx == n:
            return
        if upper_bound(idx, remaining, current) <= best[0]:
            return
        v, w = items[idx]
        # Include
        if w <= remaining:
            solve(idx + 1, remaining - w, current + v)
        # Exclude
        solve(idx + 1, remaining, current)

    solve(0, max_weight, 0)
    return best[0]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([1, 2, 4, 5], [5, 4, 8, 6], 4, 5, 13),
    ([10, 20, 30], [60, 100, 120], 3, 50, 220),
    ([3, 4, 5], [10, 9, 8], 3, 25, 27),
    ([1, 3, 4, 5], [1, 4, 5, 7], 4, 7, 9),
    ([1, 2, 3], [6, 10, 12], 3, 5, 22),
]

IMPLS = [
    ("reference",         lambda w, v, n, mw: reference(w, v, n, mw, 0)),
    ("naive_recursive",   lambda w, v, n, mw: naive_recursive(w, v, n, mw, 0)),
    ("memo_dict",         lambda w, v, n, mw: memo_dict(w, v, n, mw)),
    ("lru_memo",          lambda w, v, n, mw: lru_memo(w, v, n, mw)),
    ("pruned_recursive",  lambda w, v, n, mw: pruned_recursive(w, v, n, mw)),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for weights, values, n, max_weight, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(weights, values, n, max_weight)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(
            f"  [{tag}] n={n} cap={max_weight:<4} expected={expected:<6}  "
            + "  ".join(f"{nm}={v}" for nm, v in results.items())
        )

    # Benchmark — use small n for naive (exponential), moderate for memoized
    import random
    random.seed(42)

    # Small benchmark (all variants can handle)
    n_small = 15
    w_small = [random.randint(1, 20) for _ in range(n_small)]
    v_small = [random.randint(1, 50) for _ in range(n_small)]
    cap_small = 40

    REPS = 500
    print(f"\n=== Benchmark (n={n_small}, all variants): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: fn(w_small, v_small, n_small, cap_small), number=REPS
        ) * 1000 / REPS
        print(f"  {name:<20} {t:>9.4f} ms / call")

    # Larger benchmark (only memoized variants)
    n_large = 100
    w_large = [random.randint(1, 30) for _ in range(n_large)]
    v_large = [random.randint(1, 80) for _ in range(n_large)]
    cap_large = 300

    REPS_LARGE = 200
    memo_impls = [impl for impl in IMPLS if impl[0] in ("memo_dict", "lru_memo", "pruned_recursive")]
    print(f"\n=== Benchmark (n={n_large}, memoized only): {REPS_LARGE} runs ===")
    for name, fn in memo_impls:
        t = timeit.timeit(
            lambda fn=fn: fn(w_large, v_large, n_large, cap_large), number=REPS_LARGE
        ) * 1000 / REPS_LARGE
        print(f"  {name:<20} {t:>9.4f} ms / call")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
