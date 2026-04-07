#!/usr/bin/env python3
"""
Optimized and alternative implementations of binary shifts.

The reference reinvents shift operations via string manipulation:
- Left shift  → append zeros to the binary string
- Right shift → slice characters off the right of the binary string
- Arithmetic right shift → manually builds 2's complement, then slices

Python's <<, >>, and >>> (logical right via masking) do all of this in one
CPU instruction.  The only work needed is formatting the result string.

Three shift types:
  Logical left  (<<):  shift left, fill with 0s.  Equivalent to × 2^k.
  Logical right (>>>): shift right, fill with 0s from left (Java/C unsigned).
                       Python has no >>> operator; simulate with masking.
  Arithmetic right (>>): shift right, fill with SIGN BIT from left.
                          Python's >> is always arithmetic.

Variants covered (one per shift type):
1. lls_native   -- logical_left_shift  via native <<, format() for output
2. lrs_native   -- logical_right_shift via native >> for non-negatives
3. ars_native   -- arithmetic_right_shift via native >>, 2's-complement mask

Key interview insight:
    Reference:  string append / slice — O(n) string work
    Native ops: O(1) CPU instruction  + O(n) format only

Run:
    python bit_manipulation/binary_shifts_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bit_manipulation.binary_shifts import (
    logical_left_shift   as lls_reference,
    logical_right_shift  as lrs_reference,
    arithmetic_right_shift as ars_reference,
)


# ---------------------------------------------------------------------------
# Helper: output width used by the reference implementations
# ---------------------------------------------------------------------------

def _lls_width(number: int, shift_amount: int) -> int:
    """Width of the reference lls output = original bits + shift_amount."""
    return len(bin(number)[2:]) + shift_amount   # e.g. bin(1)='0b1' → 1 + shift


def _ars_width(number: int) -> int:
    """Width used by the reference ars: original significant bits + 1 sign bit."""
    return len(bin(abs(number))[2:]) + 1


# ---------------------------------------------------------------------------
# Variant 1 — Logical left shift via native <<
# ---------------------------------------------------------------------------

def lls_native(number: int, shift_amount: int) -> str:
    """
    Logical left shift using Python's << operator.

    Appends shift_amount zeros to the binary representation.
    Equivalent to number * 2**shift_amount.

    >>> lls_native(0, 1)
    '0b00'
    >>> lls_native(1, 1)
    '0b10'
    >>> lls_native(1, 5)
    '0b100000'
    >>> lls_native(17, 2)
    '0b1000100'
    >>> lls_native(1983, 4)
    '0b111101111110000'
    >>> lls_native(1, -1)
    Traceback (most recent call last):
        ...
    ValueError: both inputs must be positive integers
    """
    if number < 0 or shift_amount < 0:
        raise ValueError("both inputs must be positive integers")
    width = _lls_width(number, shift_amount)
    return "0b" + format(number << shift_amount, f"0{width}b")


# ---------------------------------------------------------------------------
# Variant 2 — Logical right shift via native >>
# ---------------------------------------------------------------------------

def lrs_native(number: int, shift_amount: int) -> str:
    """
    Logical right shift using Python's >> operator.

    For non-negative integers Python's >> is already logical (fills with 0s).
    Returns '0b0' when all bits are shifted out.

    >>> lrs_native(0, 1)
    '0b0'
    >>> lrs_native(1, 1)
    '0b0'
    >>> lrs_native(1, 5)
    '0b0'
    >>> lrs_native(17, 2)
    '0b100'
    >>> lrs_native(1983, 4)
    '0b1111011'
    >>> lrs_native(1, -1)
    Traceback (most recent call last):
        ...
    ValueError: both inputs must be positive integers
    """
    if number < 0 or shift_amount < 0:
        raise ValueError("both inputs must be positive integers")
    result = number >> shift_amount
    return bin(result) if result else "0b0"


# ---------------------------------------------------------------------------
# Variant 3 — Arithmetic right shift via native >>
# ---------------------------------------------------------------------------

def ars_native(number: int, shift_amount: int) -> str:
    """
    Arithmetic right shift using Python's >> operator.

    Python's >> is always arithmetic (sign-extending).  Negative results are
    formatted using the 2's-complement mask trick: n & ((1 << width) - 1)
    extracts exactly 'width' bits in two's-complement representation.

    >>> ars_native(0, 1)
    '0b00'
    >>> ars_native(1, 1)
    '0b00'
    >>> ars_native(-1, 1)
    '0b11'
    >>> ars_native(17, 2)
    '0b000100'
    >>> ars_native(-17, 2)
    '0b111011'
    >>> ars_native(-1983, 4)
    '0b111110000100'
    """
    width = _ars_width(number)
    result = number >> shift_amount

    if shift_amount >= width:
        # All bits shifted — fill with sign bit
        sign_bit = "1" if number < 0 else "0"
        return "0b" + sign_bit * width

    # Use 2's complement mask to get correct bit pattern for negative results
    mask = (1 << width) - 1
    return "0b" + format(result & mask, f"0{width}b")


# ---------------------------------------------------------------------------
# Bonus — Python logical right shift for any integer (>>> simulation)
# ---------------------------------------------------------------------------

def logical_right_shift_any(number: int, shift_amount: int, bit_width: int = 32) -> int:
    """
    Simulate Java/C unsigned right shift (>>>) on a fixed-width integer.

    Python integers are arbitrary precision; >>> doesn't exist.
    Mask to bit_width bits first, then >> fills with 0s (no sign extension).

    >>> logical_right_shift_any(-1, 1, 8)
    127
    >>> logical_right_shift_any(-1, 1, 32)
    2147483647
    >>> logical_right_shift_any(16, 2, 8)
    4
    """
    mask = (1 << bit_width) - 1
    return (number & mask) >> shift_amount


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

LLS_CASES = [
    (0,    1, "0b00"),
    (1,    1, "0b10"),
    (1,    5, "0b100000"),
    (17,   2, "0b1000100"),
    (1983, 4, "0b111101111110000"),
]

LRS_CASES = [
    (0,    1, "0b0"),
    (1,    1, "0b0"),
    (1,    5, "0b0"),
    (17,   2, "0b100"),
    (1983, 4, "0b1111011"),
]

ARS_CASES = [
    (0,     1, "0b00"),
    (1,     1, "0b00"),
    (-1,    1, "0b11"),
    (17,    2, "0b000100"),
    (-17,   2, "0b111011"),
    (-1983, 4, "0b111110000100"),
]


def run_all() -> None:
    print("\n=== Correctness: Logical Left Shift ===")
    for n, k, expected in LLS_CASES:
        ref = lls_reference(n, k)
        opt = lls_native(n, k)
        ok = ref == opt == expected
        print(f"  [{'OK' if ok else 'FAIL'}] lls({n:>4}, {k}) = {opt!r:<22}  ref={ref!r}")

    print("\n=== Correctness: Logical Right Shift ===")
    for n, k, expected in LRS_CASES:
        ref = lrs_reference(n, k)
        opt = lrs_native(n, k)
        ok = ref == opt == expected
        print(f"  [{'OK' if ok else 'FAIL'}] lrs({n:>4}, {k}) = {opt!r:<15}  ref={ref!r}")

    print("\n=== Correctness: Arithmetic Right Shift ===")
    for n, k, expected in ARS_CASES:
        ref = ars_reference(n, k)
        opt = ars_native(n, k)
        ok = ref == opt == expected
        print(f"  [{'OK' if ok else 'FAIL'}] ars({n:>6}, {k}) = {opt!r:<20}  ref={ref!r}")

    print("\n=== Bonus: logical_right_shift_any (>>> simulation) ===")
    for n, k, bw, expected in [(-1, 1, 8, 127), (-1, 1, 32, 2147483647), (16, 2, 8, 4)]:
        r = logical_right_shift_any(n, k, bw)
        print(f"  [{'OK' if r == expected else 'FAIL'}] >>>({n}, {k}, {bw} bits) = {r}  (expected {expected})")

    REPS = 300_000
    print(f"\n=== Benchmark: Logical Left Shift ({REPS} runs) ===")
    inputs = [(1, 1), (17, 2), (1983, 4)]
    for name, fn in [("reference", lls_reference), ("native <<", lls_native)]:
        t = timeit.timeit(lambda fn=fn: [fn(n, k) for n, k in inputs], number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>7.4f} ms / batch of {len(inputs)}")

    print(f"\n=== Benchmark: Logical Right Shift ({REPS} runs) ===")
    for name, fn in [("reference", lrs_reference), ("native >>", lrs_native)]:
        t = timeit.timeit(lambda fn=fn: [fn(n, k) for n, k in inputs], number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>7.4f} ms / batch of {len(inputs)}")

    print(f"\n=== Benchmark: Arithmetic Right Shift ({REPS} runs) ===")
    ars_inputs = [(17, 2), (-17, 2), (-1983, 4)]
    for name, fn in [("reference", ars_reference), ("native >>", ars_native)]:
        t = timeit.timeit(lambda fn=fn: [fn(n, k) for n, k in ars_inputs], number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>7.4f} ms / batch of {len(ars_inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
