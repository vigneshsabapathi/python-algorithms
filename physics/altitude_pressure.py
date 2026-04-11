"""
Calculate atmospheric pressure at a given altitude using the barometric formula.

The barometric formula relates the pressure at a given altitude to the pressure
at sea level:
    P = P0 * (1 - (L * h) / T0) ^ (g * M / (R * L))

where:
    P0 = sea level standard atmospheric pressure (101325 Pa)
    L  = temperature lapse rate (0.0065 K/m)
    h  = altitude (meters)
    T0 = sea level standard temperature (288.15 K)
    g  = gravitational acceleration (9.80665 m/s^2)
    M  = molar mass of dry air (0.0289644 kg/mol)
    R  = universal gas constant (8.31447 J/(mol*K))

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/altitude_pressure.py
"""


def altitude_pressure(
    altitude: float,
    pressure_at_sea_level: float = 101325.0,
    temperature_at_sea_level: float = 288.15,
) -> float:
    """
    Calculate atmospheric pressure at a given altitude.

    >>> altitude_pressure(0)
    101325.0
    >>> round(altitude_pressure(1000), 2)
    89874.76
    >>> round(altitude_pressure(5000), 2)
    54020.53
    >>> round(altitude_pressure(10000), 2)
    26436.91
    >>> altitude_pressure(-1)
    Traceback (most recent call last):
        ...
    ValueError: altitude must be non-negative
    >>> altitude_pressure(1000, pressure_at_sea_level=-1)
    Traceback (most recent call last):
        ...
    ValueError: pressure_at_sea_level must be positive
    >>> altitude_pressure(1000, temperature_at_sea_level=-1)
    Traceback (most recent call last):
        ...
    ValueError: temperature_at_sea_level must be positive
    """
    if altitude < 0:
        raise ValueError("altitude must be non-negative")
    if pressure_at_sea_level <= 0:
        raise ValueError("pressure_at_sea_level must be positive")
    if temperature_at_sea_level <= 0:
        raise ValueError("temperature_at_sea_level must be positive")

    # Constants
    lapse_rate = 0.0065  # K/m
    gravitational_accel = 9.80665  # m/s^2
    molar_mass_air = 0.0289644  # kg/mol
    gas_constant = 8.31447  # J/(mol*K)

    exponent = gravitational_accel * molar_mass_air / (gas_constant * lapse_rate)

    return pressure_at_sea_level * (
        1 - (lapse_rate * altitude) / temperature_at_sea_level
    ) ** exponent


if __name__ == "__main__":
    import doctest

    doctest.testmod()
