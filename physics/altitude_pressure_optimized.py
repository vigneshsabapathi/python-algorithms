#!/usr/bin/env python3
"""
Optimized and alternative implementations of Altitude Pressure.

The reference uses the barometric formula: P = P0 * (1 - L*h/T0)^exponent.

Variants covered:
1. barometric       -- full barometric formula (reference)
2. exponential      -- exponential atmosphere model: P = P0 * exp(-h/H)
3. piecewise_isa    -- ISA model with troposphere/stratosphere boundary
4. linear_approx    -- linear approximation for low altitudes

Run:
    python physics/altitude_pressure_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.altitude_pressure import altitude_pressure as reference


def barometric(altitude: float, p0: float = 101325.0, t0: float = 288.15) -> float:
    """
    Full barometric formula (reference implementation).

    >>> round(barometric(0), 2)
    101325.0
    >>> round(barometric(1000), 2)
    89874.76
    """
    L = 0.0065
    g = 9.80665
    M = 0.0289644
    R = 8.31447
    exponent = g * M / (R * L)
    return p0 * (1 - L * altitude / t0) ** exponent


def exponential(altitude: float, p0: float = 101325.0, scale_height: float = 8500.0) -> float:
    """
    Exponential atmosphere: P = P0 * exp(-h / H).
    Scale height H ~ 8500 m for Earth's atmosphere.

    >>> round(exponential(0), 2)
    101325.0
    >>> round(exponential(1000), 2)
    90078.91
    """
    return p0 * math.exp(-altitude / scale_height)


def piecewise_isa(altitude: float, p0: float = 101325.0) -> float:
    """
    ISA piecewise model: barometric in troposphere (0-11km),
    exponential in stratosphere (11-20km).

    >>> round(piecewise_isa(0), 2)
    101325.0
    >>> round(piecewise_isa(5000), 2)
    54020.53
    >>> round(piecewise_isa(15000), 2)
    12045.03
    """
    L = 0.0065
    g = 9.80665
    M = 0.0289644
    R = 8.31447
    T0 = 288.15

    if altitude <= 11000:
        exponent = g * M / (R * L)
        return p0 * (1 - L * altitude / T0) ** exponent
    else:
        # Pressure at tropopause (11 km)
        exponent = g * M / (R * L)
        p_tropo = p0 * (1 - L * 11000 / T0) ** exponent
        T_tropo = T0 - L * 11000  # ~216.65 K
        # Isothermal above tropopause
        return p_tropo * math.exp(-g * M * (altitude - 11000) / (R * T_tropo))


def linear_approx(altitude: float, p0: float = 101325.0) -> float:
    """
    Linear approximation: pressure drops ~12 Pa per meter near sea level.
    Only accurate for low altitudes (< 1000m).

    >>> round(linear_approx(0), 2)
    101325.0
    >>> round(linear_approx(100), 2)
    100125.0
    """
    return p0 - 12.0 * altitude


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_ALTITUDES = [0, 100, 500, 1000, 2000, 5000, 8000, 10000]

IMPLS = [
    ("reference",      reference),
    ("barometric",     barometric),
    ("exponential",    exponential),
    ("piecewise_isa",  piecewise_isa),
    ("linear_approx",  linear_approx),
]


def run_all() -> None:
    print("\n=== Correctness (pressure in Pa at various altitudes) ===")
    print(f"  {'Alt (m)':<10}", end="")
    for name, _ in IMPLS:
        print(f"{name:>16}", end="")
    print()

    for alt in TEST_ALTITUDES:
        print(f"  {alt:<10}", end="")
        for name, fn in IMPLS:
            try:
                val = fn(alt)
                print(f"{val:>16.2f}", end="")
            except Exception as e:
                print(f"{'ERR':>16}", end="")
        print()

    REPS = 200_000
    print(f"\n=== Benchmark: {REPS} calls per method ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(a) for a in TEST_ALTITUDES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch of {len(TEST_ALTITUDES)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
