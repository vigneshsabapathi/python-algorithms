#!/usr/bin/env python3
"""
Optimized and alternative implementations of single bit manipulation operations.

The reference uses the four classic bit ops:
    get_bit(n, p)   -> (n >> p) & 1
    set_bit(n, p)   -> n | (1 << p)
    clear_bit(n, p) -> n & ~(1 << p)
    flip_bit(n, p)  -> n ^ (1 << p)

Variants covered:
1. shift_and_mask  -- reference approach: shift + AND/OR/NOT/XOR with mask
2. bool_cast       -- get_bit returns bool(); set/clear use conditional logic
3. lambda_oneliner -- all four ops as lambdas (dict dispatch)
4. string_based    -- convert to binary string, manipulate character, convert back

Key interview insight:
    The shift+mask approach is universally expected.  Knowing that set_bit is
    idempotent (setting an already-set bit is a no-op) and that flip_bit is its
    own inverse (flip twice = original) are common follow-up questions.
    The string-based variant is O(n) in bit length and should be mentioned only
    to explain *why* bitwise is preferred.

Run:
    python bit_manipulation/single_bit_manipulation_operations_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bit_manipulation.single_bit_manipulation_operations import (
    clear_bit as ref_clear,
    flip_bit as ref_flip,
    get_bit as ref_get,
    set_bit as ref_set,
)


# ---------------------------------------------------------------------------
# Variant 1 — shift_and_mask (reference, inlined for benchmark fairness)
# ---------------------------------------------------------------------------

def shift_and_mask_get(number: int, position: int) -> int:
    """
    >>> shift_and_mask_get(0b1010, 1)
    1
    >>> shift_and_mask_get(0b1010, 0)
    0
    """
    return (number >> position) & 1


def shift_and_mask_set(number: int, position: int) -> int:
    """
    >>> shift_and_mask_set(0b1010, 0)
    11
    >>> shift_and_mask_set(0b1010, 1)
    10
    """
    return number | (1 << position)


def shift_and_mask_clear(number: int, position: int) -> int:
    """
    >>> shift_and_mask_clear(0b1010, 1)
    8
    >>> shift_and_mask_clear(0b1010, 0)
    10
    """
    return number & ~(1 << position)


def shift_and_mask_flip(number: int, position: int) -> int:
    """
    >>> shift_and_mask_flip(0b1010, 0)
    11
    >>> shift_and_mask_flip(0b1010, 1)
    8
    """
    return number ^ (1 << position)


# ---------------------------------------------------------------------------
# Variant 2 — bool_cast: get returns bool, set/clear use conditional
# ---------------------------------------------------------------------------

def bool_cast_get(number: int, position: int) -> int:
    """
    Return 0 or 1 using bool() cast instead of & 1.

    >>> bool_cast_get(0b1010, 1)
    1
    >>> bool_cast_get(0b1010, 0)
    0
    """
    return int(bool(number & (1 << position)))


def bool_cast_set(number: int, position: int) -> int:
    """
    Only OR if the bit is not already set (conditional set).

    >>> bool_cast_set(0b1010, 0)
    11
    >>> bool_cast_set(0b1010, 1)
    10
    """
    if not (number & (1 << position)):
        return number | (1 << position)
    return number


def bool_cast_clear(number: int, position: int) -> int:
    """
    Only clear if the bit is currently set (conditional clear).

    >>> bool_cast_clear(0b1010, 1)
    8
    >>> bool_cast_clear(0b1010, 0)
    10
    """
    if number & (1 << position):
        return number & ~(1 << position)
    return number


def bool_cast_flip(number: int, position: int) -> int:
    """
    Flip via conditional: if set then clear, else set.

    >>> bool_cast_flip(0b1010, 0)
    11
    >>> bool_cast_flip(0b1010, 1)
    8
    """
    if number & (1 << position):
        return number & ~(1 << position)
    return number | (1 << position)


# ---------------------------------------------------------------------------
# Variant 3 — lambda_oneliner: dict-dispatched lambdas
# ---------------------------------------------------------------------------

_BIT_OPS = {
    "get":   lambda n, p: (n >> p) & 1,
    "set":   lambda n, p: n | (1 << p),
    "clear": lambda n, p: n & ~(1 << p),
    "flip":  lambda n, p: n ^ (1 << p),
}


def lambda_get(number: int, position: int) -> int:
    """
    >>> lambda_get(0b1010, 1)
    1
    >>> lambda_get(0b1010, 0)
    0
    """
    return _BIT_OPS["get"](number, position)


def lambda_set(number: int, position: int) -> int:
    """
    >>> lambda_set(0b1010, 0)
    11
    >>> lambda_set(0b1010, 1)
    10
    """
    return _BIT_OPS["set"](number, position)


def lambda_clear(number: int, position: int) -> int:
    """
    >>> lambda_clear(0b1010, 1)
    8
    >>> lambda_clear(0b1010, 0)
    10
    """
    return _BIT_OPS["clear"](number, position)


def lambda_flip(number: int, position: int) -> int:
    """
    >>> lambda_flip(0b1010, 0)
    11
    >>> lambda_flip(0b1010, 1)
    8
    """
    return _BIT_OPS["flip"](number, position)


# ---------------------------------------------------------------------------
# Variant 4 — string_based: convert to bin string, manipulate, convert back
# ---------------------------------------------------------------------------

def string_get(number: int, position: int) -> int:
    """
    Get bit by indexing into the binary string representation.

    >>> string_get(0b1010, 1)
    1
    >>> string_get(0b1010, 0)
    0
    >>> string_get(0b1010, 3)
    1
    """
    bits = bin(number)[2:]  # strip '0b'
    if position >= len(bits):
        return 0
    return int(bits[-(position + 1)])


def string_set(number: int, position: int) -> int:
    """
    Set bit by replacing character in binary string.

    >>> string_set(0b1010, 0)
    11
    >>> string_set(0b1010, 1)
    10
    """
    bits = list(bin(number)[2:].zfill(position + 1))
    bits[-(position + 1)] = "1"
    return int("".join(bits), 2)


def string_clear(number: int, position: int) -> int:
    """
    Clear bit by replacing character in binary string.

    >>> string_clear(0b1010, 1)
    8
    >>> string_clear(0b1010, 0)
    10
    """
    bits = list(bin(number)[2:].zfill(position + 1))
    bits[-(position + 1)] = "0"
    return int("".join(bits), 2)


def string_flip(number: int, position: int) -> int:
    """
    Flip bit by toggling character in binary string.

    >>> string_flip(0b1010, 0)
    11
    >>> string_flip(0b1010, 1)
    8
    """
    bits = list(bin(number)[2:].zfill(position + 1))
    idx = -(position + 1)
    bits[idx] = "0" if bits[idx] == "1" else "1"
    return int("".join(bits), 2)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

# (number, position, expected_get, expected_set, expected_clear, expected_flip)
TEST_CASES = [
    (0b1010, 0, 0, 0b1011, 0b1010, 0b1011),
    (0b1010, 1, 1, 0b1010, 0b1000, 0b1000),
    (0b1010, 2, 0, 0b1110, 0b1010, 0b1110),
    (0b1010, 3, 1, 0b1010, 0b0010, 0b0010),
    (0, 0, 0, 1, 0, 1),
    (0, 5, 0, 32, 0, 32),
    (0b1111, 2, 1, 0b1111, 0b1011, 0b1011),
    (1, 0, 1, 1, 0, 0),
    (2**31, 31, 1, 2**31, 0, 0),
    (2**31, 0, 0, 2**31 + 1, 2**31, 2**31 + 1),
]

VARIANTS = [
    ("reference",      ref_get,            ref_set,            ref_clear,            ref_flip),
    ("shift_and_mask", shift_and_mask_get, shift_and_mask_set, shift_and_mask_clear, shift_and_mask_flip),
    ("bool_cast",      bool_cast_get,      bool_cast_set,      bool_cast_clear,      bool_cast_flip),
    ("lambda_oneliner", lambda_get,        lambda_set,         lambda_clear,         lambda_flip),
    ("string_based",   string_get,         string_set,         string_clear,         string_flip),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for number, pos, exp_get, exp_set, exp_clr, exp_flip in TEST_CASES:
        for name, fn_get, fn_set, fn_clear, fn_flip in VARIANTS:
            g = fn_get(number, pos)
            s = fn_set(number, pos)
            c = fn_clear(number, pos)
            f = fn_flip(number, pos)
            ok = g == exp_get and s == exp_set and c == exp_clr and f == exp_flip
            tag = "OK" if ok else "FAIL"
            if not ok:
                print(
                    f"  [{tag}] {name:<16} n={number:#06b} p={pos}  "
                    f"get={g}({exp_get}) set={s}({exp_set}) "
                    f"clr={c}({exp_clr}) flip={f}({exp_flip})"
                )
        # Print one summary line per test case
        all_ok = all(
            fn_get(number, pos) == exp_get
            and fn_set(number, pos) == exp_set
            and fn_clear(number, pos) == exp_clr
            and fn_flip(number, pos) == exp_flip
            for _, fn_get, fn_set, fn_clear, fn_flip in VARIANTS
        )
        print(f"  [{'OK' if all_ok else 'FAIL'}] n={number:<12} pos={pos}")

    REPS = 200_000
    inputs = [(n, p) for n, p, *_ in TEST_CASES]

    print(f"\n=== Benchmark: {REPS} runs, {len(inputs)} inputs each ===")
    for name, fn_get, fn_set, fn_clear, fn_flip in VARIANTS:
        t = timeit.timeit(
            lambda fg=fn_get, fs=fn_set, fc=fn_clear, ff=fn_flip: [
                (fg(n, p), fs(n, p), fc(n, p), ff(n, p)) for n, p in inputs
            ],
            number=REPS,
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch of {len(inputs)} (all 4 ops)")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
