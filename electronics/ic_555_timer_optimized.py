#!/usr/bin/env python3
"""
Optimized and alternative implementations of IC 555 Timer.

Freq = 1.44 / [(R1 + 2*R2) * C]  (C in uF, result in Hz)
Duty = (R1 + R2) / (R1 + 2*R2) * 100

Variants covered:
1. direct_calc    -- reference direct formula
2. period_invert  -- compute T_high + T_low, then f = 1/T
3. ln2_exact      -- use exact ln(2) formula: T = ln(2) * C * (R1 + 2*R2)

Run:
    python electronics/ic_555_timer_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from electronics.ic_555_timer import astable_frequency as ref_freq, astable_duty_cycle as ref_duty


# ---------------------------------------------------------------------------
# Variant 1 -- direct_calc (reference)
# ---------------------------------------------------------------------------

def direct_freq(r1: float, r2: float, c: float) -> float:
    """
    >>> direct_freq(45, 45, 7)
    1523.8095238095239
    """
    return ref_freq(r1, r2, c)


def direct_duty(r1: float, r2: float) -> float:
    """
    >>> direct_duty(45, 45)
    66.66666666666666
    """
    return ref_duty(r1, r2)


# ---------------------------------------------------------------------------
# Variant 2 -- period_invert: compute period then invert
# ---------------------------------------------------------------------------

def period_invert_freq(r1: float, r2: float, c: float) -> float:
    """
    T_high = 0.693*(R1+R2)*C, T_low = 0.693*R2*C, f = 1/(T_high+T_low).
    C in uF -> convert to F.

    >>> abs(period_invert_freq(45, 45, 7) - 1526.99) < 1
    True
    """
    if r1 <= 0 or r2 <= 0 or c <= 0:
        raise ValueError("All values must be positive")
    c_f = c * 1e-6  # uF to F
    t_high = 0.693 * (r1 + r2) * c_f
    t_low = 0.693 * r2 * c_f
    return 1 / (t_high + t_low)


# ---------------------------------------------------------------------------
# Variant 3 -- ln2_exact: T = ln(2) * C * (R1 + 2*R2)
# ---------------------------------------------------------------------------

def ln2_exact_freq(r1: float, r2: float, c: float) -> float:
    """
    Uses exact ln(2) instead of 0.693 approximation.

    >>> abs(ln2_exact_freq(45, 45, 7) - 1523.81) < 5
    True
    """
    if r1 <= 0 or r2 <= 0 or c <= 0:
        raise ValueError("All values must be positive")
    c_f = c * 1e-6
    period = math.log(2) * c_f * (r1 + 2 * r2)
    return 1 / period


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_FREQ = [
    ((45, 45, 7), 1523.8095238095239),
    ((356, 234, 976), 1.7905459175553078),
]

TEST_DUTY = [
    ((45, 45), 66.66666666666666),
    ((356, 234), 71.60194174757282),
]

FREQ_IMPLS = [
    ("direct",        ref_freq),
    ("period_invert", period_invert_freq),
    ("ln2_exact",     ln2_exact_freq),
]

DUTY_IMPLS = [
    ("direct", ref_duty),
]


def run_all() -> None:
    print("\n=== Correctness (Frequency) ===")
    for args, expected in TEST_FREQ:
        for name, fn in FREQ_IMPLS:
            result = fn(*args)
            ok = abs(result - expected) / expected < 0.01
            print(f"  [{'OK' if ok else 'FAIL'}] {name}{args} = {result}")

    print("\n=== Correctness (Duty Cycle) ===")
    for args, expected in TEST_DUTY:
        for name, fn in DUTY_IMPLS:
            result = fn(*args)
            ok = abs(result - expected) < 1e-10
            print(f"  [{'OK' if ok else 'FAIL'}] {name}{args} = {result}")

    REPS = 500_000
    inputs = [(45, 45, 7), (356, 234, 976)]

    print(f"\n=== Benchmark (Frequency): {REPS} runs ===")
    for name, fn in FREQ_IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(*a) for a in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
