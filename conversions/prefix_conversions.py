"""
Prefix Conversions (Numeric)

Convert between SI metric prefixes numerically.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/prefix_conversions.py
"""

SI_PREFIXES: dict[str, float] = {
    "yocto": 1e-24,
    "zepto": 1e-21,
    "atto": 1e-18,
    "femto": 1e-15,
    "pico": 1e-12,
    "nano": 1e-9,
    "micro": 1e-6,
    "milli": 1e-3,
    "centi": 1e-2,
    "deci": 1e-1,
    "base": 1.0,
    "deca": 1e1,
    "hecto": 1e2,
    "kilo": 1e3,
    "mega": 1e6,
    "giga": 1e9,
    "tera": 1e12,
    "peta": 1e15,
    "exa": 1e18,
    "zetta": 1e21,
    "yotta": 1e24,
}


def prefix_conversion(value: float, from_prefix: str, to_prefix: str) -> float:
    """
    Convert a value from one SI prefix to another.

    >>> prefix_conversion(1, "kilo", "base")
    1000.0
    >>> prefix_conversion(1, "mega", "kilo")
    1000.0
    >>> prefix_conversion(1, "base", "milli")
    1000.0
    >>> prefix_conversion(1, "giga", "mega")
    1000.0
    >>> prefix_conversion(0, "kilo", "mega")
    0.0
    >>> prefix_conversion(1, "invalid", "kilo")
    Traceback (most recent call last):
        ...
    ValueError: Invalid prefix: invalid
    """
    from_prefix = from_prefix.lower().strip()
    to_prefix = to_prefix.lower().strip()

    if from_prefix not in SI_PREFIXES:
        raise ValueError(f"Invalid prefix: {from_prefix}")
    if to_prefix not in SI_PREFIXES:
        raise ValueError(f"Invalid prefix: {to_prefix}")

    base_value = value * SI_PREFIXES[from_prefix]
    result = base_value / SI_PREFIXES[to_prefix]
    return round(result, 10)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    conversions = [
        (1, "kilo", "base"),
        (1, "mega", "kilo"),
        (1, "giga", "mega"),
        (1500, "milli", "base"),
        (1, "micro", "nano"),
    ]
    for val, f, t in conversions:
        result = prefix_conversion(val, f, t)
        print(f"  {val} {f} = {result} {t}")
