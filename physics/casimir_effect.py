"""
Casimir Effect.

The Casimir effect is a small attractive force between two close parallel
uncharged conducting plates caused by quantum vacuum fluctuations.

    F/A = -(pi^2 * hbar * c) / (240 * d^4)

where:
    F/A  = force per unit area (N/m^2)
    hbar = reduced Planck constant (1.0545718e-34 J*s)
    c    = speed of light (299792458 m/s)
    d    = distance between the plates (m)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/casimir_effect.py
"""

from math import pi

HBAR = 1.0545718e-34  # reduced Planck constant (J*s)
C = 299792458  # speed of light (m/s)


def casimir_force_per_area(distance: float) -> float:
    """
    Calculate the Casimir force per unit area between two parallel plates.

    Returns a negative value (attractive force).

    >>> round(casimir_force_per_area(1e-6), 4)
    -0.0013
    >>> round(casimir_force_per_area(1e-7), 2)
    -13.0
    >>> casimir_force_per_area(0)
    Traceback (most recent call last):
        ...
    ValueError: distance must be positive
    >>> casimir_force_per_area(-1e-6)
    Traceback (most recent call last):
        ...
    ValueError: distance must be positive
    """
    if distance <= 0:
        raise ValueError("distance must be positive")

    return -(pi**2 * HBAR * C) / (240 * distance**4)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
