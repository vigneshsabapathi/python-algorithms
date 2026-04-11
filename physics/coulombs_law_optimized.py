#!/usr/bin/env python3
"""
Optimized and alternative implementations of Coulomb's Law.

Variants covered:
1. standard        -- F = k*q1*q2/r^2 (reference)
2. si_units        -- F = q1*q2/(4*pi*eps0*r^2)
3. vector_form     -- returns force vector given positions

Run:
    python physics/coulombs_law_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.coulombs_law import coulombs_law as reference

K = 8.9875517873681764e9
EPS0 = 8.8541878128e-12


def standard(q1: float, q2: float, r: float) -> float:
    """
    F = k * q1 * q2 / r^2.

    >>> standard(1e-6, 1e-6, 1)
    0.009
    """
    return round(K * q1 * q2 / r ** 2, 3)


def si_permittivity(q1: float, q2: float, r: float) -> float:
    """
    F = q1*q2 / (4*pi*eps0*r^2).

    >>> si_permittivity(1e-6, 1e-6, 1)
    0.009
    """
    return round(q1 * q2 / (4 * math.pi * EPS0 * r ** 2), 3)


def vector_force(
    q1: float, q2: float,
    pos1: tuple[float, float], pos2: tuple[float, float],
) -> tuple[float, float]:
    """
    Force vector on q1 due to q2 in 2D.

    >>> fx, fy = vector_force(1e-6, 1e-6, (0, 0), (1, 0))
    >>> round(fx, 3)
    -0.009
    >>> round(fy, 3)
    0.0
    """
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    r = math.sqrt(dx ** 2 + dy ** 2)
    f_mag = K * q1 * q2 / r ** 2
    return (f_mag * dx / r, f_mag * dy / r)


TEST_CASES = [
    (1e-6, 1e-6, 1, 0.009),
    (1e-6, -1e-6, 1, -0.009),
    (2e-6, 3e-6, 0.5, 0.216),
]

IMPLS = [
    ("reference", reference),
    ("standard", standard),
    ("si_permittivity", si_permittivity),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for q1, q2, r, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(q1, q2, r)
            tag = "OK" if result == expected else "FAIL"
            print(f"  [{tag}] {name}: F({q1},{q2},{r}) = {result}")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(q1, q2, r) for q1, q2, r, _ in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
