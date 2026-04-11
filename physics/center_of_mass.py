"""
Center of Mass.

The center of mass of a system of particles is the weighted average of
their positions:
    x_cm = sum(m_i * x_i) / sum(m_i)

For 2D: compute x_cm and y_cm independently.

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/center_of_mass.py
"""

from __future__ import annotations


def center_of_mass(
    particles: list[tuple[float, float, float]],
) -> tuple[float, float]:
    """
    Calculate the 2D center of mass for a list of particles.
    Each particle is (mass, x, y).

    >>> center_of_mass([(1, 0, 0), (1, 2, 0)])
    (1.0, 0.0)
    >>> center_of_mass([(2, 0, 0), (1, 3, 0)])
    (1.0, 0.0)
    >>> center_of_mass([(1, 0, 0), (1, 0, 2)])
    (0.0, 1.0)
    >>> center_of_mass([(5, 2, 3)])
    (2.0, 3.0)
    >>> center_of_mass([])
    Traceback (most recent call last):
        ...
    ValueError: particles list must not be empty
    >>> center_of_mass([(0, 1, 2)])
    Traceback (most recent call last):
        ...
    ValueError: mass must be positive for all particles
    >>> center_of_mass([(-1, 1, 2)])
    Traceback (most recent call last):
        ...
    ValueError: mass must be positive for all particles
    """
    if not particles:
        raise ValueError("particles list must not be empty")

    total_mass = 0.0
    x_sum = 0.0
    y_sum = 0.0

    for mass, x, y in particles:
        if mass <= 0:
            raise ValueError("mass must be positive for all particles")
        total_mass += mass
        x_sum += mass * x
        y_sum += mass * y

    return (x_sum / total_mass, y_sum / total_mass)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
