#!/usr/bin/env python3
"""
Optimized and alternative implementations of Charging Inductor.

I(t) = (V/R) * (1 - e^(-tR/L))

Variants covered:
1. math_exp       -- math.exp (reference approach)
2. expm1_trick    -- uses math.expm1 for better precision near t=0
3. steady_state   -- separates I_max = V/R, then multiplies by (1-e^(-t/tau))

Run:
    python electronics/charging_inductor_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from electronics.charging_inductor import charging_inductor as reference


# ---------------------------------------------------------------------------
# Variant 1 -- math_exp (reference)
# ---------------------------------------------------------------------------

def math_exp(source_voltage: float, resistance: float, inductance: float, time: float) -> float:
    """
    >>> math_exp(5.8, 1.5, 2.3, 2)
    2.817
    """
    return reference(source_voltage, resistance, inductance, time)


# ---------------------------------------------------------------------------
# Variant 2 -- expm1_trick
# ---------------------------------------------------------------------------

def expm1_trick(source_voltage: float, resistance: float, inductance: float, time: float) -> float:
    """
    Uses -expm1(-x) = 1 - exp(-x) for better precision.

    >>> expm1_trick(5.8, 1.5, 2.3, 2)
    2.817
    >>> expm1_trick(8, 5, 3, 2)
    1.543
    """
    if source_voltage <= 0:
        raise ValueError("Source voltage must be positive.")
    if resistance <= 0:
        raise ValueError("Resistance must be positive.")
    if inductance <= 0:
        raise ValueError("Inductance must be positive.")
    tau = inductance / resistance
    return round(source_voltage / resistance * (-math.expm1(-time / tau)), 3)


# ---------------------------------------------------------------------------
# Variant 3 -- steady_state separation
# ---------------------------------------------------------------------------

def steady_state(source_voltage: float, resistance: float, inductance: float, time: float) -> float:
    """
    I_max = V/R (steady state), then I(t) = I_max * (1 - e^(-t/tau)).

    >>> steady_state(5.8, 1.5, 2.3, 2)
    2.817
    >>> steady_state(8, 5, 3, 2)
    1.543
    """
    if source_voltage <= 0:
        raise ValueError("Source voltage must be positive.")
    if resistance <= 0:
        raise ValueError("Resistance must be positive.")
    if inductance <= 0:
        raise ValueError("Inductance must be positive.")
    i_max = source_voltage / resistance
    tau = inductance / resistance  # L/R time constant
    return round(i_max * (1 - math.exp(-time / tau)), 3)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ((5.8, 1.5, 2.3, 2), 2.817),
    ((8, 5, 3, 2), 1.543),
    ((8, 500, 3, 2), 0.016),
]

IMPLS = [
    ("reference",     reference),
    ("expm1_trick",   expm1_trick),
    ("steady_state",  steady_state),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for args, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(*args)
            ok = result == expected
            print(f"  [{'OK' if ok else 'FAIL'}] {name}{args} = {result}")

    REPS = 500_000
    inputs = [(5.8, 1.5, 2.3, 2), (8, 5, 3, 2), (8, 500, 3, 2)]

    print(f"\n=== Benchmark: {REPS} runs, {len(inputs)} inputs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(*a) for a in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
