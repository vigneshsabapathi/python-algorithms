#!/usr/bin/env python3
"""
Optimized and alternative implementations of Mirror Formulae.

Variants covered:
1. standard       -- 1/f = 1/v + 1/u (reference)
2. radius_form    -- f = R/2 (focal length from radius of curvature)
3. magnification  -- m = -v/u

Run:
    python physics/mirror_formulae_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.mirror_formulae import focal_length as reference


def standard_focal(u: float, v: float) -> float:
    """
    f = (u*v)/(u+v).

    >>> round(standard_focal(-20, -30), 4)
    -12.0
    """
    return (u * v) / (u + v)


def radius_to_focal(radius_of_curvature: float) -> float:
    """
    f = R/2.

    >>> radius_to_focal(-24)
    -12.0
    >>> radius_to_focal(20)
    10.0
    """
    return radius_of_curvature / 2


def magnification(u: float, v: float) -> float:
    """
    m = -v/u. Positive = erect, negative = inverted.

    >>> magnification(-20, -30)
    -1.5
    >>> magnification(-10, 20)
    2.0
    """
    return -v / u


TEST_CASES = [
    (-20, -30, -12.0),
    (-10, -20, -6.6667),
]

IMPLS = [
    ("reference", reference),
    ("standard", standard_focal),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for u, v, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = round(fn(u, v), 4)
            tag = "OK" if abs(result - expected) < 0.001 else "FAIL"
            print(f"  [{tag}] {name}: f({u},{v}) = {result}")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(u, v) for u, v, _ in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
