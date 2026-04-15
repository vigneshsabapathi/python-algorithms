#!/usr/bin/env python3
"""
Optimized and alternative implementations of Tribonacci.

Variants covered:
1. tribonacci_dp_array   -- explicit DP array
2. tribonacci_matrix     -- matrix exponentiation O(log n)
3. tribonacci_recursive  -- memoized recursion

Run:
    python dynamic_programming/tribonacci_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.tribonacci import tribonacci as reference


# ---------------------------------------------------------------------------
# Variant 1 — DP array
# ---------------------------------------------------------------------------

def tribonacci_dp_array(n: int) -> int:
    """
    Tribonacci using explicit DP array.

    >>> [tribonacci_dp_array(i) for i in range(10)]
    [0, 0, 1, 1, 2, 4, 7, 13, 24, 44]
    >>> tribonacci_dp_array(25)
    755476
    """
    if n < 2:
        return 0
    if n == 2:
        return 1
    dp = [0] * (n + 1)
    dp[2] = 1
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2] + dp[i - 3]
    return dp[n]


# ---------------------------------------------------------------------------
# Variant 2 — Matrix exponentiation O(log n)
# ---------------------------------------------------------------------------

def tribonacci_matrix(n: int) -> int:
    """
    Tribonacci using matrix exponentiation.

    [T(n+2)]   [1 1 1]^n   [1]
    [T(n+1)] = [1 0 0]   * [0]
    [T(n)  ]   [0 1 0]     [0]

    >>> [tribonacci_matrix(i) for i in range(10)]
    [0, 0, 1, 1, 2, 4, 7, 13, 24, 44]
    >>> tribonacci_matrix(25)
    755476
    """
    if n < 2:
        return 0
    if n == 2:
        return 1

    def mat_mult(A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
        size = len(A)
        C = [[0] * size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def mat_pow(M: list[list[int]], p: int) -> list[list[int]]:
        size = len(M)
        result = [[int(i == j) for j in range(size)] for i in range(size)]
        while p > 0:
            if p % 2 == 1:
                result = mat_mult(result, M)
            M = mat_mult(M, M)
            p //= 2
        return result

    base = [[1, 1, 1], [1, 0, 0], [0, 1, 0]]
    result = mat_pow(base, n - 2)
    return result[0][0]


# ---------------------------------------------------------------------------
# Variant 3 — Memoized recursion
# ---------------------------------------------------------------------------

def tribonacci_recursive(n: int) -> int:
    """
    Tribonacci using memoized recursion.

    >>> [tribonacci_recursive(i) for i in range(10)]
    [0, 0, 1, 1, 2, 4, 7, 13, 24, 44]
    >>> tribonacci_recursive(25)
    755476
    """
    @lru_cache(maxsize=None)
    def dp(k: int) -> int:
        if k < 2:
            return 0
        if k == 2:
            return 1
        return dp(k - 1) + dp(k - 2) + dp(k - 3)

    result = dp(n)
    dp.cache_clear()
    return result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_VALS = list(range(15)) + [25]

IMPLS = [
    ("reference", reference),
    ("dp_array", tribonacci_dp_array),
    ("matrix", tribonacci_matrix),
    ("recursive", tribonacci_recursive),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for n in TEST_VALS:
        results = {name: fn(n) for name, fn in IMPLS}
        expected = results["reference"]
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] T({n:>2}) = {expected}")

    REPS = 50_000
    bench_n = 30
    print(f"\n=== Benchmark: {REPS} runs, n={bench_n} ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(bench_n), number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
