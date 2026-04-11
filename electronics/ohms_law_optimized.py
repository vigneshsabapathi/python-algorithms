#!/usr/bin/env python3
"""
Optimized and alternative implementations of Ohm's Law.

V = I * R

Variants covered:
1. if_chain       -- reference if/elif chain
2. dict_dispatch  -- dictionary-based dispatch on zero argument
3. lambda_table   -- pre-built lambda table for each unknown

Run:
    python electronics/ohms_law_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from electronics.ohms_law import ohms_law as reference


# ---------------------------------------------------------------------------
# Variant 1 -- if_chain (reference)
# ---------------------------------------------------------------------------

def if_chain(voltage: float, current: float, resistance: float) -> dict[str, float]:
    """
    >>> if_chain(10, 0, 5)
    {'current': 2.0}
    """
    return reference(voltage, current, resistance)


# ---------------------------------------------------------------------------
# Variant 2 -- dict_dispatch
# ---------------------------------------------------------------------------

def dict_dispatch(voltage: float, current: float, resistance: float) -> dict[str, float]:
    """
    >>> dict_dispatch(10, 0, 5)
    {'current': 2.0}
    >>> dict_dispatch(0, -1.5, 2)
    {'voltage': -3.0}
    """
    params = {"voltage": voltage, "current": current, "resistance": resistance}
    zeros = [k for k, v in params.items() if v == 0]
    if len(zeros) != 1:
        raise ValueError("One and only one argument must be 0")
    if resistance < 0:
        raise ValueError("Resistance cannot be negative")
    target = zeros[0]
    if target == "voltage":
        return {"voltage": float(current * resistance)}
    elif target == "current":
        return {"current": voltage / resistance}
    else:
        return {"resistance": voltage / current}


# ---------------------------------------------------------------------------
# Variant 3 -- lambda_table
# ---------------------------------------------------------------------------

def lambda_table(voltage: float, current: float, resistance: float) -> dict[str, float]:
    """
    >>> lambda_table(10, 0, 5)
    {'current': 2.0}
    >>> lambda_table(0, 2, 5)
    {'voltage': 10.0}
    """
    if resistance < 0:
        raise ValueError("Resistance cannot be negative")
    formulas = {
        "voltage":    lambda: float(current * resistance),
        "current":    lambda: voltage / resistance,
        "resistance": lambda: voltage / current,
    }
    params = {"voltage": voltage, "current": current, "resistance": resistance}
    zeros = [k for k, v in params.items() if v == 0]
    if len(zeros) != 1:
        raise ValueError("One and only one argument must be 0")
    target = zeros[0]
    return {target: formulas[target]()}


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ((10, 0, 5), {"current": 2.0}),
    ((0, -1.5, 2), {"voltage": -3.0}),
    ((-10, 1, 0), {"resistance": -10.0}),
]

IMPLS = [
    ("reference",     reference),
    ("dict_dispatch", dict_dispatch),
    ("lambda_table",  lambda_table),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for args, expected in TEST_CASES:
        key = list(expected.keys())[0]
        for name, fn in IMPLS:
            result = fn(*args)
            ok = key in result and abs(result[key] - expected[key]) < 1e-10
            print(f"  [{'OK' if ok else 'FAIL'}] {name}{args} = {result}")

    REPS = 500_000
    inputs = [(10, 0, 5), (0, 2, 5), (10, 2, 0)]

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
