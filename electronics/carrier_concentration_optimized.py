#!/usr/bin/env python3
"""
Optimized and alternative implementations of Carrier Concentration.

ni^2 = n * p  (mass action law)

Variants covered:
1. if_chain       -- reference if/elif chain with count(0) check
2. dict_dispatch  -- dictionary-based dispatch for unknown variable
3. math_sqrt      -- uses math.sqrt instead of **0.5

Run:
    python electronics/carrier_concentration_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from electronics.carrier_concentration import carrier_concentration as reference


# ---------------------------------------------------------------------------
# Variant 1 -- if_chain (reference)
# ---------------------------------------------------------------------------

def if_chain(electron_conc: float, hole_conc: float, intrinsic_conc: float) -> tuple:
    """
    >>> if_chain(25, 100, 0)
    ('intrinsic_conc', 50.0)
    >>> if_chain(0, 1600, 200)
    ('electron_conc', 25.0)
    """
    return reference(electron_conc, hole_conc, intrinsic_conc)


# ---------------------------------------------------------------------------
# Variant 2 -- dict_dispatch
# ---------------------------------------------------------------------------

def dict_dispatch(electron_conc: float, hole_conc: float, intrinsic_conc: float) -> tuple:
    """
    Maps zero-value parameter name to its computation.

    >>> dict_dispatch(25, 100, 0)
    ('intrinsic_conc', 50.0)
    >>> dict_dispatch(0, 1600, 200)
    ('electron_conc', 25.0)
    >>> dict_dispatch(1000, 0, 1200)
    ('hole_conc', 1440.0)
    """
    vals = {"electron_conc": electron_conc, "hole_conc": hole_conc, "intrinsic_conc": intrinsic_conc}
    zeros = [k for k, v in vals.items() if v == 0]
    if len(zeros) != 1:
        raise ValueError("You cannot supply more or less than 2 values")
    for v in vals.values():
        if v < 0:
            raise ValueError("Concentrations cannot be negative")
    key = zeros[0]
    if key == "electron_conc":
        return (key, intrinsic_conc**2 / hole_conc)
    elif key == "hole_conc":
        return (key, intrinsic_conc**2 / electron_conc)
    else:
        return (key, (electron_conc * hole_conc) ** 0.5)


# ---------------------------------------------------------------------------
# Variant 3 -- math_sqrt for intrinsic
# ---------------------------------------------------------------------------

def math_sqrt_variant(electron_conc: float, hole_conc: float, intrinsic_conc: float) -> tuple:
    """
    Uses math.sqrt instead of **0.5 for intrinsic calculation.

    >>> math_sqrt_variant(25, 100, 0)
    ('intrinsic_conc', 50.0)
    >>> math_sqrt_variant(0, 1600, 200)
    ('electron_conc', 25.0)
    >>> math_sqrt_variant(1000, 0, 1200)
    ('hole_conc', 1440.0)
    """
    vals = (electron_conc, hole_conc, intrinsic_conc)
    if vals.count(0) != 1:
        raise ValueError("You cannot supply more or less than 2 values")
    if any(v < 0 for v in vals):
        raise ValueError("Concentrations cannot be negative")
    if electron_conc == 0:
        return ("electron_conc", intrinsic_conc**2 / hole_conc)
    elif hole_conc == 0:
        return ("hole_conc", intrinsic_conc**2 / electron_conc)
    else:
        return ("intrinsic_conc", math.sqrt(electron_conc * hole_conc))


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ((25, 100, 0), ("intrinsic_conc", 50.0)),
    ((0, 1600, 200), ("electron_conc", 25.0)),
    ((1000, 0, 1200), ("hole_conc", 1440.0)),
]

IMPLS = [
    ("reference",      reference),
    ("dict_dispatch",  dict_dispatch),
    ("math_sqrt",      math_sqrt_variant),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for args, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(*args)
            ok = result[0] == expected[0] and abs(result[1] - expected[1]) < 1e-10
            print(f"  [{'OK' if ok else 'FAIL'}] {name}{args} = {result}")

    REPS = 500_000
    inputs = [(25, 100, 0), (0, 1600, 200), (1000, 0, 1200)]

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
