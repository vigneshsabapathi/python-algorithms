#!/usr/bin/env python3
"""
Optimized implementations of Binary XOR.

Reference uses str(bin())[2:] double-wrap + char inequality test per pair.
Better: native ^ + bin(a^b) zfill. ASCII XOR trick also works for digits.

Variants:
1. binary_xor_native  -- native ^ + format()
2. binary_xor_bin     -- bin(a ^ b) + zfill  (fastest)
3. binary_xor_ascii   -- chr(48 + (ord(ca) ^ ord(cb))) per char

Run: python bit_manipulation/binary_xor_operator_optimized.py
"""

from __future__ import annotations
import sys, os, timeit
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bit_manipulation.binary_xor_operator import binary_xor as binary_xor_reference


def binary_xor_native(a: int, b: int) -> str:
    """
    Binary XOR using Python's ^ operator.

    >>> binary_xor_native(25, 32)
    '0b111001'
    >>> binary_xor_native(37, 50)
    '0b010111'
    >>> binary_xor_native(21, 30)
    '0b01011'
    >>> binary_xor_native(58, 73)
    '0b1110011'
    >>> binary_xor_native(0, 255)
    '0b11111111'
    >>> binary_xor_native(256, 256)
    '0b000000000'
    >>> binary_xor_native(0, -1)
    Traceback (most recent call last):
        ...
    ValueError: the value of both inputs must be positive
    """
    if a < 0 or b < 0:
        raise ValueError("the value of both inputs must be positive")
    max_len = max(len(format(a, "b")), len(format(b, "b")))
    return "0b" + format(a ^ b, f"0{max_len}b")


def binary_xor_bin(a: int, b: int) -> str:
    """
    Binary XOR using bin(a ^ b) + zfill — cleanest one-liner.

    XOR result bit-length <= max(a.bit_length(), b.bit_length()).
    When both inputs are equal (a^a=0), result is 0 but must be zero-padded
    to max_len (e.g. binary_xor(256,256) -> '0b000000000', not '0b0').

    >>> binary_xor_bin(25, 32)
    '0b111001'
    >>> binary_xor_bin(37, 50)
    '0b010111'
    >>> binary_xor_bin(21, 30)
    '0b01011'
    >>> binary_xor_bin(58, 73)
    '0b1110011'
    >>> binary_xor_bin(0, 255)
    '0b11111111'
    >>> binary_xor_bin(256, 256)
    '0b000000000'
    >>> binary_xor_bin(0, -1)
    Traceback (most recent call last):
        ...
    ValueError: the value of both inputs must be positive
    """
    if a < 0 or b < 0:
        raise ValueError("the value of both inputs must be positive")
    max_len = max(a.bit_length(), b.bit_length(), 1)
    return "0b" + bin(a ^ b)[2:].zfill(max_len)


def binary_xor_ascii(a: int, b: int) -> str:
    """
    Binary XOR using ASCII arithmetic on digit characters.

    ord('0')=48, ord('1')=49. XOR of two binary digit chars:
    ord(ca) ^ ord(cb) gives 0 (same) or 1 (different).
    chr(48 + result) maps back to '0' or '1' without int() parse per char.

    >>> binary_xor_ascii(25, 32)
    '0b111001'
    >>> binary_xor_ascii(37, 50)
    '0b010111'
    >>> binary_xor_ascii(21, 30)
    '0b01011'
    >>> binary_xor_ascii(58, 73)
    '0b1110011'
    >>> binary_xor_ascii(0, 255)
    '0b11111111'
    >>> binary_xor_ascii(256, 256)
    '0b000000000'
    >>> binary_xor_ascii(0, -1)
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
        chr(48 + (ord(ca) ^ ord(cb)))
        for ca, cb in zip(a_bin.zfill(max_len), b_bin.zfill(max_len))
    )


TEST_CASES = [
    (25,  32,  "0b111001"),
    (37,  50,  "0b010111"),
    (21,  30,  "0b01011"),
    (58,  73,  "0b1110011"),
    (0,   255, "0b11111111"),
    (256, 256, "0b000000000"),
]

IMPLS = [
    ("reference", binary_xor_reference),
    ("native ^",  binary_xor_native),
    ("bin(a^b)",  binary_xor_bin),
    ("ascii xor", binary_xor_ascii),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for a, b, expected in TEST_CASES:
        results = {name: fn(a, b) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        print(f"  [{'OK' if ok else 'FAIL'}] binary_xor({a:>3},{b:>3}) = {expected!r:<20}"
              + "  ".join(f"{n}={v!r}" for n, v in results.items()))

    REPS = 200_000
    inputs = [(25, 32), (37, 50), (58, 73), (0, 255), (256, 256)]
    print(f"\n=== Benchmark: {REPS} runs, {len(inputs)} pairs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: [fn(a, b) for a, b in inputs], number=REPS) * 1000 / REPS
        print(f"  {name:<14} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
