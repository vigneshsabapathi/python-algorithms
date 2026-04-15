"""
Pressure Conversions

Convert between various pressure units.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/pressure_conversions.py
"""

# All conversions relative to pascals
PRESSURE_CHART: dict[str, float] = {
    "pascal": 1.0,
    "kilopascal": 1000.0,
    "megapascal": 1_000_000.0,
    "bar": 100_000.0,
    "millibar": 100.0,
    "atmosphere": 101_325.0,
    "torr": 133.322,
    "psi": 6894.76,
}


def pressure_conversion(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert a pressure value from one unit to another.

    >>> pressure_conversion(1, "atmosphere", "pascal")
    101325.0
    >>> pressure_conversion(1, "bar", "kilopascal")
    100.0
    >>> pressure_conversion(1, "atmosphere", "bar")
    1.01325
    >>> pressure_conversion(0, "psi", "pascal")
    0.0
    >>> pressure_conversion(1, "invalid", "pascal")
    Traceback (most recent call last):
        ...
    ValueError: Invalid unit: invalid
    """
    from_unit = from_unit.lower().strip()
    to_unit = to_unit.lower().strip()

    if from_unit not in PRESSURE_CHART:
        raise ValueError(f"Invalid unit: {from_unit}")
    if to_unit not in PRESSURE_CHART:
        raise ValueError(f"Invalid unit: {to_unit}")

    pascals = value * PRESSURE_CHART[from_unit]
    result = pascals / PRESSURE_CHART[to_unit]
    return round(result, 5)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    conversions = [
        (1, "atmosphere", "pascal"),
        (1, "bar", "kilopascal"),
        (1, "atmosphere", "bar"),
        (14.696, "psi", "atmosphere"),
        (760, "torr", "atmosphere"),
    ]
    for val, f, t in conversions:
        result = pressure_conversion(val, f, t)
        print(f"  {val} {f} = {result} {t}")
