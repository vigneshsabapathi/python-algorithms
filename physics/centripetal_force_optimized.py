#!/usr/bin/env python3
"""
Optimized and alternative implementations of Centripetal Force.

Variants covered:
1. velocity_based  -- F = m*v^2/r (reference)
2. omega_based     -- F = m*omega^2*r (angular velocity)
3. period_based    -- F = 4*pi^2*m*r/T^2 (period)

Run:
    python physics/centripetal_force_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.centripetal_force import centripetal_force as reference


def velocity_based(mass: float, velocity: float, radius: float) -> float:
    """
    F = m * v^2 / r.

    >>> velocity_based(10, 5, 2)
    125.0
    """
    return mass * velocity ** 2 / radius


def omega_based(mass: float, angular_velocity: float, radius: float) -> float:
    """
    F = m * omega^2 * r.

    >>> omega_based(10, 2.5, 2)
    125.0
    """
    return mass * angular_velocity ** 2 * radius


def period_based(mass: float, radius: float, period: float) -> float:
    """
    F = 4 * pi^2 * m * r / T^2.

    >>> round(period_based(10, 2, 2*math.pi*2/5), 4)
    125.0
    """
    return 4 * math.pi ** 2 * mass * radius / period ** 2


TEST_CASES = [
    (10, 5, 2, 125.0),
    (1, 10, 5, 20.0),
    (100, 3, 1.5, 600.0),
]

IMPLS = [
    ("reference", lambda m, v, r: reference(m, v, r)),
    ("velocity", lambda m, v, r: velocity_based(m, v, r)),
    ("omega", lambda m, v, r: omega_based(m, v / r, r)),
    ("period", lambda m, v, r: period_based(m, r, 2 * math.pi * r / v)),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for m, v, r, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = round(fn(m, v, r), 4)
            tag = "OK" if abs(result - expected) < 0.01 else "FAIL"
            print(f"  [{tag}] {name}: F({m},{v},{r}) = {result}")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(m, v, r) for m, v, r, _ in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
