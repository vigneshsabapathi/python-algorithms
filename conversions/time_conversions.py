"""
Time Conversions

Convert between various time units.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/time_conversions.py
"""

# All conversions relative to seconds
TIME_CHART: dict[str, float] = {
    "millisecond": 0.001,
    "second": 1.0,
    "minute": 60.0,
    "hour": 3600.0,
    "day": 86400.0,
    "week": 604800.0,
    "month": 2629800.0,  # average month (365.25/12 days)
    "year": 31557600.0,  # Julian year (365.25 days)
}


def time_conversion(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert a time value from one unit to another.

    >>> time_conversion(1, "hour", "minute")
    60.0
    >>> time_conversion(1, "day", "hour")
    24.0
    >>> time_conversion(1, "week", "day")
    7.0
    >>> time_conversion(1000, "millisecond", "second")
    1.0
    >>> time_conversion(0, "hour", "second")
    0.0
    >>> time_conversion(1, "invalid", "second")
    Traceback (most recent call last):
        ...
    ValueError: Invalid unit: invalid
    """
    from_unit = from_unit.lower().strip()
    to_unit = to_unit.lower().strip()

    if from_unit not in TIME_CHART:
        raise ValueError(f"Invalid unit: {from_unit}")
    if to_unit not in TIME_CHART:
        raise ValueError(f"Invalid unit: {to_unit}")

    seconds = value * TIME_CHART[from_unit]
    result = seconds / TIME_CHART[to_unit]
    return round(result, 5)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    conversions = [
        (1, "hour", "minute"),
        (1, "day", "hour"),
        (1, "week", "day"),
        (1, "year", "day"),
        (3600, "second", "hour"),
    ]
    for val, f, t in conversions:
        result = time_conversion(val, f, t)
        print(f"  {val} {f} = {result} {t}")
