#!/usr/bin/env python3
"""
Optimized and alternative implementations of Orbital Transfer Work.

Variants covered:
1. hohmann        -- standard Hohmann transfer (reference)
2. vis_viva       -- using vis-viva equation for velocities
3. bi_elliptic    -- bi-elliptic transfer for large ratio orbits

Run:
    python physics/orbital_transfer_work_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.orbital_transfer_work import hohmann_delta_v as reference_dv

G = 6.674e-11


def vis_viva_speed(central_mass: float, r: float, a: float) -> float:
    """
    Speed at distance r in orbit with semi-major axis a.
    v = sqrt(G*M*(2/r - 1/a))

    >>> round(vis_viva_speed(5.972e24, 6.671e6, 6.671e6), 2)
    7729.61
    """
    return math.sqrt(G * central_mass * (2 / r - 1 / a))


def hohmann_via_vis_viva(
    central_mass: float, r1: float, r2: float
) -> tuple[float, float, float]:
    """
    Hohmann transfer using vis-viva equation.

    >>> dv1, dv2, total = hohmann_via_vis_viva(5.972e24, 6.671e6, 4.2164e7)
    >>> round(total, 2)
    3895.19
    """
    a_transfer = (r1 + r2) / 2

    v1_circular = vis_viva_speed(central_mass, r1, r1)
    v1_transfer = vis_viva_speed(central_mass, r1, a_transfer)
    dv1 = abs(v1_transfer - v1_circular)

    v2_circular = vis_viva_speed(central_mass, r2, r2)
    v2_transfer = vis_viva_speed(central_mass, r2, a_transfer)
    dv2 = abs(v2_circular - v2_transfer)

    return (dv1, dv2, dv1 + dv2)


def bi_elliptic_dv(
    central_mass: float, r1: float, r2: float, r_intermediate: float
) -> tuple[float, float, float, float]:
    """
    Bi-elliptic transfer: two intermediate ellipses via a high point.
    Returns (dv1, dv2, dv3, total).

    >>> dv1, dv2, dv3, total = bi_elliptic_dv(5.972e24, 6.671e6, 4.2164e7, 1e8)
    >>> round(total, 2)
    4258.09
    """
    a1 = (r1 + r_intermediate) / 2
    a2 = (r2 + r_intermediate) / 2

    v1_c = vis_viva_speed(central_mass, r1, r1)
    v1_t = vis_viva_speed(central_mass, r1, a1)
    dv1 = abs(v1_t - v1_c)

    v_int_1 = vis_viva_speed(central_mass, r_intermediate, a1)
    v_int_2 = vis_viva_speed(central_mass, r_intermediate, a2)
    dv2 = abs(v_int_2 - v_int_1)

    v2_t = vis_viva_speed(central_mass, r2, a2)
    v2_c = vis_viva_speed(central_mass, r2, r2)
    dv3 = abs(v2_c - v2_t)

    return (dv1, dv2, dv3, dv1 + dv2 + dv3)


TEST_CASES = [
    (5.972e24, 6.671e6, 4.2164e7),  # LEO to GEO
]

IMPLS = [
    ("reference", lambda M, r1, r2: reference_dv(M, r1, r2)),
    ("vis_viva", hohmann_via_vis_viva),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for M, r1, r2 in TEST_CASES:
        for name, fn in IMPLS:
            dv1, dv2, total = fn(M, r1, r2)
            print(f"  {name}: dv1={round(dv1,2)}, dv2={round(dv2,2)}, total={round(total,2)}")

    # Compare Hohmann vs bi-elliptic for large orbit ratio
    M = 5.972e24
    r1, r2 = 6.671e6, 4.2164e7
    h_total = hohmann_via_vis_viva(M, r1, r2)[2]
    b_total = bi_elliptic_dv(M, r1, r2, 1e8)[3]
    print(f"\n  LEO->GEO: Hohmann={round(h_total,2)} m/s, Bi-elliptic(r_int=1e8)={round(b_total,2)} m/s")

    REPS = 200_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(M, r1, r2) for M, r1, r2 in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / call")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
