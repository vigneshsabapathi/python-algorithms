"""
Hexadecimal to Decimal Conversion

Convert a hexadecimal (base-16) string to its decimal (base-10) integer equivalent.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/hexadecimal_to_decimal.py
"""


def hexadecimal_to_decimal(hex_string: str) -> int:
    """
    Convert a hexadecimal string to a decimal integer.

    >>> hexadecimal_to_decimal("FF")
    255
    >>> hexadecimal_to_decimal("0")
    0
    >>> hexadecimal_to_decimal("1A")
    26
    >>> hexadecimal_to_decimal("CA")
    202
    >>> hexadecimal_to_decimal("10")
    16
    >>> hexadecimal_to_decimal("")
    Traceback (most recent call last):
        ...
    ValueError: Empty string is not a valid hexadecimal
    >>> hexadecimal_to_decimal("GG")
    Traceback (most recent call last):
        ...
    ValueError: Invalid hexadecimal character: G
    """
    if not hex_string:
        raise ValueError("Empty string is not a valid hexadecimal")

    hex_string = hex_string.upper().lstrip("0X")
    if not hex_string:
        return 0

    hex_map = {c: i for i, c in enumerate("0123456789ABCDEF")}

    decimal = 0
    for char in hex_string:
        if char not in hex_map:
            raise ValueError(f"Invalid hexadecimal character: {char}")
        decimal = decimal * 16 + hex_map[char]
    return decimal


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    test_cases = ["FF", "0", "1A", "CA", "10", "FFFF", "100"]
    for h in test_cases:
        print(f"  hexadecimal_to_decimal('{h}') = {hexadecimal_to_decimal(h)}")
