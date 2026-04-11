#!/usr/bin/env python3
"""
Optimized and alternative implementations of Mass-Energy Equivalence.

Variants covered:
1. standard        -- E = mc^2 (reference)
2. relativistic    -- E = gamma*m*c^2 (total relativistic energy)
3. binding_energy  -- mass defect to energy conversion

Run:
    python physics/mass_energy_equivalence_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.mass_energy_equivalence import energy as reference

C = 299792458
C_SQ = C ** 2


def standard(mass: float) -> float:
    """
    >>> standard(1)
    89875517873681764
    """
    return mass * C_SQ


def relativistic_total(mass: float, velocity: float) -> float:
    """
    Total relativistic energy: E = gamma * m * c^2.

    >>> relativistic_total(1, 0)
    8.987551787368176e+16
    >>> round(relativistic_total(1, 0.5 * C), 2)
    1.0377930887585438e+17
    """
    beta = velocity / C
    gamma = 1.0 / math.sqrt(1 - beta ** 2)
    return gamma * mass * C_SQ


def binding_energy(mass_defect_kg: float) -> float:
    """
    Convert mass defect to binding energy.

    >>> round(binding_energy(1.66054e-27), 2)
    0.0
    """
    return mass_defect_kg * C_SQ


def mass_defect_amu_to_mev(mass_defect_amu: float) -> float:
    """
    Convert mass defect in atomic mass units to MeV.
    1 amu = 931.494 MeV/c^2.

    >>> round(mass_defect_amu_to_mev(1), 3)
    931.494
    """
    return mass_defect_amu * 931.494


TEST_CASES = [
    (0, 0),
    (1, 89875517873681764),
    (0.001, 89875517873681.77),
]

IMPLS = [
    ("reference", reference),
    ("standard", standard),
    ("precomputed_c2", lambda m: m * C_SQ),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for mass, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(mass)
            tag = "OK" if result == expected else "FAIL"
            print(f"  [{tag}] {name}: E({mass}) = {result}")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    masses = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(m) for m in masses], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
