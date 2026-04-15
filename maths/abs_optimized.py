#!/usr/bin/env python3
"""
Optimized and alternative implementations of Absolute Value operations.

Variants covered:
1. abs_val_builtin      -- Python's built-in abs(); C-level, fastest.
2. abs_val_bitwise      -- bit trick for ints: (x ^ (x>>31)) - (x>>31).
3. abs_max_minmax       -- single-pass max with key=abs using max() built-in.

Run:
    python maths/abs_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.abs import abs_val as abs_val_reference, abs_max as abs_max_reference


def abs_val_builtin(num: float) -> float:
    """
    Built-in abs(). C-implementation, fastest for any numeric type.

    >>> abs_val_builtin(-5.1)
    5.1
    >>> abs_val_builtin(-5) == abs_val_builtin(5)
    True
    >>> abs_val_builtin(0)
    0
    """
    return abs(num)


def abs_val_bitwise(num: int) -> int:
    """
    Bitwise absolute value for 32-bit signed int (interview classic).

    Mask = num >> 31 (all 1s if negative, all 0s if positive).
    abs = (num ^ mask) - mask.

    For Python ints of arbitrary precision this still works because the
    arithmetic shift preserves sign, but it's only a true O(1) trick on
    fixed-width C integers.

    >>> abs_val_bitwise(-5)
    5
    >>> abs_val_bitwise(5)
    5
    >>> abs_val_bitwise(0)
    0
    >>> abs_val_bitwise(-2147483648)
    2147483648
    """
    mask = num >> 63  # use 64-bit for Python safety
    return (num ^ mask) - mask


def abs_max_builtin(x: list[int]) -> int:
    """
    Single-pass max with key=abs, one C-level loop.

    >>> abs_max_builtin([0,5,1,11])
    11
    >>> abs_max_builtin([3,-10,-2])
    -10
    >>> abs_max_builtin([])
    Traceback (most recent call last):
        ...
    ValueError: abs_max_builtin() arg is an empty sequence
    """
    if not x:
        raise ValueError("abs_max_builtin() arg is an empty sequence")
    return max(x, key=abs)


def _benchmark() -> None:
    nums = list(range(-500, 500))
    n = 20000
    print(f"Benchmark: abs operations (n={n:,} iterations)\n")

    t1 = timeit.timeit(lambda: [abs_val_reference(i) for i in nums], number=n) * 1000 / n
    t2 = timeit.timeit(lambda: [abs_val_builtin(i) for i in nums], number=n) * 1000 / n
    t3 = timeit.timeit(lambda: [abs_val_bitwise(i) for i in nums], number=n) * 1000 / n
    t4 = timeit.timeit(lambda: abs_max_reference(nums), number=n) * 1000 / n
    t5 = timeit.timeit(lambda: abs_max_builtin(nums), number=n) * 1000 / n

    print(f"  abs_val (reference ternary):   {t1:.4f} ms")
    print(f"  abs_val_builtin (abs()):       {t2:.4f} ms  [{t1/t2:.2f}x]")
    print(f"  abs_val_bitwise (xor trick):   {t3:.4f} ms  [{t1/t3:.2f}x]")
    print(f"  abs_max (reference loop):      {t4:.4f} ms")
    print(f"  abs_max_builtin (max+key):     {t5:.4f} ms  [{t4/t5:.2f}x]")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
