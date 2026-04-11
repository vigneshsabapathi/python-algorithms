#!/usr/bin/env python3
"""
Optimized and alternative implementations of Electric Power.

P = V * I

Variants covered:
1. namedtuple     -- reference NamedTuple approach
2. dict_return    -- returns dict instead of NamedTuple
3. match_stmt     -- uses dict-based dispatch (Python 3.10+ compatible)

Run:
    python electronics/electric_power_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from electronics.electric_power import electric_power as reference


# ---------------------------------------------------------------------------
# Variant 1 -- namedtuple (reference)
# ---------------------------------------------------------------------------

def namedtuple_impl(voltage: float, current: float, power: float) -> tuple:
    """
    >>> namedtuple_impl(0, 2, 5)
    Result(name='voltage', value=2.5)
    >>> namedtuple_impl(2, 2, 0)
    Result(name='power', value=4.0)
    """
    return reference(voltage, current, power)


# ---------------------------------------------------------------------------
# Variant 2 -- dict_return
# ---------------------------------------------------------------------------

def dict_return(voltage: float, current: float, power: float) -> dict[str, float]:
    """
    Returns a dict instead of NamedTuple.

    >>> dict_return(0, 2, 5)
    {'voltage': 2.5}
    >>> dict_return(2, 2, 0)
    {'power': 4.0}
    >>> dict_return(0, 0, 5)
    Traceback (most recent call last):
        ...
    ValueError: Exactly one argument must be 0
    """
    if (voltage, current, power).count(0) != 1:
        raise ValueError("Exactly one argument must be 0")
    if power < 0:
        raise ValueError("Power cannot be negative")
    if voltage == 0:
        return {"voltage": power / current}
    elif current == 0:
        return {"current": power / voltage}
    else:
        return {"power": float(round(abs(voltage * current), 2))}


# ---------------------------------------------------------------------------
# Variant 3 -- dispatch table
# ---------------------------------------------------------------------------

def dispatch_table(voltage: float, current: float, power: float) -> dict[str, float]:
    """
    Uses a dispatch table for the zero-parameter.

    >>> dispatch_table(0, 2, 5)
    {'voltage': 2.5}
    >>> dispatch_table(2, 0, 6)
    {'current': 3.0}
    >>> dispatch_table(2, 2, 0)
    {'power': 4.0}
    """
    params = {"voltage": voltage, "current": current, "power": power}
    zeros = [k for k, v in params.items() if v == 0]
    if len(zeros) != 1:
        raise ValueError("Exactly one argument must be 0")
    if power < 0:
        raise ValueError("Power cannot be negative")
    formulas = {
        "voltage": lambda: power / current,
        "current": lambda: power / voltage,
        "power":   lambda: float(round(abs(voltage * current), 2)),
    }
    target = zeros[0]
    return {target: formulas[target]()}


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ((0, 2, 5), "voltage", 2.5),
    ((2, 2, 0), "power", 4.0),
    ((2, 0, 6), "current", 3.0),
    ((-2, 3, 0), "power", 6.0),
]

IMPLS = [
    ("reference",  reference),
    ("dict",       dict_return),
    ("dispatch",   dispatch_table),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for args, key, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(*args)
            if isinstance(result, dict):
                val = result[key]
            else:
                val = result.value
            ok = abs(val - expected) < 1e-10
            print(f"  [{'OK' if ok else 'FAIL'}] {name}{args} = {result}")

    REPS = 500_000
    inputs = [(0, 2, 5), (2, 2, 0), (2, 0, 6)]

    print(f"\n=== Benchmark: {REPS} runs, {len(inputs)} inputs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(*a) for a in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<12} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
