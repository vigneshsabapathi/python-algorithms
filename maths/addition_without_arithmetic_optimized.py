#!/usr/bin/env python3
"""
Optimized and alternative implementations of addition without arithmetic ops.

Variants:
1. add_native       -- Python's `+` (baseline, C-level).
2. add_bitwise_rec  -- recursive version of the XOR-and-carry trick.
3. add_sub_neg      -- `first - (-second)` — still uses arithmetic semantically.

Run:
    python maths/addition_without_arithmetic_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.addition_without_arithmetic import add as add_reference


def add_native(a: int, b: int) -> int:
    """
    >>> add_native(3, 5)
    8
    >>> add_native(-321, 0)
    -321
    """
    return a + b


def add_bitwise_rec(a: int, b: int, mask: int = (1 << 64) - 1) -> int:
    """
    Recursive XOR/AND-shift addition, masked to 64 bits to terminate on
    negative numbers in Python's arbitrary-precision ints.

    >>> add_bitwise_rec(3, 5)
    8
    >>> add_bitwise_rec(13, 5)
    18
    """
    while b & mask:
        a, b = (a ^ b) & mask, ((a & b) << 1) & mask
    # Convert back to signed if high bit set
    if a & (1 << 63):
        a -= 1 << 64
    return a


def add_sub_neg(a: int, b: int) -> int:
    """
    >>> add_sub_neg(3, 5)
    8
    >>> add_sub_neg(-7, 2)
    -5
    """
    return a - (-b)


def _benchmark() -> None:
    pairs = [(i, i * 3) for i in range(-500, 500)]
    n = 5000
    print(f"Benchmark: addition (n={n:,} iterations over {len(pairs)} pairs)\n")

    t1 = timeit.timeit(lambda: [add_reference(a, b) for a, b in pairs], number=n) * 1000 / n
    t2 = timeit.timeit(lambda: [add_native(a, b) for a, b in pairs], number=n) * 1000 / n
    t3 = timeit.timeit(lambda: [add_sub_neg(a, b) for a, b in pairs], number=n) * 1000 / n

    print(f"  add (reference XOR/carry loop): {t1:.4f} ms")
    print(f"  add_native (+):                 {t2:.4f} ms  [{t1/t2:.1f}x faster]")
    print(f"  add_sub_neg (a - (-b)):         {t3:.4f} ms  [{t1/t3:.1f}x faster]")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
