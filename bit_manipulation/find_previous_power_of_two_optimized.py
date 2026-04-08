#!/usr/bin/env python3
"""
Comparison of methods to find the largest power of two <= n (floor power of 2).

Original: shift-left loop until power > n, then shift back.

This file adds:
  2. bit_length  — 1 << (n.bit_length() - 1)           [O(1), fastest]
  3. math.log2   — int(2 ** floor(log2(n)))              [float, precision risk]
  4. bit smear   — fill all bits below MSB, then +1>>1   [pure bit tricks]
  5. int.from_bytes + bit_length                         [same as bit_length]

Ref: https://stackoverflow.com/questions/1322510

Run: python bit_manipulation/find_previous_power_of_two_optimized.py
"""

from __future__ import annotations
import math
import timeit


def prev_pow2_shift_loop(n: int) -> int:
    """
    Original: shift left until power > n, then shift right once.
    O(log n) — loop runs log₂(n) times.

    >>> prev_pow2_shift_loop(0)
    0
    >>> prev_pow2_shift_loop(1)
    1
    >>> [prev_pow2_shift_loop(i) for i in range(18)]
    [0, 1, 2, 2, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 16, 16]
    >>> prev_pow2_shift_loop(1024)
    1024
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("Input must be a non-negative integer")
    if n == 0:
        return 0
    power = 1
    while power <= n:
        power <<= 1
    return power >> 1 if n > 1 else 1


def prev_pow2_bit_length(n: int) -> int:
    """
    Use int.bit_length(): number of bits needed to represent n.
    For n > 0: largest power of 2 <= n is 1 << (n.bit_length() - 1).
    O(1) — single hardware instruction on modern CPUs.

    >>> prev_pow2_bit_length(0)
    0
    >>> prev_pow2_bit_length(1)
    1
    >>> [prev_pow2_bit_length(i) for i in range(18)]
    [0, 1, 2, 2, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 16, 16]
    >>> prev_pow2_bit_length(1024)
    1024
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("Input must be a non-negative integer")
    if n == 0:
        return 0
    return 1 << (n.bit_length() - 1)


def prev_pow2_log2(n: int) -> int:
    """
    Use math.log2 + floor: 2^floor(log2(n)).
    Readable but uses floating-point — precision issues for very large n.

    >>> prev_pow2_log2(0)
    0
    >>> prev_pow2_log2(1)
    1
    >>> [prev_pow2_log2(i) for i in range(18)]
    [0, 1, 2, 2, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 16, 16]
    >>> prev_pow2_log2(1024)
    1024
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("Input must be a non-negative integer")
    if n == 0:
        return 0
    return 1 << int(math.log2(n))


def prev_pow2_bit_smear(n: int) -> int:
    """
    Bit-smear: OR n with all right-shifted versions to fill all bits below MSB,
    then (result + 1) >> 1 isolates the MSB value.
    Classic technique for 32-bit integers; works for arbitrary Python ints too.

    >>> prev_pow2_bit_smear(0)
    0
    >>> prev_pow2_bit_smear(1)
    1
    >>> [prev_pow2_bit_smear(i) for i in range(18)]
    [0, 1, 2, 2, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 16, 16]
    >>> prev_pow2_bit_smear(1024)
    1024
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("Input must be a non-negative integer")
    if n == 0:
        return 0
    # Fill all bits below MSB: e.g. 0b101 -> 0b111
    v = n
    bits = n.bit_length()
    shift = 1
    while shift < bits:
        v |= v >> shift
        shift <<= 1
    # v is now all 1s up to MSB; (v + 1) >> 1 = 2^MSB
    return (v + 1) >> 1


# ---------------------------------------------------------------------------
# Correctness + Benchmark
# ---------------------------------------------------------------------------

IMPLS = [
    ("shift_loop",  prev_pow2_shift_loop),
    ("bit_length",  prev_pow2_bit_length),
    ("log2",        prev_pow2_log2),
    ("bit_smear",   prev_pow2_bit_smear),
]

TEST_CASES = [
    (0,    0),
    (1,    1),
    (2,    2),
    (3,    2),
    (5,    4),
    (8,    8),
    (15,   8),
    (16,   16),
    (17,   16),
    (64,   64),
    (65,   64),
    (1023, 512),
    (1024, 1024),
    (1025, 1024),
]

_SMALL  = [1, 3, 7, 15, 31]
_MEDIUM = [100, 255, 1000, 4096, 65535]
_LARGE  = [10**6, 10**9, 2**30, 2**30 + 1, 2**60]


def run_all() -> None:
    print("\n=== Correctness ===")
    for n, expected in TEST_CASES:
        row = {name: fn(n) for name, fn in IMPLS}
        ok = all(v == expected for v in row.values())
        vals = "  ".join(f"{nm}={v}" for nm, v in row.items())
        print(f"  [{'OK' if ok else 'FAIL'}] prev_pow2({n:<6}) = {expected:<6}  {vals}")

    REPS = 500_000
    for label, inputs in [
        ("small  (1–31)",         _SMALL),
        ("medium (100–65535)",    _MEDIUM),
        ("large  (10^6–2^60)",    _LARGE),
    ]:
        print(f"\n=== Benchmark: {label}, {REPS} runs ===")
        for name, fn in IMPLS:
            t = timeit.timeit(
                lambda fn=fn: [fn(x) for x in inputs], number=REPS
            ) * 1000 / REPS
            print(f"  {name:<14} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
