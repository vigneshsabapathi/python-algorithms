#!/usr/bin/env python3
"""
Optimized and alternative implementations of Is Even.

The reference uses `number & 1 == 0` — a single bitwise AND against the LSB.
For even numbers the LSB is always 0; for odd numbers it is always 1.

Variants covered:
1. bitwise_and   -- n & 1 == 0              (reference, explicit)
2. not_bitwise   -- not (n & 1)             (truthy shorthand)
3. modulo        -- n % 2 == 0              (idiomatic Python)
4. not_modulo    -- not n % 2               (truthy shorthand)
5. last_digit    -- str(abs(n))[-1] in '02468'  (decimal digit check)

Key interview insight:
    `n & 1 == 0` and `n % 2 == 0` are functionally identical for integers.
    The bitwise form is the "bit manipulation" answer interviewers want when
    the problem says "without using the modulo operator".
    Both work correctly on negative integers in Python
    (Python's `%` always returns non-negative; `& 1` checks the true LSB).

Run:
    python bit_manipulation/is_even_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bit_manipulation.is_even import is_even as reference


# ---------------------------------------------------------------------------
# Variant 1 — bitwise AND, explicit comparison (reference)
# ---------------------------------------------------------------------------

def bitwise_and(number: int) -> bool:
    """
    Even check via bitwise AND: LSB is 0 for all even integers.

    >>> bitwise_and(0)
    True
    >>> bitwise_and(1)
    False
    >>> bitwise_and(4)
    True
    >>> bitwise_and(-2)
    True
    >>> bitwise_and(-3)
    False
    """
    return number & 1 == 0


# ---------------------------------------------------------------------------
# Variant 2 — not (n & 1): truthy shorthand
# ---------------------------------------------------------------------------

def not_bitwise(number: int) -> bool:
    """
    Even check via `not (n & 1)` — reads naturally as "no LSB set".

    >>> not_bitwise(0)
    True
    >>> not_bitwise(1)
    False
    >>> not_bitwise(4)
    True
    >>> not_bitwise(-2)
    True
    >>> not_bitwise(-3)
    False
    """
    return not (number & 1)


# ---------------------------------------------------------------------------
# Variant 3 — modulo: the idiomatic Python approach
# ---------------------------------------------------------------------------

def modulo(number: int) -> bool:
    """
    Even check via n % 2 == 0 — the standard readable approach.

    Note: Python's % always returns non-negative (floor division), so
    -3 % 2 == 1 and -4 % 2 == 0.  Consistent with the bitwise check.

    >>> modulo(0)
    True
    >>> modulo(1)
    False
    >>> modulo(4)
    True
    >>> modulo(-2)
    True
    >>> modulo(-3)
    False
    """
    return number % 2 == 0


# ---------------------------------------------------------------------------
# Variant 4 — not n % 2: truthy shorthand for modulo
# ---------------------------------------------------------------------------

def not_modulo(number: int) -> bool:
    """
    Even check via `not n % 2` — Falsy 0 means even.

    >>> not_modulo(0)
    True
    >>> not_modulo(1)
    False
    >>> not_modulo(4)
    True
    >>> not_modulo(-2)
    True
    >>> not_modulo(-3)
    False
    """
    return not number % 2


# ---------------------------------------------------------------------------
# Variant 5 — last decimal digit check (no arithmetic operators)
# ---------------------------------------------------------------------------

def last_digit(number: int) -> bool:
    """
    Even check by inspecting the last decimal digit.

    A number is even iff its last digit is in {0, 2, 4, 6, 8}.
    Works on arbitrarily large integers without division or bit ops.

    >>> last_digit(0)
    True
    >>> last_digit(1)
    False
    >>> last_digit(4)
    True
    >>> last_digit(-2)
    True
    >>> last_digit(-3)
    False
    >>> last_digit(10**100)
    True
    """
    return str(abs(number))[-1] in "02468"


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (0, True),
    (1, False),
    (2, True),
    (3, False),
    (4, True),
    (9, False),
    (40, True),
    (101, False),
    (-2, True),
    (-3, False),
    (2**31, True),
    (2**31 + 1, False),
    (2**64, True),
    (2**64 + 1, False),
]

IMPLS = [
    ("reference",   reference),
    ("bitwise_and", bitwise_and),
    ("not_bitwise", not_bitwise),
    ("modulo",      modulo),
    ("not_modulo",  not_modulo),
    ("last_digit",  last_digit),
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
            f"  [{tag}] n={str(n):<22} expected={str(expected):<6}  "
            + "  ".join(f"{nm}={v}" for nm, v in results.items())
        )

    REPS = 500_000
    inputs_small = [0, 1, 2, 3, 4, 9, 40, 101, -2, -3]
    inputs_large = [2**31, 2**31 + 1, 2**64, 2**64 + 1]

    print(f"\n=== Benchmark (small ints): {REPS} runs, {len(inputs_small)} inputs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(n) for n in inputs_small], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<12} {t:>7.4f} ms / batch of {len(inputs_small)}")

    print(f"\n=== Benchmark (large ints): {REPS} runs, {len(inputs_large)} inputs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(n) for n in inputs_large], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<12} {t:>7.4f} ms / batch of {len(inputs_large)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
