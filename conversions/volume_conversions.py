"""
Volume Conversions

Convert between various volume units.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/volume_conversions.py
"""

# All conversions relative to liters
VOLUME_CHART: dict[str, float] = {
    "milliliter": 0.001,
    "liter": 1.0,
    "kiloliter": 1000.0,
    "cubic_meter": 1000.0,
    "gallon": 3.78541,       # US gallon
    "quart": 0.946353,       # US quart
    "pint": 0.473176,        # US pint
    "cup": 0.236588,         # US cup
    "fluid_ounce": 0.0295735,
    "tablespoon": 0.0147868,
    "teaspoon": 0.00492892,
    "cubic_foot": 28.3168,
    "cubic_inch": 0.0163871,
}


def volume_conversion(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert a volume value from one unit to another.

    >>> volume_conversion(1, "liter", "milliliter")
    1000.0
    >>> volume_conversion(1, "gallon", "liter")
    3.78541
    >>> volume_conversion(1, "liter", "quart")
    1.05669
    >>> volume_conversion(0, "cup", "liter")
    0.0
    >>> volume_conversion(1, "invalid", "liter")
    Traceback (most recent call last):
        ...
    ValueError: Invalid unit: invalid
    """
    from_unit = from_unit.lower().strip()
    to_unit = to_unit.lower().strip()

    if from_unit not in VOLUME_CHART:
        raise ValueError(f"Invalid unit: {from_unit}")
    if to_unit not in VOLUME_CHART:
        raise ValueError(f"Invalid unit: {to_unit}")

    liters = value * VOLUME_CHART[from_unit]
    result = liters / VOLUME_CHART[to_unit]
    return round(result, 5)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    conversions = [
        (1, "liter", "milliliter"),
        (1, "gallon", "liter"),
        (1, "liter", "quart"),
        (1, "cup", "fluid_ounce"),
        (1, "cubic_meter", "liter"),
    ]
    for val, f, t in conversions:
        result = volume_conversion(val, f, t)
        print(f"  {val} {f} = {result} {t}")
