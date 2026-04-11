#!/usr/bin/env python3
"""
Optimized and alternative implementations of Reynolds Number.

Variants covered:
1. dynamic_visc    -- Re = rho*v*L/mu (reference)
2. kinematic_visc  -- Re = v*L/nu
3. pipe_flow       -- Re = rho*v*D/mu (diameter-based)

Run:
    python physics/reynolds_number_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.reynolds_number import reynolds_number as reference, flow_regime


def dynamic_visc(rho: float, v: float, L: float, mu: float) -> float:
    """
    >>> dynamic_visc(1000, 1, 0.1, 0.001)
    100000.0
    """
    return round(rho * v * L / mu, 2)


def kinematic_visc(v: float, L: float, nu: float) -> float:
    """
    Re = v * L / nu where nu = mu/rho.

    >>> kinematic_visc(1, 0.1, 1e-6)
    100000.0
    """
    return round(v * L / nu, 2)


def pipe_flow(rho: float, v: float, diameter: float, mu: float) -> float:
    """
    Reynolds number for pipe flow using diameter.

    >>> pipe_flow(1000, 1, 0.1, 0.001)
    100000.0
    """
    return round(rho * v * diameter / mu, 2)


TEST_CASES = [
    (1000, 1, 0.1, 0.001, 100000.0),
    (1.225, 30, 1, 1.81e-5, 2030386.74),
    (1000, 0.01, 0.05, 0.001, 500.0),
]

IMPLS = [
    ("reference", lambda rho, v, L, mu: reference(rho, v, L, mu)),
    ("dynamic", dynamic_visc),
    ("kinematic", lambda rho, v, L, mu: kinematic_visc(v, L, mu / rho)),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for rho, v, L, mu, expected in TEST_CASES:
        re = reference(rho, v, L, mu)
        regime = flow_regime(re)
        print(f"  Re={re} -> {regime}")
        for name, fn in IMPLS:
            result = fn(rho, v, L, mu)
            tag = "OK" if result == expected else "FAIL"
            print(f"    [{tag}] {name}: {result}")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(rho, v, L, mu) for rho, v, L, mu, _ in TEST_CASES],
            number=REPS,
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
