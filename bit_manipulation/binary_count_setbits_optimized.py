#!/usr/bin/env python3
"""
Optimized and alternative implementations of counting set bits (popcount).

"Count the number of 1-bits in an integer" is one of the most fundamental
bit-manipulation problems and appears directly on LeetCode (191) and CTCI.

Variants covered:
1. count_bin_str      -- bin(n).count("1")  — reference; readable, O(log n)
2. count_bit_count    -- n.bit_count()       — Python 3.10+ built-in, O(1) hw
3. count_kernighan    -- Brian Kernighan's n &= n-1 trick; O(k) k=set bits
4. count_lookup8      -- 8-bit lookup table; O(n/8) table lookups
5. count_parallel     -- parallel bit summation (SWAR/Hamming weight); O(1)

Key interview insight:
    bin().count("1"):  O(log n) string alloc + scan
    n.bit_count():     O(1) — single POPCNT instruction (Python 3.10+)
    Kernighan:         O(k) — only loops k times (k = set bits); elegant trick
    Lookup:            O(n/8) — classic embedded-systems approach
    Parallel:          O(1) — constant steps regardless of bit width

Run:
    python bit_manipulation/binary_count_setbits_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bit_manipulation.binary_count_setbits import binary_count_setbits as count_reference

# ---------------------------------------------------------------------------
# Variant 1 — Python 3.10+ built-in int.bit_count()
# ---------------------------------------------------------------------------

def count_bit_count(n: int) -> int:
    """
    Count set bits using Python 3.10+ int.bit_count() built-in.

    Maps directly to the hardware POPCNT instruction on x86/ARM.
    Fastest possible — O(1) regardless of integer size.

    >>> count_bit_count(25)
    3
    >>> count_bit_count(36)
    2
    >>> count_bit_count(16)
    1
    >>> count_bit_count(58)
    4
    >>> count_bit_count(4294967295)
    32
    >>> count_bit_count(0)
    0
    """
    return n.bit_count()


# ---------------------------------------------------------------------------
# Variant 2 — Brian Kernighan's algorithm: n &= n - 1
# ---------------------------------------------------------------------------

def count_kernighan(n: int) -> int:
    """
    Count set bits using Brian Kernighan's bit trick.

    n & (n-1) clears the lowest set bit of n.  Repeat until n == 0.
    Loop runs exactly k times where k = number of set bits.
    For sparse integers (few set bits) this is faster than scanning all bits.

    >>> count_kernighan(25)
    3
    >>> count_kernighan(36)
    2
    >>> count_kernighan(16)
    1
    >>> count_kernighan(58)
    4
    >>> count_kernighan(4294967295)
    32
    >>> count_kernighan(0)
    0
    """
    count = 0
    while n:
        n &= n - 1   # clear lowest set bit
        count += 1
    return count


# ---------------------------------------------------------------------------
# Variant 3 — 8-bit lookup table
# ---------------------------------------------------------------------------

# Pre-compute popcount for all 256 possible byte values
_LOOKUP8: list[int] = [bin(i).count("1") for i in range(256)]


def count_lookup8(n: int) -> int:
    """
    Count set bits using a 256-entry byte lookup table.

    Processes the integer one byte (8 bits) at a time.
    Classic embedded-systems approach: O(log_256 n) = O(n_bytes) lookups.

    >>> count_lookup8(25)
    3
    >>> count_lookup8(36)
    2
    >>> count_lookup8(16)
    1
    >>> count_lookup8(58)
    4
    >>> count_lookup8(4294967295)
    32
    >>> count_lookup8(0)
    0
    """
    count = 0
    while n:
        count += _LOOKUP8[n & 0xFF]
        n >>= 8
    return count


# ---------------------------------------------------------------------------
# Variant 4 — Parallel bit summation (SWAR / Hamming weight)
# ---------------------------------------------------------------------------

def count_parallel(n: int) -> int:
    """
    Count set bits using parallel bit summation (SWAR technique).

    Works on 32-bit integers. Groups bits into pairs, then nibbles,
    then bytes, then half-words — summing each group in O(1) steps
    using only bit operations.

    This is what hardware POPCNT implements internally.

    >>> count_parallel(25)
    3
    >>> count_parallel(36)
    2
    >>> count_parallel(16)
    1
    >>> count_parallel(58)
    4
    >>> count_parallel(4294967295)
    32
    >>> count_parallel(0)
    0
    """
    n = n & 0xFFFFFFFF                 # clamp to 32 bits
    n = n - ((n >> 1) & 0x55555555)   # count bits in pairs
    n = (n & 0x33333333) + ((n >> 2) & 0x33333333)   # pairs → nibbles
    n = (n + (n >> 4)) & 0x0F0F0F0F   # nibbles → bytes
    return ((n * 0x01010101) & 0xFFFFFFFF) >> 24      # bytes → total


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (25,         3),
    (36,         2),
    (16,         1),
    (58,         4),
    (4294967295, 32),
    (0,          0),
    (0b10110110, 5),
]

IMPLS = [
    ("reference",   count_reference),
    ("bit_count()", count_bit_count),
    ("kernighan",   count_kernighan),
    ("lookup8",     count_lookup8),
    ("parallel",    count_parallel),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for n, expected in TEST_CASES:
        results = {name: fn(n) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(
            f"  [{tag}] popcount({n:<12}) = {expected}  "
            + "  ".join(f"{name}={v}" for name, v in results.items())
        )

    REPS = 500_000
    inputs = [25, 36, 58, 4294967295, 0, 0b10110110101010]
    print(f"\n=== Benchmark: {REPS} runs, inputs {inputs} ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(n) for n in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<14} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
