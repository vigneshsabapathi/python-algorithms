"""
Newton's Second Law of Motion.

    F = m * a

where:
    F = force (N)
    m = mass (kg)
    a = acceleration (m/s^2)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/newtons_second_law_of_motion.py
"""


def force(mass: float, acceleration: float) -> float:
    """
    Calculate force from mass and acceleration.

    >>> force(10, 5)
    50
    >>> force(0.5, 9.8)
    4.9
    >>> force(0, 10)
    0
    >>> force(-1, 5)
    Traceback (most recent call last):
        ...
    ValueError: mass must be non-negative
    """
    if mass < 0:
        raise ValueError("mass must be non-negative")
    return round(mass * acceleration, 4)


def acceleration(force_val: float, mass: float) -> float:
    """
    Calculate acceleration from force and mass.

    >>> acceleration(50, 10)
    5.0
    >>> acceleration(0, 10)
    0.0
    >>> acceleration(50, 0)
    Traceback (most recent call last):
        ...
    ValueError: mass must be positive
    """
    if mass <= 0:
        raise ValueError("mass must be positive")
    return force_val / mass


def mass_from_force(force_val: float, accel: float) -> float:
    """
    Calculate mass from force and acceleration.

    >>> mass_from_force(50, 5)
    10.0
    >>> mass_from_force(50, 0)
    Traceback (most recent call last):
        ...
    ValueError: acceleration must not be zero
    """
    if accel == 0:
        raise ValueError("acceleration must not be zero")
    return force_val / accel


if __name__ == "__main__":
    import doctest

    doctest.testmod()
