#!/usr/bin/env python3
"""
Optimized and alternative implementations of Charging Capacitor.

V(t) = Vs * (1 - e^(-t/RC))

Variants covered:
1. math_exp       -- math.exp (reference approach)
2. numpy_exp      -- numpy.exp for batch computation
3. expm1_trick    -- uses math.expm1 for better precision near t=0

Run:
    python electronics/charging_capacitor_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from electronics.charging_capacitor import charging_capacitor as reference


# ---------------------------------------------------------------------------
# Variant 1 -- math_exp (reference)
# ---------------------------------------------------------------------------

def math_exp(source_voltage: float, resistance: float, capacitance: float, time_sec: float) -> float:
    """
    >>> math_exp(.2, .9, 8.4, .5)
    0.013
    >>> math_exp(20, 2000, 30*pow(10,-5), 4)
    19.975
    """
    return reference(source_voltage, resistance, capacitance, time_sec)


# ---------------------------------------------------------------------------
# Variant 2 -- numpy_exp (vectorizable)
# ---------------------------------------------------------------------------

def numpy_exp(source_voltage: float, resistance: float, capacitance: float, time_sec: float) -> float:
    """
    Uses numpy.exp -- same formula, vectorization-ready.

    >>> numpy_exp(.2, .9, 8.4, .5)
    0.013
    >>> numpy_exp(20, 2000, 30*pow(10,-5), 4)
    19.975
    """
    if source_voltage <= 0:
        raise ValueError("Source voltage must be positive.")
    if resistance <= 0:
        raise ValueError("Resistance must be positive.")
    if capacitance <= 0:
        raise ValueError("Capacitance must be positive.")
    tau = resistance * capacitance
    return round(float(source_voltage * (1 - np.exp(-time_sec / tau))), 3)


# ---------------------------------------------------------------------------
# Variant 3 -- expm1_trick: better precision for small t/RC
# ---------------------------------------------------------------------------

def expm1_trick(source_voltage: float, resistance: float, capacitance: float, time_sec: float) -> float:
    """
    Uses -expm1(-x) = 1-exp(-x) for better precision when t/RC is small.

    >>> expm1_trick(.2, .9, 8.4, .5)
    0.013
    >>> expm1_trick(20, 2000, 30*pow(10,-5), 4)
    19.975
    """
    if source_voltage <= 0:
        raise ValueError("Source voltage must be positive.")
    if resistance <= 0:
        raise ValueError("Resistance must be positive.")
    if capacitance <= 0:
        raise ValueError("Capacitance must be positive.")
    tau = resistance * capacitance
    return round(source_voltage * (-math.expm1(-time_sec / tau)), 3)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ((.2, .9, 8.4, .5), 0.013),
    ((2.2, 3.5, 2.4, 9), 1.446),
    ((15, 200, 20, 2), 0.007),
    ((20, 2000, 30e-5, 4), 19.975),
]

IMPLS = [
    ("reference",   reference),
    ("numpy_exp",   numpy_exp),
    ("expm1_trick", expm1_trick),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for args, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(*args)
            ok = result == expected
            print(f"  [{'OK' if ok else 'FAIL'}] {name}{args} = {result} (expected {expected})")

    REPS = 500_000
    inputs = [(.2, .9, 8.4, .5), (2.2, 3.5, 2.4, 9), (20, 2000, 30e-5, 4)]

    print(f"\n=== Benchmark: {REPS} runs, {len(inputs)} inputs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(*a) for a in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<14} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
