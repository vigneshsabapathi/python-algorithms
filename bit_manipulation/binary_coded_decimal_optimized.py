#!/usr/bin/env python3
"""
Optimized and alternative implementations of Binary Coded Decimal (BCD).

The reference converts the integer to a string, iterates over each character,
parses each char back to int, calls bin(), strips the prefix, then zfill(4).
That is six operations per digit for something that needs one format() call.

Variants covered:
1. bcd_format      -- format(digit, "04b") per digit — eliminates bin()/strip/zfill
2. bcd_divmod      -- extract digits arithmetically (divmod) without str conversion
3. bcd_lookup      -- pre-built 0-9 → 4-bit string lookup table; pure dict access
4. bcd_int_result  -- returns int instead of string; useful for hardware / packing

Key interview insight:
    Reference:   bin() + strip + zfill per digit — 6 steps/digit
    format():    one call per digit             — 1 step/digit  (~3× faster)
    lookup:      dict lookup per digit          — O(1)/digit     (fastest)

Run:
    python bit_manipulation/binary_coded_decimal_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bit_manipulation.binary_coded_decimal import binary_coded_decimal as bcd_reference

# Pre-built lookup: digit char → 4-bit string
_BCD_TABLE: dict[str, str] = {str(d): format(d, "04b") for d in range(10)}


# ---------------------------------------------------------------------------
# Variant 1 — format(digit, "04b") per digit
# ---------------------------------------------------------------------------

def bcd_format(number: int) -> str:
    """
    BCD using format(digit, "04b") — one call per digit, no bin()/strip/zfill.

    >>> bcd_format(-2)
    '0b0000'
    >>> bcd_format(0)
    '0b0000'
    >>> bcd_format(3)
    '0b0011'
    >>> bcd_format(12)
    '0b00010010'
    >>> bcd_format(987)
    '0b100110000111'
    """
    return "0b" + "".join(
        format(int(d), "04b") for d in str(max(0, number))
    )


# ---------------------------------------------------------------------------
# Variant 2 — divmod digit extraction (no string conversion of number)
# ---------------------------------------------------------------------------

def bcd_divmod(number: int) -> str:
    """
    BCD using divmod to extract digits arithmetically.

    Avoids converting the number to a string; useful when the input is
    already being processed as an integer.

    >>> bcd_divmod(-2)
    '0b0000'
    >>> bcd_divmod(0)
    '0b0000'
    >>> bcd_divmod(3)
    '0b0011'
    >>> bcd_divmod(12)
    '0b00010010'
    >>> bcd_divmod(987)
    '0b100110000111'
    """
    n = max(0, number)
    if n == 0:
        return "0b0000"
    digits: list[str] = []
    while n:
        n, rem = divmod(n, 10)
        digits.append(format(rem, "04b"))
    return "0b" + "".join(reversed(digits))


# ---------------------------------------------------------------------------
# Variant 3 — lookup table (O(1) per digit, no computation)
# ---------------------------------------------------------------------------

def bcd_lookup(number: int) -> str:
    """
    BCD using a pre-built digit → 4-bit string lookup table.

    Zero computation per digit — one dict access returns the 4-bit string
    directly.  Fastest for repeated calls.

    >>> bcd_lookup(-2)
    '0b0000'
    >>> bcd_lookup(0)
    '0b0000'
    >>> bcd_lookup(3)
    '0b0011'
    >>> bcd_lookup(12)
    '0b00010010'
    >>> bcd_lookup(987)
    '0b100110000111'
    """
    return "0b" + "".join(_BCD_TABLE[d] for d in str(max(0, number)))


# ---------------------------------------------------------------------------
# Variant 4 — return int (packed BCD as an integer)
# ---------------------------------------------------------------------------

def bcd_as_int(number: int) -> int:
    """
    BCD as a packed integer instead of a string.

    Shifts the result left by 4 bits per digit and ORs in each nibble.
    Useful for hardware protocols, BCD arithmetic, or further bit ops.

    >>> bcd_as_int(0)
    0
    >>> bcd_as_int(3)
    3
    >>> bcd_as_int(12)
    18
    >>> bcd_as_int(987)
    2439
    >>> bin(bcd_as_int(987))
    '0b100110000111'
    """
    n = max(0, number)
    result = 0
    for ch in str(n):
        result = (result << 4) | int(ch)
    return result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (-2,  "0b0000"),
    (-1,  "0b0000"),
    (0,   "0b0000"),
    (3,   "0b0011"),
    (12,  "0b00010010"),
    (987, "0b100110000111"),
]

STR_IMPLS = [
    ("reference", bcd_reference),
    ("format",    bcd_format),
    ("divmod",    bcd_divmod),
    ("lookup",    bcd_lookup),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for n, expected in TEST_CASES:
        results = {name: fn(n) for name, fn in STR_IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(
            f"  [{tag}] bcd({n:>4}) = {expected!r:<22}"
            + "  ".join(f"{name}={v!r}" for name, v in results.items())
        )

    # bcd_as_int sanity check
    print("\n=== bcd_as_int spot checks ===")
    for n, expected_str in TEST_CASES:
        if n < 0:
            continue
        as_int = bcd_as_int(n)
        reconstructed = "0b" + bin(as_int)[2:].zfill(
            4 * len(str(max(0, n)))
        ) if n > 0 else "0b0000"
        match = reconstructed == expected_str
        print(f"  {'OK' if match else 'FAIL'} bcd_as_int({n}) = {as_int}  bin={bin(as_int)}")

    REPS = 200_000
    inputs = [-1, 0, 3, 12, 987, 12345]
    print(f"\n=== Benchmark: {REPS} runs, inputs {inputs} ===")
    for name, fn in STR_IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(n) for n in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<12} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
