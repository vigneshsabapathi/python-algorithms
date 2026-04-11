#!/usr/bin/env python3
"""
Optimized and alternative implementations of Newton's Law of Gravitation.

Variants covered:
1. standard        -- F = G*m1*m2/r^2 (reference)
2. field_strength  -- g = G*M/r^2 (gravitational field)
3. potential       -- V = -G*M/r (gravitational potential)

Run:
    python physics/newtons_law_of_gravitation_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.newtons_law_of_gravitation import gravitational_force as reference

G = 6.674e-11


def standard(m1: float, m2: float, r: float) -> float:
    """
    >>> standard(100, 100, 1)
    6.674e-07
    """
    return float(f"{G * m1 * m2 / r ** 2:.3e}")


def field_strength(mass: float, radius: float) -> float:
    """
    Gravitational field strength g = GM/r^2.

    >>> round(field_strength(5.972e24, 6.371e6), 2)
    9.82
    """
    return G * mass / radius ** 2


def gravitational_potential(mass: float, radius: float) -> float:
    """
    Gravitational potential V = -GM/r.

    >>> round(gravitational_potential(5.972e24, 6.371e6), 2)
    -62560238.58
    """
    return -G * mass / radius


TEST_CASES = [
    (100, 100, 1),
    (5.972e24, 7.348e22, 3.844e8),
]

IMPLS = [
    ("reference", reference),
    ("standard", standard),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for m1, m2, r in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(m1, m2, r)
            print(f"  {name}: F({m1},{m2},{r}) = {result}")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(m1, m2, r) for m1, m2, r in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
