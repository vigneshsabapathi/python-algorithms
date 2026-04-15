"""
Compare very large numbers (like 10^1000 or a^b) by comparing log10(n):
    log10(a^b) = b * log10(a)

Used when numbers overflow standard types or are too big to compute.

>>> res = res_str(2, 100)
>>> res == '30.103'
True
>>> largest_pow([(2, 10), (3, 5), (5, 3)])
0
"""

import math


def log10_of_power(base: float, exp: float) -> float:
    """Return log10(base^exp).

    >>> round(log10_of_power(2, 10), 3)
    3.01
    """
    if base <= 0:
        raise ValueError("base must be positive")
    return exp * math.log10(base)


def res_str(base: int, exp: int) -> str:
    """Return the log10 of base^exp to 3 decimals as string."""
    return f"{log10_of_power(base, exp):.3f}"


def largest_pow(pairs: list[tuple[int, int]]) -> int:
    """Index of the pair (base, exp) with largest base**exp.

    >>> largest_pow([(10, 3), (2, 10), (3, 7)])
    2
    """
    return max(range(len(pairs)), key=lambda i: log10_of_power(*pairs[i]))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(res_str(2, 100))
    print(largest_pow([(2, 100), (3, 60), (5, 50)]))
