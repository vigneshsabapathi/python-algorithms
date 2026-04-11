"""
Ideal Gas Law.

    P * V = n * R * T

where:
    P = pressure (Pa)
    V = volume (m^3)
    n = amount of substance (mol)
    R = universal gas constant (8.314462 J/(mol*K))
    T = temperature (K)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/ideal_gas_law.py
"""

R = 8.314462  # universal gas constant J/(mol*K)


def pressure(volume: float, moles: float, temperature: float) -> float:
    """
    Calculate pressure using the ideal gas law.

    >>> round(pressure(1.0, 1.0, 273.15), 2)
    2271.1
    >>> round(pressure(0.0224, 1.0, 273.15), 2)
    101388.18
    >>> pressure(0, 1, 273)
    Traceback (most recent call last):
        ...
    ValueError: volume must be positive
    >>> pressure(1, -1, 273)
    Traceback (most recent call last):
        ...
    ValueError: moles must be positive
    >>> pressure(1, 1, -1)
    Traceback (most recent call last):
        ...
    ValueError: temperature must be positive
    """
    if volume <= 0:
        raise ValueError("volume must be positive")
    if moles <= 0:
        raise ValueError("moles must be positive")
    if temperature <= 0:
        raise ValueError("temperature must be positive")

    return moles * R * temperature / volume


def volume(pressure_val: float, moles: float, temperature: float) -> float:
    """
    Calculate volume using the ideal gas law.

    >>> round(volume(101325, 1.0, 273.15), 4)
    0.0224
    >>> volume(0, 1, 273)
    Traceback (most recent call last):
        ...
    ValueError: pressure must be positive
    """
    if pressure_val <= 0:
        raise ValueError("pressure must be positive")
    if moles <= 0:
        raise ValueError("moles must be positive")
    if temperature <= 0:
        raise ValueError("temperature must be positive")

    return moles * R * temperature / pressure_val


def temperature(pressure_val: float, volume_val: float, moles: float) -> float:
    """
    Calculate temperature using the ideal gas law.

    >>> round(temperature(101325, 0.0224, 1.0), 2)
    272.98
    """
    if pressure_val <= 0:
        raise ValueError("pressure must be positive")
    if volume_val <= 0:
        raise ValueError("volume must be positive")
    if moles <= 0:
        raise ValueError("moles must be positive")

    return pressure_val * volume_val / (moles * R)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
