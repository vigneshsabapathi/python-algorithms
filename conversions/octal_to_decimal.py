"""
Octal to Decimal Conversion

Convert an octal (base-8) number to its decimal (base-10) equivalent.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/octal_to_decimal.py
"""


def octal_to_decimal(octal: int) -> int:
    """
    Convert an octal number (as integer) to decimal.

    >>> octal_to_decimal(0)
    0
    >>> octal_to_decimal(10)
    8
    >>> octal_to_decimal(101)
    65
    >>> octal_to_decimal(377)
    255
    >>> octal_to_decimal(1750)
    1000
    >>> octal_to_decimal(-1)
    Traceback (most recent call last):
        ...
    ValueError: Negative values are not supported
    """
    if octal < 0:
        raise ValueError("Negative values are not supported")

    decimal = 0
    place = 0
    while octal > 0:
        digit = octal % 10
        if digit >= 8:
            raise ValueError(f"Invalid octal digit: {digit}")
        decimal += digit * (8 ** place)
        octal //= 10
        place += 1

    return decimal


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    test_cases = [0, 10, 101, 377, 1750, 144]
    for o in test_cases:
        print(f"  octal_to_decimal({o}) = {octal_to_decimal(o)}")
