"""
Optimized EAN-13 barcode validator.

Improvements over the original:
- String-based digit extraction instead of integer division loop
- Direct all-digit check (no separate check-digit computation needed)
- Accepts both str and int input
- Cleaner weight application via enumerate + reversed

Reference: https://en.wikipedia.org/wiki/Check_digit#Algorithms
"""


def get_check_digit(barcode: int) -> int:
    """
    Compute EAN-13 check digit using string-based digit extraction.
    Weights from the right (excluding check digit): 3, 1, 3, 1, ...

    >>> get_check_digit(8718452538119)
    9
    >>> get_check_digit(87184523)
    5
    >>> get_check_digit(87193425381086)
    9
    >>> [get_check_digit(x) for x in range(0, 100, 10)]
    [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]
    """
    digits = str(barcode)[:-1]  # exclude last (check) digit
    total = sum(
        int(d) * (3 if i % 2 == 0 else 1)
        for i, d in enumerate(reversed(digits))
    )
    return (10 - total % 10) % 10


def is_valid(barcode: int | str) -> bool:
    """
    Validate an EAN-13 barcode using the all-digit weighted sum approach:
    sum of all 13 digits with alternating weights [1, 3] from the left
    must be divisible by 10.

    This avoids a separate check-digit lookup entirely.

    >>> is_valid(8718452538119)
    True
    >>> is_valid("8718452538119")
    True
    >>> is_valid(87184525)
    False
    >>> is_valid(87193425381089)
    False
    >>> is_valid(0)
    False
    """
    s = str(barcode)
    if len(s) != 13 or not s.isdigit():
        return False
    total = sum(
        int(d) * (1 if i % 2 == 0 else 3)
        for i, d in enumerate(s)
    )
    return total % 10 == 0


def benchmark() -> None:
    import timeit

    from strings.barcode_validator import (
        get_check_digit as orig_get_check_digit,
        is_valid as orig_is_valid,
    )

    barcode = 8718452538119
    n = 500_000

    orig_gcd = timeit.timeit(lambda: orig_get_check_digit(barcode), number=n)
    opt_gcd = timeit.timeit(lambda: get_check_digit(barcode), number=n)

    orig_iv = timeit.timeit(lambda: orig_is_valid(barcode), number=n)
    opt_iv = timeit.timeit(lambda: is_valid(barcode), number=n)

    print(f"get_check_digit  — original: {orig_gcd:.3f}s  optimized: {opt_gcd:.3f}s")
    print(f"is_valid         — original: {orig_iv:.3f}s  optimized: {opt_iv:.3f}s")

    winner_gcd = "optimized" if opt_gcd < orig_gcd else "original"
    winner_iv = "optimized" if opt_iv < orig_iv else "original"
    print(f"\nFastest get_check_digit: {winner_gcd}")
    print(f"Fastest is_valid:        {winner_iv}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
