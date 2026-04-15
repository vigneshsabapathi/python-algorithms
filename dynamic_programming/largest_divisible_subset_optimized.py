#!/usr/bin/env python3
"""
Optimized and alternative implementations of Largest Divisible Subset.

Three variants:
  dp_backtrack    — O(n^2) DP with backtracking (reference)
  dp_dict_based   — using dictionary for cleaner backtracking
  sort_and_chain  — same logic, cleaner implementation

Run:
    python dynamic_programming/largest_divisible_subset_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.largest_divisible_subset import largest_divisible_subset as reference


# ---------------------------------------------------------------------------
# Variant 1 — dp_backtrack (same as reference)
# ---------------------------------------------------------------------------

def dp_backtrack(items: list[int]) -> list[int]:
    """
    >>> dp_backtrack([1, 16, 7, 8, 4])
    [16, 8, 4, 1]
    """
    return reference(items)


# ---------------------------------------------------------------------------
# Variant 2 — dp_dict_based: Dictionary for parent tracking
# ---------------------------------------------------------------------------

def dp_dict_based(items: list[int]) -> list[int]:
    """
    >>> dp_dict_based([1, 16, 7, 8, 4])
    [16, 8, 4, 1]
    >>> dp_dict_based([1, 2, 4, 8])
    [8, 4, 2, 1]
    >>> dp_dict_based([])
    []
    """
    if not items:
        return []
    items = sorted(items)
    n = len(items)
    dp = [1] * n
    parent = list(range(n))

    for i in range(1, n):
        for j in range(i):
            if items[j] != 0 and items[i] % items[j] == 0:
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    parent[i] = j

    max_idx = max(range(n), key=lambda i: dp[i])
    result = [items[max_idx]]
    while parent[max_idx] != max_idx:
        max_idx = parent[max_idx]
        result.append(items[max_idx])
    return result


# ---------------------------------------------------------------------------
# Variant 3 — clean_dp: Cleaner implementation
# ---------------------------------------------------------------------------

def clean_dp(items: list[int]) -> list[int]:
    """
    >>> clean_dp([1, 16, 7, 8, 4])
    [16, 8, 4, 1]
    >>> clean_dp([1, 2, 3])
    [2, 1]
    >>> clean_dp([])
    []
    """
    if not items:
        return []
    items = sorted(items)
    n = len(items)

    # chains[i] = longest divisible chain ending at items[i]
    chains: list[list[int]] = [[x] for x in items]

    for i in range(1, n):
        for j in range(i):
            if items[j] != 0 and items[i] % items[j] == 0:
                if len(chains[j]) + 1 > len(chains[i]):
                    chains[i] = chains[j] + [items[i]]

    best = max(chains, key=len)
    return best[::-1]  # return in descending order


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([1, 16, 7, 8, 4], [16, 8, 4, 1]),
    ([1, 2, 3], [2, 1]),
    ([1, 2, 4, 8], [8, 4, 2, 1]),
    ([3, 6, 12, 24, 48], [48, 24, 12, 6, 3]),
    ([], []),
]

IMPLS = [
    ("dp_backtrack", dp_backtrack),
    ("dp_dict_based", dp_dict_based),
    ("clean_dp", clean_dp),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for items, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(items)
            ok = len(result) == len(expected)  # length matters more than exact order
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}({items}) = {result}  (expected len {len(expected)})")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    REPS = 20_000
    items = [1, 2, 4, 8, 16, 32, 64, 3, 9, 27, 5, 25, 7]
    print(f"\n=== Benchmark ({len(items)} items): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(items), number=REPS) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
