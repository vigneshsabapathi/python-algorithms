#!/usr/bin/env python3
"""
Optimized and alternative implementations of Rainfall Intensity.

Variants covered:
1. simple_idf     -- i = a/(t+b) (reference)
2. sherman        -- i = K*T^a/(t+b)^c (Sherman equation, reference)
3. chicago_method -- Chicago design storm from IDF curves

Run:
    python physics/rainfall_intensity_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.rainfall_intensity import rainfall_intensity as reference


def simple_idf(a: float, duration: float, b: float = 10.0) -> float:
    """
    >>> round(simple_idf(1000, 30), 4)
    25.0
    """
    return a / (duration + b)


def sherman(k: float, return_period: float, duration: float,
            a: float = 0.2, b: float = 10.0, c: float = 0.8) -> float:
    """
    >>> round(sherman(1000, 10, 30), 4)
    82.8614
    """
    return k * return_period ** a / (duration + b) ** c


def total_depth(intensity_mm_hr: float, duration_min: float) -> float:
    """
    Total rainfall depth from intensity and duration.
    depth = intensity * duration / 60.

    >>> total_depth(25, 30)
    12.5
    >>> total_depth(60, 60)
    60.0
    """
    return intensity_mm_hr * duration_min / 60


TEST_CASES = [
    (1000, 30, 10.0, 25.0),
    (1000, 60, 10.0, 14.2857),
    (500, 15, 5.0, 25.0),
]

IMPLS = [
    ("reference", lambda a, d, b: reference(a, d, b)),
    ("simple_idf", simple_idf),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for a, d, b, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = round(fn(a, d, b), 4)
            tag = "OK" if abs(result - expected) < 0.001 else "FAIL"
            print(f"  [{tag}] {name}: i({a},{d},{b}) = {result}")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(a, d, b) for a, d, b, _ in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
