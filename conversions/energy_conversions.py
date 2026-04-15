"""
Energy Conversions

Convert between various energy units.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/energy_conversions.py
"""

# All conversions relative to joules
ENERGY_CHART: dict[str, float] = {
    "joule": 1.0,
    "kilojoule": 1000.0,
    "megajoule": 1_000_000.0,
    "calorie": 4.184,
    "kilocalorie": 4184.0,
    "watt_hour": 3600.0,
    "kilowatt_hour": 3_600_000.0,
    "electronvolt": 1.602176634e-19,
    "british_thermal_unit": 1055.06,
    "foot_pound": 1.35582,
}


def energy_conversion(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert an energy value from one unit to another.

    >>> energy_conversion(1, "kilojoule", "joule")
    1000.0
    >>> energy_conversion(1, "kilocalorie", "kilojoule")
    4.184
    >>> energy_conversion(1, "kilowatt_hour", "kilojoule")
    3600.0
    >>> energy_conversion(0, "joule", "calorie")
    0.0
    >>> energy_conversion(1, "invalid", "joule")
    Traceback (most recent call last):
        ...
    ValueError: Invalid unit: invalid
    """
    from_unit = from_unit.lower().strip()
    to_unit = to_unit.lower().strip()

    if from_unit not in ENERGY_CHART:
        raise ValueError(f"Invalid unit: {from_unit}")
    if to_unit not in ENERGY_CHART:
        raise ValueError(f"Invalid unit: {to_unit}")

    joules = value * ENERGY_CHART[from_unit]
    result = joules / ENERGY_CHART[to_unit]
    return round(result, 5)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    conversions = [
        (1, "kilojoule", "joule"),
        (1, "kilocalorie", "kilojoule"),
        (1, "kilowatt_hour", "kilojoule"),
        (1, "british_thermal_unit", "joule"),
        (1, "calorie", "joule"),
    ]
    for val, f, t in conversions:
        result = energy_conversion(val, f, t)
        print(f"  {val} {f} = {result} {t}")
