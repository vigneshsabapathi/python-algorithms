#!/usr/bin/env python3
"""
Optimized and alternative implementations of Ideal Gas Law.

Variants covered:
1. standard       -- PV = nRT (reference)
2. boltzmann      -- PV = NkT (particle count form)
3. density_form   -- P = rho*R*T/M (using gas density)

Run:
    python physics/ideal_gas_law_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.ideal_gas_law import pressure as reference

R = 8.314462
K_B = 1.380649e-23  # Boltzmann constant
N_A = 6.02214076e23  # Avogadro's number


def standard_pressure(v: float, n: float, t: float) -> float:
    """
    P = nRT/V.

    >>> round(standard_pressure(1.0, 1.0, 273.15), 2)
    2271.1
    """
    return n * R * t / v


def boltzmann_pressure(v: float, num_particles: float, t: float) -> float:
    """
    P = N*k_B*T/V (using particle count).

    >>> round(boltzmann_pressure(1.0, 6.022e23, 273.15), 2)
    2271.04
    """
    return num_particles * K_B * t / v


def density_pressure(density: float, molar_mass: float, t: float) -> float:
    """
    P = rho * R * T / M.

    >>> round(density_pressure(1.225, 0.029, 293.15), 2)
    102958.48
    """
    return density * R * t / molar_mass


TEST_CASES = [
    (1.0, 1.0, 273.15),
    (0.0224, 1.0, 273.15),
    (0.1, 2.0, 300.0),
]

IMPLS = [
    ("reference", reference),
    ("standard", standard_pressure),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for v, n, t in TEST_CASES:
        ref = round(reference(v, n, t), 2)
        std = round(standard_pressure(v, n, t), 2)
        bolt = round(boltzmann_pressure(v, n * N_A, t), 2)
        print(f"  V={v}, n={n}, T={t}: ref={ref}, std={std}, boltzmann={bolt}")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(v, n, temp) for v, n, temp in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
