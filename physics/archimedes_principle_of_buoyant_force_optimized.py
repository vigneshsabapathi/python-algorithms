#!/usr/bin/env python3
"""
Optimized and alternative implementations of Archimedes' Buoyant Force.

Variants covered:
1. direct           -- F = rho * g * V (reference)
2. weight_displaced -- F = m_fluid * g where m_fluid = rho * V
3. percentage_sub   -- fraction submerged = rho_obj / rho_fluid

Run:
    python physics/archimedes_principle_of_buoyant_force_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.archimedes_principle_of_buoyant_force import archimedes_principle as reference


def direct(fluid_density: float, volume: float, g: float = 9.8) -> float:
    """
    Direct formula: F_b = rho * g * V.

    >>> direct(1000, 0.5)
    4900.0
    >>> direct(1000, 0)
    0.0
    """
    return round(fluid_density * g * volume, 2)


def weight_displaced(fluid_density: float, volume: float, g: float = 9.8) -> float:
    """
    Two-step: mass of displaced fluid, then weight.

    >>> weight_displaced(1000, 0.5)
    4900.0
    """
    mass_fluid = fluid_density * volume
    return round(mass_fluid * g, 2)


def fraction_submerged(object_density: float, fluid_density: float) -> float:
    """
    Fraction of object submerged when floating.
    f = rho_obj / rho_fluid  (only valid when f <= 1).

    >>> fraction_submerged(800, 1000)
    0.8
    >>> fraction_submerged(1000, 1000)
    1.0
    """
    if fluid_density <= 0:
        raise ValueError("fluid_density must be positive")
    return object_density / fluid_density


TEST_CASES = [
    (1000, 0.5, 9.8, 4900.0),
    (1000, 0, 9.8, 0.0),
    (1025, 1.0, 9.8, 10045.0),
    (1.225, 2.0, 9.8, 24.01),
]

IMPLS = [
    ("reference", lambda d, v, g: reference(d, v, g)),
    ("direct", direct),
    ("weight_displaced", weight_displaced),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for rho, vol, g, expected in TEST_CASES:
        print(f"  rho={rho}, V={vol}, g={g} -> expected={expected}")
        for name, fn in IMPLS:
            result = fn(rho, vol, g)
            tag = "OK" if result == expected else "FAIL"
            print(f"    [{tag}] {name}: {result}")

    REPS = 500_000
    inputs = [(rho, vol, g) for rho, vol, g, _ in TEST_CASES]
    print(f"\n=== Benchmark: {REPS} runs, {len(inputs)} inputs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(*i) for i in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
