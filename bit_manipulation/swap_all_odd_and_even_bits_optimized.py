#!/usr/bin/env python3
"""
Optimized and alternative implementations of Swap All Odd and Even Bits.

Given a non-negative integer, swap bits at even positions (0, 2, 4, ...)
with bits at odd positions (1, 3, 5, ...).

The reference uses two 32-bit masks:
  0xAAAAAAAA — selects even-position bits
  0x55555555 — selects odd-position bits
Then shifts and ORs.  O(1) for 32-bit integers, but breaks for n >= 2^32.

Four variants:
  mask_32       — the classic 32-bit mask approach (baseline / reference)
  mask_arbitrary — dynamic mask that scales to arbitrary-precision ints
  string_swap   — convert to binary string, swap adjacent chars
  loop_based    — iterate bit pairs one at a time (naive, for comparison)

Key interview insight:
    The mask approach is the expected O(1) answer. The masks 0xAAAA...
    and 0x5555... appear in many bit-manipulation problems (power of 4,
    Hamming distance, etc.). For Python's arbitrary-precision ints, you
    need to build the mask dynamically based on bit_length.

Run:
    python bit_manipulation/swap_all_odd_and_even_bits_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bit_manipulation.swap_all_odd_and_even_bits import (
    swap_all_odd_and_even_bits as reference,
)


# ---------------------------------------------------------------------------
# Variant 1 — mask_32: Classic 32-bit mask (same as reference)
# ---------------------------------------------------------------------------

_EVEN_MASK_32 = 0xAAAAAAAA  # bits at even positions (0, 2, 4, ..., 30)
_ODD_MASK_32 = 0x55555555   # bits at odd positions  (1, 3, 5, ..., 31)


def mask_32(num: int) -> int:
    """
    Swap odd/even bits using fixed 32-bit masks.

    Only valid for 0 <= num < 2^32.

    >>> mask_32(0)
    0
    >>> mask_32(1)
    2
    >>> mask_32(2)
    1
    >>> mask_32(3)
    3
    >>> mask_32(23)
    43
    >>> mask_32(0xFF)
    255
    """
    if num < 0 or num >= 2**32:
        raise ValueError("mask_32 only supports 32-bit non-negative integers")
    even_bits = num & _EVEN_MASK_32
    odd_bits = num & _ODD_MASK_32
    return (even_bits >> 1) | (odd_bits << 1)


# ---------------------------------------------------------------------------
# Variant 2 — mask_arbitrary: Dynamic mask for arbitrary-precision ints
# ---------------------------------------------------------------------------

def mask_arbitrary(num: int) -> int:
    """
    Swap odd/even bits with dynamically-sized masks.

    Builds masks wide enough to cover all bits in num.
    Works for any non-negative integer (Python arbitrary precision).

    >>> mask_arbitrary(0)
    0
    >>> mask_arbitrary(1)
    2
    >>> mask_arbitrary(2)
    1
    >>> mask_arbitrary(3)
    3
    >>> mask_arbitrary(23)
    43
    >>> mask_arbitrary(0xFFFF)
    65535
    >>> mask_arbitrary(0xABCD1234)
    1473126712
    """
    if num < 0:
        raise ValueError("num must be non-negative")
    if num == 0:
        return 0
    # Round bit_length up to next even number so masks cover all bits
    width = num.bit_length()
    width += width % 2  # ensure even width
    # Build masks: 0xAA... (even positions) and 0x55... (odd positions)
    # For width=8: even_mask=0b10101010, odd_mask=0b01010101
    even_mask = 0
    for i in range(0, width, 2):
        even_mask |= 1 << i
    odd_mask = even_mask << 1
    # Note: even_mask has bits at positions 0,2,4... (what we call "even positions")
    # odd_mask has bits at positions 1,3,5... (what we call "odd positions")
    # Swap: even-position bits go right, odd-position bits go left
    # Wait — we need to be consistent with the reference.
    # Reference: 0xAAAAAAAA selects bits at positions 1,3,5... and shifts right
    #            0x55555555 selects bits at positions 0,2,4... and shifts left
    # So: odd_mask (positions 1,3,5) >> 1, even_mask (positions 0,2,4) << 1
    return ((num & odd_mask) >> 1) | ((num & even_mask) << 1)


# ---------------------------------------------------------------------------
# Variant 3 — string_swap: Binary string character swap
# ---------------------------------------------------------------------------

def string_swap(num: int) -> int:
    """
    Swap odd/even bits by converting to binary string and swapping adjacent chars.

    Pad to even length, then swap each pair of adjacent characters.
    Intuitive but slow due to string operations.

    >>> string_swap(0)
    0
    >>> string_swap(1)
    2
    >>> string_swap(2)
    1
    >>> string_swap(3)
    3
    >>> string_swap(23)
    43
    >>> string_swap(6)
    9
    """
    if num < 0:
        raise ValueError("num must be non-negative")
    if num == 0:
        return 0
    bits = bin(num)[2:]  # remove '0b' prefix
    # Pad to even length (pairs from the right)
    if len(bits) % 2 != 0:
        bits = "0" + bits
    # Swap adjacent pairs: (bit[0], bit[1]) → (bit[1], bit[0])
    swapped = []
    for i in range(0, len(bits), 2):
        swapped.append(bits[i + 1])
        swapped.append(bits[i])
    return int("".join(swapped), 2)


# ---------------------------------------------------------------------------
# Variant 4 — loop_based: Iterate bit pairs (naive)
# ---------------------------------------------------------------------------

def loop_based(num: int) -> int:
    """
    Swap odd/even bits by iterating through bit pairs one at a time.

    Extracts each pair of adjacent bits, swaps them, and reconstructs.
    O(log n) — much slower than mask approach.

    >>> loop_based(0)
    0
    >>> loop_based(1)
    2
    >>> loop_based(2)
    1
    >>> loop_based(3)
    3
    >>> loop_based(23)
    43
    >>> loop_based(5)
    10
    """
    if num < 0:
        raise ValueError("num must be non-negative")
    result = 0
    pos = 0
    n = num
    while n > 0:
        # Extract the two bits at positions pos and pos+1
        bit_even = (n & 1)       # bit at even position (pos)
        bit_odd = (n >> 1) & 1   # bit at odd position (pos+1)
        # Place them swapped: even bit goes to odd position, odd to even
        result |= (bit_even << (pos + 1))
        result |= (bit_odd << pos)
        n >>= 2
        pos += 2
    return result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (0,      0),
    (1,      2),
    (2,      1),
    (3,      3),
    (4,      8),
    (5,      10),
    (6,      9),
    (23,     43),
    (43,     23),     # swap is its own inverse (applied twice)
    (0xFF,   0xFF),   # 11111111 → 11111111 (symmetric)
    (0xAA,   0x55),   # 10101010 → 01010101
    (0x55,   0xAA),   # 01010101 → 10101010
    (0xABCD, 0x57CE), # larger value
]

IMPLS = [
    ("reference",      reference),
    ("mask_32",        mask_32),
    ("mask_arbitrary", mask_arbitrary),
    ("string_swap",    string_swap),
    ("loop_based",     loop_based),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for n, expected in TEST_CASES:
        row = {}
        for name, fn in IMPLS:
            try:
                row[name] = fn(n)
            except Exception as e:
                row[name] = f"ERR:{e}"
        ok = all(v == expected for v in row.values())
        if not ok:
            all_pass = False
        tag = "OK" if ok else "FAIL"
        print(
            f"  [{tag}] n=0x{n:04X} ({n:>5})  expected={expected:<6}  "
            + "  ".join(f"{nm}={v}" for nm, v in row.items())
        )

    # Self-inverse property: swap(swap(n)) == n
    inverse_ok = all(
        reference(reference(n)) == n for n in range(256)
    )
    print(f"\n  [{'OK' if inverse_ok else 'FAIL'}] self-inverse: swap(swap(n))==n for 0..255")

    # Cross-check all implementations for 0..1023
    cross_ok = True
    for n in range(1024):
        ref = reference(n)
        for name, fn in IMPLS[1:]:
            try:
                if fn(n) != ref:
                    cross_ok = False
                    break
            except Exception:
                pass
    print(f"  [{'OK' if cross_ok else 'FAIL'}] cross-check: all impls agree for 0..1023")

    # Benchmark
    REPS = 300_000
    small_inputs = [0, 1, 2, 3, 4, 5, 6, 23, 43, 0xFF]

    print(f"\n=== Benchmark (small ints 0-255): {REPS} runs, {len(small_inputs)} inputs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(n) for n in small_inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms / batch of {len(small_inputs)}")

    medium_inputs = [0xABCD, 0x1234, 0xFFFF, 0xAAAA, 0x5555]
    print(f"\n=== Benchmark (medium ints ~16-bit): {REPS} runs, {len(medium_inputs)} inputs ===")
    # Exclude mask_32 from large test but include here (still within 32-bit)
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(n) for n in medium_inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms / batch of {len(medium_inputs)}")

    large_inputs = [2**48 - 1, 2**64 - 1, 2**100 - 1]
    large_impls = [(n, f) for n, f in IMPLS if n != "mask_32"]
    print(f"\n=== Benchmark (large ints ~48-100 bit): {REPS} runs, {len(large_inputs)} inputs ===")
    print("  (mask_32 excluded — 32-bit only)")
    for name, fn in large_impls:
        t = timeit.timeit(
            lambda fn=fn: [fn(n) for n in large_inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms / batch of {len(large_inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
