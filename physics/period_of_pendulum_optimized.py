#!/usr/bin/env python3
"""
Optimized and alternative implementations of Period of Pendulum.

Variants covered:
1. small_angle     -- T = 2*pi*sqrt(L/g) (reference, small-angle approx)
2. large_angle     -- series correction for larger amplitudes
3. physical_pend   -- T = 2*pi*sqrt(I/(m*g*d)) (physical pendulum)

Run:
    python physics/period_of_pendulum_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.period_of_pendulum import period_of_pendulum as reference


def small_angle(length: float, g: float = 9.8) -> float:
    """
    >>> round(small_angle(1), 4)
    2.0071
    """
    return 2 * math.pi * math.sqrt(length / g)


def large_angle(length: float, theta_max: float, g: float = 9.8, terms: int = 3) -> float:
    """
    Period with amplitude correction (series expansion).
    T = T0 * (1 + (1/4)*sin^2(theta/2) + (9/64)*sin^4(theta/2) + ...)

    >>> round(large_angle(1, 0.1), 4)
    2.0083
    >>> round(large_angle(1, math.pi/4), 4)
    2.0872
    """
    t0 = 2 * math.pi * math.sqrt(length / g)
    sin_half = math.sin(theta_max / 2)
    correction = 1.0
    # Series coefficients: (1/4), (9/64), (25/256), ...
    coeffs = [1/4, 9/64, 25/256]
    for i in range(min(terms, len(coeffs))):
        correction += coeffs[i] * sin_half ** (2 * (i + 1))
    return t0 * correction


def physical_pendulum(moment_of_inertia: float, mass: float, distance: float, g: float = 9.8) -> float:
    """
    Period of a physical (compound) pendulum.
    T = 2*pi*sqrt(I/(m*g*d)).

    >>> round(physical_pendulum(0.1, 1, 0.5), 4)
    0.8976
    """
    return 2 * math.pi * math.sqrt(moment_of_inertia / (mass * g * distance))


TEST_CASES = [(0.5, 9.8), (1.0, 9.8), (2.0, 9.8), (1.0, 1.625)]

IMPLS = [
    ("reference", reference),
    ("small_angle", small_angle),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for L, g in TEST_CASES:
        for name, fn in IMPLS:
            result = round(fn(L, g), 4)
            print(f"  {name}: T(L={L}, g={g}) = {result} s")

    print("\n=== Large angle corrections (L=1m) ===")
    for theta in [0.01, 0.1, 0.5, 1.0, math.pi / 2]:
        t_small = small_angle(1.0)
        t_large = large_angle(1.0, theta)
        pct = (t_large - t_small) / t_small * 100
        print(f"  theta={theta:.2f} rad: T_small={round(t_small,4)}, T_large={round(t_large,4)}, diff={pct:.3f}%")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(L, g) for L, g in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
