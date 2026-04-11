#!/usr/bin/env python3
"""
Optimized and alternative implementations of Terminal Velocity.

Variants covered:
1. standard        -- v_t = sqrt(2mg/(rho*A*Cd)) (reference)
2. drag_force      -- find v where F_drag = F_gravity
3. stokes_law      -- v_t = 2*r^2*(rho_s-rho_f)*g/(9*mu) (small spheres)

Run:
    python physics/terminal_velocity_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.terminal_velocity import terminal_velocity as reference


def standard(mass: float, density: float, area: float, cd: float, g: float = 9.8) -> float:
    """
    >>> round(standard(80, 1.225, 0.7, 1.0), 2)
    42.76
    """
    return math.sqrt(2 * mass * g / (density * area * cd))


def drag_equals_gravity(mass: float, density: float, area: float, cd: float, g: float = 9.8) -> float:
    """
    At terminal velocity: 0.5*rho*v^2*Cd*A = m*g
    Solve for v.

    >>> round(drag_equals_gravity(80, 1.225, 0.7, 1.0), 2)
    42.76
    """
    return math.sqrt(2 * mass * g / (density * cd * area))


def stokes_terminal(radius: float, rho_solid: float, rho_fluid: float,
                    viscosity: float, g: float = 9.8) -> float:
    """
    Stokes' law for small spheres (Re < 1):
    v_t = 2*r^2*(rho_s - rho_f)*g / (9*mu).

    >>> round(stokes_terminal(0.001, 2500, 1000, 0.001), 4)
    3.2667
    """
    return 2 * radius ** 2 * (rho_solid - rho_fluid) * g / (9 * viscosity)


TEST_CASES = [
    (80, 1.225, 0.7, 1.0, 42.76),
    (0.001, 1.225, 0.0001, 0.47, 18.45),
]

IMPLS = [
    ("reference", lambda m, rho, A, cd: reference(m, rho, A, cd)),
    ("standard", lambda m, rho, A, cd: standard(m, rho, A, cd)),
    ("drag_eq_grav", lambda m, rho, A, cd: drag_equals_gravity(m, rho, A, cd)),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for m, rho, A, cd, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = round(fn(m, rho, A, cd), 2)
            tag = "OK" if result == expected else "FAIL"
            print(f"  [{tag}] {name}: v_t = {result} m/s")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(m, rho, A, cd) for m, rho, A, cd, _ in TEST_CASES],
            number=REPS,
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
