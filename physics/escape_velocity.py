"""
Escape Velocity.

The minimum velocity needed for an object to escape the gravitational
influence of a massive body:
    v_e = sqrt(2 * G * M / r)

where:
    G = gravitational constant (6.674e-11 m^3 kg^-1 s^-2)
    M = mass of the body (kg)
    r = distance from the center of mass (m)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/escape_velocity.py
"""

from math import sqrt

G = 6.674e-11  # gravitational constant


def escape_velocity(mass: float, radius: float) -> float:
    """
    Calculate the escape velocity.

    >>> round(escape_velocity(5.972e24, 6.371e6), 2)
    11185.73
    >>> round(escape_velocity(1.989e30, 6.957e8), 2)
    617752.47
    >>> escape_velocity(5.972e24, 0)
    Traceback (most recent call last):
        ...
    ValueError: radius must be positive
    >>> escape_velocity(-1, 1000)
    Traceback (most recent call last):
        ...
    ValueError: mass must be non-negative
    """
    if mass < 0:
        raise ValueError("mass must be non-negative")
    if radius <= 0:
        raise ValueError("radius must be positive")

    return sqrt(2 * G * mass / radius)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
