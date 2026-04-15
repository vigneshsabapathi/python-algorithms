"""
Decimal to Hexadecimal Conversion

Convert a decimal (base-10) integer to its hexadecimal (base-16) representation.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/decimal_to_hexadecimal.py
"""

HEX_TABLE = {i: c for i, c in enumerate("0123456789ABCDEF")}


def decimal_to_hexadecimal(decimal: int) -> str:
    """
    Convert a decimal integer to hexadecimal string.

    >>> decimal_to_hexadecimal(255)
    '0xFF'
    >>> decimal_to_hexadecimal(0)
    '0x0'
    >>> decimal_to_hexadecimal(16)
    '0x10'
    >>> decimal_to_hexadecimal(202)
    '0xCA'
    >>> decimal_to_hexadecimal(-10)
    '-0xA'
    """
    if decimal == 0:
        return "0x0"

    negative = decimal < 0
    decimal = abs(decimal)

    hex_digits = []
    while decimal > 0:
        hex_digits.append(HEX_TABLE[decimal % 16])
        decimal //= 16

    result = "0x" + "".join(reversed(hex_digits))
    return "-" + result if negative else result


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    test_cases = [0, 10, 16, 202, 255, 4096, -255]
    for num in test_cases:
        print(f"  decimal_to_hexadecimal({num}) = {decimal_to_hexadecimal(num)}")
