#!/usr/bin/env python3
"""
Optimized and alternative implementations of Kinetic Energy.

Variants covered:
1. standard       -- KE = 0.5*m*v^2 (reference)
2. momentum_form  -- KE = p^2/(2*m) where p = m*v
3. relativistic   -- KE = (gamma-1)*m*c^2

Run:
    python physics/kinetic_energy_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.kinetic_energy import kinetic_energy as reference

C = 299792458


def standard(mass: float, velocity: float) -> float:
    """
    >>> standard(10, 5)
    125.0
    """
    return 0.5 * mass * velocity ** 2


def momentum_form(momentum: float, mass: float) -> float:
    """
    KE = p^2 / (2*m).

    >>> momentum_form(50, 10)
    125.0
    """
    return momentum ** 2 / (2 * mass)


def relativistic(mass: float, velocity: float) -> float:
    """
    Relativistic KE = (gamma - 1) * m * c^2.

    >>> round(relativistic(1, 1000), 2)
    500006.95
    >>> round(relativistic(1, 0.1 * C), 6)
    452776255373623.56
    """
    if abs(velocity) >= C:
        raise ValueError("velocity must be less than speed of light")
    beta = velocity / C
    gamma = 1 / math.sqrt(1 - beta ** 2)
    return (gamma - 1) * mass * C ** 2


TEST_CASES = [
    (10, 5, 125.0),
    (1, 10, 50.0),
    (5, 0, 0.0),
    (100, 30, 45000.0),
]

IMPLS = [
    ("reference", lambda m, v: reference(m, v)),
    ("standard", standard),
    ("momentum", lambda m, v: momentum_form(m * v, m)),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for m, v, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(m, v)
            tag = "OK" if result == expected else "FAIL"
            print(f"  [{tag}] {name}: KE({m},{v}) = {result}")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(m, v) for m, v, _ in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
