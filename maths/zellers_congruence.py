"""
Zeller's Congruence
===================
Compute the day of the week for any Gregorian date.

    h = (q + ⌊13(m+1)/5⌋ + K + ⌊K/4⌋ + ⌊J/4⌋ + 5J) mod 7

with months 3..14 (Jan, Feb treated as months 13, 14 of previous year),
q = day of month, K = year mod 100, J = year // 100.

Result h: 0=Saturday, 1=Sunday, 2=Monday, ..., 6=Friday.
"""

DAYS = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


def zeller(year: int, month: int, day: int) -> str:
    """
    >>> zeller(2000, 1, 1)
    'Saturday'
    >>> zeller(1969, 7, 20)
    'Sunday'
    >>> zeller(2024, 2, 29)
    'Thursday'
    >>> zeller(1776, 7, 4)
    'Thursday'
    """
    if month < 3:
        month += 12
        year -= 1
    K = year % 100
    J = year // 100
    h = (day + 13 * (month + 1) // 5 + K + K // 4 + J // 4 + 5 * J) % 7
    return DAYS[h]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(zeller(2000, 1, 1))
    print(zeller(1969, 7, 20))
    print(zeller(2024, 2, 29))
