#!/usr/bin/env python3
"""
Optimized and alternative implementations of Inductive Reactance.

X_L = 2 * pi * f * L

Variants covered:
1. two_pi         -- reference: 2*pi*f*L
2. tau_formula    -- uses math.tau (= 2*pi) directly
3. omega_form     -- angular frequency omega = 2*pi*f, then X = omega * L

Run:
    python electronics/ind_reactance_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from electronics.ind_reactance import ind_reactance as reference


# ---------------------------------------------------------------------------
# Variant 1 -- two_pi (reference)
# ---------------------------------------------------------------------------

def two_pi(inductance: float, frequency: float, reactance: float) -> dict[str, float]:
    """
    >>> two_pi(35e-6, 1e3, 0)
    {'reactance': 0.2199114857512855}
    """
    return reference(inductance, frequency, reactance)


# ---------------------------------------------------------------------------
# Variant 2 -- tau_formula: math.tau = 2*pi
# ---------------------------------------------------------------------------

def tau_formula(inductance: float, frequency: float, reactance: float) -> dict[str, float]:
    """
    >>> tau_formula(35e-6, 1e3, 0)
    {'reactance': 0.2199114857512855}
    >>> tau_formula(0, 10e3, 50)
    {'inductance': 0.0007957747154594767}
    """
    if (inductance, frequency, reactance).count(0) != 1:
        raise ValueError("One and only one argument must be 0")
    if inductance < 0:
        raise ValueError("Inductance cannot be negative")
    if frequency < 0:
        raise ValueError("Frequency cannot be negative")
    if reactance < 0:
        raise ValueError("Inductive reactance cannot be negative")
    if inductance == 0:
        return {"inductance": reactance / (math.tau * frequency)}
    elif frequency == 0:
        return {"frequency": reactance / (math.tau * inductance)}
    else:
        return {"reactance": math.tau * frequency * inductance}


# ---------------------------------------------------------------------------
# Variant 3 -- omega_form: compute omega first
# ---------------------------------------------------------------------------

def omega_form(inductance: float, frequency: float, reactance: float) -> dict[str, float]:
    """
    Computes angular frequency omega = 2*pi*f first.

    >>> omega_form(35e-6, 1e3, 0)
    {'reactance': 0.2199114857512855}
    >>> omega_form(35e-3, 0, 50)
    {'frequency': 227.36420441699332}
    """
    if (inductance, frequency, reactance).count(0) != 1:
        raise ValueError("One and only one argument must be 0")
    if inductance < 0:
        raise ValueError("Inductance cannot be negative")
    if frequency < 0:
        raise ValueError("Frequency cannot be negative")
    if reactance < 0:
        raise ValueError("Reactance cannot be negative")
    if reactance == 0:
        omega = 2 * math.pi * frequency
        return {"reactance": omega * inductance}
    elif inductance == 0:
        omega = 2 * math.pi * frequency
        return {"inductance": reactance / omega}
    else:
        omega = reactance / inductance
        return {"frequency": omega / (2 * math.pi)}


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ((35e-6, 1e3, 0), {"reactance": 0.2199114857512855}),
    ((0, 10e3, 50), {"inductance": 0.0007957747154594767}),
    ((35e-3, 0, 50), {"frequency": 227.36420441699332}),
]

IMPLS = [
    ("reference",    reference),
    ("tau_formula",  tau_formula),
    ("omega_form",   omega_form),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for args, expected in TEST_CASES:
        key = list(expected.keys())[0]
        for name, fn in IMPLS:
            result = fn(*args)
            val = result[key]
            ok = abs(val - expected[key]) < 1e-10
            print(f"  [{'OK' if ok else 'FAIL'}] {name}: {result}")

    REPS = 500_000
    inputs = [(35e-6, 1e3, 0), (0, 10e3, 50), (35e-3, 0, 50)]

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
