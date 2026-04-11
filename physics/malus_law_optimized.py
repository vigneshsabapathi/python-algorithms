#!/usr/bin/env python3
"""
Optimized and alternative implementations of Malus's Law.

Variants covered:
1. cos_squared    -- I = I0*cos^2(theta) (reference)
2. half_angle     -- I = I0*(1+cos(2*theta))/2 (trig identity)
3. multi_filter   -- intensity through N polarizers at equal angles

Run:
    python physics/malus_law_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.malus_law import malus_law as reference


def cos_squared(i0: float, theta: float) -> float:
    """
    >>> round(cos_squared(100, 0), 4)
    100.0
    >>> round(cos_squared(100, math.pi/4), 4)
    50.0
    """
    return round(i0 * math.cos(theta) ** 2, 4)


def half_angle_identity(i0: float, theta: float) -> float:
    """
    Using cos^2(x) = (1+cos(2x))/2.

    >>> round(half_angle_identity(100, 0), 4)
    100.0
    >>> round(half_angle_identity(100, math.pi/4), 4)
    50.0
    """
    return round(i0 * (1 + math.cos(2 * theta)) / 2, 4)


def multi_polarizer(i0: float, angles: list[float]) -> float:
    """
    Intensity through multiple polarizers. Each filter reduces by cos^2(delta).

    >>> round(multi_polarizer(100, [0, math.pi/4, math.pi/2]), 4)
    25.0
    """
    intensity = i0
    prev_angle = 0.0
    for angle in angles:
        delta = angle - prev_angle
        intensity *= math.cos(delta) ** 2
        prev_angle = angle
    return round(intensity, 4)


TEST_CASES = [
    (100, 0, 100.0),
    (100, math.pi / 4, 50.0),
    (100, math.pi / 2, 0.0),
    (100, math.pi / 3, 25.0),
]

IMPLS = [
    ("reference", reference),
    ("cos_squared", cos_squared),
    ("half_angle", half_angle_identity),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for i0, theta, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(i0, theta)
            tag = "OK" if abs(result - expected) < 0.001 else "FAIL"
            print(f"  [{tag}] {name}: I({i0}, {theta:.4f}) = {result}")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(i0, theta) for i0, theta, _ in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
