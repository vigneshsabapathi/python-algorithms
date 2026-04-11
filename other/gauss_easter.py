"""
Gauss Easter Algorithm — Compute the date of Easter Sunday for a given year.

Carl Friedrich Gauss devised this algorithm to determine the date of Easter
Sunday using modular arithmetic, valid for the Gregorian calendar.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/gauss_easter.py
"""

from __future__ import annotations


def gauss_easter(year: int) -> tuple[int, int]:
    """
    Compute the date of Easter Sunday for a given year.

    Returns (month, day) tuple.

    >>> gauss_easter(2024)
    (3, 31)
    >>> gauss_easter(2023)
    (4, 9)
    >>> gauss_easter(2000)
    (4, 23)
    >>> gauss_easter(1961)
    (4, 2)
    >>> gauss_easter(2100)
    (3, 28)
    """
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7  # noqa: E741
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1

    return month, day


if __name__ == "__main__":
    import doctest

    doctest.testmod()
