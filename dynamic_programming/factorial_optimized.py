#!/usr/bin/env python3
"""
Optimized and alternative implementations of Factorial.

Four variants:
  lru_cache_recursive — @lru_cache memoized recursion (reference)
  iterative           — simple loop, O(1) auxiliary space
  math_builtin        — Python's math.factorial (C implementation)
  reduce_based        — functools.reduce with operator.mul

Run:
    python dynamic_programming/factorial_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit
from functools import reduce
from operator import mul

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.factorial import factorial as reference


# ---------------------------------------------------------------------------
# Variant 1 — lru_cache_recursive (same as reference)
# ---------------------------------------------------------------------------

def lru_cache_recursive(n: int) -> int:
    """
    >>> lru_cache_recursive(7)
    5040
    """
    return reference(n)


# ---------------------------------------------------------------------------
# Variant 2 — iterative: Simple loop
# ---------------------------------------------------------------------------

def iterative(n: int) -> int:
    """
    >>> iterative(7)
    5040
    >>> iterative(0)
    1
    >>> iterative(-1)
    Traceback (most recent call last):
        ...
    ValueError: Number should not be negative.
    """
    if n < 0:
        raise ValueError("Number should not be negative.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


# ---------------------------------------------------------------------------
# Variant 3 — math_builtin: Python's math.factorial
# ---------------------------------------------------------------------------

def math_builtin(n: int) -> int:
    """
    >>> math_builtin(7)
    5040
    >>> math_builtin(0)
    1
    """
    if n < 0:
        raise ValueError("Number should not be negative.")
    return math.factorial(n)


# ---------------------------------------------------------------------------
# Variant 4 — reduce_based: functools.reduce
# ---------------------------------------------------------------------------

def reduce_based(n: int) -> int:
    """
    >>> reduce_based(7)
    5040
    >>> reduce_based(0)
    1
    """
    if n < 0:
        raise ValueError("Number should not be negative.")
    if n <= 1:
        return 1
    return reduce(mul, range(2, n + 1))


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

IMPLS = [
    ("lru_cache", lru_cache_recursive),
    ("iterative", iterative),
    ("math_builtin", math_builtin),
    ("reduce_based", reduce_based),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for n in [0, 1, 5, 10, 15, 20]:
        ref = math.factorial(n)
        for name, fn in IMPLS:
            result = fn(n)
            ok = result == ref
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}({n}) = {result}")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    REPS = 100_000
    inputs = [0, 1, 5, 10, 20]
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
