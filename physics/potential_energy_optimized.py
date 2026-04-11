#!/usr/bin/env python3
"""
Optimized and alternative implementations of Potential Energy.

Variants covered:
1. gravitational   -- PE = mgh (reference)
2. elastic         -- PE = 0.5*k*x^2 (spring)
3. universal_grav  -- PE = -GMm/r (Newton's gravitational PE)

Run:
    python physics/potential_energy_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.potential_energy import potential_energy as reference

G = 6.674e-11


def gravitational(mass: float, height: float, g: float = 9.8) -> float:
    """
    >>> gravitational(10, 5)
    490.0
    """
    return mass * g * height


def elastic(spring_constant: float, displacement: float) -> float:
    """
    Elastic PE = 0.5 * k * x^2.

    >>> elastic(100, 0.5)
    12.5
    >>> elastic(200, 0.1)
    1.0000000000000002
    """
    return 0.5 * spring_constant * displacement ** 2


def universal_gravitational(mass1: float, mass2: float, distance: float) -> float:
    """
    PE = -G*m1*m2/r.

    >>> round(universal_gravitational(5.972e24, 1000, 6.371e6), 2)
    -62560238581.07
    """
    return -G * mass1 * mass2 / distance


TEST_CASES = [
    (10, 5, 490.0),
    (1, 100, 980.0),
    (5, 0, 0.0),
]

IMPLS = [
    ("reference", lambda m, h: reference(m, h)),
    ("gravitational", lambda m, h: gravitational(m, h)),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for m, h, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(m, h)
            tag = "OK" if abs(result - expected) < 0.01 else "FAIL"
            print(f"  [{tag}] {name}: PE({m},{h}) = {result}")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(m, h) for m, h, _ in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
