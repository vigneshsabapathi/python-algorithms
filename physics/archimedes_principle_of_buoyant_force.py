"""
Archimedes' Principle of Buoyant Force.

The buoyant force on an object submerged in a fluid equals the weight of the
fluid displaced by the object:
    F_b = rho * g * V

where:
    rho = density of the fluid (kg/m^3)
    g   = gravitational acceleration (9.8 m/s^2 default)
    V   = volume of fluid displaced (m^3)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/archimedes_principle_of_buoyant_force.py
"""


def archimedes_principle(
    fluid_density: float,
    volume_displaced: float,
    gravity: float = 9.8,
) -> float:
    """
    Calculate the buoyant force using Archimedes' principle.

    >>> archimedes_principle(1000, 0.5)
    4900.0
    >>> archimedes_principle(1000, 0)
    0.0
    >>> archimedes_principle(1.225, 2.0)
    24.01
    >>> archimedes_principle(-1, 0.5)
    Traceback (most recent call last):
        ...
    ValueError: fluid_density must be positive
    >>> archimedes_principle(1000, -0.5)
    Traceback (most recent call last):
        ...
    ValueError: volume_displaced must be non-negative
    >>> archimedes_principle(1000, 0.5, gravity=-9.8)
    Traceback (most recent call last):
        ...
    ValueError: gravity must be positive
    """
    if fluid_density <= 0:
        raise ValueError("fluid_density must be positive")
    if volume_displaced < 0:
        raise ValueError("volume_displaced must be non-negative")
    if gravity <= 0:
        raise ValueError("gravity must be positive")

    return round(fluid_density * gravity * volume_displaced, 2)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
