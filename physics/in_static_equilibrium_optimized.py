#!/usr/bin/env python3
"""
Optimized and alternative implementations of Static Equilibrium.

Variants covered:
1. loop_based     -- explicit loop summing components (reference)
2. zip_sum        -- using zip and sum builtins
3. complex_plane  -- represent 2D forces as complex numbers

Run:
    python physics/in_static_equilibrium_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.in_static_equilibrium import in_static_equilibrium as reference


def loop_based(forces: list[list[float]], tol: float = 1e-9) -> bool:
    """
    >>> loop_based([[1, 0], [-1, 0]])
    True
    >>> loop_based([[1, 0], [0, 1]])
    False
    """
    if not forces:
        return True
    dims = len(forces[0])
    totals = [0.0] * dims
    for f in forces:
        for i in range(dims):
            totals[i] += f[i]
    return all(abs(t) < tol for t in totals)


def zip_sum(forces: list[list[float]], tol: float = 1e-9) -> bool:
    """
    >>> zip_sum([[1, 0], [-1, 0]])
    True
    """
    if not forces:
        return True
    return all(abs(sum(col)) < tol for col in zip(*forces))


def complex_plane(forces: list[list[float]], tol: float = 1e-9) -> bool:
    """
    Represent 2D forces as complex numbers and check if sum ~ 0.

    >>> complex_plane([[1, 0], [-1, 0]])
    True
    >>> complex_plane([[1, 0], [0, 1]])
    False
    """
    total = sum(complex(f[0], f[1]) for f in forces)
    return abs(total) < tol


TEST_CASES = [
    ([[1, 0], [-1, 0]], True),
    ([[1, 0], [0, 1], [-1, -1]], True),
    ([[1, 0], [0, 1]], False),
    ([[10, 5], [-5, -5], [-5, 0]], True),
]

IMPLS = [
    ("reference", reference),
    ("loop_based", loop_based),
    ("zip_sum", zip_sum),
    ("complex_plane", complex_plane),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for forces, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(forces)
            tag = "OK" if result == expected else "FAIL"
            print(f"  [{tag}] {name}: {result}")

    REPS = 500_000
    big_forces = [[float(i), float(-i)] for i in range(50)]
    print(f"\n=== Benchmark: {REPS} runs, 50 forces ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(big_forces), number=REPS) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
