#!/usr/bin/env python3
"""
Optimized and alternative implementations of Largest Power of Two <= N.

Given a positive integer N, find the largest power of 2 that is <= N.

The reference uses a left-shift loop: start at 1, keep shifting left while
(res << 1) <= N.  This is O(log N) — one iteration per bit.

Four O(1) / faster alternatives:

  bit_length  — `1 << (n.bit_length() - 1)` — C-level integer intrinsic
  bit_smear   — smear the highest set bit right, then add 1 and shift
  math_log2   — `2 ** int(math.log2(n))` — float, precision trap for large n
  one_liner   — `1 << (n.bit_length() - 1)` inlined (same as bit_length)

Why bit_length works:
    n.bit_length() returns the number of bits needed to represent n.
    For any n >= 1, the highest set bit is at position (bit_length - 1).
    So `1 << (n.bit_length() - 1)` gives 2^floor(log2(n)) — the largest
    power of 2 <= n.

Why bit_smear works:
    Propagate the highest set bit to all lower positions:
        n |= n >> 1; n |= n >> 2; n |= n >> 4; ... n |= n >> 32
    Now n is all-ones from the highest bit down.  `(n + 1) >> 1` gives
    the power of 2.  This is the classic O(log(bits)) approach used in
    hardware and C (no Python intrinsic needed).

Why math_log2 is dangerous:
    `math.log2(n)` returns a float.  For n > 2^53, IEEE 754 double
    precision can't represent the result exactly, so `int(math.log2(n))`
    may be off by 1.  Safe for n < 2^53 only.

Key interview insight:
    `1 << (n.bit_length() - 1)` is the cleanest O(1) Python answer.
    The bit-smearing approach is what you'd use in C/Java (no intrinsic).
    `math.log2` is the trap answer — interviewers want you to know it fails.

Run:
    python bit_manipulation/largest_pow_of_two_le_num_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bit_manipulation.largest_pow_of_two_le_num import (
    largest_pow_of_two_le_num as reference,
)


def _guard(number: int) -> None:
    if isinstance(number, float):
        raise TypeError("Input value must be a 'int' type")
    if number <= 0:
        raise ValueError("number must be positive")


# ---------------------------------------------------------------------------
# Variant 1 — bit_length: O(1), Python-native intrinsic
# ---------------------------------------------------------------------------

def bit_length(number: int) -> int:
    """
    Largest power of 2 <= number via n.bit_length().

    n.bit_length() gives the position of the highest set bit + 1.
    So `1 << (bit_length - 1)` isolates that highest power of 2.

    >>> bit_length(1)
    1
    >>> bit_length(2)
    2
    >>> bit_length(3)
    2
    >>> bit_length(15)
    8
    >>> bit_length(16)
    16
    >>> bit_length(99)
    64
    >>> bit_length(178)
    128
    >>> bit_length(999999)
    524288
    >>> bit_length(2**100)
    1267650600228229401496703205376
    """
    _guard(number)
    return 1 << (number.bit_length() - 1)


# ---------------------------------------------------------------------------
# Variant 2 — bit-smearing: O(log(bits)), no intrinsic needed
# ---------------------------------------------------------------------------

def bit_smear(number: int) -> int:
    """
    Largest power of 2 <= number via bit-smearing (propagate highest set bit).

    Works by OR-ing the number with right-shifted copies of itself,
    filling all bits below the highest set bit with 1s, then extracting
    the power of 2 via (n + 1) >> 1.

    For arbitrary-precision Python ints, we smear in a loop based on
    bit_length rather than fixed 1/2/4/8/16/32 shifts.

    >>> bit_smear(1)
    1
    >>> bit_smear(2)
    2
    >>> bit_smear(3)
    2
    >>> bit_smear(15)
    8
    >>> bit_smear(16)
    16
    >>> bit_smear(99)
    64
    >>> bit_smear(178)
    128
    >>> bit_smear(999999)
    524288
    """
    _guard(number)
    n = number
    shift = 1
    while shift < n.bit_length():
        n |= n >> shift
        shift <<= 1
    # n is now all-ones from the highest bit down
    return (n + 1) >> 1


# ---------------------------------------------------------------------------
# Variant 3 — math.log2: O(1) but float precision trap
# ---------------------------------------------------------------------------

def math_log2(number: int) -> int:
    """
    Largest power of 2 <= number via math.log2.

    WARNING: float precision breaks for number > 2^53.  Safe for small
    inputs only.

    >>> math_log2(1)
    1
    >>> math_log2(2)
    2
    >>> math_log2(3)
    2
    >>> math_log2(15)
    8
    >>> math_log2(16)
    16
    >>> math_log2(99)
    64
    >>> math_log2(178)
    128
    >>> math_log2(999999)
    524288
    """
    _guard(number)
    exp = int(math.log2(number))
    return 1 << exp


# ---------------------------------------------------------------------------
# Variant 4 — one-liner (bit_length, for benchmark baseline)
# ---------------------------------------------------------------------------

def one_liner(number: int) -> int:
    """
    Largest power of 2 <= number — one-liner using bit_length.

    >>> one_liner(1)
    1
    >>> one_liner(15)
    8
    >>> one_liner(16)
    16
    >>> one_liner(999999)
    524288
    """
    _guard(number)
    return 1 << (number.bit_length() - 1)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (1,       1),
    (2,       2),
    (3,       2),
    (4,       4),
    (7,       4),
    (8,       8),
    (10,      8),
    (15,      8),
    (16,      16),
    (17,      16),
    (31,      16),
    (32,      32),
    (64,      64),
    (99,      64),
    (100,     64),
    (128,     128),
    (178,     128),
    (255,     128),
    (256,     256),
    (999999,  524288),
    (1048576, 1048576),  # 2^20
]

IMPLS = [
    ("reference",  reference),
    ("bit_length", bit_length),
    ("bit_smear",  bit_smear),
    ("math_log2",  math_log2),
    ("one_liner",  one_liner),
]

LARGE_IMPLS = [
    ("reference",  reference),
    ("bit_length", bit_length),
    ("bit_smear",  bit_smear),
    ("one_liner",  one_liner),
]


def run_all() -> None:
    print("\n=== Correctness ===")
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
            f"  [{tag}] n={str(n):<14} expected={str(expected):<10}  "
            + "  ".join(f"{nm}={v}" for nm, v in row.items())
        )

    # Large int correctness (math_log2 excluded — float precision)
    print("\n  --- Large int correctness (bit_length vs reference) ---")
    large_ok = True
    for exp in [50, 100, 200, 500, 1000]:
        for n in [2**exp, 2**exp + 1, 2**exp - 1]:
            ref = reference(n)
            bl = bit_length(n)
            if ref != bl:
                print(f"  [FAIL] n=2**{exp}{'+-1' if n != 2**exp else ''}  ref={ref}  bit_length={bl}")
                large_ok = False
    print(f"  [{'OK' if large_ok else 'FAIL'}] bit_length matches reference for 2^50..2^1000 (+/-1)")

    # Exhaustive small range
    fails = 0
    for i in range(1, 100_001):
        if bit_length(i) != reference(i):
            fails += 1
    print(f"  [{'OK' if fails == 0 else 'FAIL'}] bit_length: exhaustive 1..100000, {fails} failures")

    REPS = 300_000
    small_inputs = [1, 2, 3, 7, 8, 15, 16, 31, 64, 99, 128, 256, 999999]
    large_inputs = [2**50, 2**50 + 1, 2**100, 2**100 + 1]

    print(f"\n=== Benchmark (small ints): {REPS} runs, {len(small_inputs)} inputs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(n) for n in small_inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<14} {t:>7.4f} ms / batch of {len(small_inputs)}")

    print(f"\n=== Benchmark (large ints ~2^50, 2^100): {REPS} runs, {len(large_inputs)} inputs ===")
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
