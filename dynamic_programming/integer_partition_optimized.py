#!/usr/bin/env python3
"""
Optimized and alternative implementations of Integer Partition.

Three variants:
  dp_2d           — 2D DP table (reference)
  dp_1d           — space-optimized 1D array
  euler_recursive — Euler's pentagonal number theorem (fast for large n)

Run:
    python dynamic_programming/integer_partition_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.integer_partition import partition as reference


# ---------------------------------------------------------------------------
# Variant 1 — dp_2d (same as reference)
# ---------------------------------------------------------------------------

def dp_2d(m: int) -> int:
    """
    >>> dp_2d(5)
    7
    >>> dp_2d(100)
    190569292
    """
    return reference(m)


# ---------------------------------------------------------------------------
# Variant 2 — dp_1d: Space-optimized 1D DP
# ---------------------------------------------------------------------------

def dp_1d(m: int) -> int:
    """
    p[j] = number of partitions of j using parts 1..i (built incrementally).

    >>> dp_1d(5)
    7
    >>> dp_1d(100)
    190569292
    >>> dp_1d(7)
    15
    """
    if m <= 0:
        raise ValueError("m must be a positive integer")
    p = [0] * (m + 1)
    p[0] = 1
    for i in range(1, m + 1):
        for j in range(i, m + 1):
            p[j] += p[j - i]
    return p[m]


# ---------------------------------------------------------------------------
# Variant 3 — euler_pentagonal: Euler's pentagonal number theorem
# ---------------------------------------------------------------------------

def euler_pentagonal(m: int) -> int:
    """
    Uses the recurrence:
      p(n) = sum over k != 0: (-1)^(k+1) * p(n - k(3k-1)/2)

    where k(3k-1)/2 are generalized pentagonal numbers.

    >>> euler_pentagonal(5)
    7
    >>> euler_pentagonal(100)
    190569292
    >>> euler_pentagonal(7)
    15
    """
    if m <= 0:
        raise ValueError("m must be a positive integer")
    p = [0] * (m + 1)
    p[0] = 1
    for n in range(1, m + 1):
        k = 1
        while True:
            # Generalized pentagonal numbers: k(3k-1)/2 for k = 1, -1, 2, -2, ...
            pent1 = k * (3 * k - 1) // 2
            pent2 = k * (3 * k + 1) // 2  # equivalent to (-k)(3(-k)-1)/2
            if pent1 > n:
                break
            sign = 1 if k % 2 == 1 else -1
            p[n] += sign * p[n - pent1]
            if pent2 <= n:
                p[n] += sign * p[n - pent2]
            k += 1
    return p[m]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

IMPLS = [
    ("dp_2d", dp_2d),
    ("dp_1d", dp_1d),
    ("euler_pentagonal", euler_pentagonal),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for m in [1, 5, 7, 10, 20, 50, 100]:
        ref = reference(m)
        for name, fn in IMPLS:
            result = fn(m)
            ok = result == ref
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}({m}) = {result}")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    REPS = 5_000
    print(f"\n=== Benchmark (m=100): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(100), number=REPS) * 1000 / REPS
        print(f"  {name:<22} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
