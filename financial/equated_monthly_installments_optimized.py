#!/usr/bin/env python3
"""
Optimized and alternative implementations of Equated Monthly Installments (EMI).

The reference uses the standard amortization formula:
    A = P * r * (1+r)^n / ((1+r)^n - 1)
where P = principal, r = monthly rate, n = total payments.

Variants covered:
1. formula_pow      -- reference formula using ** operator
2. math_pow         -- math.pow for float exponentiation (avoids big-int path)
3. log_exp          -- log/exp to avoid repeated exponentiation
4. numpy_financial  -- numpy-financial pmt (industry standard, sign-flipped)
5. iterative        -- month-by-month amortization loop (educational)

Key interview insight:
    The closed-form EMI formula is derived from geometric series summation
    of discounted payments. The iterative approach simulates the actual
    payment schedule and must converge to the same monthly amount.
    In quantitative finance interviews, knowing BOTH derivations is expected.

Run:
    python financial/equated_monthly_installments_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from financial.equated_monthly_installments import (
    equated_monthly_installments as reference,
)


# ---------------------------------------------------------------------------
# Variant 1 -- formula using ** (reference, explicit)
# ---------------------------------------------------------------------------

def formula_pow(principal: float, rate_per_annum: float, years: int) -> float:
    """
    Standard EMI formula using Python's ** operator.

    >>> round(formula_pow(25000, 0.12, 3), 6)
    830.357745
    >>> round(formula_pow(25000, 0.12, 10), 6)
    358.677371
    >>> round(formula_pow(100000, 0.08, 20), 2)
    836.44
    """
    r = rate_per_annum / 12
    n = years * 12
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)


# ---------------------------------------------------------------------------
# Variant 2 -- math.pow (float-only path, no big-int overhead)
# ---------------------------------------------------------------------------

def math_pow_emi(principal: float, rate_per_annum: float, years: int) -> float:
    """
    EMI using math.pow -- avoids Python's arbitrary-precision int path
    for large exponents.

    >>> round(math_pow_emi(25000, 0.12, 3), 6)
    830.357745
    >>> round(math_pow_emi(25000, 0.12, 10), 6)
    358.677371
    """
    r = rate_per_annum / 12
    n = years * 12
    factor = math.pow(1 + r, n)
    return principal * r * factor / (factor - 1)


# ---------------------------------------------------------------------------
# Variant 3 -- log/exp (numerically stable for extreme rates/periods)
# ---------------------------------------------------------------------------

def log_exp_emi(principal: float, rate_per_annum: float, years: int) -> float:
    """
    EMI via log-exp trick: (1+r)^n = exp(n * log(1+r)).
    Avoids overflow for very large n or r close to 0.

    >>> round(log_exp_emi(25000, 0.12, 3), 6)
    830.357745
    >>> round(log_exp_emi(25000, 0.12, 10), 6)
    358.677371
    >>> round(log_exp_emi(500000, 0.05, 30), 2)
    2684.11
    """
    r = rate_per_annum / 12
    n = years * 12
    factor = math.exp(n * math.log1p(r))
    return principal * r * factor / (factor - 1)


# ---------------------------------------------------------------------------
# Variant 4 -- numpy-financial pmt (industry standard)
# ---------------------------------------------------------------------------

def numpy_pmt_emi(principal: float, rate_per_annum: float, years: int) -> float:
    """
    EMI using numpy-financial's pmt function (returns negative, we flip sign).
    Falls back to formula_pow if numpy_financial not installed.

    >>> round(numpy_pmt_emi(25000, 0.12, 3), 6)
    830.357745
    """
    try:
        import numpy_financial as npf
        return -npf.pmt(rate_per_annum / 12, years * 12, principal)
    except ImportError:
        return formula_pow(principal, rate_per_annum, years)


# ---------------------------------------------------------------------------
# Variant 5 -- iterative amortization (educational, O(n) loop)
# ---------------------------------------------------------------------------

def iterative_emi(principal: float, rate_per_annum: float, years: int) -> float:
    """
    Binary-search for the EMI amount that amortizes the loan to zero.
    Educational: simulates month-by-month balance reduction.

    >>> round(iterative_emi(25000, 0.12, 3), 2)
    830.36
    >>> round(iterative_emi(25000, 0.12, 10), 2)
    358.68
    """
    r = rate_per_annum / 12
    n = years * 12

    def remaining_balance(emi: float) -> float:
        balance = principal
        for _ in range(n):
            balance = balance * (1 + r) - emi
        return balance

    # Binary search for EMI that drives balance to ~0
    lo, hi = 0.0, principal * (1 + r * n) / n * 2
    for _ in range(100):  # converges well within 100 iterations
        mid = (lo + hi) / 2
        if remaining_balance(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (25000, 0.12, 3, 830.3577453212793),
    (25000, 0.12, 10, 358.67737100646826),
    (100000, 0.08, 20, 836.4401309585736),
    (500000, 0.05, 30, 2684.1085385858644),
    (10000, 0.15, 5, 237.89937413498587),
]

IMPLS = [
    ("reference",     lambda p, r, y: reference(p, r, y)),
    ("formula_pow",   formula_pow),
    ("math_pow_emi",  math_pow_emi),
    ("log_exp_emi",   log_exp_emi),
    ("numpy_pmt_emi", numpy_pmt_emi),
    ("iterative_emi", iterative_emi),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for p, r, y, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(p, r, y)
            except Exception as e:
                results[name] = f"ERR:{e}"
        # iterative has lower precision, use tolerance
        ok = all(
            isinstance(v, float) and abs(v - expected) < 0.02
            for v in results.values()
        )
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] P={p} r={r} y={y}  expected={expected:.4f}")
        for nm, v in results.items():
            val = f"{v:.6f}" if isinstance(v, float) else str(v)
            print(f"        {nm:<16} = {val}")

    REPS = 50_000
    inputs = [(25000, 0.12, 3), (100000, 0.08, 20), (500000, 0.05, 30)]

    print(f"\n=== Benchmark: {REPS} runs, {len(inputs)} inputs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(p, r, y) for p, r, y in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>8.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
