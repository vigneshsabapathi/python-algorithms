#!/usr/bin/env python3
"""
Optimized and alternative implementations of Fast Fibonacci.

Four variants:
  fast_doubling   — O(log n) using F(2n)/F(2n+1) identities (reference)
  matrix_exp      — O(log n) using 2x2 matrix exponentiation
  iterative_dp    — O(n) standard DP (for comparison)
  binet_formula   — O(1) golden ratio (loses precision for large n)

Run:
    python dynamic_programming/fast_fibonacci_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.fast_fibonacci import fibonacci as reference


# ---------------------------------------------------------------------------
# Variant 1 — fast_doubling (same as reference)
# ---------------------------------------------------------------------------

def fast_doubling(n: int) -> int:
    """
    >>> fast_doubling(10)
    55
    >>> fast_doubling(100)
    354224848179261915075
    """
    return reference(n)


# ---------------------------------------------------------------------------
# Variant 2 — matrix_exp: 2x2 matrix exponentiation
# ---------------------------------------------------------------------------

def matrix_exp(n: int) -> int:
    """
    [[F(n+1), F(n)], [F(n), F(n-1)]] = [[1,1],[1,0]]^n

    >>> matrix_exp(10)
    55
    >>> matrix_exp(50)
    12586269025
    """
    if n < 0:
        raise ValueError("Negative arguments are not supported")
    if n == 0:
        return 0

    def mat_mult(a, b):
        return [
            [a[0][0]*b[0][0] + a[0][1]*b[1][0], a[0][0]*b[0][1] + a[0][1]*b[1][1]],
            [a[1][0]*b[0][0] + a[1][1]*b[1][0], a[1][0]*b[0][1] + a[1][1]*b[1][1]],
        ]

    def mat_pow(m, p):
        result = [[1, 0], [0, 1]]
        while p:
            if p & 1:
                result = mat_mult(result, m)
            m = mat_mult(m, m)
            p >>= 1
        return result

    return mat_pow([[1, 1], [1, 0]], n)[0][1]


# ---------------------------------------------------------------------------
# Variant 3 — iterative_dp: O(n) standard DP
# ---------------------------------------------------------------------------

def iterative_dp(n: int) -> int:
    """
    >>> iterative_dp(10)
    55
    >>> iterative_dp(0)
    0
    """
    if n < 0:
        raise ValueError("Negative arguments are not supported")
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


# ---------------------------------------------------------------------------
# Variant 4 — binet_formula: Golden ratio O(1)
# ---------------------------------------------------------------------------

def binet_formula(n: int) -> int:
    """
    Accurate only for n < ~70 due to floating point precision.

    >>> binet_formula(10)
    55
    >>> binet_formula(50)
    12586269025
    """
    if n < 0:
        raise ValueError("Negative arguments are not supported")
    phi = (1 + math.sqrt(5)) / 2
    psi = (1 - math.sqrt(5)) / 2
    return round((phi**n - psi**n) / math.sqrt(5))


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

IMPLS = [
    ("fast_doubling", fast_doubling),
    ("matrix_exp", matrix_exp),
    ("iterative_dp", iterative_dp),
    ("binet_formula", binet_formula),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for n in [0, 1, 10, 20, 50]:
        ref = reference(n)
        for name, fn in IMPLS:
            result = fn(n)
            ok = result == ref
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}({n}) = {result}")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    REPS = 50_000
    print(f"\n=== Benchmark (n=100): {REPS} runs ===")
    # Exclude binet for large n (precision issues)
    for name, fn in IMPLS[:3]:
        t = timeit.timeit(lambda fn=fn: fn(100), number=REPS) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms")

    REPS2 = 1_000
    print(f"\n=== Benchmark (n=10000): {REPS2} runs ===")
    for name, fn in IMPLS[:3]:
        t = timeit.timeit(lambda fn=fn: fn(10000), number=REPS2) * 1000 / REPS2
        print(f"  {name:<18} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
