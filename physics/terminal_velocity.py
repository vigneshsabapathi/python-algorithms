"""
Terminal Velocity.

The maximum velocity attainable by an object as it falls through a fluid:
    v_t = sqrt(2 * m * g / (rho * A * Cd))

where:
    m   = mass of the falling object (kg)
    g   = gravitational acceleration (m/s^2, default 9.8)
    rho = density of the fluid (kg/m^3)
    A   = projected cross-sectional area (m^2)
    Cd  = drag coefficient (dimensionless)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/terminal_velocity.py
"""

from math import sqrt


def terminal_velocity(
    mass: float,
    density: float,
    area: float,
    drag_coefficient: float,
    gravity: float = 9.8,
) -> float:
    """
    Calculate the terminal velocity.

    >>> round(terminal_velocity(80, 1.225, 0.7, 1.0), 2)
    42.76
    >>> round(terminal_velocity(0.001, 1.225, 0.0001, 0.47), 2)
    18.45
    >>> terminal_velocity(0, 1.225, 0.7, 1.0)
    0.0
    >>> terminal_velocity(-1, 1.225, 0.7, 1.0)
    Traceback (most recent call last):
        ...
    ValueError: mass must be non-negative
    >>> terminal_velocity(80, 0, 0.7, 1.0)
    Traceback (most recent call last):
        ...
    ValueError: density must be positive
    >>> terminal_velocity(80, 1.225, 0, 1.0)
    Traceback (most recent call last):
        ...
    ValueError: area must be positive
    >>> terminal_velocity(80, 1.225, 0.7, 0)
    Traceback (most recent call last):
        ...
    ValueError: drag_coefficient must be positive
    """
    if mass < 0:
        raise ValueError("mass must be non-negative")
    if density <= 0:
        raise ValueError("density must be positive")
    if area <= 0:
        raise ValueError("area must be positive")
    if drag_coefficient <= 0:
        raise ValueError("drag_coefficient must be positive")
    if gravity <= 0:
        raise ValueError("gravity must be positive")

    if mass == 0:
        return 0.0

    return sqrt(2 * mass * gravity / (density * area * drag_coefficient))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
