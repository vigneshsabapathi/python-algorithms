#!/usr/bin/env python3
"""
Optimized and alternative implementations of Excess-3 Code.

The reference converts the integer to a string, iterates over each character,
parses each char back to int, adds 3, calls bin(), strips the prefix, then
zfill(4). That is seven operations per digit.

Excess-3 is essentially BCD + 3 per digit. Each decimal digit d is encoded
as the 4-bit binary of (d + 3).

Variants covered:
1. excess3_format    -- format(digit + 3, "04b") per digit
2. excess3_divmod    -- extract digits arithmetically (divmod), add 3, format
3. excess3_lookup    -- pre-built 0-9 → excess-3 4-bit string lookup table
4. excess3_int       -- returns packed int instead of string

Key interview insight:
    Excess-3 = BCD shifted by 3. It's self-complementing:
    9's complement of digit d = 9 - d. In excess-3:
        XS3(9 - d) = inv(XS3(d))  (bitwise NOT of each nibble)
    This property makes subtraction easy — just invert bits.

Run:
    python bit_manipulation/excess_3_code_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bit_manipulation.excess_3_code import excess_3_code as excess3_reference

# Pre-built lookup: digit char → excess-3 4-bit string
_XS3_TABLE: dict[str, str] = {str(d): format(d + 3, "04b") for d in range(10)}


# ---------------------------------------------------------------------------
# Variant 1 — format(digit + 3, "04b") per digit
# ---------------------------------------------------------------------------

def excess3_format(number: int) -> str:
    """
    Excess-3 using format(d + 3, "04b") — one call per digit.

    >>> excess3_format(-2)
    '0b0011'
    >>> excess3_format(0)
    '0b0011'
    >>> excess3_format(3)
    '0b0110'
    >>> excess3_format(2)
    '0b0101'
    >>> excess3_format(20)
    '0b01010011'
    >>> excess3_format(120)
    '0b010001010011'
    """
    return "0b" + "".join(
        format(int(d) + 3, "04b") for d in str(max(0, number))
    )


# ---------------------------------------------------------------------------
# Variant 2 — divmod digit extraction (no string conversion of number)
# ---------------------------------------------------------------------------

def excess3_divmod(number: int) -> str:
    """
    Excess-3 using divmod to extract digits arithmetically, then add 3.

    >>> excess3_divmod(-2)
    '0b0011'
    >>> excess3_divmod(0)
    '0b0011'
    >>> excess3_divmod(3)
    '0b0110'
    >>> excess3_divmod(2)
    '0b0101'
    >>> excess3_divmod(20)
    '0b01010011'
    >>> excess3_divmod(120)
    '0b010001010011'
    """
    n = max(0, number)
    if n == 0:
        return "0b0011"
    digits: list[str] = []
    while n:
        n, rem = divmod(n, 10)
        digits.append(format(rem + 3, "04b"))
    return "0b" + "".join(reversed(digits))


# ---------------------------------------------------------------------------
# Variant 3 — lookup table (O(1) per digit, no computation)
# ---------------------------------------------------------------------------

def excess3_lookup(number: int) -> str:
    """
    Excess-3 using a pre-built digit → excess-3 4-bit string lookup table.

    Zero computation per digit — one dict access returns the 4-bit string.
    Fastest for repeated calls.

    >>> excess3_lookup(-2)
    '0b0011'
    >>> excess3_lookup(0)
    '0b0011'
    >>> excess3_lookup(3)
    '0b0110'
    >>> excess3_lookup(2)
    '0b0101'
    >>> excess3_lookup(20)
    '0b01010011'
    >>> excess3_lookup(120)
    '0b010001010011'
    """
    return "0b" + "".join(_XS3_TABLE[d] for d in str(max(0, number)))


# ---------------------------------------------------------------------------
# Variant 4 — return int (packed excess-3 as an integer)
# ---------------------------------------------------------------------------

def excess3_as_int(number: int) -> int:
    """
    Excess-3 as a packed integer instead of a string.

    Shifts the result left by 4 bits per digit and ORs in (digit + 3).
    Useful for hardware protocols or further bitwise operations.

    >>> excess3_as_int(0)
    3
    >>> excess3_as_int(3)
    6
    >>> excess3_as_int(2)
    5
    >>> excess3_as_int(20)
    83
    >>> bin(excess3_as_int(20))
    '0b1010011'
    >>> excess3_as_int(120)
    1107
    >>> bin(excess3_as_int(120))
    '0b10001010011'
    """
    n = max(0, number)
    result = 0
    for ch in str(n):
        result = (result << 4) | (int(ch) + 3)
    return result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (-2,  "0b0011"),
    (-1,  "0b0011"),
    (0,   "0b0011"),
    (2,   "0b0101"),
    (3,   "0b0110"),
    (20,  "0b01010011"),
    (120, "0b010001010011"),
]

STR_IMPLS = [
    ("reference", excess3_reference),
    ("format",    excess3_format),
    ("divmod",    excess3_divmod),
    ("lookup",    excess3_lookup),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for n, expected in TEST_CASES:
        results = {name: fn(n) for name, fn in STR_IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(
            f"  [{tag}] xs3({n:>4}) = {expected!r:<22}"
            + "  ".join(f"{name}={v!r}" for name, v in results.items())
        )

    # excess3_as_int sanity check
    print("\n=== excess3_as_int spot checks ===")
    for n, expected_str in TEST_CASES:
        if n < 0:
            continue
        as_int = excess3_as_int(n)
        reconstructed = "0b" + bin(as_int)[2:].zfill(
            4 * len(str(max(0, n)))
        )
        match = reconstructed == expected_str
        print(f"  {'OK' if match else 'FAIL'} excess3_as_int({n}) = {as_int}  bin={bin(as_int)}")

    REPS = 200_000
    inputs = [-1, 0, 2, 3, 20, 120]
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
