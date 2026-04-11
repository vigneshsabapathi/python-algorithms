#!/usr/bin/env python3
"""
Optimized and alternative implementations of Hubble Parameter.

Variants covered:
1. standard        -- v = H0 * d (reference)
2. si_units        -- convert H0 from km/s/Mpc to s^-1
3. lookback_time   -- approximate lookback time for nearby galaxies

Run:
    python physics/hubble_parameter_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.hubble_parameter import hubble_velocity as reference

MPC_TO_KM = 3.0857e19  # 1 Mpc in km


def standard(distance: float, h0: float = 70.0) -> float:
    """
    v = H0 * d.

    >>> standard(100)
    7000.0
    """
    return h0 * distance


def si_hubble_constant(h0_km_s_mpc: float = 70.0) -> float:
    """
    Convert H0 from km/s/Mpc to s^-1.

    >>> round(si_hubble_constant(70), 21)
    2.269e-18
    """
    return h0_km_s_mpc / MPC_TO_KM


def lookback_time(distance_mpc: float, h0: float = 70.0) -> float:
    """
    Approximate lookback time in years for nearby galaxies: t = d/v = 1/H0.
    Returns time in billions of years.

    >>> round(lookback_time(100), 2)
    13.97
    """
    v = h0 * distance_mpc  # km/s
    d_km = distance_mpc * MPC_TO_KM
    t_seconds = d_km / v
    t_years = t_seconds / (365.25 * 24 * 3600)
    return round(t_years / 1e9, 2)


TEST_CASES = [
    (100, 70.0, 7000.0),
    (10, 73.0, 730.0),
    (0, 70.0, 0.0),
    (500, 70.0, 35000.0),
]

IMPLS = [
    ("reference", lambda d, h: reference(d, h)),
    ("standard", standard),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for d, h, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(d, h)
            tag = "OK" if result == expected else "FAIL"
            print(f"  [{tag}] {name}: v({d} Mpc) = {result} km/s")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(d, h) for d, h, _ in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
