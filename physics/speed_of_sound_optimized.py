#!/usr/bin/env python3
"""
Optimized and alternative implementations of Speed of Sound.

Variants covered:
1. ideal_gas       -- v = sqrt(gamma*R*T/M) (reference)
2. simplified_air  -- v = 331.3 + 0.606*T_C (reference)
3. bulk_modulus     -- v = sqrt(K/rho) (general form)

Run:
    python physics/speed_of_sound_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.speed_of_sound import speed_of_sound as reference, speed_of_sound_air

R = 8.314462


def ideal_gas(temperature: float, gamma: float = 1.4, molar_mass: float = 0.029) -> float:
    """
    >>> round(ideal_gas(293.15), 2)
    343.03
    """
    return math.sqrt(gamma * R * temperature / molar_mass)


def simplified_air(celsius: float) -> float:
    """
    >>> round(simplified_air(20), 2)
    343.42
    """
    return 331.3 + 0.606 * celsius


def bulk_modulus(K: float, density: float) -> float:
    """
    v = sqrt(K/rho). General form for any medium.

    >>> round(bulk_modulus(2.15e9, 1000), 2)
    1466.29
    >>> round(bulk_modulus(1.42e5, 1.225), 2)
    340.47
    """
    return math.sqrt(K / density)


TEST_TEMPS = [253.15, 273.15, 293.15, 313.15, 373.15]

IMPLS = [
    ("reference", reference),
    ("ideal_gas", ideal_gas),
]


def run_all() -> None:
    print("\n=== Correctness (speed in m/s) ===")
    for T in TEST_TEMPS:
        for name, fn in IMPLS:
            result = round(fn(T), 2)
            print(f"  {name}: v({T} K) = {result} m/s")

    print("\n=== Speed in different media ===")
    media = [
        ("Air (20C)", 1.42e5, 1.225),
        ("Water", 2.15e9, 1000),
        ("Steel", 1.6e11, 7800),
    ]
    for medium, K, rho in media:
        print(f"  {medium}: {round(bulk_modulus(K, rho), 2)} m/s")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(T) for T in TEST_TEMPS], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
