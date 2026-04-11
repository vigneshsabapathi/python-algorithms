"""
Centripetal Force.

The centripetal force is the force required to keep an object moving in a
circular path:
    F = m * v^2 / r

where:
    m = mass of the object (kg)
    v = velocity / speed of the object (m/s)
    r = radius of the circular path (m)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/centripetal_force.py
"""


def centripetal_force(mass: float, velocity: float, radius: float) -> float:
    """
    Calculate the centripetal force.

    >>> centripetal_force(10, 5, 2)
    125.0
    >>> centripetal_force(1, 10, 5)
    20.0
    >>> centripetal_force(5, 0, 3)
    0.0
    >>> centripetal_force(-1, 5, 2)
    Traceback (most recent call last):
        ...
    ValueError: mass must be positive
    >>> centripetal_force(10, 5, 0)
    Traceback (most recent call last):
        ...
    ValueError: radius must be positive
    >>> centripetal_force(10, -5, 2)
    Traceback (most recent call last):
        ...
    ValueError: velocity must be non-negative
    """
    if mass <= 0:
        raise ValueError("mass must be positive")
    if radius <= 0:
        raise ValueError("radius must be positive")
    if velocity < 0:
        raise ValueError("velocity must be non-negative")

    return mass * velocity**2 / radius


if __name__ == "__main__":
    import doctest

    doctest.testmod()
