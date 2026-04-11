"""
Static Equilibrium.

An object is in static equilibrium when the sum of all forces acting on it
is zero in every direction:
    sum(F_x) = 0
    sum(F_y) = 0

Each force is a 2D vector (Fx, Fy).

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/in_static_equilibrium.py
"""

from __future__ import annotations


def in_static_equilibrium(
    forces: list[list[float]], tolerance: float = 1e-9
) -> bool:
    """
    Determine if a set of 2D force vectors are in static equilibrium.
    Each force is [Fx, Fy].

    >>> in_static_equilibrium([[1, 0], [-1, 0]])
    True
    >>> in_static_equilibrium([[1, 0], [0, 1], [-1, -1]])
    True
    >>> in_static_equilibrium([[1, 0], [0, 1]])
    False
    >>> in_static_equilibrium([[10, 5], [-5, -5], [-5, 0]])
    True
    >>> in_static_equilibrium([])
    True
    """
    if not forces:
        return True

    dimensions = len(forces[0])
    totals = [0.0] * dimensions

    for force in forces:
        for i in range(dimensions):
            totals[i] += force[i]

    return all(abs(t) < tolerance for t in totals)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
