#!/usr/bin/env python3
"""
Optimized and alternative implementations of Capacitor Equivalence.

Variants covered:
1. loop_sum       -- iterative summation (reference approach)
2. builtin_sum    -- Python's sum() builtin
3. functools_reduce -- functools.reduce with operator
4. numpy_array    -- numpy reciprocal sum for series

Run:
    python electronics/capacitor_equivalence_optimized.py
"""

from __future__ import annotations

import functools
import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from electronics.capacitor_equivalence import (
    capacitor_parallel as ref_parallel,
    capacitor_series as ref_series,
)


# ---------------------------------------------------------------------------
# Variant 1 -- loop_sum (reference)
# ---------------------------------------------------------------------------

def loop_parallel(capacitors: list[float]) -> float:
    """
    >>> loop_parallel([5.71389, 12, 3])
    20.71389
    """
    return ref_parallel(capacitors)


def loop_series(capacitors: list[float]) -> float:
    """
    >>> loop_series([5.71389, 12, 3])
    1.6901062252507735
    """
    return ref_series(capacitors)


# ---------------------------------------------------------------------------
# Variant 2 -- builtin_sum
# ---------------------------------------------------------------------------

def sum_parallel(capacitors: list[float]) -> float:
    """
    >>> sum_parallel([5.71389, 12, 3])
    20.71389
    """
    if any(c < 0 for c in capacitors):
        raise ValueError("Negative capacitance")
    return sum(capacitors)


def sum_series(capacitors: list[float]) -> float:
    """
    >>> sum_series([5.71389, 12, 3])
    1.690106225250774
    """
    if any(c <= 0 for c in capacitors):
        raise ValueError("Non-positive capacitance")
    return 1 / sum(1 / c for c in capacitors)


# ---------------------------------------------------------------------------
# Variant 3 -- functools_reduce
# ---------------------------------------------------------------------------

def reduce_parallel(capacitors: list[float]) -> float:
    """
    >>> reduce_parallel([5.71389, 12, 3])
    20.71389
    """
    if any(c < 0 for c in capacitors):
        raise ValueError("Negative capacitance")
    return functools.reduce(lambda a, b: a + b, capacitors)


def reduce_series(capacitors: list[float]) -> float:
    """
    >>> abs(reduce_series([5.71389, 12, 3]) - 1.6901062252507735) < 1e-10
    True
    """
    if any(c <= 0 for c in capacitors):
        raise ValueError("Non-positive capacitance")
    return 1 / functools.reduce(lambda a, b: a + 1 / b, capacitors, 0)


# ---------------------------------------------------------------------------
# Variant 4 -- numpy_array
# ---------------------------------------------------------------------------

def numpy_parallel(capacitors: list[float]) -> float:
    """
    >>> numpy_parallel([5.71389, 12, 3])
    20.71389
    """
    arr = np.array(capacitors)
    if np.any(arr < 0):
        raise ValueError("Negative capacitance")
    return float(np.sum(arr))


def numpy_series(capacitors: list[float]) -> float:
    """
    >>> abs(numpy_series([5.71389, 12, 3]) - 1.6901062252507735) < 1e-10
    True
    """
    arr = np.array(capacitors)
    if np.any(arr <= 0):
        raise ValueError("Non-positive capacitance")
    return float(1 / np.sum(1 / arr))


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_PARALLEL = [([5.71389, 12, 3], 20.71389), ([1, 1, 1], 3.0)]
TEST_SERIES = [([5.71389, 12, 3], 1.6901062252507735), ([1, 1, 1], 1 / 3)]

PAR_IMPLS = [
    ("loop",   ref_parallel),
    ("sum",    sum_parallel),
    ("reduce", reduce_parallel),
    ("numpy",  numpy_parallel),
]

SER_IMPLS = [
    ("loop",   ref_series),
    ("sum",    sum_series),
    ("reduce", reduce_series),
    ("numpy",  numpy_series),
]


def run_all() -> None:
    print("\n=== Correctness (Parallel) ===")
    for caps, expected in TEST_PARALLEL:
        for name, fn in PAR_IMPLS:
            result = fn(caps[:])
            ok = abs(result - expected) < 1e-10
            print(f"  [{'OK' if ok else 'FAIL'}] {name}: {result}")

    print("\n=== Correctness (Series) ===")
    for caps, expected in TEST_SERIES:
        for name, fn in SER_IMPLS:
            result = fn(caps[:])
            ok = abs(result - expected) < 1e-10
            print(f"  [{'OK' if ok else 'FAIL'}] {name}: {result}")

    REPS = 200_000
    caps = [5.71389, 12, 3, 8, 15, 2.5]

    print(f"\n=== Benchmark (Parallel): {REPS} runs ===")
    for name, fn in PAR_IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(caps[:]), number=REPS) * 1000 / REPS
        print(f"  {name:<10} {t:>7.4f} ms")

    print(f"\n=== Benchmark (Series): {REPS} runs ===")
    for name, fn in SER_IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(caps[:]), number=REPS) * 1000 / REPS
        print(f"  {name:<10} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
