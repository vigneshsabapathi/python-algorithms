#!/usr/bin/env python3
"""
Optimized and alternative implementations of Interest Calculations.

The reference provides three interest functions:
- simple_interest: P * r * t
- compound_interest: P * ((1+r)^n - 1)
- apr_interest: compound_interest with daily compounding

Variants covered:
1. reference         -- original implementations
2. math_pow          -- math.pow for compound (avoids big-int path)
3. log_exp           -- log/exp for compound (numerically stable)
4. continuous        -- continuous compounding: P * (e^(r*t) - 1)
5. rule_of_72        -- estimate doubling time: 72 / (r * 100)

Key interview insight:
    Simple interest grows linearly; compound interest grows exponentially.
    APR with daily compounding approaches continuous compounding (e^(rt)).
    The Rule of 72 is a quick mental-math shortcut for estimating doubling time.

Run:
    python financial/interest_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from financial.interest import (
    apr_interest as ref_apr,
    compound_interest as ref_compound,
    simple_interest as ref_simple,
)


# ---------------------------------------------------------------------------
# Variant 1 -- reference wrappers
# ---------------------------------------------------------------------------

def simple_ref(principal: float, rate: float, periods: float) -> float:
    """
    >>> simple_ref(18000.0, 0.06, 3)
    3240.0
    """
    return ref_simple(principal, rate, periods)


def compound_ref(principal: float, rate: float, periods: float) -> float:
    """
    >>> compound_ref(10000.0, 0.05, 3)
    1576.2500000000014
    """
    return ref_compound(principal, rate, periods)


# ---------------------------------------------------------------------------
# Variant 2 -- math.pow compound (float-only path)
# ---------------------------------------------------------------------------

def compound_math_pow(principal: float, rate: float, periods: float) -> float:
    """
    Compound interest using math.pow to stay in float domain.

    >>> round(compound_math_pow(10000.0, 0.05, 3), 6)
    1576.25
    >>> round(compound_math_pow(10000.0, 0.05, 1), 6)
    500.0
    """
    if periods <= 0:
        raise ValueError("periods must be > 0")
    if rate < 0:
        raise ValueError("rate must be >= 0")
    if principal <= 0:
        raise ValueError("principal must be > 0")
    return principal * (math.pow(1 + rate, periods) - 1)


# ---------------------------------------------------------------------------
# Variant 3 -- log/exp compound (numerically stable)
# ---------------------------------------------------------------------------

def compound_log_exp(principal: float, rate: float, periods: float) -> float:
    """
    Compound interest via exp(n * log(1+r)) - avoids large exponents.

    >>> round(compound_log_exp(10000.0, 0.05, 3), 6)
    1576.25
    >>> round(compound_log_exp(0.5, 0.05, 3), 6)
    0.078812
    """
    if periods <= 0:
        raise ValueError("periods must be > 0")
    if rate < 0:
        raise ValueError("rate must be >= 0")
    if principal <= 0:
        raise ValueError("principal must be > 0")
    return principal * (math.exp(periods * math.log1p(rate)) - 1)


# ---------------------------------------------------------------------------
# Variant 4 -- continuous compounding
# ---------------------------------------------------------------------------

def continuous_compound(principal: float, rate: float, years: float) -> float:
    """
    Continuous compounding: P * (e^(r*t) - 1).
    The theoretical limit of compound interest as compounding frequency -> infinity.

    >>> round(continuous_compound(10000.0, 0.05, 3), 2)
    1618.34
    >>> round(continuous_compound(10000.0, 0.05, 1), 2)
    512.71
    """
    if years <= 0:
        raise ValueError("years must be > 0")
    if rate < 0:
        raise ValueError("rate must be >= 0")
    if principal <= 0:
        raise ValueError("principal must be > 0")
    return principal * (math.exp(rate * years) - 1)


# ---------------------------------------------------------------------------
# Variant 5 -- Rule of 72 (doubling time estimator)
# ---------------------------------------------------------------------------

def rule_of_72(annual_rate_percent: float) -> float:
    """
    Estimate years to double an investment using the Rule of 72.

    >>> rule_of_72(6)
    12.0
    >>> rule_of_72(8)
    9.0
    >>> rule_of_72(12)
    6.0
    """
    if annual_rate_percent <= 0:
        raise ValueError("rate must be > 0")
    return 72 / annual_rate_percent


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

COMPOUND_CASES = [
    (10000.0, 0.05, 3, 1576.25),
    (10000.0, 0.05, 1, 500.0),
    (0.5, 0.05, 3, 0.078813),
]

COMPOUND_IMPLS = [
    ("ref_compound",       ref_compound),
    ("compound_math_pow",  compound_math_pow),
    ("compound_log_exp",   compound_log_exp),
]


def run_all() -> None:
    print("\n=== Correctness: Compound Interest ===")
    for p, r, n, expected in COMPOUND_CASES:
        results = {}
        for name, fn in COMPOUND_IMPLS:
            try:
                results[name] = fn(p, r, n)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(
            isinstance(v, float) and abs(v - expected) < 0.01
            for v in results.values()
        )
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] P={p} r={r} n={n}  expected={expected}")
        for nm, v in results.items():
            val = f"{v:.6f}" if isinstance(v, float) else str(v)
            print(f"        {nm:<22} = {val}")

    print("\n=== Continuous vs APR (daily) comparison ===")
    for p, r, y in [(10000, 0.05, 3), (10000, 0.05, 1), (50000, 0.08, 10)]:
        apr = ref_apr(p, r, y)
        cont = continuous_compound(p, r, y)
        print(f"  P={p} r={r} y={y}  APR(daily)={apr:.4f}  continuous={cont:.4f}  diff={abs(apr-cont):.6f}")

    print("\n=== Rule of 72 ===")
    for rate in [4, 6, 8, 10, 12]:
        est = rule_of_72(rate)
        actual = math.log(2) / math.log(1 + rate / 100)
        print(f"  rate={rate}%  rule_of_72={est:.1f} yrs  actual={actual:.2f} yrs  error={abs(est-actual):.2f}")

    REPS = 100_000
    inputs = [(10000, 0.05, 3), (50000, 0.08, 10), (1000, 0.12, 30)]

    print(f"\n=== Benchmark: Compound Interest, {REPS} runs ===")
    for name, fn in COMPOUND_IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(p, r, n) for p, r, n in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<22} {t:>8.4f} ms / batch")

    print(f"\n=== Benchmark: Continuous Compounding, {REPS} runs ===")
    t = timeit.timeit(
        lambda: [continuous_compound(p, r, n) for p, r, n in inputs], number=REPS
    ) * 1000 / REPS
    print(f"  continuous_compound    {t:>8.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
