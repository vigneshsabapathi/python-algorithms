#!/usr/bin/env python3
"""
Optimized and alternative implementations of IMPLY Gate.

The reference uses `int(input_1 == 0 or input_2 == 1)` — material implication
is true unless the antecedent is true and the consequent is false.

Variants covered:
1. comparison    -- int(a == 0 or b == 1)           (reference, readable)
2. bitwise_or    -- (~a & 1) | b                    (NOT a OR b)
3. not_and_not   -- int(not a or bool(b))           (Pythonic boolean)
4. le_check      -- int(a <= b)                     (for binary: a<=b iff a->b)

Key interview insight:
    IMPLY (material conditional) is equivalent to NOT A OR B. It only returns 0
    when A=1 and B=0 (the antecedent is true but the consequent is false).
    In hardware, IMPLY is important for memristor-based logic circuits.

Run:
    python boolean_algebra/imply_gate_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from boolean_algebra.imply_gate import imply_gate as reference


# ---------------------------------------------------------------------------
# Variant 1 -- comparison (reference)
# ---------------------------------------------------------------------------

def comparison(input_1: int, input_2: int) -> int:
    """
    IMPLY via explicit comparison.

    >>> comparison(0, 0)
    1
    >>> comparison(0, 1)
    1
    >>> comparison(1, 0)
    0
    >>> comparison(1, 1)
    1
    """
    return int(input_1 == 0 or input_2 == 1)


# ---------------------------------------------------------------------------
# Variant 2 -- bitwise: NOT a OR b
# ---------------------------------------------------------------------------

def bitwise_or(input_1: int, input_2: int) -> int:
    """
    IMPLY via bitwise NOT a OR b.

    >>> bitwise_or(0, 0)
    1
    >>> bitwise_or(0, 1)
    1
    >>> bitwise_or(1, 0)
    0
    >>> bitwise_or(1, 1)
    1
    """
    return (~input_1 & 1) | input_2


# ---------------------------------------------------------------------------
# Variant 3 -- Pythonic boolean (not a or b)
# ---------------------------------------------------------------------------

def not_and_not(input_1: int, input_2: int) -> int:
    """
    IMPLY via Python boolean operators.

    >>> not_and_not(0, 0)
    1
    >>> not_and_not(0, 1)
    1
    >>> not_and_not(1, 0)
    0
    >>> not_and_not(1, 1)
    1
    """
    return int(not input_1 or bool(input_2))


# ---------------------------------------------------------------------------
# Variant 4 -- less-than-or-equal (a <= b for binary)
# ---------------------------------------------------------------------------

def le_check(input_1: int, input_2: int) -> int:
    """
    IMPLY via a <= b: for binary values, implication holds when a <= b.

    >>> le_check(0, 0)
    1
    >>> le_check(0, 1)
    1
    >>> le_check(1, 0)
    0
    >>> le_check(1, 1)
    1
    """
    return int(input_1 <= input_2)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (0, 0, 1),
    (0, 1, 1),
    (1, 0, 0),
    (1, 1, 1),
]

IMPLS = [
    ("reference",   reference),
    ("comparison",  comparison),
    ("bitwise_or",  bitwise_or),
    ("not_and_not", not_and_not),
    ("le_check",    le_check),
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
