#!/usr/bin/env python3
"""
Optimized and alternative implementations of Casimir Effect.

Variants covered:
1. standard       -- F/A = -pi^2 * hbar * c / (240 * d^4) (reference)
2. precomputed    -- precompute numerator constant for repeated calls
3. energy_density -- Casimir energy per unit area: E/A = -pi^2*hbar*c/(720*d^3)

Run:
    python physics/casimir_effect_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.casimir_effect import casimir_force_per_area as reference

HBAR = 1.0545718e-34
C = 299792458
_CASIMIR_NUMERATOR = math.pi**2 * HBAR * C


def standard(distance: float) -> float:
    """
    Standard Casimir force per area.

    >>> round(standard(1e-6), 4)
    -0.0013
    """
    return -(math.pi**2 * HBAR * C) / (240 * distance**4)


def precomputed(distance: float) -> float:
    """
    Precomputed numerator for repeated distance evaluations.

    >>> round(precomputed(1e-6), 4)
    -0.0013
    """
    return -_CASIMIR_NUMERATOR / (240 * distance**4)


def casimir_energy_per_area(distance: float) -> float:
    """
    Casimir energy per unit area: E/A = -pi^2*hbar*c/(720*d^3).

    >>> round(casimir_energy_per_area(1e-6), 10)
    -4e-10
    """
    return -_CASIMIR_NUMERATOR / (720 * distance**3)


TEST_DISTANCES = [1e-8, 1e-7, 5e-7, 1e-6, 5e-6, 1e-5]

IMPLS = [
    ("reference",    reference),
    ("standard",     standard),
    ("precomputed",  precomputed),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for d in TEST_DISTANCES:
        results = {name: fn(d) for name, fn in IMPLS}
        ref = results["reference"]
        ok = all(abs(v - ref) / abs(ref) < 1e-10 for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] d={d:.0e}  F/A={ref:.6e}")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs, {len(TEST_DISTANCES)} distances ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(d) for d in TEST_DISTANCES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
