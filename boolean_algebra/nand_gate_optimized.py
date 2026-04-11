#!/usr/bin/env python3
"""
Optimized and alternative implementations of NAND Gate.

The reference uses `int(not (input_1 and input_2))` — Python's boolean NOT
applied to the short-circuit AND result.

Variants covered:
1. boolean_not     -- int(not (a and b))         (reference, Pythonic)
2. bitwise_nand    -- (a & b) ^ 1                (XOR with 1 = NOT for single bit)
3. demorgan        -- int(not a or not b)        (De Morgan's law)
4. zero_check      -- int(a + b < 2)             (sum < 2 means not both 1)

Key interview insight:
    NAND is a universal gate: any boolean function can be built using only NAND
    gates. NOT(a) = NAND(a,a). AND(a,b) = NAND(NAND(a,b), NAND(a,b)).
    OR(a,b) = NAND(NAND(a,a), NAND(b,b)). This is why NAND flash memory
    and NAND-based logic design are fundamental in hardware engineering.

Run:
    python boolean_algebra/nand_gate_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from boolean_algebra.nand_gate import nand_gate as reference


# ---------------------------------------------------------------------------
# Variant 1 -- boolean NOT AND (reference)
# ---------------------------------------------------------------------------

def boolean_not(input_1: int, input_2: int) -> int:
    """
    NAND via Python boolean operators.

    >>> boolean_not(0, 0)
    1
    >>> boolean_not(0, 1)
    1
    >>> boolean_not(1, 0)
    1
    >>> boolean_not(1, 1)
    0
    """
    return int(not (input_1 and input_2))


# ---------------------------------------------------------------------------
# Variant 2 -- bitwise: AND then XOR-flip
# ---------------------------------------------------------------------------

def bitwise_nand(input_1: int, input_2: int) -> int:
    """
    NAND via bitwise: (a & b) ^ 1 flips the AND result.

    >>> bitwise_nand(0, 0)
    1
    >>> bitwise_nand(0, 1)
    1
    >>> bitwise_nand(1, 0)
    1
    >>> bitwise_nand(1, 1)
    0
    """
    return (input_1 & input_2) ^ 1


# ---------------------------------------------------------------------------
# Variant 3 -- De Morgan's law: NOT a OR NOT b
# ---------------------------------------------------------------------------

def demorgan(input_1: int, input_2: int) -> int:
    """
    NAND via De Morgan's: NOT(A AND B) = (NOT A) OR (NOT B).

    >>> demorgan(0, 0)
    1
    >>> demorgan(0, 1)
    1
    >>> demorgan(1, 0)
    1
    >>> demorgan(1, 1)
    0
    """
    return int(not input_1 or not input_2)


# ---------------------------------------------------------------------------
# Variant 4 -- sum check (a + b < 2 means not both 1)
# ---------------------------------------------------------------------------

def zero_check(input_1: int, input_2: int) -> int:
    """
    NAND via arithmetic: sum < 2 iff not both inputs are 1.

    >>> zero_check(0, 0)
    1
    >>> zero_check(0, 1)
    1
    >>> zero_check(1, 0)
    1
    >>> zero_check(1, 1)
    0
    """
    return int(input_1 + input_2 < 2)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (0, 0, 1),
    (0, 1, 1),
    (1, 0, 1),
    (1, 1, 0),
]

IMPLS = [
    ("reference",     reference),
    ("boolean_not",   boolean_not),
    ("bitwise_nand",  bitwise_nand),
    ("demorgan",      demorgan),
    ("zero_check",    zero_check),
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
