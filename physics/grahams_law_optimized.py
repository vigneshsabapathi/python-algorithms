#!/usr/bin/env python3
"""
Optimized and alternative implementations of Graham's Law.

Variants covered:
1. sqrt_ratio      -- rate1/rate2 = sqrt(M2/M1) (reference)
2. inverse_sqrt    -- rate proportional to 1/sqrt(M)
3. time_ratio      -- t1/t2 = sqrt(M1/M2) (inverse of rate ratio)

Run:
    python physics/grahams_law_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.grahams_law import grahams_law as reference


def sqrt_ratio(m1: float, m2: float) -> float:
    """
    >>> round(sqrt_ratio(2, 32), 4)
    4.0
    """
    return math.sqrt(m2 / m1)


def inverse_sqrt_ratio(m1: float, m2: float) -> float:
    """
    Using 1/sqrt relationship: rate ~ 1/sqrt(M).

    >>> round(inverse_sqrt_ratio(2, 32), 4)
    4.0
    """
    return (1 / math.sqrt(m1)) / (1 / math.sqrt(m2))


def effusion_time_ratio(m1: float, m2: float) -> float:
    """
    Time ratio (inverse of rate ratio): t1/t2 = sqrt(M1/M2).

    >>> round(effusion_time_ratio(2, 32), 4)
    0.25
    """
    return math.sqrt(m1 / m2)


TEST_CASES = [
    (2, 32, 4.0),
    (4, 28, 2.6458),
    (28, 28, 1.0),
    (28, 2, 0.2673),
]

IMPLS = [
    ("reference", reference),
    ("sqrt_ratio", sqrt_ratio),
    ("inverse_sqrt", inverse_sqrt_ratio),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for m1, m2, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = round(fn(m1, m2), 4)
            tag = "OK" if abs(result - expected) < 0.001 else "FAIL"
            print(f"  [{tag}] {name}: rate({m1},{m2}) = {result}")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(m1, m2) for m1, m2, _ in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
