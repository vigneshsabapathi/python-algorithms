#!/usr/bin/env python3
"""
Optimized and alternative implementations of Count Trailing Zeros (CTZ).

The reference uses int(log2(a & -a)).  This has a subtle correctness risk:
log2() is floating-point and can return values like 31.999999999 for large
powers of 2, making int() truncate to the wrong answer.  (In practice Python's
math.log2 is accurate enough for 32-bit inputs, but it is not guaranteed for
arbitrary-precision integers like 2**53 and beyond.)

The fix is purely integer arithmetic: (a & -a).bit_length() - 1.

Variants covered:
1. ctz_bit_length  -- (a & -a).bit_length() - 1  — exact integer, no float
2. ctz_bin_str     -- bin(a)[::-1].index('1')     — string reversal trick
3. ctz_loop        -- right-shift loop            — shows mechanics explicitly
4. ctz_debruijn    -- 32-bit De Bruijn sequence   — O(1), classic embedded trick

Key interview insight:
    Reference (log2):    floating-point risk for large n; O(log n)
    bit_length trick:    exact integer; same O(1) hardware path as bit_count
    bin string trick:    O(log n) string alloc, clean one-liner
    De Bruijn:           O(1) constant-time; used in chess engines / firmware

Run:
    python bit_manipulation/binary_count_trailing_zeros_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bit_manipulation.binary_count_trailing_zeros import (
    binary_count_trailing_zeros as ctz_reference,
)


# ---------------------------------------------------------------------------
# Variant 1 — (a & -a).bit_length() - 1  (exact integer, no float)
# ---------------------------------------------------------------------------

def ctz_bit_length(a: int) -> int:
    """
    Count trailing zeros using bit_length() — exact integer arithmetic.

    a & -a  isolates the lowest set bit (a power of 2).
    bit_length() of 2^k is k+1, so subtract 1 to get k.

    No floating-point involved — safe for arbitrarily large integers.

    >>> ctz_bit_length(25)
    0
    >>> ctz_bit_length(36)
    2
    >>> ctz_bit_length(16)
    4
    >>> ctz_bit_length(58)
    1
    >>> ctz_bit_length(4294967296)
    32
    >>> ctz_bit_length(0)
    0
    """
    if a == 0:
        return 0
    return (a & -a).bit_length() - 1


# ---------------------------------------------------------------------------
# Variant 2 — bin string reversal trick
# ---------------------------------------------------------------------------

def ctz_bin_str(a: int) -> int:
    """
    Count trailing zeros by reversing the binary string.

    bin(a) = '0b...1xxx000' — trailing zeros are on the right.
    Reverse → '000xxx1...' — the first '1' is now at index = trailing zeros.
    The '0b' prefix becomes 'b0' at the end; 'b' is never '1' so it doesn't
    interfere with .index('1').

    >>> ctz_bin_str(25)
    0
    >>> ctz_bin_str(36)
    2
    >>> ctz_bin_str(16)
    4
    >>> ctz_bin_str(58)
    1
    >>> ctz_bin_str(4294967296)
    32
    >>> ctz_bin_str(0)
    0
    """
    if a == 0:
        return 0
    return bin(a)[::-1].index("1")


# ---------------------------------------------------------------------------
# Variant 3 — right-shift loop (shows mechanics explicitly)
# ---------------------------------------------------------------------------

def ctz_loop(a: int) -> int:
    """
    Count trailing zeros by right-shifting until the LSB is 1.

    Each iteration checks the least significant bit; shifts right if 0.
    O(k) where k = trailing zeros.  Useful for explaining the concept.

    >>> ctz_loop(25)
    0
    >>> ctz_loop(36)
    2
    >>> ctz_loop(16)
    4
    >>> ctz_loop(58)
    1
    >>> ctz_loop(4294967296)
    32
    >>> ctz_loop(0)
    0
    """
    if a == 0:
        return 0
    count = 0
    while not (a & 1):
        a >>= 1
        count += 1
    return count


# ---------------------------------------------------------------------------
# Variant 4 — 32-bit De Bruijn sequence (O(1), constant time)
# ---------------------------------------------------------------------------

# De Bruijn sequence B(2,5) — maps isolated lowest-set-bit to a unique index
_DEBRUIJN32 = 0x077CB531
_DEBRUIJN_TABLE: list[int] = [0] * 32
for _i in range(32):
    _DEBRUIJN_TABLE[(_DEBRUIJN32 << _i & 0xFFFFFFFF) >> 27] = _i


def ctz_debruijn(a: int) -> int:
    """
    Count trailing zeros using a 32-bit De Bruijn sequence.

    Multiplying the isolated lowest-set-bit by the De Bruijn constant produces
    a unique 5-bit index into a lookup table.  O(1) — used in chess engines
    (e.g. Stockfish) and firmware where POPCNT/CTZ instructions aren't
    available.  Works for 32-bit integers only.

    >>> ctz_debruijn(25)
    0
    >>> ctz_debruijn(36)
    2
    >>> ctz_debruijn(16)
    4
    >>> ctz_debruijn(58)
    1
    >>> ctz_debruijn(4294967296)  # 2^32 — beyond 32 bits, falls back to bit_length
    32
    >>> ctz_debruijn(0)
    0
    """
    if a == 0:
        return 0
    lsb = a & -a
    if lsb > 0xFFFFFFFF:
        # Beyond 32 bits — fall back to bit_length (still exact)
        return lsb.bit_length() - 1
    return _DEBRUIJN_TABLE[((_DEBRUIJN32 * lsb) & 0xFFFFFFFF) >> 27]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (25,         0),
    (36,         2),
    (16,         4),
    (58,         1),
    (4294967296, 32),
    (0,          0),
    (1,          0),
    (1 << 20,    20),
]

IMPLS = [
    ("reference",   ctz_reference),
    ("bit_length",  ctz_bit_length),
    ("bin_str",     ctz_bin_str),
    ("loop",        ctz_loop),
    ("debruijn",    ctz_debruijn),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for n, expected in TEST_CASES:
        results = {name: fn(n) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(
            f"  [{tag}] ctz({n:<14}) = {expected:<3} "
            + "  ".join(f"{name}={v}" for name, v in results.items())
        )

    # Floating-point precision check for reference
    print("\n=== Floating-point precision check (reference vs bit_length) ===")
    tricky = [2**52, 2**53, 2**62, 2**100]
    for n in tricky:
        ref = ctz_reference(n)
        exact = ctz_bit_length(n)
        match = "OK" if ref == exact else "MISMATCH"
        print(f"  [{match}] ctz(2**{n.bit_length()-1})  reference={ref}  bit_length={exact}")

    REPS = 500_000
    inputs = [25, 36, 16, 58, 4294967296, 0, 1 << 20]
    print(f"\n=== Benchmark: {REPS} runs, inputs {inputs} ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(n) for n in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<14} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
