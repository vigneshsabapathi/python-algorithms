"""
Octal to Hexadecimal Conversion

Convert an octal (base-8) number to its hexadecimal (base-16) equivalent.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/octal_to_hexadecimal.py
"""


def octal_to_hexadecimal(octal: int) -> str:
    """
    Convert an octal number to hexadecimal string.

    >>> octal_to_hexadecimal(0)
    '0x0'
    >>> octal_to_hexadecimal(10)
    '0x8'
    >>> octal_to_hexadecimal(377)
    '0xFF'
    >>> octal_to_hexadecimal(17)
    '0xF'
    >>> octal_to_hexadecimal(101)
    '0x41'
    """
    # First convert octal to decimal
    decimal = 0
    place = 0
    temp = octal
    while temp > 0:
        digit = temp % 10
        decimal += digit * (8 ** place)
        temp //= 10
        place += 1

    # Then decimal to hexadecimal
    if decimal == 0:
        return "0x0"

    hex_digits = "0123456789ABCDEF"
    result = []
    while decimal > 0:
        result.append(hex_digits[decimal % 16])
        decimal //= 16

    return "0x" + "".join(reversed(result))


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    test_cases = [0, 10, 377, 17, 101, 1750]
    for o in test_cases:
        print(f"  octal_to_hexadecimal({o}) = {octal_to_hexadecimal(o)}")
