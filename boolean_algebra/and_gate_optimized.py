#!/usr/bin/env python3
"""
Optimized and alternative implementations of AND Gate.

The reference uses `int(input_1 and input_2)` — Python's short-circuit `and`
operator returns the first falsy value or the last value, then `int()` coerces
to 0 or 1.

Variants covered:
1. short_circuit   -- int(a and b)                (reference, Pythonic)
2. bitwise_and     -- a & b                       (single CPU instruction)
3. multiply        -- a * b                       (algebraic: 1*1=1, else 0)
4. min_gate        -- min(a, b)                   (AND = minimum of inputs)
5. conditional     -- 1 if a == 1 and b == 1 else 0  (explicit truth table)

Key interview insight:
    AND is the simplest composable gate. NAND (its complement) is universal --
    any boolean function can be built from NAND gates alone. In Python,
    `a & b` is the fastest for single-bit values because it maps to a single
    bitwise CPU instruction with no branching.

Run:
    python boolean_algebra/and_gate_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from boolean_algebra.and_gate import and_gate as reference


# ---------------------------------------------------------------------------
# Variant 1 -- short-circuit AND (reference)
# ---------------------------------------------------------------------------

def short_circuit(input_1: int, input_2: int) -> int:
    """
    AND via Python's short-circuit `and` operator.

    >>> short_circuit(0, 0)
    0
    >>> short_circuit(0, 1)
    0
    >>> short_circuit(1, 0)
    0
    >>> short_circuit(1, 1)
    1
    """
    return int(input_1 and input_2)


# ---------------------------------------------------------------------------
# Variant 2 -- bitwise AND (single CPU instruction)
# ---------------------------------------------------------------------------

def bitwise_and(input_1: int, input_2: int) -> int:
    """
    AND via bitwise & operator. For single-bit values, maps directly to hardware.

    >>> bitwise_and(0, 0)
    0
    >>> bitwise_and(0, 1)
    0
    >>> bitwise_and(1, 0)
    0
    >>> bitwise_and(1, 1)
    1
    """
    return input_1 & input_2


# ---------------------------------------------------------------------------
# Variant 3 -- multiplication (algebraic identity)
# ---------------------------------------------------------------------------

def multiply(input_1: int, input_2: int) -> int:
    """
    AND via multiplication: 1*1=1, all other combos yield 0.

    >>> multiply(0, 0)
    0
    >>> multiply(0, 1)
    0
    >>> multiply(1, 0)
    0
    >>> multiply(1, 1)
    1
    """
    return input_1 * input_2


# ---------------------------------------------------------------------------
# Variant 4 -- min gate (AND = minimum)
# ---------------------------------------------------------------------------

def min_gate(input_1: int, input_2: int) -> int:
    """
    AND via min(): for binary inputs, AND equals the minimum value.

    >>> min_gate(0, 0)
    0
    >>> min_gate(0, 1)
    0
    >>> min_gate(1, 0)
    0
    >>> min_gate(1, 1)
    1
    """
    return min(input_1, input_2)


# ---------------------------------------------------------------------------
# Variant 5 -- explicit conditional
# ---------------------------------------------------------------------------

def conditional(input_1: int, input_2: int) -> int:
    """
    AND via explicit comparison -- mirrors the truth table directly.

    >>> conditional(0, 0)
    0
    >>> conditional(0, 1)
    0
    >>> conditional(1, 0)
    0
    >>> conditional(1, 1)
    1
    """
    return 1 if input_1 == 1 and input_2 == 1 else 0


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (0, 0, 0),
    (0, 1, 0),
    (1, 0, 0),
    (1, 1, 1),
]

IMPLS = [
    ("reference",     reference),
    ("short_circuit", short_circuit),
    ("bitwise_and",   bitwise_and),
    ("multiply",      multiply),
    ("min_gate",      min_gate),
    ("conditional",   conditional),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for a, b, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(a, b)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(
            f"  [{tag}] ({a},{b}) expected={expected}  "
            + "  ".join(f"{nm}={v}" for nm, v in results.items())
        )

    REPS = 500_000
    inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]

    print(f"\n=== Benchmark: {REPS} runs, {len(inputs)} input pairs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(a, b) for a, b in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
