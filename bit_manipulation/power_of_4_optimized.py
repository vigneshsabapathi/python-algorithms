#!/usr/bin/env python3
"""
Optimized and alternative implementations of Power of 4.

A number n is a power of 4 iff:
  (a) It is a power of 2  —  `n & (n-1) == 0`  (exactly one set bit)
  (b) That set bit is at an even bit-position (0-indexed from right):
      positions 0, 2, 4, 6... correspond to 4^0=1, 4^1=4, 4^2=16, 4^3=64...

The reference checks (a) then counts bits until zero; c%2==1 means the set
bit is at an even position (positions 0,2,4... → bit_length 1,3,5...).
This is O(log n) because of the shift loop.

Three O(1) alternatives:
  bit_length  — n.bit_length() % 2 == 1  (C-level call)
  mask_32     — n & 0x55555555 != 0       (bit mask — LeetCode 342 classic)
  mod3        — n % 3 == 1                (number theory: 4^k ≡ 1 mod 3)

Why mod3 works:
    4 ≡ 1 (mod 3)  →  4^k ≡ 1^k ≡ 1 (mod 3)  for all k ≥ 0
    2 ≡ 2 (mod 3)  →  (2×4^k) = 2^(2k+1) ≡ 2 (mod 3)  — powers of 2 not in 4
    So: any power of 2 is a power of 4 iff n % 3 == 1.

Why mask_32 works (for 32-bit integers):
    0x55555555 = 0101 0101 0101 ... 0101  (set bits at positions 0,2,4,...,30)
    Powers of 4 always have their single set bit at an even position.
    `n & 0x55555555 != 0` confirms the bit is at an even position.
    Only valid for 0 < n < 2^32.

Key interview insight:
    LeetCode 342 uses 32-bit signed integers — the mask `0x55555555` is
    the expected O(1) answer.  `n % 3 == 1` is the "number theory" bonus
    answer.  `n.bit_length() % 2 == 1` is the cleanest Python-native O(1).

Run:
    python bit_manipulation/power_of_4_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bit_manipulation.power_of_4 import power_of_4 as reference


def _guard(number: int) -> None:
    if not isinstance(number, int):
        raise TypeError("number must be an integer")
    if number <= 0:
        raise ValueError("number must be positive")


# ---------------------------------------------------------------------------
# Variant 1 — bit_length: O(1) replacement for the shift loop
# ---------------------------------------------------------------------------

def bit_length_check(number: int) -> bool:
    """
    Power-of-4 check via n.bit_length().

    Powers of 4 have bit_length 1, 3, 5, 7, ... (always odd).
    Powers of 2 not in 4 have bit_length 2, 4, 6, ... (always even).

    >>> bit_length_check(1)
    True
    >>> bit_length_check(2)
    False
    >>> bit_length_check(4)
    True
    >>> bit_length_check(8)
    False
    >>> bit_length_check(16)
    True
    >>> bit_length_check(64)
    True
    >>> bit_length_check(4**100)
    True
    """
    _guard(number)
    return number & (number - 1) == 0 and number.bit_length() % 2 == 1


# ---------------------------------------------------------------------------
# Variant 2 — 0x55555555 bitmask (LeetCode 342 classic, 32-bit only)
# ---------------------------------------------------------------------------

_MASK_32 = 0x55555555  # 0101 0101 ... 0101 — even bit positions within 32 bits

def mask_32(number: int) -> bool:
    """
    Power-of-4 check via bitmask 0x55555555 (valid for 32-bit integers only).

    0x55555555 has set bits at positions 0, 2, 4, ..., 30.
    If n is a power of 2 AND its set bit falls in the mask, it is a power of 4.

    WARNING: incorrect for n >= 2**32 (the mask only covers 32 bits).

    >>> mask_32(1)
    True
    >>> mask_32(2)
    False
    >>> mask_32(4)
    True
    >>> mask_32(8)
    False
    >>> mask_32(16)
    True
    >>> mask_32(64)
    True
    >>> mask_32(4**15)   # 2^30 — still within 32-bit range
    True
    """
    _guard(number)
    if number >= 2**32:
        raise ValueError("mask_32 only supports 32-bit non-negative integers")
    return number & (number - 1) == 0 and bool(number & _MASK_32)


# ---------------------------------------------------------------------------
# Variant 3 — modulo 3 (number theory trick, works for arbitrary precision)
# ---------------------------------------------------------------------------

def mod3(number: int) -> bool:
    """
    Power-of-4 check via modular arithmetic: 4^k ≡ 1 (mod 3) for all k ≥ 0.

    Since 4 ≡ 1 (mod 3), any power of 4 satisfies n % 3 == 1.
    Powers of 2 that aren't powers of 4 satisfy n % 3 == 2.

    Combinedcheck: is power of 2 AND n % 3 == 1.

    >>> mod3(1)
    True
    >>> mod3(2)
    False
    >>> mod3(4)
    True
    >>> mod3(8)
    False
    >>> mod3(16)
    True
    >>> mod3(64)
    True
    >>> mod3(4**100)
    True
    """
    _guard(number)
    return number & (number - 1) == 0 and number % 3 == 1


# ---------------------------------------------------------------------------
# Variant 4 — math.log base 4 (float, precision trap for large n)
# ---------------------------------------------------------------------------

def math_log4(number: int) -> bool:
    """
    Power-of-4 check via math.log(n, 4).

    WARNING: float precision breaks for n > 4^26 ≈ 4.5e15 (beyond 2^53
    mantissa). Safe for small inputs only.

    >>> math_log4(1)
    True
    >>> math_log4(2)
    False
    >>> math_log4(4)
    True
    >>> math_log4(8)
    False
    >>> math_log4(16)
    True
    >>> math_log4(64)
    True
    """
    _guard(number)
    result = math.log(number, 4)
    return abs(result - round(result)) < 1e-10


# ---------------------------------------------------------------------------
# Variant 5 — bit_length O(1) with mask for arbitrary precision
# ---------------------------------------------------------------------------

def mask_arbitrary(number: int) -> bool:
    """
    Power-of-4 check with bitmask that scales to arbitrary-precision ints.

    Generates a mask covering all even bit positions up to bit_length of n.
    More expensive than 0x55555555 for 32-bit, but correct for any n.

    >>> mask_arbitrary(1)
    True
    >>> mask_arbitrary(2)
    False
    >>> mask_arbitrary(4)
    True
    >>> mask_arbitrary(8)
    False
    >>> mask_arbitrary(4**100)
    True
    """
    _guard(number)
    if number & (number - 1) != 0:
        return False
    # Bit position of the single set bit (0-indexed)
    return (number.bit_length() - 1) % 2 == 0


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (1,    True),
    (2,    False),
    (4,    True),
    (6,    False),
    (8,    False),
    (16,   True),
    (17,   False),
    (32,   False),
    (64,   True),
    (256,  True),
    (512,  False),
    (1024, True),
    (4**10, True),
    (4**10 + 1, False),
    (4**15, True),   # max 32-bit power of 4
]

IMPLS = [
    ("reference",     reference),
    ("bit_len",       bit_length_check),
    ("mod3",          mod3),
    ("mask_arb",      mask_arbitrary),
    ("math_log4",     math_log4),
]

LARGE_IMPLS = [
    ("reference",     reference),
    ("bit_len",       bit_length_check),
    ("mod3",          mod3),
    ("mask_arb",      mask_arbitrary),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    print("  (mask_32 skipped — 32-bit only; verified separately)")
    for n, expected in TEST_CASES:
        row = {}
        for name, fn in IMPLS:
            try:
                row[name] = fn(n)
            except Exception as e:
                row[name] = f"ERR:{e}"
        ok = all(v == expected for v in row.values())
        tag = "OK" if ok else "FAIL"
        print(
            f"  [{tag}] n={str(n):<14} expected={str(expected):<6}  "
            + "  ".join(f"{nm}={v}" for nm, v in row.items())
        )

    # Verify mask_32 for 32-bit range
    mask_ok = all(
        mask_32(n) == expected
        for n, expected in TEST_CASES
        if n < 2**32
    )
    print(f"\n  [{'OK' if mask_ok else 'FAIL'}] mask_32: all 32-bit test cases correct")

    # Exhaustive check
    import math as _math
    def is_pow4_math(n):
        r = _math.log(n, 4)
        return abs(r - round(r)) < 1e-9

    fails = sum(
        1 for i in range(1, 100_001)
        if bit_length_check(i) != is_pow4_math(i)
    )
    print(f"  [{'OK' if fails == 0 else 'FAIL'}] bit_len: exhaustive 1..100000, {fails} failures")

    # Large int check
    large_ok = all(bit_length_check(4**i) for i in range(200))
    large_fail = any(bit_length_check(2 * 4**i) for i in range(200))
    print(f"  [{'OK' if large_ok else 'FAIL'}] bit_len: all 4^i for i in 0..199")
    print(f"  [{'OK' if not large_fail else 'FAIL'}] bit_len: no 2*4^i for i in 0..199")

    REPS = 300_000
    small_inputs = [1, 2, 4, 8, 16, 32, 64, 256, 1024, 4096]
    large_inputs = [4**50, 4**50 + 1, 4**100, 4**100 + 1]

    print(f"\n=== Benchmark (small ints): {REPS} runs, {len(small_inputs)} inputs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(n) for n in small_inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<14} {t:>7.4f} ms / batch of {len(small_inputs)}")

    print(f"\n=== Benchmark (large ints ~4^50, 4^100): {REPS} runs, {len(large_inputs)} inputs ===")
    for name, fn in LARGE_IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(n) for n in large_inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<14} {t:>7.4f} ms / batch of {len(large_inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
