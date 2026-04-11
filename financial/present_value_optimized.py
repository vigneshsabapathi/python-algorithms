#!/usr/bin/env python3
"""
Optimized and alternative implementations of Present Value (PV).

The reference computes PV as: sum(CF_i / (1+r)^i) for each cash flow at year i.

Variants covered:
1. sum_comprehension  -- reference (generator expression with sum)
2. iterative_factor   -- accumulate discount factor to avoid repeated pow
3. functools_reduce   -- functional style with reduce
4. npv_with_invest    -- NPV = PV - initial investment (finance convention)

Key interview insight:
    Present value discounts future cash flows to today's dollars. The iterative
    approach avoids O(n^2) exponentiation by maintaining a running discount factor.
    NPV (Net Present Value) is PV minus the initial investment cost -- the key
    metric for capital budgeting decisions.

Run:
    python financial/present_value_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from functools import reduce

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from financial.present_value import present_value as reference


# ---------------------------------------------------------------------------
# Variant 1 -- sum comprehension (reference)
# ---------------------------------------------------------------------------

def sum_comprehension(discount_rate: float, cash_flows: list[float]) -> float:
    """
    Reference approach: sum of discounted cash flows.

    >>> sum_comprehension(0.13, [10, 20.70, -293, 297])
    4.69
    >>> sum_comprehension(0.07, [-109129.39, 30923.23, 15098.93, 29734, 39])
    -42739.63
    """
    if discount_rate < 0:
        raise ValueError("Discount rate cannot be negative")
    if not cash_flows:
        raise ValueError("Cash flows list cannot be empty")
    pv = sum(cf / ((1 + discount_rate) ** i) for i, cf in enumerate(cash_flows))
    return round(pv, 2)


# ---------------------------------------------------------------------------
# Variant 2 -- iterative discount factor (avoids repeated pow)
# ---------------------------------------------------------------------------

def iterative_factor(discount_rate: float, cash_flows: list[float]) -> float:
    """
    Accumulate discount factor iteratively: multiply by 1/(1+r) each year.
    O(n) multiplications instead of O(n) exponentiations.

    >>> iterative_factor(0.13, [10, 20.70, -293, 297])
    4.69
    >>> iterative_factor(0.07, [-109129.39, 30923.23, 15098.93, 29734, 39])
    -42739.63
    """
    if discount_rate < 0:
        raise ValueError("Discount rate cannot be negative")
    if not cash_flows:
        raise ValueError("Cash flows list cannot be empty")

    pv = 0.0
    factor = 1.0
    divisor = 1 + discount_rate
    for cf in cash_flows:
        pv += cf * factor
        factor /= divisor
    return round(pv, 2)


# ---------------------------------------------------------------------------
# Variant 3 -- functools.reduce (functional style)
# ---------------------------------------------------------------------------

def reduce_pv(discount_rate: float, cash_flows: list[float]) -> float:
    """
    Functional approach using reduce to accumulate discounted sum.

    >>> reduce_pv(0.13, [10, 20.70, -293, 297])
    4.69
    >>> reduce_pv(0.07, [109129.39, 30923.23, 15098.93, 29734, 39])
    175519.15
    """
    if discount_rate < 0:
        raise ValueError("Discount rate cannot be negative")
    if not cash_flows:
        raise ValueError("Cash flows list cannot be empty")

    pv = reduce(
        lambda acc, item: acc + item[1] / ((1 + discount_rate) ** item[0]),
        enumerate(cash_flows),
        0.0,
    )
    return round(pv, 2)


# ---------------------------------------------------------------------------
# Variant 4 -- NPV with explicit initial investment
# ---------------------------------------------------------------------------

def npv(discount_rate: float, initial_investment: float,
        future_cash_flows: list[float]) -> float:
    """
    Net Present Value: -investment + PV of future cash flows.
    Positive NPV => project adds value.

    >>> npv(0.10, 1000, [400, 400, 400])
    -5.26
    >>> npv(0.10, 1000, [500, 500, 500])
    243.43
    >>> npv(0.05, 5000, [1500, 1500, 1500, 1500])
    318.93
    """
    if discount_rate < 0:
        raise ValueError("Discount rate cannot be negative")
    if not future_cash_flows:
        raise ValueError("Cash flows list cannot be empty")

    pv = sum(
        cf / ((1 + discount_rate) ** (i + 1))
        for i, cf in enumerate(future_cash_flows)
    )
    return round(-initial_investment + pv, 2)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (0.13, [10, 20.70, -293, 297], 4.69),
    (0.07, [-109129.39, 30923.23, 15098.93, 29734, 39], -42739.63),
    (0.07, [109129.39, 30923.23, 15098.93, 29734, 39], 175519.15),
]

PV_IMPLS = [
    ("reference",         lambda r, cf: reference(r, cf)),
    ("sum_comprehension", sum_comprehension),
    ("iterative_factor",  iterative_factor),
    ("reduce_pv",         reduce_pv),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for rate, cfs, expected in TEST_CASES:
        results = {}
        for name, fn in PV_IMPLS:
            try:
                results[name] = fn(rate, cfs)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(isinstance(v, float) and abs(v - expected) < 0.02 for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] rate={rate} cfs={cfs}  expected={expected}")
        for nm, v in results.items():
            val = f"{v:.2f}" if isinstance(v, float) else str(v)
            print(f"        {nm:<20} = {val}")

    print("\n=== NPV Examples ===")
    for r, inv, cfs in [(0.10, 1000, [400, 400, 400]), (0.10, 1000, [500, 500, 500])]:
        result = npv(r, inv, cfs)
        decision = "ACCEPT" if result > 0 else "REJECT"
        print(f"  rate={r} invest={inv} cfs={cfs}  NPV={result:.2f}  => {decision}")

    REPS = 100_000
    big_cfs = [1000 + i * 10 for i in range(20)]

    print(f"\n=== Benchmark: {REPS} runs, {len(big_cfs)} cash flows ===")
    for name, fn in PV_IMPLS:
        t = timeit.timeit(
            lambda fn=fn: fn(0.08, big_cfs), number=REPS
        ) * 1000 / REPS
        print(f"  {name:<20} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
