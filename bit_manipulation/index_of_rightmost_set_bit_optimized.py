#!/usr/bin/env python3
"""
Optimized and alternative implementations for Index of Rightmost Set Bit.

The reference isolates the LSB via `n & ~(n-1)` then shifts right in a loop
counting steps — O(log n).  Python's `bit_length()` makes this O(1).

Key identity: `n & ~(n-1)` == `n & -n`  (two's complement trick).
  Proof: -n == ~n + 1  =>  ~(n-1) == ~n + 1 == -n
  So `n & ~(n-1)` always equals `n & -n`.

Variants covered:
1. two_complement  -- (n & -n).bit_length() - 1          O(1)
2. bin_string      -- trailing-zero count via binary string O(log n)
3. math_log2       -- int(math.log2(n & -n))               O(1) but float
4. debruijn        -- DeBruijn sequence lookup (32-bit)     O(1)

Key interview insight:
    `(n & -n).bit_length() - 1` is the production answer.
    `n & -n` is the classic two's complement trick to isolate the lowest set bit.
    The DeBruijn approach impresses but is for fixed-width integers (C/Java).

    Index is 0-based: bit 0 is the LSB (rightmost).
    Returns -1 for n == 0 (no bits set).

Run:
    python bit_manipulation/index_of_rightmost_set_bit_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bit_manipulation.index_of_rightmost_set_bit import (
    get_index_of_rightmost_set_bit as reference,
)


# ---------------------------------------------------------------------------
# Variant 1 — two's complement isolation + bit_length (O(1))
# ---------------------------------------------------------------------------

def two_complement(number: int) -> int:
    """
    Rightmost set bit index via `n & -n` and bit_length.

    `n & -n` isolates the lowest set bit into a power of 2.
    `bit_length() - 1` converts that power of 2 to a 0-based index.

    >>> two_complement(0)
    -1
    >>> two_complement(1)
    0
    >>> two_complement(5)
    0
    >>> two_complement(36)
    2
    >>> two_complement(8)
    3
    >>> two_complement(256)
    8
    """
    if not isinstance(number, int) or number < 0:
        raise ValueError("Input must be a non-negative integer")
    return (number & -number).bit_length() - 1


# ---------------------------------------------------------------------------
# Variant 2 — binary string trailing-zero count
# ---------------------------------------------------------------------------

def bin_string(number: int) -> int:
    """
    Rightmost set bit index by counting trailing '0' chars in bin(n).

    bin(36) = '0b100100'  → strip prefix → '100100'
    Reverse → '001001' → index of first '1' = 2

    >>> bin_string(0)
    -1
    >>> bin_string(1)
    0
    >>> bin_string(5)
    0
    >>> bin_string(36)
    2
    >>> bin_string(8)
    3
    >>> bin_string(256)
    8
    """
    if not isinstance(number, int) or number < 0:
        raise ValueError("Input must be a non-negative integer")
    if number == 0:
        return -1
    s = bin(number)[2:]  # strip '0b'
    return len(s) - len(s.rstrip('0'))


# ---------------------------------------------------------------------------
# Variant 3 — math.log2 of isolated LSB (float — precision trap for large n)
# ---------------------------------------------------------------------------

def math_log2(number: int) -> int:
    """
    Rightmost set bit index via math.log2(n & -n).

    WARNING: float precision breaks for n > 2**53 (IEEE 754 mantissa limit).
    Safe for typical 32-bit integer problems.

    >>> math_log2(0)
    -1
    >>> math_log2(1)
    0
    >>> math_log2(5)
    0
    >>> math_log2(36)
    2
    >>> math_log2(8)
    3
    >>> math_log2(256)
    8
    """
    if not isinstance(number, int) or number < 0:
        raise ValueError("Input must be a non-negative integer")
    if number == 0:
        return -1
    return int(math.log2(number & -number))


# ---------------------------------------------------------------------------
# Variant 4 — DeBruijn sequence lookup (32-bit integers only)
# ---------------------------------------------------------------------------
# Classic C bithack adapted to Python.
# Multiply the isolated LSB by a DeBruijn constant, shift right 27 bits,
# and use the result as an index into a precomputed 32-entry table.
# Only correct for values < 2**32.

_DEBRUIJN32 = 0x077CB531
_DEBRUIJN32_TABLE = [0] * 32
for _i in range(32):
    _DEBRUIJN32_TABLE[(_DEBRUIJN32 << _i & 0xFFFFFFFF) >> 27] = _i


def debruijn32(number: int) -> int:
    """
    Rightmost set bit index for 32-bit non-negative integers via DeBruijn sequence.

    Multiply the isolated LSB by a magic DeBruijn constant, take the top 5 bits,
    and look up in a 32-entry table.  O(1), no branches beyond the guard.
    Only correct for 0 <= number < 2**32.

    >>> debruijn32(0)
    -1
    >>> debruijn32(1)
    0
    >>> debruijn32(5)
    0
    >>> debruijn32(36)
    2
    >>> debruijn32(8)
    3
    >>> debruijn32(256)
    8
    >>> debruijn32(2**31)
    31
    """
    if not isinstance(number, int) or number < 0:
        raise ValueError("Input must be a non-negative integer")
    if number == 0:
        return -1
    lsb = number & -number
    return _DEBRUIJN32_TABLE[((_DEBRUIJN32 * lsb) & 0xFFFFFFFF) >> 27]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (0, -1),
    (1, 0),
    (2, 1),
    (4, 2),
    (5, 0),
    (8, 3),
    (12, 2),
    (36, 2),
    (255, 0),
    (256, 8),
    (1024, 10),
    (2**31, 31),
]

IMPLS = [
    ("reference",   reference),
    ("two_compl",   two_complement),
    ("bin_string",  bin_string),
    ("math_log2",   math_log2),
    ("debruijn32",  debruijn32),
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
            f"  [{tag}] n={str(n):<14} expected={expected:<4}  "
            + "  ".join(f"{nm}={v}" for nm, v in results.items())
        )

    REPS = 200_000
    inputs = [0, 1, 2, 5, 8, 36, 255, 256, 1024]
    print(f"\n=== Benchmark: {REPS} runs, {len(inputs)} inputs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(n) for n in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<12} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
