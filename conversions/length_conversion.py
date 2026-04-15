"""
Length Conversion

Convert between various length/distance units.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/length_conversion.py
"""

# All conversions relative to meters
LENGTH_CHART: dict[str, float] = {
    "millimeter": 0.001,
    "centimeter": 0.01,
    "meter": 1.0,
    "kilometer": 1000.0,
    "inch": 0.0254,
    "foot": 0.3048,
    "yard": 0.9144,
    "mile": 1609.344,
    "nautical_mile": 1852.0,
}


def length_conversion(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert a length value from one unit to another.

    >>> length_conversion(1, "meter", "centimeter")
    100.0
    >>> length_conversion(1, "kilometer", "meter")
    1000.0
    >>> length_conversion(1, "mile", "kilometer")
    1.609344
    >>> length_conversion(1, "foot", "inch")
    12.0
    >>> length_conversion(1, "yard", "foot")
    3.0
    >>> length_conversion(0, "meter", "mile")
    0.0
    >>> length_conversion(1, "invalid", "meter")
    Traceback (most recent call last):
        ...
    ValueError: Invalid unit: invalid
    """
    from_unit = from_unit.lower().strip()
    to_unit = to_unit.lower().strip()

    if from_unit not in LENGTH_CHART:
        raise ValueError(f"Invalid unit: {from_unit}")
    if to_unit not in LENGTH_CHART:
        raise ValueError(f"Invalid unit: {to_unit}")

    # Convert to meters first, then to target unit
    meters = value * LENGTH_CHART[from_unit]
    return round(meters / LENGTH_CHART[to_unit], 10)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    conversions = [
        (1, "meter", "centimeter"),
        (1, "kilometer", "mile"),
        (5280, "foot", "mile"),
        (1, "mile", "kilometer"),
        (1, "nautical_mile", "kilometer"),
        (100, "centimeter", "inch"),
    ]
    for val, f, t in conversions:
        result = length_conversion(val, f, t)
        print(f"  {val} {f} = {result:.4f} {t}")
