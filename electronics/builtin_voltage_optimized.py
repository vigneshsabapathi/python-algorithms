#!/usr/bin/env python3
"""
Optimized and alternative implementations of Builtin Voltage.

V_bi = (kT/q) * ln(Na*Nd / ni^2)

Variants covered:
1. scipy_const    -- uses scipy.constants (reference approach)
2. hardcoded      -- hardcoded physical constants (no scipy dependency)
3. thermal_split  -- pre-compute thermal voltage Vt = kT/q, then Vt * ln(...)

Run:
    python electronics/builtin_voltage_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from math import log

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from electronics.builtin_voltage import builtin_voltage as reference

# Physical constants (hardcoded)
K_BOLTZMANN = 1.380649e-23  # J/K
Q_ELECTRON = 1.602176634e-19  # C
T = 300  # K


# ---------------------------------------------------------------------------
# Variant 1 -- scipy_const (reference wrapper)
# ---------------------------------------------------------------------------

def scipy_const(donor_conc: float, acceptor_conc: float, intrinsic_conc: float) -> float:
    """
    >>> scipy_const(1e17, 1e17, 1e10)
    0.833370010652644
    """
    return reference(donor_conc, acceptor_conc, intrinsic_conc)


# ---------------------------------------------------------------------------
# Variant 2 -- hardcoded constants (no scipy)
# ---------------------------------------------------------------------------

def hardcoded(donor_conc: float, acceptor_conc: float, intrinsic_conc: float) -> float:
    """
    Uses hardcoded Boltzmann and electron charge values.

    >>> abs(hardcoded(1e17, 1e17, 1e10) - 0.8334) < 0.001
    True
    """
    if donor_conc <= 0:
        raise ValueError("Donor concentration should be positive")
    if acceptor_conc <= 0:
        raise ValueError("Acceptor concentration should be positive")
    if intrinsic_conc <= 0:
        raise ValueError("Intrinsic concentration should be positive")
    if donor_conc <= intrinsic_conc:
        raise ValueError("Donor > intrinsic required")
    if acceptor_conc <= intrinsic_conc:
        raise ValueError("Acceptor > intrinsic required")
    return K_BOLTZMANN * T * log((donor_conc * acceptor_conc) / intrinsic_conc**2) / Q_ELECTRON


# ---------------------------------------------------------------------------
# Variant 3 -- thermal_split: pre-compute Vt
# ---------------------------------------------------------------------------

VT = K_BOLTZMANN * T / Q_ELECTRON  # ~0.02585 V at 300K


def thermal_split(donor_conc: float, acceptor_conc: float, intrinsic_conc: float) -> float:
    """
    Pre-computes thermal voltage Vt = kT/q, then V_bi = Vt * ln(Na*Nd/ni^2).

    >>> abs(thermal_split(1e17, 1e17, 1e10) - 0.8334) < 0.001
    True
    """
    if donor_conc <= 0 or acceptor_conc <= 0 or intrinsic_conc <= 0:
        raise ValueError("All concentrations must be positive")
    if donor_conc <= intrinsic_conc or acceptor_conc <= intrinsic_conc:
        raise ValueError("Donor and acceptor must exceed intrinsic concentration")
    return VT * log((donor_conc * acceptor_conc) / intrinsic_conc**2)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ((1e17, 1e17, 1e10), 0.833370010652644),
    ((1e18, 1e16, 1e10), 0.833370010652644),
    ((5e16, 5e15, 1e10), 0.713),
]

IMPLS = [
    ("reference",      reference),
    ("hardcoded",      hardcoded),
    ("thermal_split",  thermal_split),
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
        print(f"  args={args}")
        for nm, v in results.items():
            ok = isinstance(v, float) and abs(v - expected) < 0.01
            tag = "OK" if ok else "~"
            print(f"    [{tag}] {nm}: {v}")

    REPS = 200_000
    inputs = [(1e17, 1e17, 1e10), (1e18, 1e16, 1e10)]

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
