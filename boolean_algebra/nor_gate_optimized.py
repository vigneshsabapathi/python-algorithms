#!/usr/bin/env python3
"""
Optimized and alternative implementations of NOR Gate.

The reference uses `int(input_1 == input_2 == 0)` — Python's chained
comparison checks both inputs are zero simultaneously.

Variants covered:
1. chained_eq    -- int(a == b == 0)              (reference, Pythonic)
2. bitwise_nor   -- (a | b) ^ 1                   (OR then flip, branchless)
3. demorgan      -- int(not a and not b)           (De Morgan's: NOT(A OR B))
4. sum_check     -- int(a + b == 0)                (sum is 0 iff both are 0)

Key interview insight:
    NOR is the other universal gate (alongside NAND): any boolean function
    can be built using only NOR gates. NOT(a) = NOR(a,a).
    OR(a,b) = NOR(NOR(a,b), NOR(a,b)). AND(a,b) = NOR(NOR(a,a), NOR(b,b)).
    NOR-only logic was used in the Apollo Guidance Computer.

Run:
    python boolean_algebra/nor_gate_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from boolean_algebra.nor_gate import nor_gate as reference


# ---------------------------------------------------------------------------
# Variant 1 -- chained equality (reference)
# ---------------------------------------------------------------------------

def chained_eq(input_1: int, input_2: int) -> int:
    """
    NOR via chained comparison.

    >>> chained_eq(0, 0)
    1
    >>> chained_eq(0, 1)
    0
    >>> chained_eq(1, 0)
    0
    >>> chained_eq(1, 1)
    0
    """
    return int(input_1 == input_2 == 0)


# ---------------------------------------------------------------------------
# Variant 2 -- bitwise: OR then XOR-flip
# ---------------------------------------------------------------------------

def bitwise_nor(input_1: int, input_2: int) -> int:
    """
    NOR via bitwise: (a | b) ^ 1 flips the OR result.

    >>> bitwise_nor(0, 0)
    1
    >>> bitwise_nor(0, 1)
    0
    >>> bitwise_nor(1, 0)
    0
    >>> bitwise_nor(1, 1)
    0
    """
    return (input_1 | input_2) ^ 1


# ---------------------------------------------------------------------------
# Variant 3 -- De Morgan's: NOT A AND NOT B
# ---------------------------------------------------------------------------

def demorgan(input_1: int, input_2: int) -> int:
    """
    NOR via De Morgan's: NOT(A OR B) = (NOT A) AND (NOT B).

    >>> demorgan(0, 0)
    1
    >>> demorgan(0, 1)
    0
    >>> demorgan(1, 0)
    0
    >>> demorgan(1, 1)
    0
    """
    return int(not input_1 and not input_2)


# ---------------------------------------------------------------------------
# Variant 4 -- sum check
# ---------------------------------------------------------------------------

def sum_check(input_1: int, input_2: int) -> int:
    """
    NOR via arithmetic: sum == 0 iff both inputs are 0.

    >>> sum_check(0, 0)
    1
    >>> sum_check(0, 1)
    0
    >>> sum_check(1, 0)
    0
    >>> sum_check(1, 1)
    0
    """
    return int(input_1 + input_2 == 0)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (0, 0, 1),
    (0, 1, 0),
    (1, 0, 0),
    (1, 1, 0),
]

IMPLS = [
    ("reference",    reference),
    ("chained_eq",   chained_eq),
    ("bitwise_nor",  bitwise_nor),
    ("demorgan",     demorgan),
    ("sum_check",    sum_check),
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
