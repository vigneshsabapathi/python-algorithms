"""
Basic Orbital Capture.

Determines if a satellite can be captured into orbit around a body based on
its velocity relative to the escape velocity.

Escape velocity:  v_e = sqrt(2 * G * M / r)

A satellite is captured if its velocity < escape velocity at the given distance.

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/basic_orbital_capture.py
"""

from math import sqrt

# Gravitational constant
G = 6.674e-11  # m^3 kg^-1 s^-2


def escape_velocity(mass: float, radius: float) -> float:
    """
    Calculate the escape velocity for a body of given mass at a given distance.

    >>> round(escape_velocity(5.972e24, 6.371e6), 2)
    11185.73
    >>> escape_velocity(0, 1000)
    0.0
    >>> escape_velocity(5.972e24, -1)
    Traceback (most recent call last):
        ...
    ValueError: radius must be positive
    """
    if radius <= 0:
        raise ValueError("radius must be positive")
    if mass < 0:
        raise ValueError("mass must be non-negative")
    return sqrt(2 * G * mass / radius)


def is_captured(mass: float, radius: float, velocity: float) -> bool:
    """
    Determine if a satellite with the given velocity will be captured.

    >>> is_captured(5.972e24, 6.371e6, 5000)
    True
    >>> is_captured(5.972e24, 6.371e6, 20000)
    False
    >>> is_captured(5.972e24, 6.371e6, -1)
    Traceback (most recent call last):
        ...
    ValueError: velocity must be non-negative
    """
    if velocity < 0:
        raise ValueError("velocity must be non-negative")
    return velocity < escape_velocity(mass, radius)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
