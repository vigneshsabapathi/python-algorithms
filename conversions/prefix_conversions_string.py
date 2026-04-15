"""
Prefix Conversions (String)

Convert between SI metric prefix string representations (e.g., "1 km" -> "1000 m").

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/prefix_conversions_string.py
"""

SI_PREFIX_SYMBOLS: dict[str, float] = {
    "y": 1e-24,   # yocto
    "z": 1e-21,   # zepto
    "a": 1e-18,   # atto
    "f": 1e-15,   # femto
    "p": 1e-12,   # pico
    "n": 1e-9,    # nano
    "u": 1e-6,    # micro
    "m": 1e-3,    # milli
    "c": 1e-2,    # centi
    "d": 1e-1,    # deci
    "": 1.0,      # base
    "da": 1e1,    # deca
    "h": 1e2,     # hecto
    "k": 1e3,     # kilo
    "M": 1e6,     # mega
    "G": 1e9,     # giga
    "T": 1e12,    # tera
    "P": 1e15,    # peta
    "E": 1e18,    # exa
    "Z": 1e21,    # zetta
    "Y": 1e24,    # yotta
}

PREFIX_NAMES = {
    "y": "yocto", "z": "zepto", "a": "atto", "f": "femto",
    "p": "pico", "n": "nano", "u": "micro", "m": "milli",
    "c": "centi", "d": "deci", "": "base", "da": "deca",
    "h": "hecto", "k": "kilo", "M": "mega", "G": "giga",
    "T": "tera", "P": "peta", "E": "exa", "Z": "zetta", "Y": "yotta",
}


def add_si_prefix(value: float, unit: str = "m") -> str:
    """
    Find the best SI prefix for a value.

    >>> add_si_prefix(0.001, "m")
    '1.0 mm'
    >>> add_si_prefix(1000, "g")
    '1.0 kg'
    >>> add_si_prefix(0.000001, "s")
    '1.0 us'
    >>> add_si_prefix(1000000, "W")
    '1.0 MW'
    """
    if value == 0:
        return f"0.0 {unit}"

    import math

    abs_val = abs(value)
    # Find appropriate prefix
    sorted_prefixes = sorted(SI_PREFIX_SYMBOLS.items(), key=lambda x: x[1])

    best_prefix = ""
    for symbol, factor in sorted_prefixes:
        if factor <= abs_val:
            best_prefix = symbol
        else:
            break

    factor = SI_PREFIX_SYMBOLS[best_prefix]
    scaled = value / factor

    return f"{scaled:.1f} {best_prefix}{unit}"


def parse_si_prefix(value_string: str) -> float:
    """
    Parse a string with SI prefix to a base-unit float.

    >>> parse_si_prefix("1 km")
    1000.0
    >>> parse_si_prefix("500 mg")
    0.5
    >>> parse_si_prefix("1 MW")
    1000000.0
    """
    parts = value_string.strip().split()
    if len(parts) != 2:
        raise ValueError(f"Cannot parse: {value_string}")

    number = float(parts[0])
    unit_str = parts[1]

    # Try to match prefix (longest match first)
    for prefix in sorted(SI_PREFIX_SYMBOLS.keys(), key=len, reverse=True):
        if prefix and unit_str.startswith(prefix):
            return number * SI_PREFIX_SYMBOLS[prefix]

    # No prefix, base unit
    return number


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    values = [0.001, 1000, 0.000001, 1000000, 0.1]
    for v in values:
        result = add_si_prefix(v, "m")
        print(f"  add_si_prefix({v}, 'm') = '{result}'")

    strings = ["1 km", "500 mg", "1 MW", "100 cm"]
    for s in strings:
        result = parse_si_prefix(s)
        print(f"  parse_si_prefix('{s}') = {result}")
