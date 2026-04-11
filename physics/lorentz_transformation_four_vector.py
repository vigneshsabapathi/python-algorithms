"""
Lorentz Transformation (Four-Vector).

In special relativity, the Lorentz transformation converts coordinates
between two inertial frames moving at relative velocity v:

    gamma = 1 / sqrt(1 - beta^2)
    beta  = v / c

    t' = gamma * (t - beta * x / c)
    x' = gamma * (x - v * t)
    y' = y
    z' = z

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/lorentz_transformation_four_vector.py
"""

from __future__ import annotations

from math import sqrt

C = 299792458  # speed of light (m/s)


def lorentz_factor(velocity: float) -> float:
    """
    Calculate the Lorentz factor (gamma).

    >>> lorentz_factor(0)
    1.0
    >>> round(lorentz_factor(0.5 * 299792458), 4)
    1.1547
    >>> round(lorentz_factor(0.9 * 299792458), 4)
    2.2942
    >>> lorentz_factor(299792458)
    Traceback (most recent call last):
        ...
    ValueError: velocity must be less than the speed of light
    >>> lorentz_factor(-299792458)
    Traceback (most recent call last):
        ...
    ValueError: velocity must be less than the speed of light
    """
    if abs(velocity) >= C:
        raise ValueError("velocity must be less than the speed of light")

    beta = velocity / C
    return 1.0 / sqrt(1 - beta**2)


def lorentz_transform(
    event: tuple[float, float, float, float],
    velocity: float,
) -> tuple[float, float, float, float]:
    """
    Apply Lorentz transformation to a four-vector (t, x, y, z).

    Returns the transformed (t', x', y', z') in the primed frame.

    >>> t, x, y, z = lorentz_transform((1, 0, 0, 0), 0)
    >>> (round(t, 4), round(x, 4), y, z)
    (1.0, 0.0, 0, 0)
    >>> t, x, y, z = lorentz_transform((0, 1, 0, 0), 0)
    >>> (round(t, 4), round(x, 4), y, z)
    (0.0, 1.0, 0, 0)
    """
    t, x, y, z = event
    gamma = lorentz_factor(velocity)
    beta = velocity / C

    t_prime = gamma * (t - beta * x / C)
    x_prime = gamma * (x - velocity * t)
    y_prime = y
    z_prime = z

    return (t_prime, x_prime, y_prime, z_prime)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
