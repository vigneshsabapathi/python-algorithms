"""
RMS Speed of a Molecule.

The root-mean-square speed of molecules in an ideal gas:
    v_rms = sqrt(3 * R * T / M)

where:
    R = universal gas constant (8.314462 J/(mol*K))
    T = temperature (K)
    M = molar mass (kg/mol)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/rms_speed_of_molecule.py
"""

from math import sqrt

R = 8.314462  # universal gas constant J/(mol*K)


def rms_speed(temperature: float, molar_mass: float) -> float:
    """
    Calculate the RMS speed of molecules.

    >>> round(rms_speed(300, 0.028), 2)
    516.96
    >>> round(rms_speed(300, 0.032), 2)
    483.57
    >>> round(rms_speed(300, 0.002), 2)
    1934.3
    >>> rms_speed(-1, 0.028)
    Traceback (most recent call last):
        ...
    ValueError: temperature must be positive
    >>> rms_speed(300, 0)
    Traceback (most recent call last):
        ...
    ValueError: molar_mass must be positive
    """
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    if molar_mass <= 0:
        raise ValueError("molar_mass must be positive")

    return sqrt(3 * R * temperature / molar_mass)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
