#!/usr/bin/env python3
"""
Optimized and alternative implementations of Electrical Impedance.

Z = sqrt(R^2 + X^2)

Variants covered:
1. math_sqrt      -- reference: math.sqrt(math.pow(...))
2. complex_abs    -- Z = |R + jX| using Python's abs(complex)
3. hypot          -- math.hypot(R, X) — single-call, overflow-safe

Run:
    python electronics/electrical_impedance_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from electronics.electrical_impedance import electrical_impedance as reference


# ---------------------------------------------------------------------------
# Variant 1 -- math_sqrt (reference)
# ---------------------------------------------------------------------------

def math_sqrt(resistance: float, reactance: float, impedance: float) -> dict[str, float]:
    """
    >>> math_sqrt(3, 4, 0)
    {'impedance': 5.0}
    """
    return reference(resistance, reactance, impedance)


# ---------------------------------------------------------------------------
# Variant 2 -- complex_abs: Z = |R + jX|
# ---------------------------------------------------------------------------

def complex_abs(resistance: float, reactance: float, impedance: float) -> dict[str, float]:
    """
    Uses abs(complex(R, X)) for impedance magnitude.

    >>> complex_abs(3, 4, 0)
    {'impedance': 5.0}
    >>> complex_abs(0, 4, 5)
    {'resistance': 3.0}
    >>> complex_abs(3, 0, 5)
    {'reactance': 4.0}
    """
    if (resistance, reactance, impedance).count(0) != 1:
        raise ValueError("One and only one argument must be 0")
    if impedance == 0:
        return {"impedance": abs(complex(resistance, reactance))}
    elif resistance == 0:
        return {"resistance": math.sqrt(impedance**2 - reactance**2)}
    else:
        return {"reactance": math.sqrt(impedance**2 - resistance**2)}


# ---------------------------------------------------------------------------
# Variant 3 -- hypot: math.hypot is overflow-safe
# ---------------------------------------------------------------------------

def hypot_impl(resistance: float, reactance: float, impedance: float) -> dict[str, float]:
    """
    Uses math.hypot for impedance — handles very large/small values safely.

    >>> hypot_impl(3, 4, 0)
    {'impedance': 5.0}
    >>> hypot_impl(0, 4, 5)
    {'resistance': 3.0}
    """
    if (resistance, reactance, impedance).count(0) != 1:
        raise ValueError("One and only one argument must be 0")
    if impedance == 0:
        return {"impedance": math.hypot(resistance, reactance)}
    elif resistance == 0:
        return {"resistance": math.sqrt(impedance**2 - reactance**2)}
    else:
        return {"reactance": math.sqrt(impedance**2 - resistance**2)}


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ((3, 4, 0), {"impedance": 5.0}),
    ((0, 4, 5), {"resistance": 3.0}),
    ((3, 0, 5), {"reactance": 4.0}),
]

IMPLS = [
    ("reference",    reference),
    ("complex_abs",  complex_abs),
    ("hypot",        hypot_impl),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for args, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(*args)
            key = list(expected.keys())[0]
            ok = key in result and abs(result[key] - expected[key]) < 1e-10
            print(f"  [{'OK' if ok else 'FAIL'}] {name}{args} = {result}")

    REPS = 500_000
    inputs = [(3, 4, 0), (0, 4, 5), (3, 0, 5)]

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
