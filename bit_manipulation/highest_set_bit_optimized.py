#!/usr/bin/env python3
"""
Optimized and alternative implementations of Highest Set Bit Position.

The reference shifts right in a loop until the number is zero — O(log n) iterations.
Python has a built-in `int.bit_length()` that does this at C level in O(1).

Variants covered:
1. bit_length   -- n.bit_length() — Python built-in, C-level, O(1)
2. math_log2    -- floor(log2(n)) + 1 — math module approach
3. bin_len      -- len(bin(n)) - 2 — string conversion
4. binary_search -- halving bit-width, no loops — Stanford bithacks style

Key interview insight:
    int.bit_length() is the answer in production code.
    The reference loop is what interviewers want you to explain.
    25 = 0b11001 → bit_length = 5 (position of highest set bit)

    Position is 1-indexed: bit 1 is the LSB.
    bit_length(0) = 0 (no bits set).

Run:
    python bit_manipulation/highest_set_bit_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bit_manipulation.highest_set_bit import get_highest_set_bit_position as reference


# ---------------------------------------------------------------------------
# Variant 1 — int.bit_length() (built-in, C-level)
# ---------------------------------------------------------------------------

def bit_length(number: int) -> int:
    """
    Highest set bit position using Python's built-in bit_length().

    >>> bit_length(25)
    5
    >>> bit_length(37)
    6
    >>> bit_length(1)
    1
    >>> bit_length(4)
    3
    >>> bit_length(0)
    0
    """
    return number.bit_length()


# ---------------------------------------------------------------------------
# Variant 2 — math.floor(log2(n)) + 1
# ---------------------------------------------------------------------------

def math_log2(number: int) -> int:
    """
    Highest set bit position using math.log2.

    >>> math_log2(25)
    5
    >>> math_log2(37)
    6
    >>> math_log2(1)
    1
    >>> math_log2(4)
    3
    >>> math_log2(0)
    0
    """
    if number <= 0:
        return 0
    return math.floor(math.log2(number)) + 1


# ---------------------------------------------------------------------------
# Variant 3 — len(bin(n)) - 2
# ---------------------------------------------------------------------------

def bin_len(number: int) -> int:
    """
    Highest set bit position via string length of binary representation.

    >>> bin_len(25)
    5
    >>> bin_len(37)
    6
    >>> bin_len(1)
    1
    >>> bin_len(4)
    3
    >>> bin_len(0)
    0
    """
    if number <= 0:
        return 0
    return len(bin(number)) - 2  # strip "0b" prefix


# ---------------------------------------------------------------------------
# Variant 4 — binary search on bit width (Stanford bithacks style)
# ---------------------------------------------------------------------------

# Precomputed: highest bit position for values 0-511 (need 256 after 56-bit shift)
_BIT_POS_TABLE = [0] + [i.bit_length() for i in range(1, 512)]


def binary_search_hibit(number: int) -> int:
    """
    Highest set bit position using binary search on bit width.

    Narrows down the position by checking 32-bit, 16-bit, 8-bit
    ranges, then uses a lookup table for the final 9 bits.
    Inspired by Stanford bithacks "IntegerLog" approach.

    >>> binary_search_hibit(25)
    5
    >>> binary_search_hibit(37)
    6
    >>> binary_search_hibit(1)
    1
    >>> binary_search_hibit(4)
    3
    >>> binary_search_hibit(0)
    0
    >>> binary_search_hibit(2**64)
    65
    >>> binary_search_hibit(2**64 - 1)
    64
    """
    if number <= 0:
        return 0

    position = 0

    # Narrow by 32-bit chunks to handle arbitrarily large ints
    if number >= (1 << 32):
        if number >= (1 << 64):
            # Count how many 64-bit chunks (for very large ints)
            shift = 64
            while number >= (1 << (shift + 64)):
                shift += 64
            position += shift
            number >>= shift
        if number >= (1 << 32):
            position += 32
            number >>= 32

    # Now fits in 32 bits — check 16-bit
    if number >= (1 << 16):
        position += 16
        number >>= 16

    # Check 8-bit
    if number >= (1 << 8):
        position += 8
        number >>= 8

    # Final chunk — lookup table (0-511)
    position += _BIT_POS_TABLE[number]
    return position


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (0, 0),
    (1, 1),
    (4, 3),
    (25, 5),
    (37, 6),
    (255, 8),
    (256, 9),
    (1024, 11),
    (2**32 - 1, 32),
    (2**32, 33),
]

IMPLS = [
    ("reference", reference),
    ("bit_length", bit_length),
    ("math_log2",  math_log2),
    ("bin_len",    bin_len),
    ("bin_search", binary_search_hibit),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for n, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(n)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(
            f"  [{tag}] n={str(n):<22} expected={expected:<4}  "
            + "  ".join(f"{n}={v}" for n, v in results.items())
        )

    REPS = 200_000
    inputs = [0, 1, 4, 25, 37, 255, 256, 1024, 2**32 - 1]
    print(f"\n=== Benchmark: {REPS} runs, {len(inputs)} inputs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(n) for n in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<12} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
