"""
Speeds of Gas Molecules.

Three characteristic speeds of molecules in an ideal gas:

    v_rms  = sqrt(3 * R * T / M)      (root-mean-square speed)
    v_avg  = sqrt(8 * R * T / (pi*M)) (mean speed)
    v_mp   = sqrt(2 * R * T / M)      (most probable speed)

where:
    R = universal gas constant (8.314462 J/(mol*K))
    T = temperature (K)
    M = molar mass (kg/mol)

Relationship: v_mp < v_avg < v_rms

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/speeds_of_gas_molecules.py
"""

from math import pi, sqrt

R = 8.314462  # universal gas constant


def rms_speed(temperature: float, molar_mass: float) -> float:
    """
    Root-mean-square speed.

    >>> round(rms_speed(300, 0.028), 2)
    516.96
    >>> rms_speed(-1, 0.028)
    Traceback (most recent call last):
        ...
    ValueError: temperature must be positive
    """
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    if molar_mass <= 0:
        raise ValueError("molar_mass must be positive")
    return sqrt(3 * R * temperature / molar_mass)


def mean_speed(temperature: float, molar_mass: float) -> float:
    """
    Mean (average) speed.

    >>> round(mean_speed(300, 0.028), 2)
    476.29
    """
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    if molar_mass <= 0:
        raise ValueError("molar_mass must be positive")
    return sqrt(8 * R * temperature / (pi * molar_mass))


def most_probable_speed(temperature: float, molar_mass: float) -> float:
    """
    Most probable speed.

    >>> round(most_probable_speed(300, 0.028), 2)
    422.1
    """
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    if molar_mass <= 0:
        raise ValueError("molar_mass must be positive")
    return sqrt(2 * R * temperature / molar_mass)


def all_speeds(
    temperature: float, molar_mass: float
) -> dict[str, float]:
    """
    Return all three speeds as a dictionary.

    >>> speeds = all_speeds(300, 0.028)
    >>> round(speeds['most_probable'], 2)
    422.1
    >>> round(speeds['mean'], 2)
    476.29
    >>> round(speeds['rms'], 2)
    516.96
    """
    return {
        "most_probable": most_probable_speed(temperature, molar_mass),
        "mean": mean_speed(temperature, molar_mass),
        "rms": rms_speed(temperature, molar_mass),
    }


if __name__ == "__main__":
    import doctest

    doctest.testmod()
