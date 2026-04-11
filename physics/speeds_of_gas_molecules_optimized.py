#!/usr/bin/env python3
"""
Optimized and alternative implementations of Speeds of Gas Molecules.

Variants covered:
1. standard         -- v_rms, v_avg, v_mp from R,T,M (reference)
2. boltzmann_form   -- same using k_B and particle mass
3. ratio_method     -- compute v_mp then derive others from known ratios

Run:
    python physics/speeds_of_gas_molecules_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.speeds_of_gas_molecules import all_speeds as reference

R = 8.314462
K_B = 1.380649e-23
N_A = 6.02214076e23


def standard_all(T: float, M: float) -> dict[str, float]:
    """
    >>> s = standard_all(300, 0.028)
    >>> round(s['rms'], 2)
    516.96
    """
    return {
        "most_probable": math.sqrt(2 * R * T / M),
        "mean": math.sqrt(8 * R * T / (math.pi * M)),
        "rms": math.sqrt(3 * R * T / M),
    }


def ratio_method(T: float, M: float) -> dict[str, float]:
    """
    Compute v_mp then derive v_avg = v_mp*sqrt(4/pi), v_rms = v_mp*sqrt(3/2).

    >>> s = ratio_method(300, 0.028)
    >>> round(s['rms'], 2)
    516.96
    """
    v_mp = math.sqrt(2 * R * T / M)
    return {
        "most_probable": v_mp,
        "mean": v_mp * math.sqrt(4 / math.pi),
        "rms": v_mp * math.sqrt(3 / 2),
    }


def boltzmann_all(T: float, particle_mass: float) -> dict[str, float]:
    """
    Using k_B and per-particle mass.

    >>> s = boltzmann_all(300, 0.028 / 6.02214076e23)
    >>> round(s['rms'], 2)
    516.96
    """
    return {
        "most_probable": math.sqrt(2 * K_B * T / particle_mass),
        "mean": math.sqrt(8 * K_B * T / (math.pi * particle_mass)),
        "rms": math.sqrt(3 * K_B * T / particle_mass),
    }


TEST_CASES = [
    (300, 0.028, "N2"),
    (300, 0.032, "O2"),
    (300, 0.002, "H2"),
    (500, 0.044, "CO2"),
]

IMPLS = [
    ("reference", reference),
    ("standard", standard_all),
    ("ratio_method", ratio_method),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for T, M, label in TEST_CASES:
        print(f"\n  {label} at {T}K:")
        for name, fn in IMPLS:
            s = fn(T, M)
            print(f"    {name}: v_mp={round(s['most_probable'],2)}, "
                  f"v_avg={round(s['mean'],2)}, v_rms={round(s['rms'],2)}")

    REPS = 200_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(T, M) for T, M, _ in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
