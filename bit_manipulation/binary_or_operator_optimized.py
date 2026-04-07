#!/usr/bin/env python3
"""
Optimized and alternative implementations of Binary OR.

The reference converts both integers to binary strings via bin(), strips the
'0b' prefix manually (str(bin(a))[2:] — double-wrapping str() on an already-
str result from bin()), zero-pads, then checks "1" in (char_a, char_b) per
pair.  This re-implements what the CPU does in one instruction.

Variants covered:
1. binary_or_native  -- single | operator; format result to match width
2. binary_or_format  -- format(a, "b") avoids bin()/str() double-wrap
3. binary_or_bin     -- bin(a | b) + zfill; idiomatic Python one-liner
4. binary_or_bitwise -- char-level '|' using ord() arithmetic; no int() parse

Key interview insight:
    Reference:  O(n) string char-by-char  — reinvents | in Python
    Native |:   O(1) CPU OR + O(n) format — single hardware instruction
    bin() form: cleanest one-liner        — same complexity as native

Width rule: result width = max(len(bin(a)[2:]), len(bin(b)[2:])).
OR can only set bits already present in a or b, so the highest bit of the
wider input is always preserved.

Run:
    python bit_manipulation/binary_or_operator_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bit_manipulation.binary_or_operator import binary_or as binary_or_reference


# ---------------------------------------------------------------------------
# Variant 1 — Native | operator
# ---------------------------------------------------------------------------

def binary_or_native(a: int, b: int) -> str:
    """
    Binary OR using Python's built-in | operator.

    Produces the same zero-padded '0b...' string as the reference.
    Width = max(bit_length(a), bit_length(b)), matching reference behaviour.

    >>> binary_or_native(25, 32)
    '0b111001'
    >>> binary_or_native(37, 50)
    '0b110111'
    >>> binary_or_native(21, 30)
    '0b11111'
    >>> binary_or_native(58, 73)
    '0b1111011'
    >>> binary_or_native(0, 255)
    '0b11111111'
    >>> binary_or_native(0, 256)
    '0b100000000'
    >>> binary_or_native(0, -1)
    Traceback (most recent call last):
        ...
    ValueError: the value of both inputs must be positive
    """
    if a < 0 or b < 0:
        raise ValueError("the value of both inputs must be positive")
    max_len = max(len(format(a, "b")), len(format(b, "b")))
    return "0b" + format(a | b, f"0{max_len}b")


# ---------------------------------------------------------------------------
# Variant 2 — format() per digit (avoids str(bin()) double-wrap)
# ---------------------------------------------------------------------------

def binary_or_format(a: int, b: int) -> str:
    """
    Binary OR using format(a, "b") — removes the str(bin()) double-wrap.

    The reference uses str(bin(a))[2:]; bin() already returns a str so
    str() is redundant.  format(a, "b") is the idiomatic single call.

    >>> binary_or_format(25, 32)
    '0b111001'
    >>> binary_or_format(37, 50)
    '0b110111'
    >>> binary_or_format(21, 30)
    '0b11111'
    >>> binary_or_format(58, 73)
    '0b1111011'
    >>> binary_or_format(0, 255)
    '0b11111111'
    >>> binary_or_format(0, 256)
    '0b100000000'
    >>> binary_or_format(0, -1)
    Traceback (most recent call last):
        ...
    ValueError: the value of both inputs must be positive
    """
    if a < 0 or b < 0:
        raise ValueError("the value of both inputs must be positive")
    a_bin = format(a, "b")
    b_bin = format(b, "b")
    max_len = max(len(a_bin), len(b_bin))
    return "0b" + "".join(
        str(int("1" in (ca, cb)))
        for ca, cb in zip(a_bin.zfill(max_len), b_bin.zfill(max_len))
    )


# ---------------------------------------------------------------------------
# Variant 3 — bin(a | b) + zfill (cleanest one-liner)
# ---------------------------------------------------------------------------

def binary_or_bin(a: int, b: int) -> str:
    """
    Binary OR using bin(a | b) and zfill.

    OR can only set bits already in a or b, so the result bit-length equals
    max(a.bit_length(), b.bit_length()).  bin(a | b)[2:].zfill(max_len)
    zero-pads to that width.

    >>> binary_or_bin(25, 32)
    '0b111001'
    >>> binary_or_bin(37, 50)
    '0b110111'
    >>> binary_or_bin(21, 30)
    '0b11111'
    >>> binary_or_bin(58, 73)
    '0b1111011'
    >>> binary_or_bin(0, 255)
    '0b11111111'
    >>> binary_or_bin(0, 256)
    '0b100000000'
    >>> binary_or_bin(0, -1)
    Traceback (most recent call last):
        ...
    ValueError: the value of both inputs must be positive
    """
    if a < 0 or b < 0:
        raise ValueError("the value of both inputs must be positive")
    max_len = max(a.bit_length(), b.bit_length(), 1)
    return "0b" + bin(a | b)[2:].zfill(max_len)


# ---------------------------------------------------------------------------
# Variant 4 — bitwise char OR using ord() (no int() parse per character)
# ---------------------------------------------------------------------------

def binary_or_bitwise_char(a: int, b: int) -> str:
    """
    Binary OR using ord()-based char manipulation — no int() parse per step.

    '0' = ord 48, '1' = ord 49.  OR of two ASCII digit chars:
    '0'|'0'=48, '0'|'1'=49, '1'|'0'=49, '1'|'1'=49.
    (ord('0') | ord('1')) == ord('1') — OR maps naturally onto ASCII digits.

    >>> binary_or_bitwise_char(25, 32)
    '0b111001'
    >>> binary_or_bitwise_char(37, 50)
    '0b110111'
    >>> binary_or_bitwise_char(21, 30)
    '0b11111'
    >>> binary_or_bitwise_char(58, 73)
    '0b1111011'
    >>> binary_or_bitwise_char(0, 255)
    '0b11111111'
    >>> binary_or_bitwise_char(0, 256)
    '0b100000000'
    >>> binary_or_bitwise_char(0, -1)
    Traceback (most recent call last):
        ...
    ValueError: the value of both inputs must be positive
    """
    if a < 0 or b < 0:
        raise ValueError("the value of both inputs must be positive")
    a_bin = format(a, "b")
    b_bin = format(b, "b")
    max_len = max(len(a_bin), len(b_bin))
    return "0b" + "".join(
        chr(ord(ca) | ord(cb))
        for ca, cb in zip(a_bin.zfill(max_len), b_bin.zfill(max_len))
    )


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (25,  32,  "0b111001"),
    (37,  50,  "0b110111"),
    (21,  30,  "0b11111"),
    (58,  73,  "0b1111011"),
    (0,   255, "0b11111111"),
    (0,   256, "0b100000000"),
]

IMPLS = [
    ("reference",     binary_or_reference),
    ("native |",      binary_or_native),
    ("format()",      binary_or_format),
    ("bin(a|b)",      binary_or_bin),
    ("bitwise_char",  binary_or_bitwise_char),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for a, b, expected in TEST_CASES:
        results = {name: fn(a, b) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(
            f"  [{tag}] binary_or({a:>3}, {b:>3})  expected={expected!r:<18}"
            + "  ".join(f"{n}={v!r}" for n, v in results.items())
        )

    REPS = 200_000
    inputs = [(25, 32), (37, 50), (58, 73), (0, 255), (0, 256)]
    print(f"\n=== Benchmark: {REPS} runs, {len(inputs)} pairs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(a, b) for a, b in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
