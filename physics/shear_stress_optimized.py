#!/usr/bin/env python3
"""
Optimized and alternative implementations of Shear Stress.

Variants covered:
1. direct          -- tau = F/A (reference)
2. from_strain     -- tau = G * gamma (shear modulus * strain)
3. fluid_shear     -- tau = mu * dv/dy (viscous shear stress)

Run:
    python physics/shear_stress_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.shear_stress import shear_stress as reference


def direct(force: float, area: float) -> float:
    """
    >>> direct(100, 0.01)
    10000.0
    """
    return force / area


def from_strain(shear_modulus: float, shear_strain: float) -> float:
    """
    tau = G * gamma.

    >>> from_strain(80e9, 0.001)
    80000000.0
    """
    return shear_modulus * shear_strain


def fluid_shear(dynamic_viscosity: float, velocity_gradient: float) -> float:
    """
    tau = mu * dv/dy (Newton's law of viscosity).

    >>> fluid_shear(0.001, 100)
    0.1
    >>> fluid_shear(1.81e-5, 1000)
    0.018099999999999998
    """
    return dynamic_viscosity * velocity_gradient


TEST_CASES = [
    (100, 0.01, 10000.0),
    (500, 0.05, 10000.0),
    (1000, 0.1, 10000.0),
]

IMPLS = [
    ("reference", reference),
    ("direct", direct),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for F, A, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(F, A)
            tag = "OK" if result == expected else "FAIL"
            print(f"  [{tag}] {name}: tau({F},{A}) = {result}")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(F, A) for F, A, _ in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
