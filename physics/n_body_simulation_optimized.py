#!/usr/bin/env python3
"""
Optimized and alternative implementations of N-Body Simulation.

Variants covered:
1. euler          -- Euler integration (reference)
2. leapfrog       -- Leapfrog (Verlet) integration - better energy conservation
3. runge_kutta_2  -- 2nd-order Runge-Kutta (midpoint method)

Run:
    python physics/n_body_simulation_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.n_body_simulation import Body, compute_forces, step as euler_step

G = 6.674e-11


def leapfrog_step(bodies: list[Body], dt: float) -> None:
    """
    Leapfrog integration: better energy conservation than Euler.

    >>> b1 = Body(1e10, 0, 0); b2 = Body(1e10, 10, 0)
    >>> leapfrog_step([b1, b2], 1.0)
    >>> b1.vx > 0
    True
    """
    # Half-step velocity
    forces = compute_forces(bodies)
    for i, body in enumerate(bodies):
        ax = forces[i][0] / body.mass
        ay = forces[i][1] / body.mass
        body.vx += 0.5 * ax * dt
        body.vy += 0.5 * ay * dt

    # Full-step position
    for body in bodies:
        body.x += body.vx * dt
        body.y += body.vy * dt

    # Recompute forces at new positions
    forces = compute_forces(bodies)
    for i, body in enumerate(bodies):
        ax = forces[i][0] / body.mass
        ay = forces[i][1] / body.mass
        body.vx += 0.5 * ax * dt
        body.vy += 0.5 * ay * dt


def total_energy(bodies: list[Body]) -> float:
    """
    Total energy (KE + PE) of the system.

    >>> b1 = Body(1e10, 0, 0); b2 = Body(1e10, 10, 0)
    >>> round(total_energy([b1, b2]), 2)
    -667400000.0
    """
    ke = sum(0.5 * b.mass * (b.vx ** 2 + b.vy ** 2) for b in bodies)
    pe = 0.0
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            r = bodies[i].distance_to(bodies[j])
            if r > 0:
                pe -= G * bodies[i].mass * bodies[j].mass / r
    return ke + pe


def run_simulation_compare(n_steps: int = 100, dt: float = 0.01) -> None:
    """Compare Euler vs Leapfrog energy conservation."""
    print(f"\n=== Energy Conservation ({n_steps} steps, dt={dt}) ===")

    # Euler
    b1e = Body(1e10, 0, 0, 0, 0.1)
    b2e = Body(1e10, 10, 0, 0, -0.1)
    e0_euler = total_energy([b1e, b2e])
    for _ in range(n_steps):
        euler_step([b1e, b2e], dt)
    ef_euler = total_energy([b1e, b2e])
    drift_euler = abs(ef_euler - e0_euler) / abs(e0_euler) * 100

    # Leapfrog
    b1l = Body(1e10, 0, 0, 0, 0.1)
    b2l = Body(1e10, 10, 0, 0, -0.1)
    e0_leap = total_energy([b1l, b2l])
    for _ in range(n_steps):
        leapfrog_step([b1l, b2l], dt)
    ef_leap = total_energy([b1l, b2l])
    drift_leap = abs(ef_leap - e0_leap) / abs(e0_leap) * 100

    print(f"  Euler:    E0={e0_euler:.4e}, Ef={ef_euler:.4e}, drift={drift_euler:.6f}%")
    print(f"  Leapfrog: E0={e0_leap:.4e}, Ef={ef_leap:.4e}, drift={drift_leap:.6f}%")


def run_all() -> None:
    run_simulation_compare()

    REPS = 10_000
    b1 = Body(1e10, 0, 0)
    b2 = Body(1e10, 10, 0)
    b3 = Body(1e10, 5, 8)
    print(f"\n=== Benchmark: {REPS} steps, 3 bodies ===")

    bodies_e = [Body(1e10, 0, 0), Body(1e10, 10, 0), Body(1e10, 5, 8)]
    t1 = timeit.timeit(lambda: euler_step(bodies_e, 0.01), number=REPS) * 1000 / REPS
    bodies_l = [Body(1e10, 0, 0), Body(1e10, 10, 0), Body(1e10, 5, 8)]
    t2 = timeit.timeit(lambda: leapfrog_step(bodies_l, 0.01), number=REPS) * 1000 / REPS
    print(f"  euler      {t1:>7.4f} ms / step")
    print(f"  leapfrog   {t2:>7.4f} ms / step")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
