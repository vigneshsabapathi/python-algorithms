#!/usr/bin/env python3
"""
Optimized and alternative implementations of NOT Gate.

The reference uses `1 if input_1 == 0 else 0` — a simple conditional that
flips a binary value.

Variants covered:
1. conditional   -- 1 if a == 0 else 0            (reference, explicit)
2. xor_flip      -- a ^ 1                         (XOR with 1 flips the bit)
3. subtraction   -- 1 - a                          (algebraic complement)
4. bitwise_not   -- (~a) & 1                       (bitwise NOT, masked to 1 bit)

Key interview insight:
    NOT is the simplest gate but crucial in De Morgan's laws:
    NOT(A AND B) = (NOT A) OR (NOT B) and NOT(A OR B) = (NOT A) AND (NOT B).
    In Python, `a ^ 1` is the idiomatic single-bit NOT because Python's `~`
    operator returns -(a+1) for integers (two's complement), so you must
    mask with `& 1` to get a single-bit result.

Run:
    python boolean_algebra/not_gate_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from boolean_algebra.not_gate import not_gate as reference


# ---------------------------------------------------------------------------
# Variant 1 -- conditional (reference)
# ---------------------------------------------------------------------------

def conditional(input_1: int) -> int:
    """
    NOT via conditional expression.

    >>> conditional(0)
    1
    >>> conditional(1)
    0
    """
    return 1 if input_1 == 0 else 0


# ---------------------------------------------------------------------------
# Variant 2 -- XOR flip (single-bit NOT)
# ---------------------------------------------------------------------------

def xor_flip(input_1: int) -> int:
    """
    NOT via XOR with 1: flips the least significant bit.

    >>> xor_flip(0)
    1
    >>> xor_flip(1)
    0
    """
    return input_1 ^ 1


# ---------------------------------------------------------------------------
# Variant 3 -- subtraction (algebraic complement)
# ---------------------------------------------------------------------------

def subtraction(input_1: int) -> int:
    """
    NOT via 1 - a: algebraic complement for binary values.

    >>> subtraction(0)
    1
    >>> subtraction(1)
    0
    """
    return 1 - input_1


# ---------------------------------------------------------------------------
# Variant 4 -- bitwise NOT masked to 1 bit
# ---------------------------------------------------------------------------

def bitwise_not(input_1: int) -> int:
    """
    NOT via Python's ~ operator masked to 1 bit.
    ~0 = -1 in Python (two's complement), so & 1 extracts the LSB.

    >>> bitwise_not(0)
    1
    >>> bitwise_not(1)
    0
    """
    return (~input_1) & 1


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (0, 1),
    (1, 0),
]

IMPLS = [
    ("reference",    reference),
    ("conditional",  conditional),
    ("xor_flip",     xor_flip),
    ("subtraction",  subtraction),
    ("bitwise_not",  bitwise_not),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for a, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(a)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(
            f"  [{tag}] ({a}) expected={expected}  "
            + "  ".join(f"{nm}={v}" for nm, v in results.items())
        )

    REPS = 500_000
    inputs = [0, 1]

    print(f"\n=== Benchmark: {REPS} runs, {len(inputs)} inputs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(a) for a in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
