"""
Doomsday Algorithm — Determine the day of the week for any date.

John Conway's Doomsday algorithm uses the fact that certain easy-to-remember
dates (called "doomsdays") always fall on the same day of the week in any
given year.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/doomsday.py
"""

from __future__ import annotations


DAYS = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]

# Doomsday dates for each month (1-indexed): dates that always share
# the same day of the week in a given year
DOOMSDAYS_LEAP = [0, 4, 29, 7, 4, 9, 6, 11, 8, 5, 10, 7, 12]
DOOMSDAYS_NOT_LEAP = [0, 3, 28, 7, 4, 9, 6, 11, 8, 5, 10, 7, 12]


def is_leap_year(year: int) -> bool:
    """
    >>> is_leap_year(2000)
    True
    >>> is_leap_year(1900)
    False
    >>> is_leap_year(2024)
    True
    >>> is_leap_year(2023)
    False
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def doomsday(year: int, month: int, day: int) -> str:
    """
    Return the day of the week for a given date using Conway's Doomsday algorithm.

    >>> doomsday(2023, 10, 15)
    'Sunday'
    >>> doomsday(2000, 1, 1)
    'Saturday'
    >>> doomsday(1969, 7, 20)
    'Sunday'
    >>> doomsday(2024, 2, 29)
    'Thursday'
    >>> doomsday(1900, 1, 1)
    'Monday'
    """
    # Century anchor: the doomsday for the century's first year
    century = year // 100
    # Anchor days cycle: 0=Sun for 1800s, 5=Fri for 1900s, 3=Wed for 2000s, 2=Tue for 2100s
    anchor = (2 + 5 * (century % 4)) % 7

    # Year within century
    y = year % 100
    # Doomsday for this year: anchor + y + y//4
    doomsday_day = (anchor + y + y // 4) % 7

    # Get the doomsday date for this month
    doomsdays = DOOMSDAYS_LEAP if is_leap_year(year) else DOOMSDAYS_NOT_LEAP
    doomsday_date = doomsdays[month]

    # Day of week = doomsday + (day - doomsday_date)
    day_of_week = (doomsday_day + (day - doomsday_date)) % 7

    return DAYS[day_of_week]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
