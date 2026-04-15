"""
Weight Conversion

Convert between various weight/mass units.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/weight_conversion.py
"""

# All conversions relative to kilograms
WEIGHT_CHART: dict[str, float] = {
    "milligram": 0.000001,
    "gram": 0.001,
    "kilogram": 1.0,
    "metric_ton": 1000.0,
    "ounce": 0.0283495,
    "pound": 0.453592,
    "stone": 6.35029,
    "us_ton": 907.185,
    "imperial_ton": 1016.05,
}


def weight_conversion(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert a weight value from one unit to another.

    >>> weight_conversion(1, "kilogram", "gram")
    1000.0
    >>> weight_conversion(1, "kilogram", "pound")
    2.20462
    >>> weight_conversion(1, "pound", "ounce")
    16.0
    >>> weight_conversion(0, "gram", "kilogram")
    0.0
    >>> weight_conversion(1, "invalid", "gram")
    Traceback (most recent call last):
        ...
    ValueError: Invalid unit: invalid
    """
    from_unit = from_unit.lower().strip()
    to_unit = to_unit.lower().strip()

    if from_unit not in WEIGHT_CHART:
        raise ValueError(f"Invalid unit: {from_unit}")
    if to_unit not in WEIGHT_CHART:
        raise ValueError(f"Invalid unit: {to_unit}")

    kilograms = value * WEIGHT_CHART[from_unit]
    result = kilograms / WEIGHT_CHART[to_unit]
    return round(result, 5)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    conversions = [
        (1, "kilogram", "gram"),
        (1, "kilogram", "pound"),
        (1, "pound", "ounce"),
        (1, "metric_ton", "kilogram"),
        (100, "gram", "ounce"),
    ]
    for val, f, t in conversions:
        result = weight_conversion(val, f, t)
        print(f"  {val} {f} = {result} {t}")
