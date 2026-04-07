#!/usr/bin/env python3
"""
Optimized and alternative implementations of Binary AND.

The reference manually converts both integers to binary strings, zero-pads
them, then zips and compares characters one by one.  This is O(n) string work
but it reinvents what the CPU already does in a single instruction.

Variants covered:
1. binary_and_native   -- single & operator; format result to match reference
                          output width.  One CPU instruction for the AND.
2. binary_and_bin      -- uses built-in bin() + int() round-trip; idiomatic
                          Python, same complexity as native.
3. binary_and_bitshift -- manual bit-by-bit construction with shifts; shows
                          the underlying mechanics clearly for interviews.

Key interview insight:
    Reference:    O(n) string-zip   — manual char comparison
    Native &:     O(1) CPU AND      — then O(n) formatting only
    All produce identical output for valid inputs.

Run:
    python bit_manipulation/binary_and_operator_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bit_manipulation.binary_and_operator import binary_and as binary_and_reference


# ---------------------------------------------------------------------------
# Variant 1 — Native & operator (one CPU instruction)
# ---------------------------------------------------------------------------

def binary_and_native(a: int, b: int) -> str:
    """
    Binary AND using Python's built-in & operator.

    Produces the same zero-padded '0b...' string as the reference.
    The AND itself is a single hardware instruction; only the formatting
    is O(n) where n = number of bits in max(a, b).

    >>> binary_and_native(25, 32)
    '0b000000'
    >>> binary_and_native(37, 50)
    '0b100000'
    >>> binary_and_native(21, 30)
    '0b10100'
    >>> binary_and_native(58, 73)
    '0b0001000'
    >>> binary_and_native(0, 255)
    '0b00000000'
    >>> binary_and_native(256, 256)
    '0b100000000'
    >>> binary_and_native(0, -1)
    Traceback (most recent call last):
        ...
    ValueError: the value of both inputs must be positive
    """
    if a < 0 or b < 0:
        raise ValueError("the value of both inputs must be positive")

    result = a & b
    max_len = max(len(format(a, "b")), len(format(b, "b")))
    return "0b" + format(result, f"0{max_len}b")


# ---------------------------------------------------------------------------
# Variant 2 — bin() + int() round-trip
# ---------------------------------------------------------------------------

def binary_and_bin(a: int, b: int) -> str:
    """
    Binary AND using bin() and int() built-ins.

    bin(a & b) returns e.g. '0b10100'.  We strip the prefix, zero-pad
    to match the reference width, then reattach '0b'.

    >>> binary_and_bin(25, 32)
    '0b000000'
    >>> binary_and_bin(37, 50)
    '0b100000'
    >>> binary_and_bin(21, 30)
    '0b10100'
    >>> binary_and_bin(58, 73)
    '0b0001000'
    >>> binary_and_bin(0, 255)
    '0b00000000'
    >>> binary_and_bin(256, 256)
    '0b100000000'
    >>> binary_and_bin(0, -1)
    Traceback (most recent call last):
        ...
    ValueError: the value of both inputs must be positive
    """
    if a < 0 or b < 0:
        raise ValueError("the value of both inputs must be positive")

    max_len = max(a.bit_length(), b.bit_length(), 1)
    result_bits = bin(a & b)[2:].zfill(max_len)
    return "0b" + result_bits


# ---------------------------------------------------------------------------
# Variant 3 — Explicit bit-by-bit with shifts (shows mechanics)
# ---------------------------------------------------------------------------

def binary_and_bitshift(a: int, b: int) -> str:
    """
    Binary AND built bit-by-bit using right-shifts and & 1.

    Demonstrates the underlying mechanics clearly — useful in interviews
    when asked to implement bitwise operations from scratch.

    >>> binary_and_bitshift(25, 32)
    '0b000000'
    >>> binary_and_bitshift(37, 50)
    '0b100000'
    >>> binary_and_bitshift(21, 30)
    '0b10100'
    >>> binary_and_bitshift(58, 73)
    '0b0001000'
    >>> binary_and_bitshift(0, 255)
    '0b00000000'
    >>> binary_and_bitshift(256, 256)
    '0b100000000'
    >>> binary_and_bitshift(0, -1)
    Traceback (most recent call last):
        ...
    ValueError: the value of both inputs must be positive
    """
    if a < 0 or b < 0:
        raise ValueError("the value of both inputs must be positive")

    max_len = max(a.bit_length(), b.bit_length(), 1)
    bits = []
    for i in range(max_len - 1, -1, -1):
        bit_a = (a >> i) & 1
        bit_b = (b >> i) & 1
        bits.append(str(bit_a & bit_b))
    return "0b" + "".join(bits)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (25,  32,  "0b000000"),
    (37,  50,  "0b100000"),
    (21,  30,  "0b10100"),
    (58,  73,  "0b0001000"),
    (0,   255, "0b00000000"),
    (256, 256, "0b100000000"),
]

IMPLS = [
    ("reference",  binary_and_reference),
    ("native &",   binary_and_native),
    ("bin()",      binary_and_bin),
    ("bitshift",   binary_and_bitshift),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for a, b, expected in TEST_CASES:
        results = {name: fn(a, b) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(
            f"  [{tag}] binary_and({a:>3}, {b:>3})  expected={expected!r:<18}"
            + "  ".join(f"{n}={v!r}" for n, v in results.items())
        )

    REPS = 100_000
    print(f"\n=== Benchmark: {REPS} runs, mixed inputs ===")
    inputs = [(37, 50), (58, 73), (256, 256), (0, 255)]
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(a, b) for a, b in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<12} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
