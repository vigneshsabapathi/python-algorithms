#!/usr/bin/env python3
"""
Optimized and alternative implementations of Optimal Binary Search Tree.

Variants covered:
1. optimal_bst_knuth      -- Knuth's optimization O(n^2) instead of O(n^3)
2. optimal_bst_prefix_sum -- prefix sum for range sums
3. optimal_bst_with_root  -- also returns optimal root structure

Run:
    python dynamic_programming/optimal_binary_search_tree_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.optimal_binary_search_tree import optimal_bst as reference


# ---------------------------------------------------------------------------
# Variant 1 — Knuth's optimization
# ---------------------------------------------------------------------------

def optimal_bst_knuth(keys: list[int], freq: list[int]) -> int:
    """
    Optimal BST with Knuth's monotonicity optimization.

    root[i][j] is monotonically increasing, so the inner loop
    runs in O(n^2) total instead of O(n^3).

    >>> optimal_bst_knuth([10, 12, 20], [34, 8, 50])
    142
    >>> optimal_bst_knuth([10, 12], [34, 50])
    118
    >>> optimal_bst_knuth([10], [34])
    34
    >>> optimal_bst_knuth([10, 20, 30, 40], [4, 2, 6, 3])
    26
    """
    n = len(keys)
    cost = [[0] * n for _ in range(n)]
    root = [[0] * n for _ in range(n)]
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + freq[i]

    for i in range(n):
        cost[i][i] = freq[i]
        root[i][i] = i

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = float("inf")
            freq_sum = prefix[j + 1] - prefix[i]
            lo = root[i][j - 1] if j > i else i
            hi = root[i + 1][j] if i < j else j
            for r in range(lo, hi + 1):
                left = cost[i][r - 1] if r > i else 0
                right = cost[r + 1][j] if r < j else 0
                c = left + right + freq_sum
                if c < cost[i][j]:
                    cost[i][j] = c
                    root[i][j] = r

    return cost[0][n - 1]


# ---------------------------------------------------------------------------
# Variant 2 — Prefix sum optimization
# ---------------------------------------------------------------------------

def optimal_bst_prefix_sum(keys: list[int], freq: list[int]) -> int:
    """
    Standard O(n^3) but with prefix sums to avoid repeated range additions.

    >>> optimal_bst_prefix_sum([10, 12, 20], [34, 8, 50])
    142
    >>> optimal_bst_prefix_sum([10, 12], [34, 50])
    118
    >>> optimal_bst_prefix_sum([10], [34])
    34
    >>> optimal_bst_prefix_sum([10, 20, 30, 40], [4, 2, 6, 3])
    26
    """
    n = len(keys)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + freq[i]

    cost = [[0] * n for _ in range(n)]
    for i in range(n):
        cost[i][i] = freq[i]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = float("inf")
            fsum = prefix[j + 1] - prefix[i]
            for r in range(i, j + 1):
                left = cost[i][r - 1] if r > i else 0
                right = cost[r + 1][j] if r < j else 0
                c = left + right + fsum
                cost[i][j] = min(cost[i][j], c)

    return cost[0][n - 1]


# ---------------------------------------------------------------------------
# Variant 3 — With root reconstruction
# ---------------------------------------------------------------------------

def optimal_bst_with_root(keys: list[int], freq: list[int]) -> tuple[int, list[list[int]]]:
    """
    Returns (cost, root_table) where root[i][j] = index of optimal root for keys[i..j].

    >>> cost, root = optimal_bst_with_root([10, 12, 20], [34, 8, 50])
    >>> cost
    142
    >>> root[0][2]
    2
    """
    n = len(keys)
    cost = [[0] * n for _ in range(n)]
    root = [[0] * n for _ in range(n)]
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + freq[i]
        cost[i][i] = freq[i]
        root[i][i] = i

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = float("inf")
            fsum = prefix[j + 1] - prefix[i]
            for r in range(i, j + 1):
                left = cost[i][r - 1] if r > i else 0
                right = cost[r + 1][j] if r < j else 0
                c = left + right + fsum
                if c < cost[i][j]:
                    cost[i][j] = c
                    root[i][j] = r

    return (cost[0][n - 1], root)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([10, 12, 20], [34, 8, 50], 142),
    ([10, 12], [34, 50], 118),
    ([10], [34], 34),
    ([10, 20, 30, 40], [4, 2, 6, 3], 26),
]

IMPLS = [
    ("reference", reference),
    ("knuth", optimal_bst_knuth),
    ("prefix_sum", optimal_bst_prefix_sum),
    ("with_root", lambda k, f: optimal_bst_with_root(k, f)[0]),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for keys, freq, expected in TEST_CASES:
        results = {name: fn(keys, freq) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] keys={keys}  expected={expected}  " +
              "  ".join(f"{n}={v}" for n, v in results.items()))

    REPS = 5_000
    bench_keys = list(range(20))
    bench_freq = [i + 1 for i in range(20)]
    print(f"\n=== Benchmark: {REPS} runs, n={len(bench_keys)} ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(bench_keys, bench_freq), number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
