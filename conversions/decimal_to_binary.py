"""
Decimal to Binary Conversion

Convert a decimal (base-10) integer to its binary (base-2) string representation.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/decimal_to_binary.py
"""


def decimal_to_binary(decimal: int) -> str:
    """
    Convert a decimal integer to binary string.

    >>> decimal_to_decimal_to_binary(5)
    Traceback (most recent call last):
        ...
    NameError: name 'decimal_to_decimal_to_binary' is not defined
    >>> decimal_to_binary(5)
    '0b101'
    >>> decimal_to_binary(15)
    '0b1111'
    >>> decimal_to_binary(0)
    '0b0'
    >>> decimal_to_binary(1)
    '0b1'
    >>> decimal_to_binary(255)
    '0b11111111'
    >>> decimal_to_binary(-5)
    '-0b101'
    """
    if decimal == 0:
        return "0b0"

    negative = decimal < 0
    decimal = abs(decimal)

    binary_digits = []
    while decimal > 0:
        binary_digits.append(str(decimal % 2))
        decimal //= 2

    result = "0b" + "".join(reversed(binary_digits))
    return "-" + result if negative else result


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    test_cases = [0, 1, 5, 15, 255, 1024, -7]
    for num in test_cases:
        print(f"  decimal_to_binary({num}) = {decimal_to_binary(num)}")
