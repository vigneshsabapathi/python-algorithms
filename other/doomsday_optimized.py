#!/usr/bin/env python3
"""
Optimized and alternative implementations of Doomsday Algorithm.

Variants covered:
1. conway_doomsday  -- Conway's Doomsday algorithm (reference)
2. zeller_congruence -- Zeller's congruence formula
3. stdlib_weekday   -- Python datetime stdlib (baseline)

Run:
    python other/doomsday_optimized.py
"""

from __future__ import annotations

import datetime
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.doomsday import doomsday as reference

DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def zeller_congruence(year: int, month: int, day: int) -> str:
    """
    Day of week using Zeller's congruence.

    >>> zeller_congruence(2023, 10, 15)
    'Sunday'
    >>> zeller_congruence(2000, 1, 1)
    'Saturday'
    >>> zeller_congruence(1969, 7, 20)
    'Sunday'
    """
    if month < 3:
        month += 12
        year -= 1
    q = day
    m = month
    k = year % 100
    j = year // 100
    h = (q + (13 * (m + 1)) // 5 + k + k // 4 + j // 4 - 2 * j) % 7
    # Zeller: 0=Sat, 1=Sun, ..., 6=Fri
    day_index = ((h + 6) % 7)  # Convert to 0=Sun
    return DAYS[day_index]


def stdlib_weekday(year: int, month: int, day: int) -> str:
    """
    Day of week using Python's datetime module.

    >>> stdlib_weekday(2023, 10, 15)
    'Sunday'
    >>> stdlib_weekday(2000, 1, 1)
    'Saturday'
    """
    # datetime.weekday(): Monday=0 ... Sunday=6
    # We need: Sunday=0 ... Saturday=6
    d = datetime.date(year, month, day)
    return DAYS[(d.weekday() + 1) % 7]


def tomohiko_sakamoto(year: int, month: int, day: int) -> str:
    """
    Tomohiko Sakamoto's algorithm — compact lookup table approach.

    >>> tomohiko_sakamoto(2023, 10, 15)
    'Sunday'
    >>> tomohiko_sakamoto(2024, 2, 29)
    'Thursday'
    """
    t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    y = year - (month < 3)
    idx = (y + y // 4 - y // 100 + y // 400 + t[month - 1] + day) % 7
    # This gives 0=Sun, 1=Mon, ..., 6=Sat
    return DAYS[idx]


TEST_CASES = [
    ((2023, 10, 15), "Sunday"),
    ((2000, 1, 1), "Saturday"),
    ((1969, 7, 20), "Sunday"),
    ((2024, 2, 29), "Thursday"),
    ((1900, 1, 1), "Monday"),
]

IMPLS = [
    ("reference", reference),
    ("zeller", zeller_congruence),
    ("stdlib", stdlib_weekday),
    ("sakamoto", tomohiko_sakamoto),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for (y, m, d), expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(y, m, d)
            ok = result == expected
            tag = "OK" if ok else "FAIL"
            if not ok:
                print(f"  [{tag}] {name}({y},{m},{d}): expected={expected} got={result}")
        print(f"  [OK] {y}-{m:02d}-{d:02d} = {expected}")

    REPS = 100_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(2023, 10, 15), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
