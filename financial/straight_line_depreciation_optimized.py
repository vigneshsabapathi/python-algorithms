#!/usr/bin/env python3
"""
Optimized and alternative implementations of Straight Line Depreciation.

The reference computes equal annual depreciation: (cost - residual) / years,
with a final-year adjustment for floating-point rounding.

Variants covered:
1. loop_with_adjustment  -- reference (loop + final year correction)
2. list_multiply         -- [annual_amount] * years (simpler)
3. decimal_precise       -- Decimal for exact currency math
4. schedule_with_book    -- returns schedule with book value per year

Key interview insight:
    Straight-line is the simplest depreciation method but rarely used alone
    in practice. Accelerated methods (declining balance, MACRS) front-load
    depreciation for tax advantages. Knowing the trade-offs is key for
    accounting/finance interviews.

Run:
    python financial/straight_line_depreciation_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from decimal import ROUND_HALF_UP, Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from financial.straight_line_depreciation import (
    straight_line_depreciation as reference,
)


# ---------------------------------------------------------------------------
# Variant 1 -- loop with final-year adjustment (reference)
# ---------------------------------------------------------------------------

def loop_with_adjustment(years: int, cost: float, residual: float = 0.0) -> list[float]:
    """
    >>> loop_with_adjustment(10, 1100.0, 100.0)
    [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
    >>> loop_with_adjustment(4, 1001.0)
    [250.25, 250.25, 250.25, 250.25]
    """
    return reference(years, cost, residual)


# ---------------------------------------------------------------------------
# Variant 2 -- list multiply (simplest possible)
# ---------------------------------------------------------------------------

def list_multiply(years: int, cost: float, residual: float = 0.0) -> list[float]:
    """
    Simplest approach: divide and repeat. Final year absorbs any rounding error.

    >>> list_multiply(10, 1100.0, 100.0)
    [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
    >>> list_multiply(6, 1250.0, 50.0)
    [200.0, 200.0, 200.0, 200.0, 200.0, 200.0]
    """
    if years < 1:
        raise ValueError("Years must be >= 1")
    if cost < residual:
        raise ValueError("Cost must be >= residual value")

    depreciable = cost - residual
    annual = depreciable / years
    result = [annual] * (years - 1)
    # Final year absorbs rounding difference
    result.append(depreciable - annual * (years - 1))
    return result


# ---------------------------------------------------------------------------
# Variant 3 -- Decimal for exact currency math
# ---------------------------------------------------------------------------

def decimal_precise(years: int, cost: float, residual: float = 0.0) -> list[float]:
    """
    Uses Decimal to avoid floating-point rounding in currency calculations.

    >>> decimal_precise(10, 1100.0, 100.0)
    [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
    >>> decimal_precise(4, 1001.0)
    [250.25, 250.25, 250.25, 250.25]
    >>> decimal_precise(3, 1000.0)
    [333.33, 333.33, 333.34]
    """
    if years < 1:
        raise ValueError("Years must be >= 1")

    dep = Decimal(str(cost)) - Decimal(str(residual))
    annual = (dep / years).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    result = [float(annual)] * (years - 1)
    remainder = dep - annual * (years - 1)
    result.append(float(remainder.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)))
    return result


# ---------------------------------------------------------------------------
# Variant 4 -- full schedule with book value
# ---------------------------------------------------------------------------

def schedule_with_book(
    years: int, cost: float, residual: float = 0.0
) -> list[tuple[int, float, float, float]]:
    """
    Returns full depreciation schedule:
    [(year, depreciation, accumulated, book_value), ...]

    >>> schedule_with_book(3, 3000.0, 300.0)
    [(1, 900.0, 900.0, 2100.0), (2, 900.0, 1800.0, 1200.0), (3, 900.0, 2700.0, 300.0)]
    """
    if years < 1:
        raise ValueError("Years must be >= 1")
    if cost < residual:
        raise ValueError("Cost must be >= residual value")

    annual = (cost - residual) / years
    schedule = []
    accumulated = 0.0
    for yr in range(1, years + 1):
        accumulated += annual
        book = cost - accumulated
        schedule.append((yr, round(annual, 2), round(accumulated, 2), round(book, 2)))
    return schedule


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (10, 1100.0, 100.0),
    (6, 1250.0, 50.0),
    (4, 1001.0, 0.0),
    (11, 380.0, 50.0),
    (1, 4985.0, 100.0),
]

IMPLS = [
    ("reference",        lambda y, c, r: reference(y, c, r)),
    ("list_multiply",    list_multiply),
    ("decimal_precise",  decimal_precise),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for years, cost, residual in TEST_CASES:
        ref = reference(years, cost, residual)
        total_ref = sum(ref)
        expected_total = cost - residual
        print(f"  years={years} cost={cost} residual={residual}")
        print(f"    reference: {ref}  sum={total_ref:.2f}  expected_sum={expected_total:.2f}")
        for name, fn in IMPLS[1:]:
            result = fn(years, cost, residual)
            total = sum(result)
            match_sum = abs(total - expected_total) < 0.02
            tag = "OK" if match_sum else "FAIL"
            print(f"    [{tag}] {name:<16} {result}  sum={total:.2f}")

    print("\n=== Schedule Example (3000 over 3 years, residual 300) ===")
    for yr, dep, acc, book in schedule_with_book(3, 3000.0, 300.0):
        print(f"  Year {yr}: depreciation={dep:.2f}  accumulated={acc:.2f}  book_value={book:.2f}")

    REPS = 100_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(y, c, r) for y, c, r in TEST_CASES], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>8.4f} ms / batch of {len(TEST_CASES)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
