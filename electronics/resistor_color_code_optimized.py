#!/usr/bin/env python3
"""
Optimized and alternative implementations of Resistor Color Code.

Variants covered:
1. sequential     -- reference: sequential band parsing
2. single_pass    -- single-pass with slice indexing
3. enum_based     -- uses IntEnum for color values (type-safe)

Run:
    python electronics/resistor_color_code_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from enum import IntEnum

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from electronics.resistor_color_code import calculate_resistance as reference


# ---------------------------------------------------------------------------
# Variant 1 -- sequential (reference)
# ---------------------------------------------------------------------------

def sequential(n_bands: int, colors: list) -> dict:
    """
    >>> sequential(3, ["Black", "Blue", "Orange"])
    {'resistance': '6000Ω +/-20% '}
    """
    return reference(n_bands, colors)


# ---------------------------------------------------------------------------
# Variant 2 -- single_pass: all logic in one function
# ---------------------------------------------------------------------------

SIG = {"Black": 0, "Brown": 1, "Red": 2, "Orange": 3, "Yellow": 4,
       "Green": 5, "Blue": 6, "Violet": 7, "Grey": 8, "White": 9}
MUL = {"Black": 1, "Brown": 10, "Red": 100, "Orange": 1e3, "Yellow": 1e4,
       "Green": 1e5, "Blue": 1e6, "Violet": 1e7, "Grey": 1e8, "White": 1e9,
       "Gold": 0.1, "Silver": 0.01}
TOL = {"Brown": 1, "Red": 2, "Orange": 0.05, "Yellow": 0.02, "Green": 0.5,
       "Blue": 0.25, "Violet": 0.1, "Grey": 0.01, "Gold": 5, "Silver": 10}
TEMP = {"Black": 250, "Brown": 100, "Red": 50, "Orange": 15, "Yellow": 25,
        "Green": 20, "Blue": 10, "Violet": 5, "Grey": 1}


def single_pass(n_bands: int, colors: list) -> dict:
    """
    All decoding in one function with direct dict lookups.

    >>> single_pass(3, ["Black", "Blue", "Orange"])
    {'resistance': '6000Ω +/-20% '}
    >>> single_pass(5, ["Violet", "Brown", "Grey", "Silver", "Green"])
    {'resistance': '7.18Ω +/-0.5% '}
    """
    if n_bands not in (3, 4, 5, 6):
        raise ValueError("Bands must be 3-6")
    if len(colors) != n_bands:
        raise ValueError(f"Expected {n_bands} colors, got {len(colors)}")
    n_sig = 3 if n_bands >= 5 else 2
    digits = ""
    for c in colors[:n_sig]:
        if c not in SIG:
            raise ValueError(f"{c} invalid for significant band")
        digits += str(SIG[c])
    mul_color = colors[n_sig]
    if mul_color not in MUL:
        raise ValueError(f"{mul_color} invalid for multiplier")
    resistance = int(digits) * MUL[mul_color]
    r_str = str(int(resistance)) if resistance == int(resistance) else str(resistance)
    tolerance = TOL.get(colors[n_sig + 1], 20) if n_bands >= 4 else 20
    if n_bands == 6:
        tc = TEMP.get(colors[n_sig + 2], 0)
        return {"resistance": f"{r_str}\u03a9 +/-{tolerance}% {tc} ppm/K"}
    return {"resistance": f"{r_str}\u03a9 +/-{tolerance}% "}


# ---------------------------------------------------------------------------
# Variant 3 -- enum_based
# ---------------------------------------------------------------------------

class Color(IntEnum):
    Black = 0; Brown = 1; Red = 2; Orange = 3; Yellow = 4
    Green = 5; Blue = 6; Violet = 7; Grey = 8; White = 9


def enum_based(n_bands: int, colors: list) -> dict:
    """
    Uses IntEnum for type-safe color lookups.

    >>> enum_based(3, ["Black", "Blue", "Orange"])
    {'resistance': '6000Ω +/-20% '}
    """
    if n_bands not in (3, 4, 5, 6) or len(colors) != n_bands:
        raise ValueError("Invalid band count")
    n_sig = 3 if n_bands >= 5 else 2
    digits = ""
    for c in colors[:n_sig]:
        digits += str(Color[c].value)
    resistance = int(digits) * MUL[colors[n_sig]]
    r_str = str(int(resistance)) if resistance == int(resistance) else str(resistance)
    tolerance = TOL.get(colors[n_sig + 1], 20) if n_bands >= 4 else 20
    if n_bands == 6:
        tc = TEMP.get(colors[n_sig + 2], 0)
        return {"resistance": f"{r_str}\u03a9 +/-{tolerance}% {tc} ppm/K"}
    return {"resistance": f"{r_str}\u03a9 +/-{tolerance}% "}


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ((3, ["Black", "Blue", "Orange"]), "6000\u03a9 +/-20% "),
    ((4, ["Orange", "Green", "Blue", "Gold"]), "35000000\u03a9 +/-5% "),
    ((5, ["Violet", "Brown", "Grey", "Silver", "Green"]), "7.18\u03a9 +/-0.5% "),
]

IMPLS = [
    ("reference",    reference),
    ("single_pass",  single_pass),
    ("enum_based",   enum_based),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for (nb, colors), expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(nb, colors[:])
            ok = result["resistance"] == expected
            safe = result["resistance"].encode("ascii", "replace").decode()
            print(f"  [{'OK' if ok else 'FAIL'}] {name}: {safe}")

    REPS = 200_000
    inputs = [(3, ["Black", "Blue", "Orange"]),
              (4, ["Orange", "Green", "Blue", "Gold"]),
              (5, ["Violet", "Brown", "Grey", "Silver", "Green"])]

    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(nb, cs[:]) for nb, cs in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<14} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
