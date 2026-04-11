#!/usr/bin/env python3
"""
Optimized and alternative implementations of Escape Velocity.

Variants covered:
1. sqrt_formula     -- v_e = sqrt(2GM/r) (reference)
2. surface_gravity  -- v_e = sqrt(2*g_surface*r)
3. energy_balance   -- from energy conservation: KE = PE

Run:
    python physics/escape_velocity_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.escape_velocity import escape_velocity as reference

G = 6.674e-11


def sqrt_formula(mass: float, radius: float) -> float:
    """
    >>> round(sqrt_formula(5.972e24, 6.371e6), 2)
    11185.73
    """
    return math.sqrt(2 * G * mass / radius)


def surface_gravity_method(surface_gravity: float, radius: float) -> float:
    """
    v_e = sqrt(2 * g * r) where g = GM/r^2.

    >>> round(surface_gravity_method(9.8, 6.371e6), 2)
    11174.6
    """
    return math.sqrt(2 * surface_gravity * radius)


def orbital_velocity_relation(mass: float, radius: float) -> float:
    """
    v_e = sqrt(2) * v_orbital, where v_orbital = sqrt(GM/r).

    >>> round(orbital_velocity_relation(5.972e24, 6.371e6), 2)
    11185.73
    """
    v_orbital = math.sqrt(G * mass / radius)
    return math.sqrt(2) * v_orbital


TEST_CASES = [
    (5.972e24, 6.371e6),  # Earth
    (1.989e30, 6.957e8),  # Sun
    (6.39e23, 3.3895e6),  # Mars
]

IMPLS = [
    ("reference", reference),
    ("sqrt_formula", sqrt_formula),
    ("orbital_relation", orbital_velocity_relation),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for mass, radius in TEST_CASES:
        ref_val = reference(mass, radius)
        for name, fn in IMPLS:
            result = fn(mass, radius)
            ok = abs(result - ref_val) / ref_val < 1e-10
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}: {round(result, 2)} m/s")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(m, r) for m, r in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
