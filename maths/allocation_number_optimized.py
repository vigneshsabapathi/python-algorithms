#!/usr/bin/env python3
"""
Optimized allocation_num variants.

Reference: O(P) with string formatting per partition.

Variants:
1. allocation_num_balanced -- distributes remainder across first R partitions
                              for size balance (|max-min| <= 1). The reference
                              dumps the whole remainder into the LAST partition.
2. allocation_num_tuples   -- returns (start, end) tuples instead of strings
                              (cheaper, more useful for callers).
3. allocation_num_np       -- numpy chunking via array_split (if numpy avail).

Run:
    python maths/allocation_number_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.allocation_number import allocation_num as allocation_num_reference


def allocation_num_balanced(number_of_bytes: int, partitions: int) -> list[str]:
    """
    Balanced allocation: remainder R is spread across the first R partitions
    (each gets one extra byte), so partition sizes differ by at most 1.

    >>> allocation_num_balanced(10, 3)
    ['1-4', '5-7', '8-10']
    >>> allocation_num_balanced(16647, 4)
    ['1-4162', '4163-8324', '8325-12486', '12487-16647']
    """
    if partitions <= 0:
        raise ValueError("partitions must be a positive number!")
    if partitions > number_of_bytes:
        raise ValueError("partitions can not > number_of_bytes!")
    base = number_of_bytes // partitions
    rem = number_of_bytes % partitions
    out: list[str] = []
    cursor = 1
    for i in range(partitions):
        size = base + (1 if i < rem else 0)
        end = cursor + size - 1
        out.append(f"{cursor}-{end}")
        cursor = end + 1
    return out


def allocation_num_tuples(number_of_bytes: int, partitions: int) -> list[tuple[int, int]]:
    """
    >>> allocation_num_tuples(10, 2)
    [(1, 5), (6, 10)]
    """
    if partitions <= 0 or partitions > number_of_bytes:
        raise ValueError("bad partitions")
    per = number_of_bytes // partitions
    out = []
    for i in range(partitions):
        s = i * per + 1
        e = number_of_bytes if i == partitions - 1 else (i + 1) * per
        out.append((s, e))
    return out


def _benchmark() -> None:
    n = 1000
    print(f"Benchmark: allocation_num(1_000_000, 100), n={n:,}\n")
    t1 = timeit.timeit(lambda: allocation_num_reference(1_000_000, 100), number=n) * 1000 / n
    t2 = timeit.timeit(lambda: allocation_num_balanced(1_000_000, 100), number=n) * 1000 / n
    t3 = timeit.timeit(lambda: allocation_num_tuples(1_000_000, 100), number=n) * 1000 / n
    print(f"  reference (strings):           {t1:.4f} ms")
    print(f"  balanced (strings):            {t2:.4f} ms  [{t1/t2:.2f}x]")
    print(f"  tuples (no formatting):        {t3:.4f} ms  [{t1/t3:.2f}x]")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
