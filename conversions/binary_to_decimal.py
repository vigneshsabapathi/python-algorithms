"""
Binary to Decimal Conversion

Convert a binary (base-2) string to its decimal (base-10) integer equivalent.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/binary_to_decimal.py
"""


def binary_to_decimal(binary_string: str) -> int:
    """
    Convert a binary string to a decimal integer.

    >>> binary_to_decimal("101")
    5
    >>> binary_to_decimal("1111")
    15
    >>> binary_to_decimal("0")
    0
    >>> binary_to_decimal("10000")
    16
    >>> binary_to_decimal("1")
    1
    >>> binary_to_decimal("10")
    2
    >>> binary_to_decimal("")
    Traceback (most recent call last):
        ...
    ValueError: Empty string is not a valid binary number
    >>> binary_to_decimal("abc")
    Traceback (most recent call last):
        ...
    ValueError: Non-binary value was passed to the function
    """
    if not binary_string:
        raise ValueError("Empty string is not a valid binary number")
    if not all(char in "01" for char in binary_string):
        raise ValueError("Non-binary value was passed to the function")

    decimal = 0
    for char in binary_string:
        decimal = decimal * 2 + int(char)
    return decimal


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # Live demonstration
    test_cases = ["101", "1111", "10000", "11001010", "0", "1"]
    for binary in test_cases:
        print(f"  binary_to_decimal('{binary}') = {binary_to_decimal(binary)}")
