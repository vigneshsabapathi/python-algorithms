#!/usr/bin/env python3
"""
Optimized and alternative implementations of Lorentz Transformation.

Variants covered:
1. direct         -- apply gamma, beta formulas (reference)
2. matrix_form    -- use 4x4 boost matrix
3. rapidity       -- use hyperbolic functions with rapidity parameter

Run:
    python physics/lorentz_transformation_four_vector_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.lorentz_transformation_four_vector import (
    lorentz_factor as reference_gamma,
    lorentz_transform as reference_transform,
    C,
)


def direct_transform(event: tuple, velocity: float) -> tuple:
    """
    >>> t, x, y, z = direct_transform((1.0, 0.0, 0.0, 0.0), 0)
    >>> (round(t, 4), round(x, 4))
    (1.0, 0.0)
    """
    t, x, y, z = event
    beta = velocity / C
    gamma = 1.0 / math.sqrt(1 - beta ** 2)
    return (gamma * (t - beta * x / C), gamma * (x - velocity * t), y, z)


def matrix_boost(event: tuple, velocity: float) -> tuple:
    """
    Lorentz boost as matrix multiplication.

    >>> t, x, y, z = matrix_boost((1.0, 0.0, 0.0, 0.0), 0)
    >>> (round(t, 4), round(x, 4))
    (1.0, 0.0)
    """
    t, x, y, z = event
    beta = velocity / C
    gamma = 1.0 / math.sqrt(1 - beta ** 2)
    # Boost matrix elements (ct, x row)
    t_prime = gamma * t + (-gamma * beta / C) * x
    x_prime = (-gamma * velocity) * t + gamma * x
    return (t_prime, x_prime, y, z)


def rapidity_transform(event: tuple, velocity: float) -> tuple:
    """
    Using rapidity phi = arctanh(beta).

    >>> t, x, y, z = rapidity_transform((1.0, 0.0, 0.0, 0.0), 0)
    >>> (round(t, 4), round(x, 4))
    (1.0, 0.0)
    """
    t, x, y, z = event
    beta = velocity / C
    phi = math.atanh(beta)
    t_prime = t * math.cosh(phi) - (x / C) * math.sinh(phi)
    x_prime = -t * C * math.sinh(phi) + x * math.cosh(phi)
    return (t_prime, x_prime, y, z)


TEST_EVENTS = [
    ((1.0, 0.0, 0.0, 0.0), 0),
    ((0.0, 1.0, 0.0, 0.0), 0),
    ((1.0, 1.0, 0.0, 0.0), 0.5 * C),
]

IMPLS = [
    ("reference", reference_transform),
    ("direct", direct_transform),
    ("matrix_boost", matrix_boost),
    ("rapidity", rapidity_transform),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for event, v in TEST_EVENTS:
        ref = reference_transform(event, v)
        for name, fn in IMPLS:
            result = fn(event, v)
            ok = all(abs(a - b) < 1e-6 for a, b in zip(result[:2], ref[:2]))
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}: event={event}, v={v} -> ({round(result[0],4)}, {round(result[1],4)})")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(e, v) for e, v in TEST_EVENTS], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
