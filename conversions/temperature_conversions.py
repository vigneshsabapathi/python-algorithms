"""
Temperature Conversions

Convert between Celsius, Fahrenheit, Kelvin, and Rankine temperature scales.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/temperature_conversions.py
"""


def celsius_to_fahrenheit(celsius: float, ndigits: int = 2) -> float:
    """
    >>> celsius_to_fahrenheit(0)
    32.0
    >>> celsius_to_fahrenheit(100)
    212.0
    >>> celsius_to_fahrenheit(-40)
    -40.0
    >>> celsius_to_fahrenheit(37)
    98.6
    """
    return round(celsius * 9 / 5 + 32, ndigits)


def fahrenheit_to_celsius(fahrenheit: float, ndigits: int = 2) -> float:
    """
    >>> fahrenheit_to_celsius(32)
    0.0
    >>> fahrenheit_to_celsius(212)
    100.0
    >>> fahrenheit_to_celsius(-40)
    -40.0
    >>> fahrenheit_to_celsius(98.6)
    37.0
    """
    return round((fahrenheit - 32) * 5 / 9, ndigits)


def celsius_to_kelvin(celsius: float, ndigits: int = 2) -> float:
    """
    >>> celsius_to_kelvin(0)
    273.15
    >>> celsius_to_kelvin(100)
    373.15
    >>> celsius_to_kelvin(-273.15)
    0.0
    """
    return round(celsius + 273.15, ndigits)


def kelvin_to_celsius(kelvin: float, ndigits: int = 2) -> float:
    """
    >>> kelvin_to_celsius(273.15)
    0.0
    >>> kelvin_to_celsius(373.15)
    100.0
    >>> kelvin_to_celsius(0)
    -273.15
    """
    return round(kelvin - 273.15, ndigits)


def fahrenheit_to_kelvin(fahrenheit: float, ndigits: int = 2) -> float:
    """
    >>> fahrenheit_to_kelvin(32)
    273.15
    >>> fahrenheit_to_kelvin(212)
    373.15
    """
    return round((fahrenheit - 32) * 5 / 9 + 273.15, ndigits)


def kelvin_to_fahrenheit(kelvin: float, ndigits: int = 2) -> float:
    """
    >>> kelvin_to_fahrenheit(273.15)
    32.0
    >>> kelvin_to_fahrenheit(373.15)
    212.0
    """
    return round((kelvin - 273.15) * 9 / 5 + 32, ndigits)


def celsius_to_rankine(celsius: float, ndigits: int = 2) -> float:
    """
    >>> celsius_to_rankine(0)
    491.67
    >>> celsius_to_rankine(100)
    671.67
    """
    return round((celsius + 273.15) * 9 / 5, ndigits)


def rankine_to_celsius(rankine: float, ndigits: int = 2) -> float:
    """
    >>> rankine_to_celsius(491.67)
    0.0
    >>> rankine_to_celsius(671.67)
    100.0
    """
    return round((rankine / (9 / 5)) - 273.15, ndigits)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print("  Temperature Conversions:")
    print(f"    0C  -> {celsius_to_fahrenheit(0)}F")
    print(f"    100C -> {celsius_to_fahrenheit(100)}F")
    print(f"    0C  -> {celsius_to_kelvin(0)}K")
    print(f"    32F -> {fahrenheit_to_celsius(32)}C")
    print(f"    212F -> {fahrenheit_to_kelvin(212)}K")
    print(f"    0C  -> {celsius_to_rankine(0)}R")
    print(f"    491.67R -> {rankine_to_celsius(491.67)}C")
