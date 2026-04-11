#!/usr/bin/env python3
"""
Optimized and alternative implementations of Photoelectric Effect.

Variants covered:
1. standard         -- KE = hf - phi (reference)
2. wavelength_form  -- KE = hc/lambda - phi
3. stopping_voltage -- V_s = KE_max / e

Run:
    python physics/photoelectric_effect_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.photoelectric_effect import max_kinetic_energy as reference

H = 6.62607015e-34
C = 299792458
E_CHARGE = 1.602176634e-19  # electron charge


def standard(frequency: float, work_function: float) -> float:
    """
    >>> round(standard(1e15, 3e-19), 22)
    3.626e-19
    """
    return H * frequency - work_function


def wavelength_form(wavelength: float, work_function: float) -> float:
    """
    KE = hc/lambda - phi.

    >>> round(wavelength_form(300e-9, 3e-19), 22)
    3.621e-19
    """
    return H * C / wavelength - work_function


def stopping_voltage(frequency: float, work_function: float) -> float:
    """
    Stopping voltage V_s = KE_max / e.

    >>> round(stopping_voltage(1e15, 3e-19), 4)
    2.2632
    """
    ke = H * frequency - work_function
    return ke / E_CHARGE


TEST_CASES = [
    (1e15, 3e-19),
    (5e14, 2e-19),
    (2e15, 5e-19),
]

IMPLS = [
    ("reference", reference),
    ("standard", standard),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for f, phi in TEST_CASES:
        for name, fn in IMPLS:
            try:
                result = fn(f, phi)
                print(f"  {name}: KE({f:.0e}, {phi:.0e}) = {result:.4e} J")
            except ValueError as e:
                print(f"  {name}: {e}")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(f, phi) for f, phi in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
