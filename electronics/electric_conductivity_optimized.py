#!/usr/bin/env python3
"""
Optimized and alternative implementations of Electric Conductivity.

sigma = n * e * mu

Variants covered:
1. if_chain       -- reference approach
2. dict_dispatch  -- dictionary-based dispatch
3. scipy_const    -- uses scipy.constants.e for electron charge

Run:
    python electronics/electric_conductivity_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from electronics.electric_conductivity import electric_conductivity as reference, ELECTRON_CHARGE


# ---------------------------------------------------------------------------
# Variant 1 -- if_chain (reference)
# ---------------------------------------------------------------------------

def if_chain(conductivity: float, electron_conc: float, mobility: float) -> tuple[str, float]:
    """
    >>> if_chain(25, 100, 0)
    ('mobility', 1.5604519068722301e+18)
    """
    return reference(conductivity, electron_conc, mobility)


# ---------------------------------------------------------------------------
# Variant 2 -- dict_dispatch
# ---------------------------------------------------------------------------

def dict_dispatch(conductivity: float, electron_conc: float, mobility: float) -> tuple[str, float]:
    """
    >>> dict_dispatch(25, 100, 0)
    ('mobility', 1.5604519068722301e+18)
    >>> dict_dispatch(0, 1600, 200)
    ('conductivity', 5.12672e-14)
    """
    params = {"conductivity": conductivity, "electron_conc": electron_conc, "mobility": mobility}
    zeros = [k for k, v in params.items() if v == 0]
    if len(zeros) != 1:
        raise ValueError("You cannot supply more or less than 2 values")
    if conductivity < 0:
        raise ValueError("Conductivity cannot be negative")
    if electron_conc < 0:
        raise ValueError("Electron concentration cannot be negative")
    if mobility < 0:
        raise ValueError("mobility cannot be negative")
    target = zeros[0]
    e = ELECTRON_CHARGE
    if target == "conductivity":
        return ("conductivity", mobility * electron_conc * e)
    elif target == "electron_conc":
        return ("electron_conc", conductivity / (mobility * e))
    else:
        return ("mobility", conductivity / (electron_conc * e))


# ---------------------------------------------------------------------------
# Variant 3 -- scipy_const
# ---------------------------------------------------------------------------

def scipy_const(conductivity: float, electron_conc: float, mobility: float) -> tuple[str, float]:
    """
    Uses scipy.constants.e for electron charge.

    >>> result = scipy_const(25, 100, 0)
    >>> result[0]
    'mobility'
    >>> abs(result[1] - 1.56e18) < 1e16
    True
    """
    from scipy.constants import e as q_e
    params = (conductivity, electron_conc, mobility)
    if params.count(0) != 1:
        raise ValueError("You cannot supply more or less than 2 values")
    if conductivity < 0 or electron_conc < 0 or mobility < 0:
        raise ValueError("Values cannot be negative")
    if conductivity == 0:
        return ("conductivity", mobility * electron_conc * q_e)
    elif electron_conc == 0:
        return ("electron_conc", conductivity / (mobility * q_e))
    else:
        return ("mobility", conductivity / (electron_conc * q_e))


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ((25, 100, 0), ("mobility", 1.5604519068722301e+18)),
    ((0, 1600, 200), ("conductivity", 5.12672e-14)),
    ((1000, 0, 1200), ("electron_conc", 5.201506356240767e+18)),
]

IMPLS = [
    ("reference",     reference),
    ("dict_dispatch", dict_dispatch),
    ("scipy_const",   scipy_const),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for args, (ek, ev) in TEST_CASES:
        for name, fn in IMPLS:
            k, v = fn(*args)
            ok = k == ek and abs(v - ev) / max(abs(ev), 1e-30) < 0.01
            print(f"  [{'OK' if ok else 'FAIL'}] {name}: ({k}, {v})")

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
