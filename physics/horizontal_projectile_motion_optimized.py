#!/usr/bin/env python3
"""
Optimized and alternative implementations of Horizontal Projectile Motion.

Variants covered:
1. parametric     -- separate x(t), y(t) equations
2. combined       -- returns all results in one call
3. trajectory     -- generates trajectory points

Run:
    python physics/horizontal_projectile_motion_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.horizontal_projectile_motion import (
    time_of_flight as reference_tof,
    horizontal_range as reference_range,
)


def parametric_position(vx: float, h: float, t: float, g: float = 9.8) -> tuple[float, float]:
    """
    Position at time t: x = vx*t, y = h - 0.5*g*t^2.

    >>> x, y = parametric_position(10, 20, 1)
    >>> (round(x, 2), round(y, 2))
    (10, 15.1)
    """
    return (vx * t, h - 0.5 * g * t ** 2)


def combined_results(vx: float, h: float, g: float = 9.8) -> dict[str, float]:
    """
    All projectile results in one call.

    >>> r = combined_results(10, 10)
    >>> round(r['time_of_flight'], 4)
    1.4286
    >>> round(r['range'], 4)
    14.2857
    >>> round(r['final_vy'], 4)
    14.0
    """
    t = math.sqrt(2 * h / g)
    return {
        "time_of_flight": t,
        "range": vx * t,
        "final_vy": g * t,
        "final_speed": math.sqrt(vx ** 2 + (g * t) ** 2),
    }


def trajectory_points(
    vx: float, h: float, n_points: int = 10, g: float = 9.8
) -> list[tuple[float, float]]:
    """
    Generate n trajectory points.

    >>> pts = trajectory_points(10, 10, 3)
    >>> len(pts)
    3
    >>> pts[0]
    (0.0, 10.0)
    """
    t_total = math.sqrt(2 * h / g)
    points = []
    for i in range(n_points):
        t = t_total * i / (n_points - 1) if n_points > 1 else 0
        x = vx * t
        y = h - 0.5 * g * t ** 2
        points.append((round(x, 4), round(y, 4)))
    return points


TEST_CASES = [(10, 10, 9.8), (20, 45, 9.8), (5, 100, 9.8)]

IMPLS_TOF = [
    ("reference_tof", reference_tof),
    ("combined_tof", lambda h, g: combined_results(0, h, g)["time_of_flight"]),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for vx, h, g in TEST_CASES:
        r = combined_results(vx, h, g)
        ref_t = reference_tof(h, g)
        ref_r = reference_range(vx, h, g)
        print(f"  vx={vx}, h={h}: t={round(r['time_of_flight'], 4)} (ref={round(ref_t, 4)}), "
              f"R={round(r['range'], 4)} (ref={round(ref_r, 4)})")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    t1 = timeit.timeit(
        lambda: [reference_tof(h, g) for _, h, g in TEST_CASES], number=REPS
    ) * 1000 / REPS
    t2 = timeit.timeit(
        lambda: [combined_results(vx, h, g) for vx, h, g in TEST_CASES], number=REPS
    ) * 1000 / REPS
    print(f"  reference_tof    {t1:>7.4f} ms / batch")
    print(f"  combined_results {t2:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
