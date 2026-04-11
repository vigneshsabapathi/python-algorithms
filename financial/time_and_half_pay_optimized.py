#!/usr/bin/env python3
"""
Optimized and alternative implementations of Time and Half Pay.

The reference calculates: normal_pay + overtime * rate / 2
where overtime = max(0, hours_worked - threshold).

Variants covered:
1. split_calc       -- reference (normal + overtime bonus)
2. conditional      -- explicit if/else for clarity
3. tiered_overtime   -- double-time after additional threshold (real-world)
4. weekly_paycheck  -- full weekly pay with tax withholding

Key interview insight:
    Time-and-a-half means 1.5x the normal rate for overtime hours.
    The reference cleverly computes this as: (all hours * rate) + (overtime * rate/2)
    which equals: (normal * rate) + (overtime * 1.5 * rate).
    In practice, overtime rules vary by jurisdiction (California has daily OT,
    federal law uses weekly), and double-time kicks in at higher thresholds.

Run:
    python financial/time_and_half_pay_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from financial.time_and_half_pay import pay as reference


# ---------------------------------------------------------------------------
# Variant 1 -- split calculation (reference logic)
# ---------------------------------------------------------------------------

def split_calc(hours_worked: float, pay_rate: float, threshold: float = 40) -> float:
    """
    Reference approach: all hours at base rate + overtime bonus.

    >>> split_calc(41, 1)
    41.5
    >>> split_calc(65, 19)
    1472.5
    >>> split_calc(10, 1)
    10.0
    """
    normal_pay = hours_worked * pay_rate
    overtime = max(0, hours_worked - threshold)
    overtime_bonus = overtime * pay_rate / 2
    return normal_pay + overtime_bonus


# ---------------------------------------------------------------------------
# Variant 2 -- explicit conditional (more readable)
# ---------------------------------------------------------------------------

def conditional(hours_worked: float, pay_rate: float, threshold: float = 40) -> float:
    """
    Clear if/else separating normal and overtime pay.

    >>> conditional(41, 1)
    41.5
    >>> conditional(65, 19)
    1472.5
    >>> conditional(10, 1)
    10
    >>> conditional(40, 25)
    1000
    """
    if hours_worked <= threshold:
        return hours_worked * pay_rate
    else:
        normal = threshold * pay_rate
        overtime = (hours_worked - threshold) * pay_rate * 1.5
        return normal + overtime


# ---------------------------------------------------------------------------
# Variant 3 -- tiered overtime (1.5x then 2x)
# ---------------------------------------------------------------------------

def tiered_overtime(
    hours_worked: float,
    pay_rate: float,
    ot_threshold: float = 40,
    double_threshold: float = 60,
) -> float:
    """
    Real-world tiered overtime:
    - Up to ot_threshold: 1x rate
    - ot_threshold to double_threshold: 1.5x rate
    - Beyond double_threshold: 2x rate

    >>> tiered_overtime(30, 20)
    600
    >>> tiered_overtime(50, 20)
    1100.0
    >>> tiered_overtime(70, 20)
    1800.0
    """
    if hours_worked <= ot_threshold:
        return hours_worked * pay_rate

    normal_pay = ot_threshold * pay_rate

    ot_hours = min(hours_worked - ot_threshold, double_threshold - ot_threshold)
    ot_pay = ot_hours * pay_rate * 1.5

    dt_hours = max(0, hours_worked - double_threshold)
    dt_pay = dt_hours * pay_rate * 2.0

    return normal_pay + ot_pay + dt_pay


# ---------------------------------------------------------------------------
# Variant 4 -- weekly paycheck with tax withholding
# ---------------------------------------------------------------------------

def weekly_paycheck(
    hours_worked: float,
    pay_rate: float,
    threshold: float = 40,
    tax_rate: float = 0.22,
) -> tuple[float, float, float]:
    """
    Returns (gross_pay, tax_withheld, net_pay).

    >>> weekly_paycheck(45, 30)
    (1425.0, 313.5, 1111.5)
    >>> weekly_paycheck(40, 25)
    (1000, 220.0, 780.0)
    """
    gross = conditional(hours_worked, pay_rate, threshold)
    tax = round(gross * tax_rate, 2)
    net = round(gross - tax, 2)
    return (gross, tax, net)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (41, 1, 40, 41.5),
    (65, 19, 40, 1472.5),
    (10, 1, 40, 10.0),
    (40, 25, 40, 1000.0),
    (50, 20, 40, 1100.0),
    (80, 15, 40, 1500.0),
]

IMPLS = [
    ("reference",    lambda h, r, t: reference(h, r, t)),
    ("split_calc",   split_calc),
    ("conditional",  conditional),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for hrs, rate, thresh, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(hrs, rate, thresh)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(isinstance(v, float) and abs(v - expected) < 0.01 for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] hrs={hrs} rate={rate} thresh={thresh}  expected={expected}")
        for nm, v in results.items():
            val = f"{v:.2f}" if isinstance(v, float) else str(v)
            print(f"        {nm:<14} = {val}")

    print("\n=== Tiered Overtime Examples ===")
    for hrs in [30, 40, 50, 60, 70, 80]:
        pay = tiered_overtime(hrs, 20)
        print(f"  {hrs} hrs @ $20/hr = ${pay:.2f}")

    print("\n=== Weekly Paycheck Examples ===")
    for hrs, rate in [(40, 25), (45, 30), (60, 20)]:
        gross, tax, net = weekly_paycheck(hrs, rate)
        print(f"  {hrs}hrs @ ${rate}/hr: gross=${gross:.2f}  tax=${tax:.2f}  net=${net:.2f}")

    REPS = 200_000
    inputs = [(41, 1, 40), (65, 19, 40), (10, 1, 40), (50, 20, 40)]

    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(h, r, t) for h, r, t in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<14} {t:>8.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
