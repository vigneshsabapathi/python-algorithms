#!/usr/bin/env python3
"""
Optimized and alternative implementations of Center of Mass.

Variants covered:
1. loop_based    -- explicit loop (reference)
2. zip_sum       -- using zip and sum builtins
3. numpy_style   -- weighted average (pure Python, numpy-like logic)

Run:
    python physics/center_of_mass_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.center_of_mass import center_of_mass as reference


def loop_based(particles: list[tuple[float, float, float]]) -> tuple[float, float]:
    """
    Explicit loop.

    >>> loop_based([(1, 0, 0), (1, 2, 0)])
    (1.0, 0.0)
    """
    total_m = sum(m for m, _, _ in particles)
    x_cm = sum(m * x for m, x, _ in particles) / total_m
    y_cm = sum(m * y for m, _, y in particles) / total_m
    return (x_cm, y_cm)


def zip_sum(particles: list[tuple[float, float, float]]) -> tuple[float, float]:
    """
    Using zip to separate components.

    >>> zip_sum([(1, 0, 0), (1, 2, 0)])
    (1.0, 0.0)
    """
    masses, xs, ys = zip(*particles)
    total = sum(masses)
    return (sum(m * x for m, x in zip(masses, xs)) / total,
            sum(m * y for m, y in zip(masses, ys)) / total)


def weighted_avg(particles: list[tuple[float, float, float]]) -> tuple[float, float]:
    """
    Weighted average style.

    >>> weighted_avg([(2, 0, 0), (1, 3, 0)])
    (1.0, 0.0)
    """
    total_m = 0.0
    wx = wy = 0.0
    for m, x, y in particles:
        total_m += m
        wx += m * x
        wy += m * y
    return (wx / total_m, wy / total_m)


TEST_CASES = [
    ([(1, 0, 0), (1, 2, 0)], (1.0, 0.0)),
    ([(2, 0, 0), (1, 3, 0)], (1.0, 0.0)),
    ([(5, 2, 3)], (2.0, 3.0)),
    ([(1, 0, 0), (1, 0, 2)], (0.0, 1.0)),
]

IMPLS = [
    ("reference", reference),
    ("loop_based", loop_based),
    ("zip_sum", zip_sum),
    ("weighted_avg", weighted_avg),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for particles, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(particles)
            ok = all(abs(r - e) < 1e-9 for r, e in zip(result, expected))
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}: {result}")

    REPS = 200_000
    big_input = [(float(i), float(i), float(i * 2)) for i in range(1, 51)]
    print(f"\n=== Benchmark: {REPS} runs, 50 particles ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(big_input), number=REPS) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
