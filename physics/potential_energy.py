"""
Potential Energy (Gravitational).

    PE = m * g * h

where:
    m = mass (kg)
    g = gravitational acceleration (m/s^2, default 9.8)
    h = height above reference point (m)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/potential_energy.py
"""


def potential_energy(
    mass: float, height: float, gravity: float = 9.8
) -> float:
    """
    Calculate gravitational potential energy.

    >>> potential_energy(10, 5)
    490.0
    >>> potential_energy(1, 100)
    980.0000000000001
    >>> potential_energy(5, 0)
    0.0
    >>> potential_energy(-1, 5)
    Traceback (most recent call last):
        ...
    ValueError: mass must be non-negative
    >>> potential_energy(1, -5)
    Traceback (most recent call last):
        ...
    ValueError: height must be non-negative
    >>> potential_energy(1, 5, -9.8)
    Traceback (most recent call last):
        ...
    ValueError: gravity must be positive
    """
    if mass < 0:
        raise ValueError("mass must be non-negative")
    if height < 0:
        raise ValueError("height must be non-negative")
    if gravity <= 0:
        raise ValueError("gravity must be positive")

    return mass * gravity * height


if __name__ == "__main__":
    import doctest

    doctest.testmod()
