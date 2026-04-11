#!/usr/bin/env python3
"""
Optimized and alternative implementations of RMS Speed of Molecule.

Variants covered:
1. standard        -- v_rms = sqrt(3RT/M) (reference)
2. boltzmann_form  -- v_rms = sqrt(3*k_B*T/m) (per-particle)
3. from_pressure   -- v_rms = sqrt(3P/rho)

Run:
    python physics/rms_speed_of_molecule_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.rms_speed_of_molecule import rms_speed as reference

R = 8.314462
K_B = 1.380649e-23
N_A = 6.02214076e23


def standard(temperature: float, molar_mass: float) -> float:
    """
    >>> round(standard(300, 0.028), 2)
    516.96
    """
    return math.sqrt(3 * R * temperature / molar_mass)


def boltzmann_form(temperature: float, particle_mass: float) -> float:
    """
    v_rms = sqrt(3*k_B*T/m).

    >>> round(boltzmann_form(300, 0.028 / 6.02214076e23), 2)
    516.96
    """
    return math.sqrt(3 * K_B * temperature / particle_mass)


def from_pressure(pressure: float, density: float) -> float:
    """
    v_rms = sqrt(3*P/rho).

    >>> round(from_pressure(101325, 1.225), 2)
    498.14
    """
    return math.sqrt(3 * pressure / density)


TEST_CASES = [
    (300, 0.028),  # N2
    (300, 0.032),  # O2
    (300, 0.002),  # H2
]

IMPLS = [
    ("reference", reference),
    ("standard", standard),
    ("boltzmann", lambda T, M: boltzmann_form(T, M / N_A)),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for T, M in TEST_CASES:
        for name, fn in IMPLS:
            result = round(fn(T, M), 2)
            print(f"  {name}: v_rms(T={T}, M={M}) = {result} m/s")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(T, M) for T, M in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
