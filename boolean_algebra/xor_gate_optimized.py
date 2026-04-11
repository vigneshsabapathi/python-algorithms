#!/usr/bin/env python3
"""
Optimized and alternative implementations of XOR Gate.

The reference uses `(input_1, input_2).count(0) % 2` — counts zeros and
checks parity. XOR is 1 when the count of zeros is odd (i.e., inputs differ).

Variants covered:
1. count_parity  -- (a,b).count(0) % 2            (reference)
2. bitwise_xor   -- a ^ b                          (single CPU instruction)
3. not_equal     -- int(a != b)                    (Pythonic equality check)
4. arithmetic    -- (a + b) % 2                    (sum parity)

Key interview insight:
    XOR has unique properties: a ^ a = 0, a ^ 0 = a (identity), and it is
    associative + commutative. This makes it essential for: swap without temp
    (a^=b, b^=a, a^=b), finding the missing/duplicate number in an array,
    Gray code generation, and parity checking. XOR is the basis of half-adders
    in hardware arithmetic circuits.

Run:
    python boolean_algebra/xor_gate_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from boolean_algebra.xor_gate import xor_gate as reference


# ---------------------------------------------------------------------------
# Variant 1 -- count parity (reference)
# ---------------------------------------------------------------------------

def count_parity(input_1: int, input_2: int) -> int:
    """
    XOR via zero-count parity.

    >>> count_parity(0, 0)
    0
    >>> count_parity(0, 1)
    1
    >>> count_parity(1, 0)
    1
    >>> count_parity(1, 1)
    0
    """
    return (input_1, input_2).count(0) % 2


# ---------------------------------------------------------------------------
# Variant 2 -- bitwise XOR (single instruction)
# ---------------------------------------------------------------------------

def bitwise_xor(input_1: int, input_2: int) -> int:
    """
    XOR via bitwise ^ operator. Maps to single CPU instruction.

    >>> bitwise_xor(0, 0)
    0
    >>> bitwise_xor(0, 1)
    1
    >>> bitwise_xor(1, 0)
    1
    >>> bitwise_xor(1, 1)
    0
    """
    return input_1 ^ input_2


# ---------------------------------------------------------------------------
# Variant 3 -- not-equal check
# ---------------------------------------------------------------------------

def not_equal(input_1: int, input_2: int) -> int:
    """
    XOR via inequality: XOR is 1 exactly when inputs differ.

    >>> not_equal(0, 0)
    0
    >>> not_equal(0, 1)
    1
    >>> not_equal(1, 0)
    1
    >>> not_equal(1, 1)
    0
    """
    return int(input_1 != input_2)


# ---------------------------------------------------------------------------
# Variant 4 -- arithmetic (sum mod 2)
# ---------------------------------------------------------------------------

def arithmetic(input_1: int, input_2: int) -> int:
    """
    XOR via (a + b) % 2: sum parity equals XOR for binary inputs.

    >>> arithmetic(0, 0)
    0
    >>> arithmetic(0, 1)
    1
    >>> arithmetic(1, 0)
    1
    >>> arithmetic(1, 1)
    0
    """
    return (input_1 + input_2) % 2


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (0, 0, 0),
    (0, 1, 1),
    (1, 0, 1),
    (1, 1, 0),
]

IMPLS = [
    ("reference",     reference),
    ("count_parity",  count_parity),
    ("bitwise_xor",   bitwise_xor),
    ("not_equal",     not_equal),
    ("arithmetic",    arithmetic),
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
