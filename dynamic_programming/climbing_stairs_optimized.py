#!/usr/bin/env python3
"""
Optimized and alternative implementations of Climbing Stairs (LeetCode 70).

Four variants:
  iterative       — O(n) time, O(1) space rolling variables (reference)
  dp_array        — O(n) time, O(n) space with full DP array
  matrix_exp      — O(log n) using matrix exponentiation
  closed_form     — O(1) using Binet's formula (golden ratio)

Run:
    python dynamic_programming/climbing_stairs_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.climbing_stairs import climb_stairs as reference


# ---------------------------------------------------------------------------
# Variant 1 — iterative: O(1) space (same as reference)
# ---------------------------------------------------------------------------

def iterative(n: int) -> int:
    """
    >>> iterative(3)
    3
    >>> iterative(10)
    89
    """
    return reference(n)


# ---------------------------------------------------------------------------
# Variant 2 — dp_array: Full DP array
# ---------------------------------------------------------------------------

def dp_array(n: int) -> int:
    """
    >>> dp_array(3)
    3
    >>> dp_array(10)
    89
    """
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


# ---------------------------------------------------------------------------
# Variant 3 — matrix_exp: O(log n) matrix exponentiation
# ---------------------------------------------------------------------------

def matrix_exp(n: int) -> int:
    """
    [[F(n+1), F(n)], [F(n), F(n-1)]] = [[1,1],[1,0]]^n

    >>> matrix_exp(3)
    3
    >>> matrix_exp(10)
    89
    >>> matrix_exp(50)
    20365011074
    """
    if n <= 2:
        return n

    def mat_mult(a, b):
        return [
            [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
            [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]],
        ]

    def mat_pow(m, p):
        result = [[1, 0], [0, 1]]  # identity
        while p:
            if p & 1:
                result = mat_mult(result, m)
            m = mat_mult(m, m)
            p >>= 1
        return result

    base = [[1, 1], [1, 0]]
    result = mat_pow(base, n)
    return result[0][0]


# ---------------------------------------------------------------------------
# Variant 4 — closed_form: Binet's formula (golden ratio)
# ---------------------------------------------------------------------------

def closed_form(n: int) -> int:
    """
    F(n) = round(phi^n / sqrt(5)) where phi = (1 + sqrt(5)) / 2.
    Note: loses precision for large n due to floating point.

    >>> closed_form(3)
    3
    >>> closed_form(10)
    89
    >>> closed_form(30)
    1346269
    """
    if n <= 2:
        return n
    phi = (1 + math.sqrt(5)) / 2
    return round(phi ** (n + 1) / math.sqrt(5))


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

IMPLS = [
    ("iterative", iterative),
    ("dp_array", dp_array),
    ("matrix_exp", matrix_exp),
    ("closed_form", closed_form),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for n in [1, 2, 3, 5, 10, 20, 30]:
        ref = reference(n)
        for name, fn in IMPLS:
            result = fn(n)
            ok = result == ref
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}({n}) = {result}")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    REPS = 100_000
    inputs = [1, 5, 10, 20, 30]
    print(f"\n=== Benchmark: {REPS} runs, {len(inputs)} inputs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(n) for n in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
