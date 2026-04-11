#!/usr/bin/env python3
"""
Optimized and alternative implementations of Resonant Frequency.

f = 1 / (2 * pi * sqrt(L * C))

Variants covered:
1. pi_sqrt        -- reference: math.pi + math.sqrt
2. tau_formula    -- uses math.tau (= 2*pi)
3. angular_freq   -- compute omega = 1/sqrt(LC), then f = omega/(2*pi)

Run:
    python electronics/resonant_frequency_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from electronics.resonant_frequency import resonant_frequency as reference


# ---------------------------------------------------------------------------
# Variant 1 -- pi_sqrt (reference)
# ---------------------------------------------------------------------------

def pi_sqrt(inductance: float, capacitance: float) -> tuple:
    """
    >>> pi_sqrt(10, 5)
    ('Resonant frequency', 0.022507907903927652)
    """
    return reference(inductance, capacitance)


# ---------------------------------------------------------------------------
# Variant 2 -- tau_formula
# ---------------------------------------------------------------------------

def tau_formula(inductance: float, capacitance: float) -> tuple:
    """
    Uses math.tau instead of 2*math.pi.

    >>> tau_formula(10, 5)
    ('Resonant frequency', 0.022507907903927652)
    """
    if inductance <= 0:
        raise ValueError("Inductance cannot be 0 or negative")
    if capacitance <= 0:
        raise ValueError("Capacitance cannot be 0 or negative")
    return ("Resonant frequency", 1 / (math.tau * math.sqrt(inductance * capacitance)))


# ---------------------------------------------------------------------------
# Variant 3 -- angular_freq: omega first
# ---------------------------------------------------------------------------

def angular_freq(inductance: float, capacitance: float) -> tuple:
    """
    Computes angular frequency omega = 1/sqrt(LC), then f = omega / (2*pi).

    >>> angular_freq(10, 5)
    ('Resonant frequency', 0.022507907903927652)
    """
    if inductance <= 0:
        raise ValueError("Inductance cannot be 0 or negative")
    if capacitance <= 0:
        raise ValueError("Capacitance cannot be 0 or negative")
    omega = 1 / math.sqrt(inductance * capacitance)
    return ("Resonant frequency", omega / (2 * math.pi))


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ((10, 5), 0.022507907903927652),
    ((1, 1), 1 / (2 * math.pi)),
    ((100, 0.001), 1 / (2 * math.pi * math.sqrt(0.1))),
]

IMPLS = [
    ("reference",    reference),
    ("tau_formula",  tau_formula),
    ("angular_freq", angular_freq),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for args, expected in TEST_CASES:
        for name, fn in IMPLS:
            _, result = fn(*args)
            ok = abs(result - expected) < 1e-12
            print(f"  [{'OK' if ok else 'FAIL'}] {name}{args} = {result}")

    REPS = 500_000
    inputs = [(10, 5), (1, 1), (100, 0.001)]

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
