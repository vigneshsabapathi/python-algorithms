"""
Astronomical Length Scale Conversion

Convert between astronomical distance units.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/astronomical_length_scale_conversion.py
"""

# All conversions relative to meters
ASTRONOMICAL_UNITS: dict[str, float] = {
    "meter": 1.0,
    "kilometer": 1e3,
    "astronomical_unit": 1.495978707e11,
    "light_year": 9.4607304725808e15,
    "light_minute": 1.799e10,
    "light_second": 2.998e8,
    "parsec": 3.0856775814913673e16,
    "kiloparsec": 3.0856775814913673e19,
    "megaparsec": 3.0856775814913673e22,
    "gigaparsec": 3.0856775814913673e25,
}


def astronomical_length_conversion(
    value: float, from_unit: str, to_unit: str
) -> float:
    """
    Convert between astronomical length units.

    >>> astronomical_length_conversion(1, "light_year", "kilometer")
    9460730472580.8
    >>> astronomical_length_conversion(1, "parsec", "light_year")
    3.26156
    >>> astronomical_length_conversion(1, "astronomical_unit", "kilometer")
    149597870.7
    >>> astronomical_length_conversion(0, "meter", "light_year")
    0.0
    >>> astronomical_length_conversion(1, "invalid", "meter")
    Traceback (most recent call last):
        ...
    ValueError: Invalid unit: invalid
    """
    from_unit = from_unit.lower().strip()
    to_unit = to_unit.lower().strip()

    if from_unit not in ASTRONOMICAL_UNITS:
        raise ValueError(f"Invalid unit: {from_unit}")
    if to_unit not in ASTRONOMICAL_UNITS:
        raise ValueError(f"Invalid unit: {to_unit}")

    meters = value * ASTRONOMICAL_UNITS[from_unit]
    result = meters / ASTRONOMICAL_UNITS[to_unit]
    return round(result, 5)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    conversions = [
        (1, "light_year", "kilometer"),
        (1, "parsec", "light_year"),
        (1, "astronomical_unit", "kilometer"),
        (1, "megaparsec", "light_year"),
    ]
    for val, f, t in conversions:
        result = astronomical_length_conversion(val, f, t)
        print(f"  {val} {f} = {result} {t}")
