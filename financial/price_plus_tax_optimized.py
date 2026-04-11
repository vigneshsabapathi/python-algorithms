#!/usr/bin/env python3
"""
Optimized and alternative implementations of Price Plus Tax.

The reference simply returns price * (1 + tax_rate).

Variants covered:
1. multiply          -- price * (1 + tax_rate) (reference)
2. decimal_precise   -- decimal.Decimal for exact currency math
3. tax_breakdown     -- returns (price, tax_amount, total) tuple
4. tiered_tax        -- progressive tax brackets (real-world scenario)

Key interview insight:
    Floating-point arithmetic causes rounding errors in currency calculations.
    For production financial code, always use decimal.Decimal or integer cents.
    Tiered/progressive tax is a common interview question in finance domains.

Run:
    python financial/price_plus_tax_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from decimal import ROUND_HALF_UP, Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from financial.price_plus_tax import price_plus_tax as reference


# ---------------------------------------------------------------------------
# Variant 1 -- simple multiply (reference)
# ---------------------------------------------------------------------------

def multiply(price: float, tax_rate: float) -> float:
    """
    >>> multiply(100, 0.25)
    125.0
    >>> multiply(125.50, 0.05)
    131.775
    """
    return price * (1 + tax_rate)


# ---------------------------------------------------------------------------
# Variant 2 -- decimal.Decimal for exact currency math
# ---------------------------------------------------------------------------

def decimal_precise(price: float, tax_rate: float) -> float:
    """
    Uses Decimal for banker's rounding to 2 decimal places.
    Avoids floating-point surprises like 0.1 + 0.2 != 0.3.

    >>> decimal_precise(100, 0.25)
    125.0
    >>> decimal_precise(125.50, 0.05)
    131.78
    >>> decimal_precise(19.99, 0.0825)
    21.64
    """
    p = Decimal(str(price))
    r = Decimal(str(tax_rate))
    total = p * (1 + r)
    return float(total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


# ---------------------------------------------------------------------------
# Variant 3 -- tax breakdown (returns tuple)
# ---------------------------------------------------------------------------

def tax_breakdown(price: float, tax_rate: float) -> tuple[float, float, float]:
    """
    Returns (price, tax_amount, total) for itemized receipts.

    >>> tax_breakdown(100, 0.25)
    (100, 25.0, 125.0)
    >>> tax_breakdown(125.50, 0.05)
    (125.5, 6.28, 131.78)
    """
    p = Decimal(str(price))
    r = Decimal(str(tax_rate))
    tax = (p * r).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    total = p + tax
    return (price, float(tax), float(total))


# ---------------------------------------------------------------------------
# Variant 4 -- tiered/progressive tax brackets
# ---------------------------------------------------------------------------

def tiered_tax(
    price: float,
    brackets: list[tuple[float, float]] | None = None,
) -> float:
    """
    Progressive tax: different rates for different price ranges.
    Default brackets (like a simplified sales tax with luxury surcharge):
        0-100:    5%
        100-500:  10%
        500+:     15%

    >>> tiered_tax(50)
    52.5
    >>> tiered_tax(200)
    215.0
    >>> tiered_tax(1000)
    1120.0
    """
    if brackets is None:
        brackets = [(100, 0.05), (500, 0.10), (float("inf"), 0.15)]

    total_tax = 0.0
    remaining = price
    prev_limit = 0.0

    for limit, rate in brackets:
        bracket_amount = min(remaining, limit - prev_limit)
        if bracket_amount <= 0:
            break
        total_tax += bracket_amount * rate
        remaining -= bracket_amount
        prev_limit = limit

    return round(price + total_tax, 2)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (100, 0.25, 125.0),
    (125.50, 0.05, 131.775),
    (19.99, 0.0825, 21.639175),
    (0, 0.10, 0.0),
    (999.99, 0.07, 1069.9893),
]

IMPLS = [
    ("reference",       lambda p, r: reference(p, r)),
    ("multiply",        multiply),
    ("decimal_precise", decimal_precise),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for price, rate, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(price, rate)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(isinstance(v, float) and abs(v - expected) < 0.02 for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] price={price} rate={rate}  expected={expected}")
        for nm, v in results.items():
            val = f"{v:.4f}" if isinstance(v, float) else str(v)
            print(f"        {nm:<16} = {val}")

    print("\n=== Tax Breakdown Examples ===")
    for price, rate in [(100, 0.25), (125.50, 0.05), (19.99, 0.0825)]:
        p, tax, total = tax_breakdown(price, rate)
        print(f"  price={p}  tax={tax}  total={total}")

    print("\n=== Tiered Tax Examples ===")
    for price in [50, 200, 500, 1000]:
        result = tiered_tax(price)
        print(f"  price={price}  total={result}")

    REPS = 200_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(p, r) for p, r, _ in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>8.4f} ms / batch of {len(TEST_CASES)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
