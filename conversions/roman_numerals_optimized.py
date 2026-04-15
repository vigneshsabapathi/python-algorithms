"""
Roman Numerals - Optimized Variants with Benchmarks
"""

import timeit

INT_TO_ROMAN = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]

ROMAN_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def int_to_roman_greedy(number: int) -> str:
    """
    Greedy subtraction approach.

    >>> int_to_roman_greedy(1994)
    'MCMXCIV'
    """
    result = []
    for value, numeral in INT_TO_ROMAN:
        while number >= value:
            result.append(numeral)
            number -= value
    return "".join(result)


def int_to_roman_divmod(number: int) -> str:
    """
    Divmod for fewer iterations.

    >>> int_to_roman_divmod(1994)
    'MCMXCIV'
    """
    result = []
    for value, numeral in INT_TO_ROMAN:
        count, number = divmod(number, value)
        result.append(numeral * count)
    return "".join(result)


def int_to_roman_hardcoded(number: int) -> str:
    """
    Hardcoded digit tables (fastest for small numbers).

    >>> int_to_roman_hardcoded(1994)
    'MCMXCIV'
    """
    thousands = ["", "M", "MM", "MMM"]
    hundreds = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
    tens = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    ones = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
    return thousands[number // 1000] + hundreds[(number % 1000) // 100] + tens[(number % 100) // 10] + ones[number % 10]


def roman_to_int_reverse(roman: str) -> int:
    """
    Reverse scan with subtraction rule.

    >>> roman_to_int_reverse("MCMXCIV")
    1994
    """
    total = 0
    prev = 0
    for char in reversed(roman):
        val = ROMAN_VALUES[char]
        if val < prev:
            total -= val
        else:
            total += val
        prev = val
    return total


def benchmark():
    number = 100_000
    test_num = 1994
    test_roman = "MCMXCIV"
    print(f"Benchmark: int->roman {test_num}, roman->int '{test_roman}' ({number:,} iterations)\n")
    results = []
    for label, func, arg in [
        ("Greedy", int_to_roman_greedy, test_num),
        ("Divmod", int_to_roman_divmod, test_num),
        ("Hardcoded", int_to_roman_hardcoded, test_num),
        ("Reverse scan", roman_to_int_reverse, test_roman),
    ]:
        t = timeit.timeit(lambda: func(arg), number=number)
        ms = t / number * 1000
        results.append((label, ms))
        print(f"  {label:<20} {ms:.4f} ms/call")
    fastest = min(results, key=lambda x: x[1])
    print(f"\n  Fastest: {fastest[0]} at {fastest[1]:.4f} ms/call")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
