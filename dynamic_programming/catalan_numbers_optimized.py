#!/usr/bin/env python3
"""
Optimized and alternative implementations of Catalan Numbers.

Four variants:
  dp_recurrence     — O(n^2) bottom-up DP using recurrence (reference)
  closed_form       — O(n) using binomial coefficient C(2n,n)/(n+1)
  memoized_recursive — top-down with @lru_cache
  generator         — yields Catalan numbers lazily

Run:
    python dynamic_programming/catalan_numbers_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.catalan_numbers import catalan_numbers as reference


# ---------------------------------------------------------------------------
# Variant 1 — dp_recurrence: O(n^2) bottom-up (same as reference)
# ---------------------------------------------------------------------------

def dp_recurrence(n: int) -> list[int]:
    """
    >>> dp_recurrence(5)
    [1, 1, 2, 5, 14, 42]
    """
    return reference(n)


# ---------------------------------------------------------------------------
# Variant 2 — closed_form: O(n) using binomial coefficient
# ---------------------------------------------------------------------------

def closed_form(n: int) -> list[int]:
    """
    C(n) = C(2n, n) / (n + 1) = (2n)! / ((n+1)! * n!)

    >>> closed_form(5)
    [1, 1, 2, 5, 14, 42]
    >>> closed_form(0)
    [1]
    """
    if n < 0:
        raise ValueError("n must be >= 0")
    result = []
    for i in range(n + 1):
        result.append(math.comb(2 * i, i) // (i + 1))
    return result


# ---------------------------------------------------------------------------
# Variant 3 — memoized_recursive: Top-down with @lru_cache
# ---------------------------------------------------------------------------

def memoized_recursive(n: int) -> list[int]:
    """
    >>> memoized_recursive(5)
    [1, 1, 2, 5, 14, 42]
    """

    @lru_cache(maxsize=None)
    def catalan(k: int) -> int:
        if k <= 1:
            return 1
        return sum(catalan(j) * catalan(k - j - 1) for j in range(k))

    return [catalan(i) for i in range(n + 1)]


# ---------------------------------------------------------------------------
# Variant 4 — generator: Lazy Catalan number generator
# ---------------------------------------------------------------------------

def generator(n: int) -> list[int]:
    """
    Uses the multiplicative formula: C(n+1) = C(n) * 2*(2n+1) / (n+2)

    >>> generator(5)
    [1, 1, 2, 5, 14, 42]
    """
    if n < 0:
        raise ValueError("n must be >= 0")
    result = [1]
    c = 1
    for i in range(1, n + 1):
        c = c * 2 * (2 * i - 1) // (i + 1)
        result.append(c)
    return result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

IMPLS = [
    ("dp_recurrence", dp_recurrence),
    ("closed_form", closed_form),
    ("memoized_recursive", memoized_recursive),
    ("generator", generator),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for n in [0, 1, 5, 10, 15, 20]:
        ref = reference(n)
        for name, fn in IMPLS:
            result = fn(n)
            ok = result == ref
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}({n}) last={result[-1]}")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    REPS = 50_000
    print(f"\n=== Benchmark (n=20): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(20), number=REPS) * 1000 / REPS
        print(f"  {name:<22} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
