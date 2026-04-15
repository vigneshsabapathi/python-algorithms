"""
Speed Conversions

Convert between various speed/velocity units.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/speed_conversions.py
"""

# All conversions relative to meters per second (m/s)
SPEED_CHART: dict[str, float] = {
    "meters_per_second": 1.0,
    "kilometers_per_hour": 0.277778,
    "miles_per_hour": 0.44704,
    "knot": 0.514444,
    "feet_per_second": 0.3048,
    "mach": 340.29,  # at sea level, 20C
}


def speed_conversion(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert a speed value from one unit to another.

    >>> speed_conversion(1, "meters_per_second", "kilometers_per_hour")
    3.6
    >>> speed_conversion(100, "kilometers_per_hour", "miles_per_hour")
    62.13717
    >>> speed_conversion(1, "mach", "meters_per_second")
    340.29
    >>> speed_conversion(0, "knot", "miles_per_hour")
    0.0
    >>> speed_conversion(1, "invalid", "knot")
    Traceback (most recent call last):
        ...
    ValueError: Invalid unit: invalid
    """
    from_unit = from_unit.lower().strip()
    to_unit = to_unit.lower().strip()

    if from_unit not in SPEED_CHART:
        raise ValueError(f"Invalid unit: {from_unit}")
    if to_unit not in SPEED_CHART:
        raise ValueError(f"Invalid unit: {to_unit}")

    mps = value * SPEED_CHART[from_unit]
    result = mps / SPEED_CHART[to_unit]
    return round(result, 5)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    conversions = [
        (1, "meters_per_second", "kilometers_per_hour"),
        (100, "kilometers_per_hour", "miles_per_hour"),
        (60, "miles_per_hour", "knot"),
        (1, "mach", "kilometers_per_hour"),
    ]
    for val, f, t in conversions:
        result = speed_conversion(val, f, t)
        print(f"  {val} {f} = {result} {t}")
