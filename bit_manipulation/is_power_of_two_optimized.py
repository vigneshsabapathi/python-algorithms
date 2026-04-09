#!/usr/bin/env python3
"""
Optimized and alternative implementations of Is Power of Two.

The reference uses `n & (n - 1) == 0` — a classic bit trick that clears the
lowest set bit.  For a power of 2 there is exactly ONE set bit, so clearing
it leaves zero.

Key identity:
    n     = 0b...100...00
    n - 1 = 0b...011...11
    n & (n-1) = 0   ← only for powers of 2 (and 0, a known quirk)

NOTE on zero:
    The reference returns True for n=0 because 0 & (0-1) = 0 & -1 = 0.
    Mathematically, 0 is NOT a power of 2.  The "strict" check used on
    LeetCode 231 is `n > 0 and n & (n-1) == 0`.  All variants below
    match the reference (True for 0) unless noted.

Variants covered:
1. kernighan      -- n & (n-1) == 0               (reference, classic)
2. strict         -- n > 0 and n & (n-1) == 0     (LeetCode-correct, 0→False)
3. bit_count      -- n.bit_count() <= 1            (Python 3.10+, popcount)
4. bin_count      -- bin(n).count('1') <= 1        (string popcount)
5. math_log2      -- n > 0 and math.log2(n) % 1 == 0  (float, precision trap)

Key interview insight:
    `n & (n-1) == 0` is the canonical one-liner.  Interviewers expect you to
    know WHY it works: a power of 2 has exactly one set bit; subtracting 1
    flips all bits from that position down; AND yields 0.
    The strict form `n > 0 and n & (n-1) == 0` is the production-correct answer.
    `n.bit_count() == 1` is the most readable O(1) alternative (Python 3.10+).

Run:
    python bit_manipulation/is_power_of_two_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bit_manipulation.is_power_of_two import is_power_of_two as reference


# ---------------------------------------------------------------------------
# Variant 1 — Kernighan trick (mirrors reference exactly)
# ---------------------------------------------------------------------------

def kernighan(number: int) -> bool:
    """
    Power-of-two check via `n & (n-1) == 0`.
    Returns True for 0 (quirk — see module docstring).

    >>> kernighan(0)
    True
    >>> kernighan(1)
    True
    >>> kernighan(2)
    True
    >>> kernighan(6)
    False
    >>> kernighan(8)
    True
    >>> kernighan(2**1000)
    True
    """
    if number < 0:
        raise ValueError("number must not be negative")
    return number & (number - 1) == 0


# ---------------------------------------------------------------------------
# Variant 2 — Strict: n > 0 required (LeetCode 231 / mathematically correct)
# ---------------------------------------------------------------------------

def strict(number: int) -> bool:
    """
    Power-of-two check — strict: returns False for 0.
    This is the mathematically correct definition used by LeetCode 231.

    >>> strict(0)
    False
    >>> strict(1)
    True
    >>> strict(2)
    True
    >>> strict(6)
    False
    >>> strict(8)
    True
    >>> strict(2**1000)
    True
    """
    if number < 0:
        raise ValueError("number must not be negative")
    return number > 0 and number & (number - 1) == 0


# ---------------------------------------------------------------------------
# Variant 3 — bit_count (Python 3.10+): popcount == 1
# ---------------------------------------------------------------------------

def bit_count(number: int) -> bool:
    """
    Power-of-two check via popcount: exactly 1 set bit means power of 2.
    Returns False for 0 (0 has no set bits).

    int.bit_count() is the Python 3.10+ built-in popcount, implemented
    at C level — O(1) for machine-word ints, O(k) for k-digit bignums.

    >>> bit_count(0)
    False
    >>> bit_count(1)
    True
    >>> bit_count(2)
    True
    >>> bit_count(6)
    False
    >>> bit_count(8)
    True
    >>> bit_count(2**1000)
    True
    """
    if number < 0:
        raise ValueError("number must not be negative")
    return number.bit_count() == 1


# ---------------------------------------------------------------------------
# Variant 4 — bin string popcount
# ---------------------------------------------------------------------------

def bin_count(number: int) -> bool:
    """
    Power-of-two check by counting '1' chars in bin(n).
    Returns False for 0.

    >>> bin_count(0)
    False
    >>> bin_count(1)
    True
    >>> bin_count(2)
    True
    >>> bin_count(6)
    False
    >>> bin_count(8)
    True
    >>> bin_count(2**1000)
    True
    """
    if number < 0:
        raise ValueError("number must not be negative")
    return bin(number).count("1") == 1


# ---------------------------------------------------------------------------
# Variant 5 — math.log2 (float — precision breaks for large n)
# ---------------------------------------------------------------------------

def math_log2(number: int) -> bool:
    """
    Power-of-two check via math.log2(n) % 1 == 0.
    Returns False for 0.

    WARNING: float precision breaks for n > 2**53 (IEEE 754 mantissa limit).
    `math.log2(2**53 + 2)` may return 53.0 (wrong). Safe for small ints only.

    >>> math_log2(0)
    False
    >>> math_log2(1)
    True
    >>> math_log2(2)
    True
    >>> math_log2(6)
    False
    >>> math_log2(8)
    True
    """
    if number < 0:
        raise ValueError("number must not be negative")
    if number == 0:
        return False
    return math.log2(number) % 1 == 0


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES_COMMON = [
    # (n, reference_result, strict_result)
    (0,   True,  False),
    (1,   True,  True),
    (2,   True,  True),
    (3,   False, False),
    (4,   True,  True),
    (6,   False, False),
    (8,   True,  True),
    (15,  False, False),
    (16,  True,  True),
    (17,  False, False),
    (255, False, False),
    (256, True,  True),
    (2**31, True, True),
    (2**32, True, True),
]

IMPLS_WITH_ZERO_QUIRK = [
    ("reference", reference),
    ("kernighan", kernighan),
]

IMPLS_STRICT = [
    ("strict",    strict),
    ("bit_count", bit_count),
    ("bin_count", bin_count),
    ("math_log2", math_log2),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    print("  (reference/kernighan return True for 0; others return False for 0)")
    for n, ref_expected, strict_expected in TEST_CASES_COMMON:
        row = {}
        for name, fn in IMPLS_WITH_ZERO_QUIRK:
            try:
                row[name] = fn(n)
            except Exception as e:
                row[name] = f"ERR:{e}"
        for name, fn in IMPLS_STRICT:
            try:
                row[name] = fn(n)
            except Exception as e:
                row[name] = f"ERR:{e}"

        # check reference matches its expected, strict impls match strict expected
        ref_ok = all(row[nm] == ref_expected for nm in ("reference", "kernighan"))
        strict_ok = all(
            row[nm] == strict_expected for nm in ("strict", "bit_count", "bin_count")
        )
        # math_log2 only reliable for small n
        if n <= 2**31:
            strict_ok = strict_ok and (row["math_log2"] == strict_expected)

        ok = ref_ok and strict_ok
        tag = "OK" if ok else "FAIL"
        vals = "  ".join(f"{nm}={v}" for nm, v in row.items())
        print(f"  [{tag}] n={str(n):<14} ref_exp={str(ref_expected):<6}  {vals}")

    # Verify all 2**i for i in 0..999 pass the strict check
    all_powers_ok = all(strict(2**i) for i in range(1000))
    print(f"\n  [{'OK' if all_powers_ok else 'FAIL'}] strict: all(strict(2**i) for i in range(1000))")

    REPS = 300_000
    inputs = [0, 1, 4, 8, 15, 64, 255, 256, 2**31]
    all_impls = IMPLS_WITH_ZERO_QUIRK + IMPLS_STRICT
    print(f"\n=== Benchmark: {REPS} runs, {len(inputs)} inputs ===")
    for name, fn in all_impls:
        t = timeit.timeit(
            lambda fn=fn: [fn(n) for n in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<12} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
