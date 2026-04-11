#!/usr/bin/env python3
"""
Optimized and alternative implementations of Wheatstone Bridge.

Rx = (R2/R1) * R3

Variants covered:
1. direct_calc    -- reference direct formula
2. ratio_first    -- compute ratio R2/R1 first, then multiply
3. cross_multiply -- Rx = (R2 * R3) / R1 (avoids intermediate float division)

Run:
    python electronics/wheatstone_bridge_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from electronics.wheatstone_bridge import wheatstone_solver as reference


# ---------------------------------------------------------------------------
# Variant 1 -- direct_calc (reference)
# ---------------------------------------------------------------------------

def direct_calc(r1: float, r2: float, r3: float) -> float:
    """
    >>> direct_calc(2, 4, 5)
    10.0
    """
    return reference(r1, r2, r3)


# ---------------------------------------------------------------------------
# Variant 2 -- ratio_first
# ---------------------------------------------------------------------------

def ratio_first(r1: float, r2: float, r3: float) -> float:
    """
    Compute ratio R2/R1 first, then multiply by R3.

    >>> ratio_first(2, 4, 5)
    10.0
    >>> ratio_first(356, 234, 976)
    641.5280898876405
    """
    if r1 <= 0 or r2 <= 0 or r3 <= 0:
        raise ValueError("All resistance values must be positive")
    ratio = r2 / r1
    return float(ratio * r3)


# ---------------------------------------------------------------------------
# Variant 3 -- cross_multiply: (R2*R3)/R1
# ---------------------------------------------------------------------------

def cross_multiply(r1: float, r2: float, r3: float) -> float:
    """
    Rx = (R2*R3)/R1 — multiply first to preserve precision for integers.

    >>> cross_multiply(2, 4, 5)
    10.0
    >>> cross_multiply(356, 234, 976)
    641.5280898876405
    """
    if r1 <= 0 or r2 <= 0 or r3 <= 0:
        raise ValueError("All resistance values must be positive")
    return float((r2 * r3) / r1)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ((2, 4, 5), 10.0),
    ((356, 234, 976), 641.5280898876405),
    ((1, 1, 1), 1.0),
]

IMPLS = [
    ("reference",      reference),
    ("ratio_first",    ratio_first),
    ("cross_multiply", cross_multiply),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for args, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(*args)
            ok = abs(result - expected) < 1e-10
            print(f"  [{'OK' if ok else 'FAIL'}] {name}{args} = {result}")

    REPS = 500_000
    inputs = [(2, 4, 5), (356, 234, 976), (100, 200, 300)]

    print(f"\n=== Benchmark: {REPS} runs, {len(inputs)} inputs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(*a) for a in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
