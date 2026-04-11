"""
Period of a Simple Pendulum.

    T = 2 * pi * sqrt(L / g)

where:
    T = period (s)
    L = length of pendulum (m)
    g = gravitational acceleration (m/s^2, default 9.8)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/period_of_pendulum.py
"""

from math import pi, sqrt


def period_of_pendulum(length: float, gravity: float = 9.8) -> float:
    """
    Calculate the period of a simple pendulum.

    >>> round(period_of_pendulum(1), 4)
    2.0071
    >>> round(period_of_pendulum(2), 4)
    2.8385
    >>> round(period_of_pendulum(0.5), 4)
    1.4192
    >>> period_of_pendulum(0)
    0.0
    >>> period_of_pendulum(-1)
    Traceback (most recent call last):
        ...
    ValueError: length must be non-negative
    >>> period_of_pendulum(1, 0)
    Traceback (most recent call last):
        ...
    ValueError: gravity must be positive
    """
    if length < 0:
        raise ValueError("length must be non-negative")
    if gravity <= 0:
        raise ValueError("gravity must be positive")

    return 2 * pi * sqrt(length / gravity)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
