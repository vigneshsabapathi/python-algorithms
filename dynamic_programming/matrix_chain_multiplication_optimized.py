#!/usr/bin/env python3
"""
Optimized and alternative implementations of Matrix Chain Multiplication.

Three variants:
  bottom_up       — O(n^3) iterative DP (reference)
  top_down_cache  — @cache recursive (reference)
  with_parens     — returns optimal parenthesization string

Run:
    python dynamic_programming/matrix_chain_multiplication_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from functools import cache

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.matrix_chain_multiplication import (
    matrix_chain_multiply as ref_bu,
    matrix_chain_order as ref_td,
)


# ---------------------------------------------------------------------------
# Variant 1 — bottom_up (same as reference)
# ---------------------------------------------------------------------------

def bottom_up(arr: list[int]) -> int:
    """
    >>> bottom_up([1, 2, 3, 4, 3])
    30
    """
    return ref_bu(arr)


# ---------------------------------------------------------------------------
# Variant 2 — top_down_cache (same as reference)
# ---------------------------------------------------------------------------

def top_down_cache(arr: list[int]) -> int:
    """
    >>> top_down_cache([1, 2, 3, 4, 3])
    30
    """
    return ref_td(arr)


# ---------------------------------------------------------------------------
# Variant 3 — with_parenthesization: Returns cost + optimal grouping
# ---------------------------------------------------------------------------

def with_parenthesization(arr: list[int]) -> tuple[int, str]:
    """
    Returns (min_cost, parenthesization_string).

    >>> with_parenthesization([1, 2, 3, 4, 3])
    (30, '((A1(A2A3))A4)')
    >>> with_parenthesization([10])
    (0, '')
    >>> with_parenthesization([10, 20])
    (0, 'A1')
    """
    if len(arr) < 2:
        return 0, ""
    if len(arr) == 2:
        return 0, "A1"

    n = len(arr)
    INF = float("inf")
    dp = [[INF] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]

    for i in range(1, n):
        dp[i][i] = 0

    for length in range(2, n):
        for i in range(1, n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + arr[i - 1] * arr[k] * arr[j]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    split[i][j] = k

    def build(i: int, j: int) -> str:
        if i == j:
            return f"A{i}"
        k = split[i][j]
        left = build(i, k)
        right = build(k + 1, j)
        return f"({left}{right})"

    return int(dp[1][n - 1]), build(1, n - 1)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([1, 2, 3, 4, 3], 30),
    ([40, 20, 30, 10, 30], 26000),
    ([10, 20, 30, 40, 30], 30000),
    ([19, 2, 19], 722),
    ([10], 0),
    ([10, 20], 0),
]

IMPLS = [
    ("bottom_up", bottom_up),
    ("top_down_cache", top_down_cache),
    ("with_parens", lambda arr: with_parenthesization(arr)[0]),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for arr, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(arr)
            ok = result == expected
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}({arr}) = {result}")

    print(f"\n=== Parenthesization examples ===")
    for arr in [[1, 2, 3, 4, 3], [40, 20, 30, 10, 30]]:
        cost, parens = with_parenthesization(arr)
        print(f"  MCM({arr}) = {cost}, grouping = {parens}")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    REPS = 10_000
    arr = list(range(1, 20))
    print(f"\n=== Benchmark ({len(arr)} matrices): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(arr), number=REPS) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
