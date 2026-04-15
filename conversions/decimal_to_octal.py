"""
Decimal to Octal Conversion

Convert a decimal (base-10) integer to its octal (base-8) representation.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/decimal_to_octal.py
"""


def decimal_to_octal(decimal: int) -> int:
    """
    Convert a decimal integer to octal representation (as integer).

    >>> decimal_to_octal(0)
    0
    >>> decimal_to_octal(8)
    10
    >>> decimal_to_octal(65)
    101
    >>> decimal_to_octal(255)
    377
    >>> decimal_to_octal(1000)
    1750
    >>> decimal_to_octal(-1)
    Traceback (most recent call last):
        ...
    ValueError: Negative values are not supported
    """
    if decimal < 0:
        raise ValueError("Negative values are not supported")
    if decimal == 0:
        return 0

    octal_digits = []
    while decimal > 0:
        octal_digits.append(str(decimal % 8))
        decimal //= 8

    return int("".join(reversed(octal_digits)))


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    test_cases = [0, 8, 65, 255, 1000, 4096]
    for num in test_cases:
        print(f"  decimal_to_octal({num}) = {decimal_to_octal(num)}")
