#!/usr/bin/env python3
"""
Optimized and alternative implementations of Doppler Frequency.

Variants covered:
1. classical       -- f' = f*(v+vo)/(v+vs) (reference)
2. relativistic    -- f' = f*sqrt((1+beta)/(1-beta)) for EM waves
3. wavelength      -- lambda' = lambda*(v+vs)/(v+vo)

Run:
    python physics/doppler_frequency_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from physics.doppler_frequency import doppler_frequency as reference


def classical(f: float, v: float, vo: float = 0, vs: float = 0) -> float:
    """
    Classical Doppler: f' = f*(v+vo)/(v+vs).

    >>> round(classical(440, 343, 30, 0), 2)
    478.48
    """
    return f * (v + vo) / (v + vs)


def relativistic(f: float, beta: float) -> float:
    """
    Relativistic Doppler for EM waves: f' = f*sqrt((1+beta)/(1-beta)).
    beta = v/c, positive = approaching.

    >>> round(relativistic(440, 0.1), 2)
    486.44
    >>> round(relativistic(440, -0.1), 2)
    397.99
    """
    if abs(beta) >= 1:
        raise ValueError("beta must be between -1 and 1 exclusive")
    return f * math.sqrt((1 + beta) / (1 - beta))


def wavelength_shift(
    wavelength: float, v: float, vo: float = 0, vs: float = 0
) -> float:
    """
    Doppler effect in terms of wavelength.
    lambda' = lambda * (v + vs) / (v + vo).

    >>> round(wavelength_shift(0.78, 343, 30, 0), 4)
    0.7173
    """
    return wavelength * (v + vs) / (v + vo)


TEST_CASES = [
    (440, 343, 0, 0, 440.0),
    (440, 343, 30, 0, 478.48),
    (440, 343, 0, 30, 404.61),
    (440, 343, 30, -30, 524.35),
]

IMPLS = [
    ("reference", lambda f, v, vo, vs: reference(f, v, vo, vs)),
    ("classical", classical),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for f, v, vo, vs, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = round(fn(f, v, vo, vs), 2)
            tag = "OK" if result == expected else "FAIL"
            print(f"  [{tag}] {name}: f'={result} (expected {expected})")

    REPS = 500_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(f, v, vo, vs) for f, v, vo, vs, _ in TEST_CASES],
            number=REPS,
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
