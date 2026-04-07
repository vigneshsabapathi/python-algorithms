#!/usr/bin/env python3
"""
Comparison of popcount methods centred on Brian Kernighan's algorithm.

Brian Kernighan's insight: n & (n-1) clears the LOWEST set bit of n in one
operation.  Loop runs exactly k times where k = number of set bits.
For sparse integers (few 1s) this is faster than scanning all bits.

This file benchmarks Kernighan against the full popcount family:
1. kernighan    -- n &= n-1 loop (this file's algorithm)
2. bit_count    -- n.bit_count()  Python 3.10+ POPCNT  [fastest]
3. bin_count    -- bin(n).count("1")
4. lookup8      -- 256-entry byte lookup table

Run: python bit_manipulation/count_1s_brian_kernighan_method_optimized.py
"""

from __future__ import annotations
import sys, os, timeit
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bit_manipulation.count_1s_brian_kernighan_method import get_1s_count as kernighan_ref

_LOOKUP8: list[int] = [bin(i).count("1") for i in range(256)]


def popcount_bit_count(n: int) -> int:
    """
    Python 3.10+ built-in — maps to hardware POPCNT instruction.

    >>> popcount_bit_count(25)
    3
    >>> popcount_bit_count(0)
    0
    >>> popcount_bit_count(4294967295)
    32
    """
    return n.bit_count()


def popcount_bin(n: int) -> int:
    """
    bin(n).count("1") — O(log n), readable one-liner.

    >>> popcount_bin(25)
    3
    >>> popcount_bin(0)
    0
    >>> popcount_bin(4294967295)
    32
    """
    return bin(n).count("1")


def popcount_kernighan(n: int) -> int:
    """
    Brian Kernighan: n &= n-1 clears lowest set bit each iteration.
    Loop runs k times (k = set bits). O(k), best for sparse integers.

    >>> popcount_kernighan(25)
    3
    >>> popcount_kernighan(0)
    0
    >>> popcount_kernighan(4294967295)
    32
    """
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


def popcount_lookup8(n: int) -> int:
    """
    8-bit lookup table — one dict access per byte, O(n/8).

    >>> popcount_lookup8(25)
    3
    >>> popcount_lookup8(0)
    0
    >>> popcount_lookup8(4294967295)
    32
    """
    count = 0
    while n:
        count += _LOOKUP8[n & 0xFF]
        n >>= 8
    return count


TEST_CASES = [(25, 3), (37, 3), (21, 3), (58, 4), (0, 0), (256, 1), (0xFFFFFFFF, 32)]

IMPLS = [
    ("kernighan",   popcount_kernighan),
    ("bit_count()", popcount_bit_count),
    ("bin.count",   popcount_bin),
    ("lookup8",     popcount_lookup8),
]

# Sparse vs dense benchmark inputs
_SPARSE = [1, 4, 16, 64, 256]           # 1 bit each — Kernighan finishes in 1 step
_DENSE  = [0b10110111, 0b11111111, 0xFFFFFFFF, 0b10101010, 0b11001100]  # many bits


def run_all() -> None:
    print("\n=== Correctness ===")
    for n, expected in TEST_CASES:
        results = {name: fn(n) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        print(f"  [{'OK' if ok else 'FAIL'}] popcount({n:<12}) = {expected}  "
              + "  ".join(f"{nm}={v}" for nm, v in results.items()))

    REPS = 500_000
    for label, inputs in [("sparse (1 set bit each)", _SPARSE),
                           ("dense  (many set bits)",  _DENSE)]:
        print(f"\n=== Benchmark: {label}, {REPS} runs ===")
        for name, fn in IMPLS:
            t = timeit.timeit(lambda fn=fn: [fn(n) for n in inputs], number=REPS) * 1000 / REPS
            print(f"  {name:<14} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
