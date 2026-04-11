#!/usr/bin/env python3
"""
Optimized and alternative implementations of Apparent Power.

The reference computes S = V_rect * I_rect via cmath.rect conversion.

Variants covered:
1. phasor_rect    -- cmath.rect multiplication (reference approach)
2. polar_formula  -- S = V*I, angle = Vangle + Iangle (stay in polar)
3. trig_manual    -- manual cos/sin expansion without cmath
4. numpy_exp      -- numpy complex exponential: V*e^(j*theta)

Key interview insight:
    Apparent power is V*I (not V*I*), unlike complex power.
    S = |V||I|*e^j(theta_v + theta_i).

Run:
    python electronics/apparent_power_optimized.py
"""

from __future__ import annotations

import cmath
import math
import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from electronics.apparent_power import apparent_power as reference


# ---------------------------------------------------------------------------
# Variant 1 -- phasor_rect (reference approach, explicit)
# ---------------------------------------------------------------------------

def phasor_rect(
    voltage: float, current: float, voltage_angle: float, current_angle: float
) -> complex:
    """
    >>> phasor_rect(100, 5, 0, 0)
    (500+0j)
    >>> phasor_rect(100, 5, 90, 0)
    (3.061616997868383e-14+500j)
    """
    v = cmath.rect(voltage, math.radians(voltage_angle))
    i = cmath.rect(current, math.radians(current_angle))
    return v * i


# ---------------------------------------------------------------------------
# Variant 2 -- polar_formula: stay in polar, return complex
# ---------------------------------------------------------------------------

def polar_formula(
    voltage: float, current: float, voltage_angle: float, current_angle: float
) -> complex:
    """
    S = |V|*|I| at angle (theta_v + theta_i), converted to rect at the end.

    >>> polar_formula(100, 5, 0, 0)
    (500+0j)
    >>> polar_formula(100, 5, 90, 0)
    (3.061616997868383e-14+500j)
    """
    magnitude = voltage * current
    angle_rad = math.radians(voltage_angle + current_angle)
    return cmath.rect(magnitude, angle_rad)


# ---------------------------------------------------------------------------
# Variant 3 -- trig_manual: no cmath, pure math trig
# ---------------------------------------------------------------------------

def trig_manual(
    voltage: float, current: float, voltage_angle: float, current_angle: float
) -> complex:
    """
    Manual expansion: real = V*I*cos(sum), imag = V*I*sin(sum).

    >>> trig_manual(100, 5, 0, 0)
    (500+0j)
    >>> abs(trig_manual(100, 5, 90, 0).imag - 500) < 1e-10
    True
    """
    magnitude = voltage * current
    angle_rad = math.radians(voltage_angle + current_angle)
    return complex(magnitude * math.cos(angle_rad), magnitude * math.sin(angle_rad))


# ---------------------------------------------------------------------------
# Variant 4 -- numpy_exp: numpy complex exponential
# ---------------------------------------------------------------------------

def numpy_exp(
    voltage: float, current: float, voltage_angle: float, current_angle: float
) -> complex:
    """
    V*I * e^(j*(theta_v+theta_i)) via numpy.

    >>> numpy_exp(100, 5, 0, 0)
    (500+0j)
    >>> abs(numpy_exp(100, 5, 90, 0).imag - 500) < 1e-10
    True
    """
    magnitude = voltage * current
    angle_rad = math.radians(voltage_angle + current_angle)
    result = magnitude * np.exp(1j * angle_rad)
    return complex(result)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ((100, 5, 0, 0), (500 + 0j)),
    ((100, 5, 90, 0), None),  # check magnitude ~500
    ((200, 10, -30, -90), None),  # check magnitude ~2000
]

IMPLS = [
    ("reference",     reference),
    ("phasor_rect",   phasor_rect),
    ("polar_formula", polar_formula),
    ("trig_manual",   trig_manual),
    ("numpy_exp",     numpy_exp),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for args, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(*args)
            except Exception as e:
                results[name] = f"ERR:{e}"
        if expected is not None:
            ok = all(
                isinstance(v, complex) and abs(v - expected) < 1e-6
                for v in results.values()
            )
        else:
            magnitudes = [abs(v) for v in results.values() if isinstance(v, complex)]
            ok = len(magnitudes) == len(results) and max(magnitudes) - min(magnitudes) < 1e-6
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] args={args}")
        for nm, v in results.items():
            print(f"       {nm}: {v}")

    REPS = 200_000
    inputs = [(100, 5, 0, 0), (100, 5, 90, 0), (200, 10, -30, -90), (100, 5, -45, -60)]

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
