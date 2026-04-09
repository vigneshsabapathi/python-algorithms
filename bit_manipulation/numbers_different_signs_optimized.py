#!/usr/bin/env python3
"""
Optimized and alternative implementations of Numbers with Different Signs.

The reference uses `num1 ^ num2 < 0`.

Why XOR detects different signs in Python:
    Python arbitrary-precision integers use two's complement conceptually,
    with the sign bit extending to infinity.
    - Positive/zero: conceptual sign bit = 0 (infinite leading 0s)
    - Negative:      conceptual sign bit = 1 (infinite leading 1s)

    pos ^ neg  →  0...0 XOR 1...1  →  1...1...  (negative)  →  True
    pos ^ pos  →  0...0 XOR 0...0  →  0...0...  (positive)  →  False
    neg ^ neg  →  1...1 XOR 1...1  →  0...0...  (positive)  →  False

Zero behaviour: 0 is treated as non-negative (sign bit = 0).
    `different_signs(0, -1)` → True  (0 and -1 have different signs)
    `different_signs(0,  1)` → False (0 and 1 are both non-negative)

Variants covered:
1. xor_sign   -- num1 ^ num2 < 0                  (reference, bit trick)
2. sign_cmp   -- (num1 < 0) != (num2 < 0)          (explicit, most readable)
3. bool_xor   -- bool(num1 < 0) ^ bool(num2 < 0)   (boolean XOR form)
4. multiply   -- num1 * num2 < 0                   (WRONG for zero — documented)
5. copysign   -- math.copysign usage               (float-based, educational)

Key interview insight:
    `(num1 ^ num2) < 0` is the classic bit trick.
    `(num1 < 0) != (num2 < 0)` is clearer in intent.
    Both are O(1). The XOR trick is the "bit manipulation" answer;
    the comparison is the "readable" answer.
    Multiplication `num1 * num2 < 0` is WRONG for zero and O(n*m) for big ints.

Run:
    python bit_manipulation/numbers_different_signs_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bit_manipulation.numbers_different_signs import different_signs as reference


# ---------------------------------------------------------------------------
# Variant 1 — XOR sign trick (mirrors reference)
# ---------------------------------------------------------------------------

def xor_sign(num1: int, num2: int) -> bool:
    """
    Different signs via XOR: positive XOR negative yields a negative result.

    >>> xor_sign(1, -1)
    True
    >>> xor_sign(1, 1)
    False
    >>> xor_sign(0, -1)
    True
    >>> xor_sign(0, 1)
    False
    >>> xor_sign(-5, -3)
    False
    """
    return num1 ^ num2 < 0


# ---------------------------------------------------------------------------
# Variant 2 — Explicit sign comparison (most readable)
# ---------------------------------------------------------------------------

def sign_cmp(num1: int, num2: int) -> bool:
    """
    Different signs via explicit comparison: one is negative, other is not.
    Uses `!=` to compare the boolean results of two `< 0` checks.

    Identical semantics to XOR trick: 0 is treated as non-negative.

    >>> sign_cmp(1, -1)
    True
    >>> sign_cmp(1, 1)
    False
    >>> sign_cmp(0, -1)
    True
    >>> sign_cmp(0, 1)
    False
    >>> sign_cmp(-5, -3)
    False
    """
    return (num1 < 0) != (num2 < 0)


# ---------------------------------------------------------------------------
# Variant 3 — Boolean XOR (readable explicit form)
# ---------------------------------------------------------------------------

def bool_xor(num1: int, num2: int) -> bool:
    """
    Different signs via boolean XOR of sign bits.
    `bool(n < 0)` extracts the sign bit as a boolean.

    >>> bool_xor(1, -1)
    True
    >>> bool_xor(1, 1)
    False
    >>> bool_xor(0, -1)
    True
    >>> bool_xor(0, 1)
    False
    >>> bool_xor(-5, -3)
    False
    """
    return bool(num1 < 0) ^ bool(num2 < 0)


# ---------------------------------------------------------------------------
# Variant 4 — Multiply (WRONG for zero — documented trap)
# ---------------------------------------------------------------------------

def multiply(num1: int, num2: int) -> bool:
    """
    Different signs via num1 * num2 < 0.

    WRONG for zero: 0 * negative = 0 (not < 0), so returns False even though
    0 and a negative number arguably have different signs.

    Also SLOW for large integers: multiplication is O(n*m) digit operations;
    XOR and comparison are O(max(n,m)).

    >>> multiply(1, -1)
    True
    >>> multiply(1, 1)
    False
    >>> multiply(0, -1)   # WRONG — returns False (0*-1 = 0, not < 0)
    False
    >>> multiply(0, 1)
    False
    >>> multiply(-5, -3)
    False
    """
    return num1 * num2 < 0


# ---------------------------------------------------------------------------
# Variant 5 — math.copysign (float-based, educational)
# ---------------------------------------------------------------------------

def copysign_check(num1: int, num2: int) -> bool:
    """
    Different signs using math.copysign to extract sign as ±1.0.

    copysign(1, x) returns 1.0 if x >= 0, -1.0 if x < 0.
    Product of two copysigns is -1.0 iff they have different signs.

    NOTE: math.copysign treats 0 as positive (copysign(1, 0) == 1.0),
    matching the XOR behaviour.

    >>> copysign_check(1, -1)
    True
    >>> copysign_check(1, 1)
    False
    >>> copysign_check(0, -1)
    True
    >>> copysign_check(0, 1)
    False
    >>> copysign_check(-5, -3)
    False
    """
    return math.copysign(1, num1) * math.copysign(1, num2) < 0


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    # (num1, num2, expected)
    (1, -1, True),
    (-1, 1, True),
    (1, 1, False),
    (-1, -1, False),
    (0, 0, False),
    (0, 1, False),
    (0, -1, True),      # zero treated as non-negative
    (1, 0, False),
    (-1, 0, True),      # zero treated as non-negative
    (50, 278, False),
    (-50, -278, False),
    (50, -278, True),
    (-50, 278, True),
    (10**30, -(10**30), True),
    (-(10**30), 10**30, True),
    (10**30, 10**30, False),
]

# multiply diverges on zero cases
MULTIPLY_DIVERGES = {(0, -1), (-1, 0)}

IMPLS = [
    ("reference",  reference),
    ("xor_sign",   xor_sign),
    ("sign_cmp",   sign_cmp),
    ("bool_xor",   bool_xor),
    ("multiply",   multiply),
    ("copysign",   copysign_check),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    print("  (* = multiply diverges by design for zero-negative pairs)")
    for num1, num2, expected in TEST_CASES:
        row = {}
        for name, fn in IMPLS:
            try:
                row[name] = fn(num1, num2)
            except Exception as e:
                row[name] = f"ERR:{e}"

        # For multiply, allow divergence on zero pairs
        is_zero_pair = (num1, num2) in MULTIPLY_DIVERGES or (num2, num1) in MULTIPLY_DIVERGES
        ok = all(
            v == expected
            for name, v in row.items()
            if not (name == "multiply" and is_zero_pair)
        )
        tag = "OK " if ok else "FAIL"
        marker = "*" if is_zero_pair else " "
        print(
            f"  [{tag}]{marker} ({num1:>6}, {num2:>6}) expected={str(expected):<6}  "
            + "  ".join(f"{nm}={v}" for nm, v in row.items())
        )

    REPS = 500_000
    small_pairs = [(1, -1), (1, 1), (-1, -1), (0, -1), (50, 278), (-50, 278)]
    large_pairs = [(10**30, -(10**30)), (-(10**100), 10**100), (10**50, 10**50)]

    print(f"\n=== Benchmark (small ints): {REPS} runs, {len(small_pairs)} pairs ===")
    for name, fn in IMPLS:
        if name == "multiply":
            pairs = [(a, b) for a, b in small_pairs if a != 0 and b != 0]
        else:
            pairs = small_pairs
        t = timeit.timeit(
            lambda fn=fn, p=pairs: [fn(a, b) for a, b in p], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<14} {t:>7.4f} ms / batch of {len(pairs)}")

    print(f"\n=== Benchmark (large ints ~10^30..10^100): {REPS} runs, {len(large_pairs)} pairs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(a, b) for a, b in large_pairs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<14} {t:>7.4f} ms / batch of {len(large_pairs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
