"""
N-Body Gravitational Simulation.

Simulates the gravitational interaction of N bodies using direct pairwise
force calculation (O(N^2) per time step) with a simple Euler integrator.

    F = G * m1 * m2 / r^2  (direction: along the line connecting bodies)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/n_body_simulation.py
"""

from __future__ import annotations

from math import sqrt

G = 6.674e-11  # gravitational constant


class Body:
    """A body with position, velocity, and mass in 2D."""

    def __init__(
        self,
        mass: float,
        x: float = 0.0,
        y: float = 0.0,
        vx: float = 0.0,
        vy: float = 0.0,
    ) -> None:
        """
        >>> b = Body(1e10, 0, 0, 1, 0)
        >>> b.mass
        10000000000.0
        """
        if mass <= 0:
            raise ValueError("mass must be positive")
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def distance_to(self, other: Body) -> float:
        """
        >>> Body(1, 0, 0).distance_to(Body(1, 3, 4))
        5.0
        """
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


def compute_forces(bodies: list[Body]) -> list[tuple[float, float]]:
    """
    Compute net gravitational force on each body.

    >>> b1 = Body(1e10, 0, 0)
    >>> b2 = Body(1e10, 1, 0)
    >>> forces = compute_forces([b1, b2])
    >>> forces[0][0]
    6674000000.0
    >>> forces[1][0]
    -6674000000.0
    """
    n = len(bodies)
    forces = [(0.0, 0.0)] * n
    fx = [0.0] * n
    fy = [0.0] * n

    for i in range(n):
        for j in range(i + 1, n):
            dx = bodies[j].x - bodies[i].x
            dy = bodies[j].y - bodies[i].y
            dist = sqrt(dx**2 + dy**2)
            if dist == 0:
                continue
            force = G * bodies[i].mass * bodies[j].mass / dist**2
            # Unit vector components
            ux = dx / dist
            uy = dy / dist
            fx[i] += force * ux
            fy[i] += force * uy
            fx[j] -= force * ux
            fy[j] -= force * uy

    return [(fx[i], fy[i]) for i in range(n)]


def step(bodies: list[Body], dt: float) -> None:
    """
    Advance the simulation by one time step using Euler integration.

    >>> b1 = Body(1e10, 0, 0)
    >>> b2 = Body(1e10, 10, 0)
    >>> step([b1, b2], 1.0)
    >>> b1.vx > 0  # attracted towards b2
    True
    >>> b2.vx < 0  # attracted towards b1
    True
    """
    if dt <= 0:
        raise ValueError("time step dt must be positive")

    forces = compute_forces(bodies)

    for i, body in enumerate(bodies):
        ax = forces[i][0] / body.mass
        ay = forces[i][1] / body.mass
        body.vx += ax * dt
        body.vy += ay * dt
        body.x += body.vx * dt
        body.y += body.vy * dt


def simulate(bodies: list[Body], dt: float, steps: int) -> list[Body]:
    """
    Run simulation for a given number of steps.

    >>> b1 = Body(1e10, 0, 0)
    >>> b2 = Body(1e10, 10, 0)
    >>> result = simulate([b1, b2], 1.0, 5)
    >>> len(result)
    2
    """
    for _ in range(steps):
        step(bodies, dt)
    return bodies


if __name__ == "__main__":
    import doctest

    doctest.testmod()
