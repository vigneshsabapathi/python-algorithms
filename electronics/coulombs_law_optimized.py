#!/usr/bin/env python3
"""
Optimized and alternative implementations of Coulomb's Law.

F = k * |q1*q2| / r^2

Variants covered:
1. if_chain       -- reference if/elif approach
2. dict_dispatch  -- dictionary-based dispatch on the zero argument
3. scipy_const    -- uses scipy.constants for Coulomb's constant

Run:
    python electronics/coulombs_law_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from electronics.coulombs_law import couloumbs_law as reference, COULOMBS_CONSTANT


# ---------------------------------------------------------------------------
# Variant 1 -- if_chain (reference)
# ---------------------------------------------------------------------------

def if_chain(force: float, charge1: float, charge2: float, distance: float) -> dict[str, float]:
    """
    >>> if_chain(0, 3, 5, 2000)
    {'force': 33705.0}
    """
    return reference(force, charge1, charge2, distance)


# ---------------------------------------------------------------------------
# Variant 2 -- dict_dispatch
# ---------------------------------------------------------------------------

def dict_dispatch(force: float, charge1: float, charge2: float, distance: float) -> dict[str, float]:
    """
    >>> dict_dispatch(0, 3, 5, 2000)
    {'force': 33705.0}
    >>> dict_dispatch(10, 0, 5, 2000)
    {'charge1': 0.0008900756564307966}
    """
    k = COULOMBS_CONSTANT
    params = {"force": force, "charge1": charge1, "charge2": charge2, "distance": distance}
    zeros = [name for name, val in params.items() if val == 0]
    if len(zeros) != 1:
        raise ValueError("One and only one argument must be 0")
    if distance < 0:
        raise ValueError("Distance cannot be negative")
    cp = abs(charge1 * charge2)
    target = zeros[0]
    if target == "force":
        return {"force": k * cp / distance**2}
    elif target == "charge1":
        return {"charge1": abs(force) * distance**2 / (k * charge2)}
    elif target == "charge2":
        return {"charge2": abs(force) * distance**2 / (k * charge1)}
    else:
        return {"distance": (k * cp / abs(force)) ** 0.5}


# ---------------------------------------------------------------------------
# Variant 3 -- scipy_const
# ---------------------------------------------------------------------------

def scipy_const(force: float, charge1: float, charge2: float, distance: float) -> dict[str, float]:
    """
    Uses scipy.constants for Coulomb's constant value.

    >>> result = scipy_const(0, 3, 5, 2000)
    >>> abs(result['force'] - 33705.0) < 100
    True
    """
    from scipy.constants import epsilon_0
    from math import pi
    k = 1 / (4 * pi * epsilon_0)
    params = {"force": force, "charge1": charge1, "charge2": charge2, "distance": distance}
    zeros = [name for name, val in params.items() if val == 0]
    if len(zeros) != 1:
        raise ValueError("One and only one argument must be 0")
    if distance < 0:
        raise ValueError("Distance cannot be negative")
    cp = abs(charge1 * charge2)
    target = zeros[0]
    if target == "force":
        return {"force": k * cp / distance**2}
    elif target == "charge1":
        return {"charge1": abs(force) * distance**2 / (k * charge2)}
    elif target == "charge2":
        return {"charge2": abs(force) * distance**2 / (k * charge1)}
    else:
        return {"distance": (k * cp / abs(force)) ** 0.5}


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ((0, 3, 5, 2000), "force", 33705.0),
    ((10, 0, 5, 2000), "charge1", 0.0008900756564307966),
    ((10, 3, 5, 0), "distance", 116112.01488218177),
]

IMPLS = [
    ("reference",     reference),
    ("dict_dispatch", dict_dispatch),
    ("scipy_const",   scipy_const),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for args, key, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(*args)
            val = result[key]
            ok = abs(val - expected) / max(abs(expected), 1e-10) < 0.01
            print(f"  [{'OK' if ok else 'FAIL'}] {name}: {result}")

    REPS = 300_000
    inputs = [(0, 3, 5, 2000), (10, 0, 5, 2000), (10, 3, 5, 0)]

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
