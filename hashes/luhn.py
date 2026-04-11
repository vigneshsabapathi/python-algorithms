"""
Luhn Algorithm -- a checksum formula used to validate identification numbers
such as credit card numbers, IMEI numbers, and Canadian Social Insurance Numbers.

The algorithm:
1. From the rightmost digit (check digit), double every second digit.
2. If doubling results in a number > 9, subtract 9.
3. Sum all digits.
4. If the total modulo 10 is 0, the number is valid.

source: https://en.wikipedia.org/wiki/Luhn_algorithm
"""

from __future__ import annotations


def is_luhn(string: str) -> bool:
    """
    Perform Luhn validation on an input string.

    >>> test_cases = (79927398710, 79927398711, 79927398712, 79927398713,
    ...     79927398714, 79927398715, 79927398716, 79927398717, 79927398718,
    ...     79927398719)
    >>> [is_luhn(str(test_case)) for test_case in test_cases]
    [False, False, False, True, False, False, False, False, False, False]

    >>> is_luhn('4532015112830366')
    True

    >>> is_luhn('0')
    True
    """
    check_digit: int
    _vector: list[str] = list(string)
    __vector, check_digit = _vector[:-1], int(_vector[-1])
    vector: list[int] = [int(digit) for digit in __vector]

    vector.reverse()
    for i, digit in enumerate(vector):
        if i & 1 == 0:
            doubled: int = digit * 2
            if doubled > 9:
                doubled -= 9
            check_digit += doubled
        else:
            check_digit += digit

    return check_digit % 10 == 0


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    assert is_luhn("79927398713")
    assert not is_luhn("79927398714")
