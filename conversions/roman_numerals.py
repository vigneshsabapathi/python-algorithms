"""
Roman Numerals Conversion

Convert between Roman numerals and decimal integers.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/roman_numerals.py
"""

ROMAN_VALUES = {
    "I": 1, "V": 5, "X": 10, "L": 50,
    "C": 100, "D": 500, "M": 1000,
}

INT_TO_ROMAN = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]


def int_to_roman(number: int) -> str:
    """
    Convert an integer to a Roman numeral string.

    >>> int_to_roman(1)
    'I'
    >>> int_to_roman(4)
    'IV'
    >>> int_to_roman(9)
    'IX'
    >>> int_to_roman(58)
    'LVIII'
    >>> int_to_roman(1994)
    'MCMXCIV'
    >>> int_to_roman(3999)
    'MMMCMXCIX'
    >>> int_to_roman(0)
    Traceback (most recent call last):
        ...
    ValueError: Input must be between 1 and 3999
    """
    if not 1 <= number <= 3999:
        raise ValueError("Input must be between 1 and 3999")

    result = []
    for value, numeral in INT_TO_ROMAN:
        while number >= value:
            result.append(numeral)
            number -= value
    return "".join(result)


def roman_to_int(roman: str) -> int:
    """
    Convert a Roman numeral string to an integer.

    >>> roman_to_int("I")
    1
    >>> roman_to_int("IV")
    4
    >>> roman_to_int("IX")
    9
    >>> roman_to_int("LVIII")
    58
    >>> roman_to_int("MCMXCIV")
    1994
    >>> roman_to_int("")
    Traceback (most recent call last):
        ...
    ValueError: Empty string is not a valid Roman numeral
    >>> roman_to_int("ABC")
    Traceback (most recent call last):
        ...
    ValueError: Invalid Roman numeral character: A
    """
    if not roman:
        raise ValueError("Empty string is not a valid Roman numeral")

    roman = roman.upper()
    for char in roman:
        if char not in ROMAN_VALUES:
            raise ValueError(f"Invalid Roman numeral character: {char}")

    total = 0
    prev_value = 0
    for char in reversed(roman):
        value = ROMAN_VALUES[char]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value

    return total


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    numbers = [1, 4, 9, 14, 42, 58, 1994, 3999]
    for n in numbers:
        roman = int_to_roman(n)
        back = roman_to_int(roman)
        print(f"  {n} -> {roman} -> {back}")
