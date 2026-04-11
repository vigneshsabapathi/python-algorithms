"""
Hubble Parameter.

Hubble's Law describes the relationship between a galaxy's distance and
its recession velocity:
    v = H0 * d

where:
    v  = recession velocity (km/s)
    H0 = Hubble constant (km/s/Mpc, typically ~70)
    d  = distance to the galaxy (Mpc)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/hubble_parameter.py
"""


def hubble_velocity(
    distance: float, hubble_constant: float = 70.0
) -> float:
    """
    Calculate the recession velocity of a galaxy.

    >>> hubble_velocity(100)
    7000.0
    >>> hubble_velocity(0)
    0.0
    >>> hubble_velocity(10, 73.0)
    730.0
    >>> hubble_velocity(-1)
    Traceback (most recent call last):
        ...
    ValueError: distance must be non-negative
    >>> hubble_velocity(1, -70)
    Traceback (most recent call last):
        ...
    ValueError: hubble_constant must be positive
    """
    if distance < 0:
        raise ValueError("distance must be non-negative")
    if hubble_constant <= 0:
        raise ValueError("hubble_constant must be positive")

    return hubble_constant * distance


def hubble_distance(
    velocity: float, hubble_constant: float = 70.0
) -> float:
    """
    Calculate distance from recession velocity.

    >>> hubble_distance(7000)
    100.0
    >>> hubble_distance(0)
    0.0
    >>> hubble_distance(-1)
    Traceback (most recent call last):
        ...
    ValueError: velocity must be non-negative
    """
    if velocity < 0:
        raise ValueError("velocity must be non-negative")
    if hubble_constant <= 0:
        raise ValueError("hubble_constant must be positive")

    return velocity / hubble_constant


if __name__ == "__main__":
    import doctest

    doctest.testmod()
