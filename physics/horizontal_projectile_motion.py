"""
Horizontal Projectile Motion.

An object launched horizontally from a height h with initial horizontal
velocity v_x (no initial vertical velocity):
    Time of flight:   t = sqrt(2 * h / g)
    Range:            R = v_x * t
    Final vertical velocity: v_y = g * t

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/horizontal_projectile_motion.py
"""

from math import sqrt


def time_of_flight(height: float, gravity: float = 9.8) -> float:
    """
    Calculate the time of flight for horizontal projectile motion.

    >>> round(time_of_flight(10), 4)
    1.4286
    >>> round(time_of_flight(45), 4)
    3.0305
    >>> time_of_flight(-1)
    Traceback (most recent call last):
        ...
    ValueError: height must be non-negative
    """
    if height < 0:
        raise ValueError("height must be non-negative")
    if gravity <= 0:
        raise ValueError("gravity must be positive")
    return sqrt(2 * height / gravity)


def horizontal_range(
    velocity: float, height: float, gravity: float = 9.8
) -> float:
    """
    Calculate the horizontal range.

    >>> round(horizontal_range(10, 10), 4)
    14.2857
    >>> round(horizontal_range(20, 45), 4)
    60.6092
    >>> horizontal_range(-1, 10)
    Traceback (most recent call last):
        ...
    ValueError: velocity must be non-negative
    """
    if velocity < 0:
        raise ValueError("velocity must be non-negative")
    t = time_of_flight(height, gravity)
    return velocity * t


def final_vertical_velocity(height: float, gravity: float = 9.8) -> float:
    """
    Calculate the final vertical velocity on impact.

    >>> round(final_vertical_velocity(10), 4)
    14.0
    >>> round(final_vertical_velocity(45), 4)
    29.6985
    """
    t = time_of_flight(height, gravity)
    return gravity * t


if __name__ == "__main__":
    import doctest

    doctest.testmod()
