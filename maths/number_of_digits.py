"""
Count digits in a non-negative integer.

>>> number_of_digits(0)
1
>>> number_of_digits(9)
1
>>> number_of_digits(1234)
4
>>> number_of_digits(10**100)
101
"""

import math


def number_of_digits(n: int) -> int:
    """O(log n) via math.log10, with special-case for 0.

    >>> number_of_digits(99999)
    5
    """
    if n < 0:
        n = -n
    if n == 0:
        return 1
    return int(math.log10(n)) + 1


def number_of_digits_str(n: int) -> int:
    """Via str conversion."""
    return len(str(abs(n)))


def number_of_digits_loop(n: int) -> int:
    """Divide by 10 in a loop."""
    n = abs(n)
    if n == 0:
        return 1
    count = 0
    while n:
        n //= 10
        count += 1
    return count


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(number_of_digits(1234))
