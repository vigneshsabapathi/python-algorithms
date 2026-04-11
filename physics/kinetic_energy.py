"""
Kinetic Energy.

The kinetic energy of an object is the energy it possesses due to its motion:
    KE = 0.5 * m * v^2

where:
    m = mass (kg)
    v = velocity (m/s)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/kinetic_energy.py
"""


def kinetic_energy(mass: float, velocity: float) -> float:
    """
    Calculate the kinetic energy of an object.

    >>> kinetic_energy(10, 5)
    125.0
    >>> kinetic_energy(1, 10)
    50.0
    >>> kinetic_energy(5, 0)
    0.0
    >>> kinetic_energy(0, 10)
    0.0
    >>> kinetic_energy(-1, 5)
    Traceback (most recent call last):
        ...
    ValueError: mass must be non-negative
    >>> kinetic_energy(1, -5)
    Traceback (most recent call last):
        ...
    ValueError: velocity must be non-negative
    """
    if mass < 0:
        raise ValueError("mass must be non-negative")
    if velocity < 0:
        raise ValueError("velocity must be non-negative")

    return 0.5 * mass * velocity**2


if __name__ == "__main__":
    import doctest

    doctest.testmod()
