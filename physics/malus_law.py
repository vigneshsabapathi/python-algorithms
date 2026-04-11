"""
Malus's Law.

When polarized light passes through a polarizing filter, the transmitted
intensity is:
    I = I0 * cos^2(theta)

where:
    I0    = initial intensity (W/m^2)
    theta = angle between polarization direction and filter axis (radians)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/malus_law.py
"""

from math import cos, pi


def malus_law(initial_intensity: float, angle: float) -> float:
    """
    Calculate transmitted intensity using Malus's Law.

    >>> malus_law(100, 0)
    100.0
    >>> round(malus_law(100, pi / 4), 4)
    50.0
    >>> round(malus_law(100, pi / 2), 4)
    0.0
    >>> round(malus_law(100, pi / 3), 4)
    25.0
    >>> malus_law(-1, 0)
    Traceback (most recent call last):
        ...
    ValueError: initial_intensity must be non-negative
    """
    if initial_intensity < 0:
        raise ValueError("initial_intensity must be non-negative")

    return round(initial_intensity * cos(angle) ** 2, 4)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
