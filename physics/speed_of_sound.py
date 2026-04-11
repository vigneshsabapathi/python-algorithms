"""
Speed of Sound.

In an ideal gas:
    v = sqrt(gamma * R * T / M)

where:
    gamma = adiabatic index (ratio of specific heats; 1.4 for air)
    R     = universal gas constant (8.314462 J/(mol*K))
    T     = temperature (K)
    M     = molar mass of the gas (kg/mol; 0.029 for air)

Simplified for air:
    v ≈ 331.3 + 0.606 * T_celsius

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/speed_of_sound.py
"""

from math import sqrt

R = 8.314462  # universal gas constant


def speed_of_sound(
    temperature: float,
    gamma: float = 1.4,
    molar_mass: float = 0.029,
) -> float:
    """
    Calculate the speed of sound in an ideal gas.

    >>> round(speed_of_sound(293.15), 2)
    343.03
    >>> round(speed_of_sound(273.15), 2)
    331.12
    >>> round(speed_of_sound(373.15), 2)
    387.01
    >>> speed_of_sound(0)
    Traceback (most recent call last):
        ...
    ValueError: temperature must be positive
    >>> speed_of_sound(300, gamma=0)
    Traceback (most recent call last):
        ...
    ValueError: gamma must be positive
    """
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    if gamma <= 0:
        raise ValueError("gamma must be positive")
    if molar_mass <= 0:
        raise ValueError("molar_mass must be positive")

    return sqrt(gamma * R * temperature / molar_mass)


def speed_of_sound_air(celsius: float) -> float:
    """
    Simplified speed of sound in air from temperature in Celsius.

    >>> round(speed_of_sound_air(20), 2)
    343.42
    >>> round(speed_of_sound_air(0), 2)
    331.3
    >>> speed_of_sound_air(-274)
    Traceback (most recent call last):
        ...
    ValueError: temperature must be above absolute zero (-273.15 C)
    """
    if celsius < -273.15:
        raise ValueError("temperature must be above absolute zero (-273.15 C)")

    return 331.3 + 0.606 * celsius


if __name__ == "__main__":
    import doctest

    doctest.testmod()
