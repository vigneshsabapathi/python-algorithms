#!/usr/bin/env python3
"""
Optimized and alternative implementations of Lens Formulae.

Variants covered:
1. standard         -- 1/f = 1/v - 1/u (reference)
2. magnification    -- m = v/u = h_i/h_o
3. power_diopters   -- P = 1/f (in meters)

Run:
    python physics/lens_formulae_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.lens_formulae import focal_length as reference


def standard_focal(u: float, v: float) -> float:
    """
    f = (u*v) / (u - v).

    >>> round(standard_focal(-20, 30), 4)
    12.0
    """
    return (u * v) / (u - v)


def magnification(u: float, v: float) -> float:
    """
    Linear magnification m = v / u.

    >>> magnification(-20, 30)
    -1.5
    """
    return v / u


def power_diopters(focal_length_m: float) -> float:
    """
    Lens power in diopters: P = 1/f (f in meters).

    >>> round(power_diopters(0.5), 2)
    2.0
    >>> round(power_diopters(-0.25), 2)
    -4.0
    """
    return 1.0 / focal_length_m


TEST_CASES = [
    (-20, 30, 12.0),
    (-10, 20, 6.6667),
    (-30, 15, -10.0),
]

IMPLS = [
    ("reference", reference),
    ("standard", standard_focal),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for u, v, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = round(fn(u, v), 4)
            tag = "OK" if abs(result - expected) < 0.001 else "FAIL"
            print(f"  [{tag}] {name}: f({u},{v}) = {result}")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(u, v) for u, v, _ in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
