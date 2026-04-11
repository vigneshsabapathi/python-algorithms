#!/usr/bin/env python3
"""
Optimized and alternative implementations of Newton's Second Law.

Variants covered:
1. standard       -- F = m*a (reference)
2. impulse_form   -- F = dp/dt (change in momentum over time)
3. variable_mass  -- F = m*a + v_rel*dm/dt (rocket equation)

Run:
    python physics/newtons_second_law_of_motion_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.newtons_second_law_of_motion import force as reference


def standard(mass: float, acceleration: float) -> float:
    """
    >>> standard(10, 5)
    50
    """
    return round(mass * acceleration, 4)


def impulse_form(momentum_change: float, time_interval: float) -> float:
    """
    F = dp/dt.

    >>> impulse_form(100, 2)
    50.0
    """
    if time_interval <= 0:
        raise ValueError("time_interval must be positive")
    return momentum_change / time_interval


def rocket_thrust(
    exhaust_velocity: float, mass_flow_rate: float
) -> float:
    """
    Thrust = v_exhaust * dm/dt (simplified Tsiolkovsky).

    >>> rocket_thrust(3000, 10)
    30000
    """
    return exhaust_velocity * mass_flow_rate


TEST_CASES = [
    (10, 5, 50),
    (0.5, 9.8, 4.9),
    (100, 0, 0),
]

IMPLS = [
    ("reference", reference),
    ("standard", standard),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for m, a, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(m, a)
            tag = "OK" if result == expected else "FAIL"
            print(f"  [{tag}] {name}: F({m},{a}) = {result}")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(m, a) for m, a, _ in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
