#!/usr/bin/env python3
"""
Optimized and alternative implementations of the Luhn Algorithm.

The Luhn algorithm validates identification numbers (credit cards, IMEI, etc.)
by doubling every second digit from the right, subtracting 9 if > 9, summing
all digits, and checking if the total is divisible by 10.

Variants:
  reference     -- TheAlgorithms implementation (reverse + enumerate)
  lookup_table  -- pre-computed doubled-digit table (avoids conditionals)
  generator     -- generator expression one-liner
  generate_check -- compute the check digit for a number

Run:
    python hashes/luhn_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hashes.luhn import is_luhn as reference


# Pre-computed lookup: doubled[d] = (d*2) if d*2 <= 9 else (d*2 - 9)
_DOUBLED = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]


# ---------------------------------------------------------------------------
# Variant 1 -- lookup_table: pre-computed doubling results
# ---------------------------------------------------------------------------

def lookup_table(string: str) -> bool:
    """
    Luhn validation using a pre-computed lookup table for doubled digits.

    Eliminates the if/else branch in the inner loop.

    >>> lookup_table('79927398713')
    True
    >>> lookup_table('79927398714')
    False
    >>> lookup_table('4532015112830366')
    True
    >>> lookup_table('0')
    True
    """
    digits = [int(c) for c in string]
    total = 0
    # Process from right to left: index 0 = check digit (not doubled)
    for i, d in enumerate(reversed(digits)):
        if i & 1:  # odd position from right = double
            total += _DOUBLED[d]
        else:
            total += d
    return total % 10 == 0


# ---------------------------------------------------------------------------
# Variant 2 -- generator: one-liner with generator expression
# ---------------------------------------------------------------------------

def generator(string: str) -> bool:
    """
    Luhn validation via generator expression.

    >>> generator('79927398713')
    True
    >>> generator('79927398714')
    False
    >>> generator('0')
    True
    """
    digits = [int(c) for c in reversed(string)]
    return sum(
        _DOUBLED[d] if i & 1 else d
        for i, d in enumerate(digits)
    ) % 10 == 0


# ---------------------------------------------------------------------------
# Variant 3 -- generate_check: compute the Luhn check digit
# ---------------------------------------------------------------------------

def generate_check_digit(number: str) -> int:
    """
    Generate the Luhn check digit for a given number string.

    Append this digit to the number to make it pass Luhn validation.

    >>> generate_check_digit('7992739871')
    3
    >>> is_valid = lookup_table('7992739871' + str(generate_check_digit('7992739871')))
    >>> is_valid
    True

    >>> generate_check_digit('453201511283036')
    6
    """
    # Append a 0, compute Luhn sum, then find what makes it mod 10 == 0
    digits = [int(c) for c in reversed(number)]
    total = 0
    for i, d in enumerate(digits):
        # Shift: the appended check digit will be at position 0,
        # so existing digits shift by 1 (odd positions get doubled)
        if i & 1 == 0:  # even index = odd position after check digit
            total += _DOUBLED[d]
        else:
            total += d
    return (10 - (total % 10)) % 10


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

VALID_NUMBERS = [
    "79927398713",
    "4532015112830366",
    "0",
    "49927398716",
    "1234567812345670",
]

INVALID_NUMBERS = [
    "79927398714",
    "79927398710",
    "1234567812345678",
]

IMPLS = [
    ("reference", reference),
    ("lookup_table", lookup_table),
    ("generator", generator),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for num in VALID_NUMBERS:
        row = {name: fn(num) for name, fn in IMPLS}
        ok = all(row.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] is_luhn({num}) = True  {row}")

    for num in INVALID_NUMBERS:
        row = {name: fn(num) for name, fn in IMPLS}
        ok = all(not v for v in row.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] is_luhn({num}) = False  {row}")

    # Check digit generation
    for base, expected_check in [("7992739871", 3), ("453201511283036", 6)]:
        check = generate_check_digit(base)
        full = base + str(check)
        valid = lookup_table(full)
        ok = check == expected_check and valid
        print(f"  [{'OK' if ok else 'FAIL'}] generate_check_digit({base}) = {check}, valid={valid}")

    # Exhaustive: all 10 check digits for prefix "7992739871"
    prefix = "7992739871"
    valid_count = sum(1 for d in range(10) if lookup_table(prefix + str(d)))
    print(f"  [{'OK' if valid_count == 1 else 'FAIL'}] Exactly 1 valid check digit for '{prefix}': {valid_count}")

    REPS = 200_000
    test_numbers = VALID_NUMBERS + INVALID_NUMBERS

    print(f"\n=== Benchmark: {REPS} runs, {len(test_numbers)} numbers ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(n) for n in test_numbers], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<14} {t:>8.4f} ms / batch of {len(test_numbers)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
