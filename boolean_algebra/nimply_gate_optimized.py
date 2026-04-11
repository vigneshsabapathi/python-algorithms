#!/usr/bin/env python3
"""
Optimized and alternative implementations of NIMPLY Gate.

The reference uses `int(input_1 == 1 and input_2 == 0)` — NIMPLY is true
only when the first input is 1 and the second is 0. It is the negation of
material implication (NOT IMPLY).

Variants covered:
1. comparison    -- int(a == 1 and b == 0)        (reference, explicit)
2. bitwise       -- a & (~b & 1)                  (A AND NOT B, branchless)
3. subtraction   -- max(a - b, 0)                 (1-0=1, else 0)
4. gt_check      -- int(a > b)                    (for binary: a>b iff NIMPLY)

Key interview insight:
    NIMPLY = A AND (NOT B). It is the complement of IMPLY. Together with
    the constant 0, NIMPLY is functionally complete (can express all boolean
    functions). NIMPLY(A,A) = 0, which provides the constant false,
    and combining NIMPLY operations can build NOT, AND, OR.

Run:
    python boolean_algebra/nimply_gate_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from boolean_algebra.nimply_gate import nimply_gate as reference


# ---------------------------------------------------------------------------
# Variant 1 -- comparison (reference)
# ---------------------------------------------------------------------------

def comparison(input_1: int, input_2: int) -> int:
    """
    NIMPLY via explicit comparison.

    >>> comparison(0, 0)
    0
    >>> comparison(0, 1)
    0
    >>> comparison(1, 0)
    1
    >>> comparison(1, 1)
    0
    """
    return int(input_1 == 1 and input_2 == 0)


# ---------------------------------------------------------------------------
# Variant 2 -- bitwise: A AND NOT B
# ---------------------------------------------------------------------------

def bitwise(input_1: int, input_2: int) -> int:
    """
    NIMPLY via bitwise: a & (~b & 1).

    >>> bitwise(0, 0)
    0
    >>> bitwise(0, 1)
    0
    >>> bitwise(1, 0)
    1
    >>> bitwise(1, 1)
    0
    """
    return input_1 & (~input_2 & 1)


# ---------------------------------------------------------------------------
# Variant 3 -- subtraction with clamp
# ---------------------------------------------------------------------------

def subtraction(input_1: int, input_2: int) -> int:
    """
    NIMPLY via max(a - b, 0): only 1-0 yields positive.

    >>> subtraction(0, 0)
    0
    >>> subtraction(0, 1)
    0
    >>> subtraction(1, 0)
    1
    >>> subtraction(1, 1)
    0
    """
    return max(input_1 - input_2, 0)


# ---------------------------------------------------------------------------
# Variant 4 -- greater-than check
# ---------------------------------------------------------------------------

def gt_check(input_1: int, input_2: int) -> int:
    """
    NIMPLY via a > b: for binary, true only when a=1 and b=0.

    >>> gt_check(0, 0)
    0
    >>> gt_check(0, 1)
    0
    >>> gt_check(1, 0)
    1
    >>> gt_check(1, 1)
    0
    """
    return int(input_1 > input_2)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (0, 0, 0),
    (0, 1, 0),
    (1, 0, 1),
    (1, 1, 0),
]

IMPLS = [
    ("reference",    reference),
    ("comparison",   comparison),
    ("bitwise",      bitwise),
    ("subtraction",  subtraction),
    ("gt_check",     gt_check),
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
