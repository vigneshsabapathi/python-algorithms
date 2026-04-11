"""
Shear Stress.

    tau = F / A

where:
    tau = shear stress (Pa)
    F   = force applied parallel to the surface (N)
    A   = cross-sectional area (m^2)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/shear_stress.py
"""


def shear_stress(force: float, area: float) -> float:
    """
    Calculate shear stress.

    >>> shear_stress(100, 0.01)
    10000.0
    >>> shear_stress(500, 0.05)
    10000.0
    >>> shear_stress(0, 1)
    0.0
    >>> shear_stress(100, 0)
    Traceback (most recent call last):
        ...
    ValueError: area must be positive
    >>> shear_stress(100, -1)
    Traceback (most recent call last):
        ...
    ValueError: area must be positive
    """
    if area <= 0:
        raise ValueError("area must be positive")

    return force / area


if __name__ == "__main__":
    import doctest

    doctest.testmod()
