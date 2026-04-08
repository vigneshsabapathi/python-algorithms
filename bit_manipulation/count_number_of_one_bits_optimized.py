#!/usr/bin/env python3
"""
Comparison of popcount methods — extending count_number_of_one_bits.py.

Original file has two approaches:
  1. Brian Kernighan  (n &= n-1, loop k times)
  2. Modulo operator  (n % 2 check, loop log2(n) times)

This file adds:
  3. n.bit_count()    Python 3.10+ — maps to hardware POPCNT   [fastest]
  4. bin(n).count("1") — readable one-liner
  5. Right-shift      (n >>= 1, check LSB with & 1)
  6. Lookup8          8-bit byte lookup table
  7. SWAR parallel    Hamming-weight popcount (divide-and-conquer)

See: https://graphics.stanford.edu/~seander/bithacks.html#CountBitsSet64

Run: python bit_manipulation/count_number_of_one_bits_optimized.py
"""

from __future__ import annotations
import timeit

# Pre-computed 8-bit lookup: index → number of 1-bits in that byte
_LOOKUP8: list[int] = [bin(i).count("1") for i in range(256)]


# ---------------------------------------------------------------------------
# Core implementations
# ---------------------------------------------------------------------------


def popcount_brian_kernighan(n: int) -> int:
    """
    Brian Kernighan: n &= n-1 clears the lowest set bit each iteration.
    Loop runs exactly k times where k = number of set bits. O(k).

    >>> popcount_brian_kernighan(25)
    3
    >>> popcount_brian_kernighan(0)
    0
    >>> popcount_brian_kernighan(0xFFFFFFFF)
    32
    """
    if n < 0:
        raise ValueError("the value of input must not be negative")
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


def popcount_modulo(n: int) -> int:
    """
    Modulo operator: check each bit via n % 2, shift right.
    Loops log2(n) times regardless of set-bit count. O(log n).

    >>> popcount_modulo(25)
    3
    >>> popcount_modulo(0)
    0
    >>> popcount_modulo(0xFFFFFFFF)
    32
    """
    if n < 0:
        raise ValueError("the value of input must not be negative")
    count = 0
    while n:
        if n % 2 == 1:
            count += 1
        n >>= 1
    return count


def popcount_rshift(n: int) -> int:
    """
    Right-shift + AND: check LSB with n & 1, shift right.
    Same O(log n) as modulo but & 1 is faster than % 2.

    >>> popcount_rshift(25)
    3
    >>> popcount_rshift(0)
    0
    >>> popcount_rshift(0xFFFFFFFF)
    32
    """
    if n < 0:
        raise ValueError("the value of input must not be negative")
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count


def popcount_bin(n: int) -> int:
    """
    bin(n).count("1") — O(log n), one-liner, no loops in Python.

    >>> popcount_bin(25)
    3
    >>> popcount_bin(0)
    0
    >>> popcount_bin(0xFFFFFFFF)
    32
    """
    if n < 0:
        raise ValueError("the value of input must not be negative")
    return bin(n).count("1")


def popcount_bit_count(n: int) -> int:
    """
    Python 3.10+ built-in int.bit_count() — maps to POPCNT hardware instruction.
    Fastest available; O(1) at the hardware level.

    >>> popcount_bit_count(25)
    3
    >>> popcount_bit_count(0)
    0
    >>> popcount_bit_count(0xFFFFFFFF)
    32
    """
    if n < 0:
        raise ValueError("the value of input must not be negative")
    return n.bit_count()


def popcount_lookup8(n: int) -> int:
    """
    8-bit lookup table: one table access per byte, O(n/8) where n = bit width.
    Processes 8 bits at a time — much faster than per-bit loops for dense ints.

    >>> popcount_lookup8(25)
    3
    >>> popcount_lookup8(0)
    0
    >>> popcount_lookup8(0xFFFFFFFF)
    32
    """
    if n < 0:
        raise ValueError("the value of input must not be negative")
    count = 0
    while n:
        count += _LOOKUP8[n & 0xFF]
        n >>= 8
    return count


def popcount_swar(n: int) -> int:
    """
    SWAR (SIMD Within A Register) / divide-and-conquer popcount for 32-bit int.
    Computes all bit counts in parallel using integer arithmetic — O(log 32) = O(1).
    Classic Hamming-weight algorithm used in hardware POPCNT designs.

    Only correct for 32-bit non-negative integers (0 ≤ n ≤ 0xFFFFFFFF).

    >>> popcount_swar(25)
    3
    >>> popcount_swar(0)
    0
    >>> popcount_swar(0xFFFFFFFF)
    32
    """
    if n < 0:
        raise ValueError("the value of input must not be negative")
    n = n & 0xFFFFFFFF                     # clamp to 32 bits
    n = n - ((n >> 1) & 0x55555555)        # count pairs
    n = (n & 0x33333333) + ((n >> 2) & 0x33333333)   # count nibbles
    n = (n + (n >> 4)) & 0x0F0F0F0F        # count bytes
    return ((n * 0x01010101) & 0xFFFFFFFF) >> 24      # sum bytes via high byte


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

IMPLS = [
    ("brian_kernighan", popcount_brian_kernighan),
    ("modulo_%2",       popcount_modulo),
    ("rshift_&1",       popcount_rshift),
    ("bin.count",       popcount_bin),
    ("bit_count()",     popcount_bit_count),
    ("lookup8",         popcount_lookup8),
    ("swar_32bit",      popcount_swar),
]

TEST_CASES = [
    (25,         3),
    (37,         3),
    (21,         3),
    (58,         4),
    (0,          0),
    (256,        1),
    (0xFFFFFFFF, 32),
]

# Sparse = few set bits (Kernighan's sweet spot)
_SPARSE = [1, 4, 16, 64, 256]
# Dense  = many set bits (lookup/bit_count shine)
_DENSE  = [0b10110111, 0b11111111, 0xFFFFFFFF, 0b10101010, 0b11001100]


def run_all() -> None:
    print("\n=== Correctness ===")
    for n, expected in TEST_CASES:
        row = {name: fn(n) for name, fn in IMPLS}
        ok = all(v == expected for v in row.values())
        status = "OK" if ok else "FAIL"
        vals = "  ".join(f"{nm}={v}" for nm, v in row.items())
        print(f"  [{status}] popcount({n:<12}) = {expected}  {vals}")

    REPS = 500_000
    for label, inputs in [("sparse (1 set bit each)", _SPARSE),
                           ("dense  (many set bits)",  _DENSE)]:
        print(f"\n=== Benchmark: {label}, {REPS} runs ===")
        for name, fn in IMPLS:
            t = timeit.timeit(
                lambda fn=fn: [fn(x) for x in inputs], number=REPS
            ) * 1000 / REPS
            print(f"  {name:<18} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
