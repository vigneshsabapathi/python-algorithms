"""
Convert Number to Words

Convert an integer to its English word representation.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/convert_number_to_words.py
"""

ONES = [
    "", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
    "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
    "Seventeen", "Eighteen", "Nineteen",
]

TENS = [
    "", "", "Twenty", "Thirty", "Forty", "Fifty",
    "Sixty", "Seventy", "Eighty", "Ninety",
]

THOUSANDS = ["", "Thousand", "Million", "Billion", "Trillion"]


def number_to_words(number: int) -> str:
    """
    Convert an integer to English words.

    >>> number_to_words(0)
    'Zero'
    >>> number_to_words(1)
    'One'
    >>> number_to_words(15)
    'Fifteen'
    >>> number_to_words(100)
    'One Hundred'
    >>> number_to_words(123)
    'One Hundred Twenty Three'
    >>> number_to_words(1000)
    'One Thousand'
    >>> number_to_words(1000000)
    'One Million'
    >>> number_to_words(-42)
    'Negative Forty Two'
    >>> number_to_words(12345)
    'Twelve Thousand Three Hundred Forty Five'
    """
    if number == 0:
        return "Zero"

    if number < 0:
        return "Negative " + number_to_words(-number)

    def _three_digits(n: int) -> str:
        """Convert a number 0-999 to words."""
        if n == 0:
            return ""
        elif n < 20:
            return ONES[n]
        elif n < 100:
            tens_part = TENS[n // 10]
            ones_part = ONES[n % 10]
            return f"{tens_part} {ones_part}".strip()
        else:
            hundreds_part = f"{ONES[n // 100]} Hundred"
            rest = _three_digits(n % 100)
            return f"{hundreds_part} {rest}".strip()

    parts = []
    group_index = 0
    while number > 0:
        group = number % 1000
        if group != 0:
            group_words = _three_digits(group)
            if THOUSANDS[group_index]:
                group_words += " " + THOUSANDS[group_index]
            parts.append(group_words)
        number //= 1000
        group_index += 1

    return " ".join(reversed(parts))


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    test_cases = [0, 1, 15, 42, 100, 123, 1000, 12345, 1000000, -99]
    for num in test_cases:
        print(f"  number_to_words({num}) = '{number_to_words(num)}'")
