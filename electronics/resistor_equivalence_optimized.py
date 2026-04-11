#!/usr/bin/env python3
"""
Optimized and alternative implementations of Resistor Equivalence.

Variants covered:
1. loop_sum       -- reference iterative approach
2. builtin_sum    -- Python sum() builtin
3. functools_reduce -- functools.reduce

Run:
    python electronics/resistor_equivalence_optimized.py
"""

from __future__ import annotations

import functools
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from electronics.resistor_equivalence import (
    resistor_parallel as ref_parallel,
    resistor_series as ref_series,
)


# ---------------------------------------------------------------------------
# Variant 1 -- loop (reference)
# ---------------------------------------------------------------------------

def loop_parallel(resistors: list[float]) -> float:
    """
    >>> loop_parallel([3.21389, 2, 3])
    0.8737571620498019
    """
    return ref_parallel(resistors)


def loop_series(resistors: list[float]) -> float:
    """
    >>> loop_series([3.21389, 2, 3])
    8.21389
    """
    return ref_series(resistors)


# ---------------------------------------------------------------------------
# Variant 2 -- builtin_sum
# ---------------------------------------------------------------------------

def sum_parallel(resistors: list[float]) -> float:
    """
    >>> sum_parallel([3.21389, 2, 3])
    0.8737571620498019
    """
    if any(r <= 0 for r in resistors):
        raise ValueError("Non-positive resistance")
    return 1 / sum(1 / r for r in resistors)


def sum_series(resistors: list[float]) -> float:
    """
    >>> sum_series([3.21389, 2, 3])
    8.21389
    """
    if any(r < 0 for r in resistors):
        raise ValueError("Negative resistance")
    return sum(resistors)


# ---------------------------------------------------------------------------
# Variant 3 -- functools_reduce
# ---------------------------------------------------------------------------

def reduce_parallel(resistors: list[float]) -> float:
    """
    Parallel via reduce: 1/Req = 1/R1 + 1/R2 + ...

    >>> abs(reduce_parallel([3.21389, 2, 3]) - 0.8737571620498019) < 1e-10
    True
    """
    if any(r <= 0 for r in resistors):
        raise ValueError("Non-positive resistance")
    return 1 / functools.reduce(lambda a, b: a + 1 / b, resistors, 0.0)


def reduce_series(resistors: list[float]) -> float:
    """
    >>> reduce_series([3.21389, 2, 3])
    8.21389
    """
    if any(r < 0 for r in resistors):
        raise ValueError("Negative resistance")
    return functools.reduce(lambda a, b: a + b, resistors)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_PARALLEL = [([3.21389, 2, 3], 0.8737571620498019)]
TEST_SERIES = [([3.21389, 2, 3], 8.21389)]

PAR_IMPLS = [("loop", ref_parallel), ("sum", sum_parallel), ("reduce", reduce_parallel)]
SER_IMPLS = [("loop", ref_series), ("sum", sum_series), ("reduce", reduce_series)]


def run_all() -> None:
    print("\n=== Correctness (Parallel) ===")
    for rs, expected in TEST_PARALLEL:
        for name, fn in PAR_IMPLS:
            result = fn(rs[:])
            ok = abs(result - expected) < 1e-10
            print(f"  [{'OK' if ok else 'FAIL'}] {name}: {result}")

    print("\n=== Correctness (Series) ===")
    for rs, expected in TEST_SERIES:
        for name, fn in SER_IMPLS:
            result = fn(rs[:])
            ok = abs(result - expected) < 1e-10
            print(f"  [{'OK' if ok else 'FAIL'}] {name}: {result}")

    REPS = 500_000
    rs = [3.21389, 2, 3, 10, 47, 100]

    print(f"\n=== Benchmark (Parallel): {REPS} runs ===")
    for name, fn in PAR_IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(rs[:]), number=REPS) * 1000 / REPS
        print(f"  {name:<10} {t:>7.4f} ms")

    print(f"\n=== Benchmark (Series): {REPS} runs ===")
    for name, fn in SER_IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(rs[:]), number=REPS) * 1000 / REPS
        print(f"  {name:<10} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
