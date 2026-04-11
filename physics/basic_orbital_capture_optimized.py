#!/usr/bin/env python3
"""
Optimized and alternative implementations of Basic Orbital Capture.

Variants covered:
1. sqrt_formula    -- v_e = sqrt(2GM/r) (reference)
2. energy_based    -- compare KE vs gravitational PE
3. specific_energy -- check if specific orbital energy < 0

Run:
    python physics/basic_orbital_capture_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.basic_orbital_capture import escape_velocity as reference_ve
from physics.basic_orbital_capture import is_captured as reference_cap

G = 6.674e-11


def sqrt_formula(mass: float, radius: float) -> float:
    """
    Escape velocity via sqrt(2GM/r).

    >>> round(sqrt_formula(5.972e24, 6.371e6), 2)
    11185.73
    """
    return math.sqrt(2 * G * mass / radius)


def energy_based_capture(mass: float, radius: float, velocity: float) -> bool:
    """
    Compare kinetic energy to gravitational potential energy.
    Captured if 0.5*v^2 < G*M/r.

    >>> energy_based_capture(5.972e24, 6.371e6, 5000)
    True
    >>> energy_based_capture(5.972e24, 6.371e6, 20000)
    False
    """
    ke_specific = 0.5 * velocity ** 2
    pe_specific = G * mass / radius
    return ke_specific < pe_specific


def specific_orbital_energy(mass: float, radius: float, velocity: float) -> float:
    """
    Specific orbital energy: E = v^2/2 - GM/r.
    Negative = captured, positive = escaping.

    >>> round(specific_orbital_energy(5.972e24, 6.371e6, 5000), 2)
    -50060238.58
    """
    return 0.5 * velocity ** 2 - G * mass / radius


TEST_CASES = [
    (5.972e24, 6.371e6, 5000, True),
    (5.972e24, 6.371e6, 20000, False),
    (5.972e24, 6.371e6, 11185, True),
    (5.972e24, 6.371e6, 11186, False),
]

IMPLS = [
    ("reference", lambda m, r, v: reference_cap(m, r, v)),
    ("energy_based", energy_based_capture),
    ("soe_negative", lambda m, r, v: specific_orbital_energy(m, r, v) < 0),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for m, r, v, expected in TEST_CASES:
        print(f"  v={v} m/s -> expected captured={expected}")
        for name, fn in IMPLS:
            result = fn(m, r, v)
            tag = "OK" if result == expected else "FAIL"
            print(f"    [{tag}] {name}: {result}")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    m, r = 5.972e24, 6.371e6
    velocities = [1000, 5000, 8000, 11000, 15000, 20000]
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(m, r, v) for v in velocities], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch of {len(velocities)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
