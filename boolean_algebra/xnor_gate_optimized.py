#!/usr/bin/env python3
"""
Optimized and alternative implementations of XNOR Gate.

The reference uses `1 if input_1 == input_2 else 0` — direct equality check.
XNOR outputs 1 when both inputs are the same.

Variants covered:
1. equality      -- 1 if a == b else 0            (reference, explicit)
2. bitwise_xnor  -- (a ^ b) ^ 1                   (XOR then flip)
3. int_eq        -- int(a == b)                    (Pythonic one-liner)
4. not_xor       -- int(not (a ^ b))              (boolean NOT of XOR)

Key interview insight:
    XNOR is the complement of XOR and acts as an equality detector.
    In hardware, XNOR gates are used in comparators. A chain of XNOR gates
    across corresponding bits, fed into an AND gate, creates a multi-bit
    equality comparator. XNOR is also called the "equivalence gate".

Run:
    python boolean_algebra/xnor_gate_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from boolean_algebra.xnor_gate import xnor_gate as reference


# ---------------------------------------------------------------------------
# Variant 1 -- equality check (reference)
# ---------------------------------------------------------------------------

def equality(input_1: int, input_2: int) -> int:
    """
    XNOR via direct equality comparison.

    >>> equality(0, 0)
    1
    >>> equality(0, 1)
    0
    >>> equality(1, 0)
    0
    >>> equality(1, 1)
    1
    """
    return 1 if input_1 == input_2 else 0


# ---------------------------------------------------------------------------
# Variant 2 -- bitwise: XOR then flip
# ---------------------------------------------------------------------------

def bitwise_xnor(input_1: int, input_2: int) -> int:
    """
    XNOR via bitwise: (a ^ b) ^ 1 — XOR gives difference, flip gives equality.

    >>> bitwise_xnor(0, 0)
    1
    >>> bitwise_xnor(0, 1)
    0
    >>> bitwise_xnor(1, 0)
    0
    >>> bitwise_xnor(1, 1)
    1
    """
    return (input_1 ^ input_2) ^ 1


# ---------------------------------------------------------------------------
# Variant 3 -- int(a == b) one-liner
# ---------------------------------------------------------------------------

def int_eq(input_1: int, input_2: int) -> int:
    """
    XNOR via int() cast of equality.

    >>> int_eq(0, 0)
    1
    >>> int_eq(0, 1)
    0
    >>> int_eq(1, 0)
    0
    >>> int_eq(1, 1)
    1
    """
    return int(input_1 == input_2)


# ---------------------------------------------------------------------------
# Variant 4 -- boolean NOT of XOR
# ---------------------------------------------------------------------------

def not_xor(input_1: int, input_2: int) -> int:
    """
    XNOR via NOT(XOR): explicitly shows XNOR = complement of XOR.

    >>> not_xor(0, 0)
    1
    >>> not_xor(0, 1)
    0
    >>> not_xor(1, 0)
    0
    >>> not_xor(1, 1)
    1
    """
    return int(not (input_1 ^ input_2))


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (0, 0, 1),
    (0, 1, 0),
    (1, 0, 0),
    (1, 1, 1),
]

IMPLS = [
    ("reference",     reference),
    ("equality",      equality),
    ("bitwise_xnor",  bitwise_xnor),
    ("int_eq",        int_eq),
    ("not_xor",       not_xor),
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
