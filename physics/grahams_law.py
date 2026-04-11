"""
Graham's Law of Effusion.

The rate of effusion of a gas is inversely proportional to the square root
of its molar mass:
    rate1 / rate2 = sqrt(M2 / M1)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/grahams_law.py
"""

from math import sqrt


def grahams_law(
    molar_mass_1: float, molar_mass_2: float
) -> float:
    """
    Calculate the ratio of effusion rates (rate1/rate2) for two gases.

    >>> round(grahams_law(2, 32), 4)
    4.0
    >>> round(grahams_law(4, 28), 4)
    2.6458
    >>> round(grahams_law(28, 28), 4)
    1.0
    >>> grahams_law(0, 32)
    Traceback (most recent call last):
        ...
    ValueError: molar masses must be positive
    >>> grahams_law(2, -1)
    Traceback (most recent call last):
        ...
    ValueError: molar masses must be positive
    """
    if molar_mass_1 <= 0 or molar_mass_2 <= 0:
        raise ValueError("molar masses must be positive")

    return sqrt(molar_mass_2 / molar_mass_1)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
