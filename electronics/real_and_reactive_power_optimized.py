#!/usr/bin/env python3
"""
Optimized and alternative implementations of Real and Reactive Power.

P_real = S * pf
P_reactive = S * sqrt(1 - pf^2)

Variants covered:
1. math_sqrt      -- reference: math.sqrt
2. acos_sin       -- P_reactive = S * sin(acos(pf))
3. complex_power  -- S_complex = P + jQ via complex arithmetic

Run:
    python electronics/real_and_reactive_power_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from electronics.real_and_reactive_power import real_power as ref_real, reactive_power as ref_reactive


# ---------------------------------------------------------------------------
# Variant 1 -- math_sqrt (reference)
# ---------------------------------------------------------------------------

def math_sqrt_real(apparent_power: float, power_factor: float) -> float:
    """
    >>> math_sqrt_real(100, 0.9)
    90.0
    """
    return ref_real(apparent_power, power_factor)


def math_sqrt_reactive(apparent_power: float, power_factor: float) -> float:
    """
    >>> math_sqrt_reactive(100, 0.9)
    43.58898943540673
    """
    return ref_reactive(apparent_power, power_factor)


# ---------------------------------------------------------------------------
# Variant 2 -- acos_sin: Q = S * sin(acos(pf))
# ---------------------------------------------------------------------------

def acos_sin_reactive(apparent_power: float, power_factor: float) -> float:
    """
    Computes reactive power via sin(acos(pf)) identity.

    >>> abs(acos_sin_reactive(100, 0.9) - 43.589) < 0.001
    True
    >>> acos_sin_reactive(0, 0.8)
    0.0
    """
    if not isinstance(power_factor, (int, float)) or power_factor < -1 or power_factor > 1:
        raise ValueError("power_factor must be between -1 and 1")
    angle = math.acos(abs(power_factor))
    return apparent_power * math.sin(angle)


# ---------------------------------------------------------------------------
# Variant 3 -- complex_power: S = P + jQ
# ---------------------------------------------------------------------------

def complex_power(apparent_power: float, power_factor: float) -> complex:
    """
    Returns S as complex: real part = P, imaginary part = Q.

    >>> result = complex_power(100, 0.9)
    >>> abs(result.real - 90.0) < 1e-10
    True
    >>> abs(result.imag - 43.589) < 0.001
    True
    """
    if not isinstance(power_factor, (int, float)) or power_factor < -1 or power_factor > 1:
        raise ValueError("power_factor must be between -1 and 1")
    p = apparent_power * power_factor
    q = apparent_power * math.sqrt(1 - power_factor**2)
    return complex(p, q)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ((100, 0.9), 90.0, 43.58898943540673),
    ((0, 0.8), 0.0, 0.0),
    ((100, -0.9), -90.0, 43.58898943540673),
]

REAL_IMPLS = [("ref_real", ref_real), ("math_sqrt_real", math_sqrt_real)]
REACT_IMPLS = [("ref_reactive", ref_reactive), ("acos_sin", acos_sin_reactive)]


def run_all() -> None:
    print("\n=== Correctness (Real Power) ===")
    for args, exp_r, _ in TEST_CASES:
        for name, fn in REAL_IMPLS:
            result = fn(*args)
            ok = abs(result - exp_r) < 1e-10
            print(f"  [{'OK' if ok else 'FAIL'}] {name}{args} = {result}")

    print("\n=== Correctness (Reactive Power) ===")
    for args, _, exp_q in TEST_CASES:
        for name, fn in REACT_IMPLS:
            result = fn(*args)
            ok = abs(result - exp_q) < 1e-6
            print(f"  [{'OK' if ok else 'FAIL'}] {name}{args} = {result}")

    print("\n=== Complex Power ===")
    for args, exp_r, exp_q in TEST_CASES:
        s = complex_power(*args)
        ok = abs(s.real - exp_r) < 1e-6 and abs(s.imag - exp_q) < 1e-6
        print(f"  [{'OK' if ok else 'FAIL'}] complex_power{args} = {s}")

    REPS = 500_000
    inputs = [(100, 0.9), (200, 0.7), (50, 1.0)]

    print(f"\n=== Benchmark (Reactive): {REPS} runs ===")
    for name, fn in REACT_IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(*a) for a in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
