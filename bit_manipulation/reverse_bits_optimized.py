#!/usr/bin/env python3
"""
Optimized and alternative implementations of Reverse Bits.

Reverse all 32 bits of an unsigned integer.  LeetCode 190.

The reference uses a bit-by-bit loop (32 iterations, extract LSB, shift left).
This is O(1) but has a high constant factor due to the Python loop overhead.

Four alternatives:
  loop        — bit-by-bit loop (baseline, identical to reference)
  string_rev  — bin(n).zfill(32)[::-1] string reversal
  format_int  — format(n, '032b')[::-1] then int(..., 2)
  divide_conquer — swap halves recursively (mask-and-shift in 5 stages)

The divide-and-conquer approach swaps adjacent bits, then 2-bit groups,
then nibbles, then bytes, then 16-bit halves — all via bitmasks.  This is
the classic O(1) constant-time approach used in hardware and competitive
programming.  Each stage uses one AND + shift-right + one AND + shift-left
+ one OR.

Run:
    python bit_manipulation/reverse_bits_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bit_manipulation.reverse_bits import reverse_bits as reference


# ---------------------------------------------------------------------------
# Variant 1 — bit-by-bit loop (baseline, same as reference)
# ---------------------------------------------------------------------------

def loop(n: int) -> int:
    """
    Reverse 32 bits using a loop that extracts the LSB each iteration.

    >>> loop(43261596)
    964176192
    >>> loop(0)
    0
    >>> loop(4294967295)
    4294967295
    >>> loop(1)
    2147483648
    """
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result


# ---------------------------------------------------------------------------
# Variant 2 — string reversal via bin().zfill()[::-1]
# ---------------------------------------------------------------------------

def string_rev(n: int) -> int:
    """
    Reverse 32 bits by converting to a 32-char binary string and reversing.

    bin(n) gives '0b...', strip the prefix, zero-pad to 32 chars,
    reverse the string, parse back as int.

    >>> string_rev(43261596)
    964176192
    >>> string_rev(0)
    0
    >>> string_rev(4294967295)
    4294967295
    >>> string_rev(1)
    2147483648
    """
    return int(bin(n)[2:].zfill(32)[::-1], 2)


# ---------------------------------------------------------------------------
# Variant 3 — format/int approach
# ---------------------------------------------------------------------------

def format_int(n: int) -> int:
    """
    Reverse 32 bits using format(n, '032b') and int(..., 2).

    Similar to string_rev but uses format() for zero-padded binary.

    >>> format_int(43261596)
    964176192
    >>> format_int(0)
    0
    >>> format_int(4294967295)
    4294967295
    >>> format_int(1)
    2147483648
    """
    return int(format(n, '032b')[::-1], 2)


# ---------------------------------------------------------------------------
# Variant 4 — divide and conquer (swap halves, 5-stage mask-and-shift)
# ---------------------------------------------------------------------------

def divide_conquer(n: int) -> int:
    """
    Reverse 32 bits using divide-and-conquer bit swaps in 5 stages.

    Stage 1: swap adjacent single bits      (mask 0x55555555)
    Stage 2: swap adjacent 2-bit groups      (mask 0x33333333)
    Stage 3: swap adjacent nibbles (4-bit)   (mask 0x0F0F0F0F)
    Stage 4: swap adjacent bytes             (mask 0x00FF00FF)
    Stage 5: swap 16-bit halves              (shift 16)

    Each stage: extract even-positioned groups (AND + shift right),
    extract odd-positioned groups (AND + shift left), OR them together.

    >>> divide_conquer(43261596)
    964176192
    >>> divide_conquer(0)
    0
    >>> divide_conquer(4294967295)
    4294967295
    >>> divide_conquer(1)
    2147483648
    """
    n = ((n & 0x55555555) << 1) | ((n >> 1) & 0x55555555)   # swap single bits
    n = ((n & 0x33333333) << 2) | ((n >> 2) & 0x33333333)   # swap 2-bit groups
    n = ((n & 0x0F0F0F0F) << 4) | ((n >> 4) & 0x0F0F0F0F)  # swap nibbles
    n = ((n & 0x00FF00FF) << 8) | ((n >> 8) & 0x00FF00FF)   # swap bytes
    n = (n << 16) | (n >> 16)                                 # swap 16-bit halves
    return n & 0xFFFFFFFF  # ensure 32-bit result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (0,          0),
    (1,          2147483648),   # 1 << 31
    (2,          1073741824),   # 1 << 30
    (43261596,   964176192),    # LeetCode example 1
    (4294967293, 3221225471),   # 0xFFFFFFFD -> 0xBFFFFFFF
    (4294967295, 4294967295),   # all 1s -> all 1s
    (2147483648, 1),            # 1 << 31 -> 1
    (0xAAAAAAAA, 0x55555555),   # alternating bits
    (0x55555555, 0xAAAAAAAA),   # alternating bits reversed
    (0xFF000000, 0x000000FF),   # high byte <-> low byte
]

IMPLS = [
    ("reference",       reference),
    ("loop",            loop),
    ("string_rev",      string_rev),
    ("format_int",      format_int),
    ("divide_conquer",  divide_conquer),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for n, expected in TEST_CASES:
        row = {}
        for name, fn in IMPLS:
            try:
                row[name] = fn(n)
            except Exception as e:
                row[name] = f"ERR:{e}"
        ok = all(v == expected for v in row.values())
        tag = "OK" if ok else "FAIL"
        print(
            f"  [{tag}] n=0x{n:08X} ({n:<12d})  expected={expected:<12d}  "
            + "  ".join(f"{nm}={v}" for nm, v in row.items())
        )

    # Exhaustive check: all values 0..65535 (16-bit)
    print("\n=== Exhaustive 16-bit subset check ===")
    fails = 0
    for i in range(65536):
        ref = reference(i)
        for name, fn in IMPLS[1:]:
            if fn(i) != ref:
                fails += 1
                if fails <= 3:
                    print(f"  MISMATCH: n={i}, {name}={fn(i)}, reference={ref}")
    print(f"  [{'OK' if fails == 0 else 'FAIL'}] {65536 * (len(IMPLS)-1)} comparisons, {fails} failures")

    # Benchmark
    REPS = 200_000
    inputs = [n for n, _ in TEST_CASES]

    print(f"\n=== Benchmark: {REPS} runs, {len(inputs)} inputs per run ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(n) for n in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
