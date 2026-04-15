"""
Zeller's congruence variants + benchmark.

1. zeller_classic   - direct formula
2. datetime_lookup  - datetime(year, month, day).weekday()
3. tomohiko_sakamoto - clever O(1) trick using a 12-entry table
"""
from __future__ import annotations

import datetime
import time

DAYS = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
DT_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def zeller_classic(y, m, d):
    if m < 3:
        m += 12
        y -= 1
    K = y % 100
    J = y // 100
    h = (d + 13 * (m + 1) // 5 + K + K // 4 + J // 4 + 5 * J) % 7
    return DAYS[h]


def datetime_lookup(y, m, d):
    return DT_DAYS[datetime.date(y, m, d).weekday()]


def tomohiko_sakamoto(y, m, d):
    t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    if m < 3:
        y -= 1
    h = (y + y // 4 - y // 100 + y // 400 + t[m - 1] + d) % 7
    # 0 = Sunday, 1 = Monday, ..., 6 = Saturday
    names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    return names[h]


def benchmark() -> None:
    cases = [(2000, 1, 1), (1969, 7, 20), (2024, 2, 29), (1776, 7, 4)]
    print(f"{'fn':<22}{'ms':>12}")
    for fn in (zeller_classic, datetime_lookup, tomohiko_sakamoto):
        t = time.perf_counter()
        for _ in range(100_000):
            for c in cases:
                fn(*c)
        dt = (time.perf_counter() - t) * 1000
        print(f"{fn.__name__:<22}{dt:>12.2f}")
    print("Sample agreement:")
    for c in cases:
        print(c, zeller_classic(*c), datetime_lookup(*c), tomohiko_sakamoto(*c))


if __name__ == "__main__":
    benchmark()
