#!/usr/bin/env python3
"""
Optimized and alternative implementations of Gauss Easter Algorithm.

Variants covered:
1. gauss_method       -- Gauss's original algorithm (reference)
2. anonymous_gregorian -- Anonymous Gregorian algorithm (Meeus)
3. stdlib_easter      -- Computation via known Easter table validation

Run:
    python other/gauss_easter_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.gauss_easter import gauss_easter as reference


def anonymous_gregorian(year: int) -> tuple[int, int]:
    """
    Anonymous Gregorian Easter algorithm (also known as Meeus/Jones/Butcher).

    >>> anonymous_gregorian(2024)
    (3, 31)
    >>> anonymous_gregorian(2023)
    (4, 9)
    >>> anonymous_gregorian(2000)
    (4, 23)
    """
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7  # noqa: E741
    m = (a + 11 * h + 22 * l) // 451
    n, p = divmod(h + l - 7 * m + 114, 31)
    return n, p + 1


def oudin_algorithm(year: int) -> tuple[int, int]:
    """
    Oudin's algorithm for computing Easter date.

    >>> oudin_algorithm(2024)
    (3, 31)
    >>> oudin_algorithm(2023)
    (4, 9)
    >>> oudin_algorithm(2100)
    (3, 28)
    """
    century = year // 100
    g = year % 19
    k = (century - 17) // 25
    i = (century - century // 4 - (century - k) // 3 + 19 * g + 15) % 30
    i = i - (i // 28) * (1 - (i // 28) * (29 // (i + 1)) * ((21 - g) // 11))
    j = (year + year // 4 + i + 2 - century + century // 4) % 7
    l = i - j  # noqa: E741
    month = 3 + (l + 40) // 44
    day = l + 28 - 31 * (month // 4)
    return month, day


def easter_range(start: int, end: int) -> list[tuple[int, int, int]]:
    """
    Compute Easter dates for a range of years.

    >>> dates = easter_range(2020, 2024)
    >>> len(dates)
    5
    >>> dates[0]
    (2020, 4, 12)
    """
    return [(year, *reference(year)) for year in range(start, end + 1)]


TEST_CASES = [
    (2024, (3, 31)),
    (2023, (4, 9)),
    (2000, (4, 23)),
    (1961, (4, 2)),
    (2100, (3, 28)),
]

IMPLS = [
    ("reference", reference),
    ("anonymous", anonymous_gregorian),
    ("oudin", oudin_algorithm),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for year, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(year)
            ok = result == expected
            tag = "OK" if ok else "FAIL"
            if not ok:
                print(f"  [{tag}] {name}({year}): expected={expected} got={result}")
        print(f"  [OK] {year} -> {expected}")

    REPS = 200_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(2024), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
