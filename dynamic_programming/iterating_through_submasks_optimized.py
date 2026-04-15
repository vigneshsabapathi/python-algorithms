#!/usr/bin/env python3
"""
Optimized and alternative implementations of Iterating Through Submasks.

Three variants:
  bit_decrement   — (s-1) & mask trick (reference, optimal)
  recursive       — recursive enumeration of submasks
  brute_force     — check all numbers 0..mask (naive baseline)

Run:
    python dynamic_programming/iterating_through_submasks_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.iterating_through_submasks import list_of_submasks as reference


# ---------------------------------------------------------------------------
# Variant 1 — bit_decrement (same as reference)
# ---------------------------------------------------------------------------

def bit_decrement(mask: int) -> list[int]:
    """
    >>> bit_decrement(13)
    [13, 12, 9, 8, 5, 4, 1]
    """
    return reference(mask)


# ---------------------------------------------------------------------------
# Variant 2 — recursive: Recursive submask enumeration
# ---------------------------------------------------------------------------

def recursive(mask: int) -> list[int]:
    """
    >>> recursive(13)
    [13, 12, 9, 8, 5, 4, 1]
    """
    assert isinstance(mask, int) and mask > 0
    result: list[int] = []

    # Get positions of set bits
    bits = []
    temp = mask
    pos = 0
    while temp:
        if temp & 1:
            bits.append(pos)
        temp >>= 1
        pos += 1

    def generate(idx: int, current: int) -> None:
        if idx == len(bits):
            if current > 0:
                result.append(current)
            return
        # Include this bit
        generate(idx + 1, current | (1 << bits[idx]))
        # Exclude this bit
        generate(idx + 1, current)

    generate(0, 0)
    result.sort(reverse=True)
    return result


# ---------------------------------------------------------------------------
# Variant 3 — brute_force: Check all numbers (naive)
# ---------------------------------------------------------------------------

def brute_force(mask: int) -> list[int]:
    """
    >>> brute_force(13)
    [13, 12, 9, 8, 5, 4, 1]
    """
    assert isinstance(mask, int) and mask > 0
    result = []
    for i in range(mask, 0, -1):
        if (i & mask) == i:
            result.append(i)
    return result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

IMPLS = [
    ("bit_decrement", bit_decrement),
    ("recursive", recursive),
    ("brute_force", brute_force),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for mask in [7, 13, 15, 31, 255]:
        ref = reference(mask)
        for name, fn in IMPLS:
            result = fn(mask)
            ok = result == ref
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}({mask}) — {len(result)} submasks")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    REPS = 10_000
    print(f"\n=== Benchmark (mask=255, 255 submasks): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(255), number=REPS) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
