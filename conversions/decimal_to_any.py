"""
Decimal to Any Base Conversion

Convert a decimal (base-10) integer to any base (2-36).

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/decimal_to_any.py
"""


def decimal_to_any(num: int, base: int) -> str:
    """
    Convert a positive integer to any base from 2 to 36.

    >>> decimal_to_any(0, 2)
    '0'
    >>> decimal_to_any(5, 2)
    '101'
    >>> decimal_to_any(255, 16)
    'FF'
    >>> decimal_to_any(10, 10)
    '10'
    >>> decimal_to_any(35, 36)
    'Z'
    >>> decimal_to_any(100, 8)
    '144'
    >>> decimal_to_any(5, 1)
    Traceback (most recent call last):
        ...
    ValueError: Base must be between 2 and 36
    >>> decimal_to_any(-1, 2)
    Traceback (most recent call last):
        ...
    ValueError: Number must be non-negative
    """
    if base < 2 or base > 36:
        raise ValueError("Base must be between 2 and 36")
    if num < 0:
        raise ValueError("Number must be non-negative")
    if num == 0:
        return "0"

    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = []
    while num > 0:
        result.append(digits[num % base])
        num //= base

    return "".join(reversed(result))


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    examples = [(255, 2), (255, 8), (255, 16), (100, 7), (35, 36)]
    for num, base in examples:
        print(f"  decimal_to_any({num}, {base}) = {decimal_to_any(num, base)}")
