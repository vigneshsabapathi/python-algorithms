#!/usr/bin/env python3
"""
Optimized and alternative implementations of Pascal's Triangle.

The reference provides standard row-by-row generation and a symmetry-optimized
version. Both are O(n^2) time and space.

Three alternatives:
  combinatorial  -- Use C(n,k) = n! / (k! * (n-k)!) directly
  generator      -- Yield rows lazily (memory efficient for large triangles)
  single_row     -- Generate only the nth row without building full triangle

Run:
    python matrix/pascal_triangle_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from math import comb

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matrix.pascal_triangle import generate_pascal_triangle as reference


# ---------------------------------------------------------------------------
# Variant 1 -- Combinatorial: C(n, k) for each element
# ---------------------------------------------------------------------------

def pascal_combinatorial(num_rows: int) -> list[list[int]]:
    """
    Generate Pascal's triangle using math.comb. Each element is C(row, col).

    >>> pascal_combinatorial(0)
    []
    >>> pascal_combinatorial(1)
    [[1]]
    >>> pascal_combinatorial(5)
    [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
    """
    if num_rows <= 0:
        return [] if num_rows == 0 else []
    return [[comb(r, c) for c in range(r + 1)] for r in range(num_rows)]


# ---------------------------------------------------------------------------
# Variant 2 -- Generator: yield rows lazily
# ---------------------------------------------------------------------------

def pascal_generator(num_rows: int):
    """
    Yield Pascal's triangle rows one at a time. Memory efficient.

    >>> list(pascal_generator(5))
    [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
    >>> list(pascal_generator(0))
    []
    >>> list(pascal_generator(1))
    [[1]]
    """
    if num_rows <= 0:
        return
    row = [1]
    yield row
    for _ in range(1, num_rows):
        row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]
        yield row


# ---------------------------------------------------------------------------
# Variant 3 -- Single row: get just the nth row (0-indexed)
# ---------------------------------------------------------------------------

def pascal_nth_row(n: int) -> list[int]:
    """
    Generate only the nth row of Pascal's triangle (0-indexed).
    Uses the multiplicative formula: C(n,k) = C(n,k-1) * (n-k+1) / k.

    >>> pascal_nth_row(0)
    [1]
    >>> pascal_nth_row(1)
    [1, 1]
    >>> pascal_nth_row(4)
    [1, 4, 6, 4, 1]
    >>> pascal_nth_row(7)
    [1, 7, 21, 35, 35, 21, 7, 1]
    """
    row = [1]
    for k in range(1, n + 1):
        row.append(row[-1] * (n - k + 1) // k)
    return row


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    n = 100
    number = 10_000
    print(f"Benchmark ({number} generations of {n}-row triangle):\n")

    funcs = [
        ("reference (standard)", lambda: reference(n)),
        ("combinatorial (math.comb)", lambda: pascal_combinatorial(n)),
        ("generator (lazy)", lambda: list(pascal_generator(n))),
        ("nth_row only (row 99)", lambda: pascal_nth_row(n - 1)),
    ]

    for name, func in funcs:
        t = timeit.timeit(func, number=number)
        print(f"  {name:35s} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
